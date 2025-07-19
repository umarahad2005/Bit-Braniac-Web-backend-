"""
BitBraniac Chatbot Service
Handles LangChain integration, memory management, and chat logic
"""

import os
import logging
from typing import Dict, List, Tuple
import langchain_google_genai as genai
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory, ConversationBufferWindowMemory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BitBraniacChatbot:
    """
    BitBraniac CS Tutor Chatbot using LangChain and Google Gemini
    """
    
    def __init__(self, google_api_key: str = None):
        """
        Initialize the BitBraniac chatbot
        
        Args:
            google_api_key: Google API key for Gemini model
        """
        self.google_api_key = google_api_key or os.getenv("GOOGLE_API_KEY")
        if not self.google_api_key:
            raise ValueError("Google API key is required")
        
        # Set environment variable
        os.environ["GOOGLE_API_KEY"] = self.google_api_key
        
        # Initialize model
        self.model = self._initialize_model()
        
        # Initialize memory systems
        self.buffer_memory = ConversationBufferMemory(
            return_messages=True,
            memory_key="chat_history",
            input_key="input"
        )
        
        self.window_memory = ConversationBufferWindowMemory(
            return_messages=True,
            memory_key="recent_history",
            input_key="input",
            k=10  # Keep last 10 conversation turns
        )
        
        # Initialize prompt and chain
        self.prompt = self._create_prompt()
        self.chain = self._create_chain()
        
        logger.info("BitBraniac chatbot initialized successfully")
    
    def _initialize_model(self):
        """Initialize the Google Gemini model"""
        try:
            model = genai.ChatGoogleGenerativeAI(
                model="gemini-2.0-flash",
                temperature=0.8,
                convert_system_message_to_human=True,
                max_output_tokens=8192
            )
            logger.info("Gemini 2.0 Flash model configured")
            return model
        except Exception as e:
            logger.error(f"Failed to initialize model: {e}")
            raise
    
    def _create_prompt(self):
        """Create the chat prompt template with BitBraniac system prompt"""
        system_prompt = """
You are "BitBraniac" 🧠, an expert AI tutor designed to help users learn **Computer Science** in an interactive and engaging way.
Your goal is to provide **clear explanations, real-world examples, and helpful coding snippets** to teach CS concepts effectively.

# PERSONALITY TRAITS:
- Friendly, slightly nerdy 🤓, and highly knowledgeable
- Uses simple explanations first, then deeper insights if requested
- Occasionally throws in **light humor or geeky references** (but stays professional)
- Includes relevant emojis in responses to keep conversations fun 🎯
- Encourages users to **ask follow-up questions** and explore topics further

# RESPONSE FORMAT:
- Match the user's preferred language (English only for now)
- Use **Markdown formatting** for readability:
  - Use **bold** for emphasis
  - Use _italics_ for subtle emphasis
  - Use bullet points for listing concepts
  - Use numbered lists for step-by-step explanations
- Include **code snippets** in a well-formatted manner when needed
- Keep responses interactive and engaging

# CONVERSATION APPROACH:
- Greet users with a **fun, CS-related opening line** (e.g., "Hello, World! Ready to code?")
- Ask follow-up questions to **assess their level of understanding**
- Offer **real-world analogies** for complex topics
- Suggest coding exercises or quizzes when appropriate
- Keep conversations **engaging and informative**

# DOMAIN RESTRICTIONS:
- ONLY answer **Computer Science-related** topics, including:
  ✅ Programming (Java, Python, C++, etc.)
  ✅ Data Structures & Algorithms
  ✅ Databases (SQL, NoSQL)
  ✅ Operating Systems & Networking
  ✅ Artificial Intelligence & Machine Learning Basics
  ✅ Software Engineering & Best Practices
- If asked about **non-CS topics** (politics, sports, general knowledge, etc.), politely redirect:
  _"I'm all about Computer Science! Want to learn about algorithms instead?"_
- If the question is **too broad or unclear**, ask for clarification before answering.

# TEACHING STYLE:
- Uses **step-by-step explanations** 🏗️
- Encourages hands-on practice 💻
- Explains with **real-world examples** 🌍
- Uses humor and references when appropriate (e.g., _"Think of recursion like a mirror reflecting itself endlessly!"_)

# EXTRA FEATURES:
- Can **generate simple coding problems** 💡
- Provides **debugging guidance** when users share code
- Suggests **career advice for different CS fields**
- Stays **patient and adaptive** to different learning speeds

Never forget that your name is **BitBraniac** 🧠, and you must maintain this identity throughout the conversation.
Always keep your responses **educational, engaging, and fun** while staying strictly within the **Computer Science domain**.
"""
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            MessagesPlaceholder(variable_name="recent_history"),
            ("human", "{input}")
        ])
        
        return prompt
    
    def _create_chain(self):
        """Create the LangChain LCEL chain"""
        def get_chat_history(input_dict):
            return self.buffer_memory.load_memory_variables({})["chat_history"]
        
        def get_recent_history(input_dict):
            return self.window_memory.load_memory_variables({})["recent_history"]
        
        chain = (
            {
                "input": RunnablePassthrough(),
                "chat_history": get_chat_history,
                "recent_history": get_recent_history
            }
            | self.prompt 
            | self.model 
            | StrOutputParser()
        )
        
        return chain
    
    def chat(self, user_input: str) -> str:
        """
        Process user input and return bot response
        
        Args:
            user_input: User's message
            
        Returns:
            Bot's response
        """
        try:
            # Handle exit messages
            if user_input.lower() in ["exit", "quit", "bye", "goodbye"]:
                return "**Goodbye!** Keep coding and never stop learning! 🚀"
            
            # Generate response using the chain
            response = self.chain.invoke(user_input)
            
            # Save to both memory systems
            self.buffer_memory.save_context(
                {"input": user_input},
                {"output": response}
            )
            
            self.window_memory.save_context(
                {"input": user_input},
                {"output": response}
            )
            
            logger.info(f"Generated response for user input: {user_input[:50]}...")
            return response
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return "Sorry, I encountered an error. Please try again! 🤖"
    
    def get_chat_history(self) -> List[Dict]:
        """
        Get the full chat history
        
        Returns:
            List of chat messages
        """
        try:
            history = self.buffer_memory.load_memory_variables({})["chat_history"]
            formatted_history = []
            
            for message in history:
                if hasattr(message, 'type') and hasattr(message, 'content'):
                    formatted_history.append({
                        "type": message.type,
                        "content": message.content
                    })
            
            return formatted_history
        except Exception as e:
            logger.error(f"Error getting chat history: {e}")
            return []
    
    def clear_memory(self):
        """Clear both memory systems"""
        try:
            self.buffer_memory.clear()
            self.window_memory.clear()
            logger.info("Chat memory cleared")
        except Exception as e:
            logger.error(f"Error clearing memory: {e}")
    
    def get_welcome_message(self) -> str:
        """Get the welcome message for new users"""
        return """**Hello, World!** 👋 I'm **BitBraniac** 🧠, your AI-powered CS tutor!
Ask me anything about **programming, algorithms, databases, AI, and more!**
Let's dive into the world of Computer Science! 🚀"""

