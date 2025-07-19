"""
Chat routes for BitBraniac API
Handles chat endpoints and integrates with the chatbot service
"""

import os
import logging
from flask import Blueprint, jsonify, request
from src.services.chatbot_service import BitBraniacChatbot

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

chat_bp = Blueprint('chat', __name__)

# Initialize chatbot instance (will be created on first request)
chatbot_instance = None

def get_chatbot():
    """Get or create chatbot instance"""
    global chatbot_instance
    if chatbot_instance is None:
        try:
            # Get API key from environment or use default for demo
            api_key = os.getenv("GOOGLE_API_KEY", "AIzaSyD1q-8NDNoiHSzJO8JvdYmWUBgUVv4n9Vs")
            chatbot_instance = BitBraniacChatbot(google_api_key=api_key)
            logger.info("Chatbot instance created successfully")
        except Exception as e:
            logger.error(f"Failed to create chatbot instance: {e}")
            raise
    return chatbot_instance

@chat_bp.route('/chat/message', methods=['POST'])
def send_message():
    """
    Send a message to BitBraniac and get response
    
    Expected JSON payload:
    {
        "message": "Your question here"
    }
    
    Returns:
    {
        "response": "BitBraniac's response",
        "success": true
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({
                "error": "Message is required",
                "success": False
            }), 400
        
        user_message = data['message'].strip()
        
        if not user_message:
            return jsonify({
                "error": "Message cannot be empty",
                "success": False
            }), 400
        
        # Get chatbot instance and generate response
        chatbot = get_chatbot()
        response = chatbot.chat(user_message)
        
        return jsonify({
            "response": response,
            "success": True
        })
        
    except Exception as e:
        logger.error(f"Error in send_message: {e}")
        return jsonify({
            "error": "Internal server error",
            "success": False
        }), 500

@chat_bp.route('/chat/history', methods=['GET'])
def get_chat_history():
    """
    Get the full chat history
    
    Returns:
    {
        "history": [
            {"type": "human", "content": "User message"},
            {"type": "ai", "content": "Bot response"}
        ],
        "success": true
    }
    """
    try:
        chatbot = get_chatbot()
        history = chatbot.get_chat_history()
        
        return jsonify({
            "history": history,
            "success": True
        })
        
    except Exception as e:
        logger.error(f"Error in get_chat_history: {e}")
        return jsonify({
            "error": "Internal server error",
            "success": False
        }), 500

@chat_bp.route('/chat/clear', methods=['POST'])
def clear_chat():
    """
    Clear the chat history
    
    Returns:
    {
        "message": "Chat history cleared",
        "success": true
    }
    """
    try:
        chatbot = get_chatbot()
        chatbot.clear_memory()
        
        return jsonify({
            "message": "Chat history cleared successfully",
            "success": True
        })
        
    except Exception as e:
        logger.error(f"Error in clear_chat: {e}")
        return jsonify({
            "error": "Internal server error",
            "success": False
        }), 500

@chat_bp.route('/chat/welcome', methods=['GET'])
def get_welcome_message():
    """
    Get the welcome message for new users
    
    Returns:
    {
        "message": "Welcome message",
        "success": true
    }
    """
    try:
        chatbot = get_chatbot()
        welcome_msg = chatbot.get_welcome_message()
        
        return jsonify({
            "message": welcome_msg,
            "success": True
        })
        
    except Exception as e:
        logger.error(f"Error in get_welcome_message: {e}")
        return jsonify({
            "error": "Internal server error",
            "success": False
        }), 500

@chat_bp.route('/chat/health', methods=['GET'])
def health_check():
    """
    Health check endpoint for the chat service
    
    Returns:
    {
        "status": "healthy",
        "service": "BitBraniac Chat API",
        "success": true
    }
    """
    try:
        # Try to get chatbot instance to verify it's working
        chatbot = get_chatbot()
        
        return jsonify({
            "status": "healthy",
            "service": "BitBraniac Chat API",
            "version": "1.0.0",
            "success": True
        })
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({
            "status": "unhealthy",
            "service": "BitBraniac Chat API",
            "error": str(e),
            "success": False
        }), 500

