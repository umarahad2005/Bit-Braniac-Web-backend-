# BitBraniac - AI-Powered CS Tutor

A modern, production-ready QA chatbot application converted from Jupyter Notebook to a full-stack solution with Flask backend and React frontend.

## 🚀 Project Overview

BitBraniac is an AI-powered Computer Science tutor that helps users learn programming, algorithms, databases, and other CS concepts through interactive conversations. The application has been completely converted from a Jupyter Notebook with Gradio frontend to a professional full-stack application.

### Key Features

- 🧠 **AI-Powered Tutoring**: Uses Google's Gemini 2.0 Flash model via LangChain
- 💬 **Interactive Chat Interface**: Modern React-based UI with real-time messaging
- 🎯 **CS-Focused**: Specialized in Computer Science topics and programming
- 📚 **Memory Management**: Maintains conversation context with dual memory systems
- 🎨 **Modern UI**: Beautiful, responsive design with dark/light mode support
- 🔄 **Real-time Updates**: Live connection status and typing indicators
- 📱 **Mobile Responsive**: Works seamlessly on desktop and mobile devices

## 🏗️ Architecture

### Backend (Flask)
- **Framework**: Flask with CORS support
- **AI Integration**: LangChain + Google Generative AI (Gemini 2.0 Flash)
- **Memory**: Dual memory system (Buffer + Window memory)
- **API**: RESTful endpoints for chat functionality
- **Configuration**: Environment-based configuration management

### Frontend (React)
- **Framework**: React with modern hooks
- **UI Components**: shadcn/ui with Tailwind CSS
- **State Management**: React hooks for local state
- **Icons**: Lucide React icons
- **Styling**: Tailwind CSS with custom theming

## 📁 Project Structure

```
bitbraniac-project/
├── bitbraniac-backend/          # Flask backend application
│   ├── src/
│   │   ├── services/
│   │   │   └── chatbot_service.py    # LangChain chatbot logic
│   │   ├── routes/
│   │   │   └── chat.py               # Chat API endpoints
│   │   ├── config.py                 # Configuration management
│   │   └── main.py                   # Flask application entry point
│   ├── venv/                         # Python virtual environment
│   └── requirements.txt              # Python dependencies
├── bitbraniac-frontend/         # React frontend application
│   ├── src/
│   │   ├── components/
│   │   │   ├── ui/                   # shadcn/ui components
│   │   │   ├── ChatMessage.jsx       # Chat message component
│   │   │   └── ChatInput.jsx         # Chat input component
│   │   ├── services/
│   │   │   └── chatService.js        # API communication service
│   │   ├── App.jsx                   # Main application component
│   │   └── main.jsx                  # React entry point
│   ├── package.json                  # Node.js dependencies
│   └── index.html                    # HTML entry point
└── README.md                    # This documentation
```

## 🛠️ Setup Instructions

### Prerequisites

- Python 3.11+
- Node.js 18+
- pnpm (or npm)
- Google API key for Gemini

### Backend Setup

1. **Navigate to backend directory**:
   ```bash
   cd bitbraniac-backend
   ```

2. **Activate virtual environment**:
   ```bash
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set environment variables**:
   ```bash
   export GOOGLE_API_KEY="your-google-api-key-here"
   ```

5. **Start the Flask server**:
   ```bash
   python src/main.py
   ```

   The backend will run on `http://localhost:5001`

### Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd bitbraniac-frontend
   ```

2. **Install dependencies**:
   ```bash
   pnpm install
   ```

3. **Start the development server**:
   ```bash
   pnpm run dev
   ```

   The frontend will run on `http://localhost:5173`

## 🔧 Configuration

### Environment Variables

#### Backend
- `GOOGLE_API_KEY`: Your Google API key for Gemini (required)
- `SECRET_KEY`: Flask secret key (optional, has default)
- `DEBUG`: Enable debug mode (optional, default: False)
- `MODEL_NAME`: Gemini model name (optional, default: gemini-2.0-flash)
- `MODEL_TEMPERATURE`: Model temperature (optional, default: 0.8)
- `MAX_OUTPUT_TOKENS`: Maximum output tokens (optional, default: 8192)
- `CONVERSATION_WINDOW_SIZE`: Memory window size (optional, default: 10)

#### Frontend
The frontend automatically connects to the backend at `http://localhost:5001`. For production deployment, update the `API_BASE_URL` in `src/services/chatService.js`.

## 🚀 Deployment

### Backend Deployment

1. **Update requirements.txt**:
   ```bash
   cd bitbraniac-backend
   source venv/bin/activate
   pip freeze > requirements.txt
   ```

2. **Set production environment variables**
3. **Use a production WSGI server** (e.g., Gunicorn):
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5001 src.main:app
   ```

### Frontend Deployment

1. **Build the production bundle**:
   ```bash
   cd bitbraniac-frontend
   pnpm run build
   ```

2. **Serve the built files** using a web server (nginx, Apache, etc.)

### Full-Stack Deployment

For a complete deployment, you can:
1. Build the React frontend
2. Copy the built files to Flask's static directory
3. Configure Flask to serve the frontend
4. Deploy as a single application

## 📚 API Documentation

### Endpoints

#### `GET /api/chat/health`
Check backend service health.

**Response:**
```json
{
  "status": "healthy",
  "service": "BitBraniac Chat API",
  "version": "1.0.0",
  "success": true
}
```

#### `GET /api/chat/welcome`
Get the welcome message.

**Response:**
```json
{
  "message": "Welcome message content",
  "success": true
}
```

#### `POST /api/chat/message`
Send a message to BitBraniac.

**Request:**
```json
{
  "message": "Your question here"
}
```

**Response:**
```json
{
  "response": "BitBraniac's response",
  "success": true
}
```

#### `GET /api/chat/history`
Get chat history.

**Response:**
```json
{
  "history": [
    {"type": "human", "content": "User message"},
    {"type": "ai", "content": "Bot response"}
  ],
  "success": true
}
```

#### `POST /api/chat/clear`
Clear chat history.

**Response:**
```json
{
  "message": "Chat history cleared successfully",
  "success": true
}
```

## 🎨 Features Comparison

| Feature | Original (Jupyter + Gradio) | New (Flask + React) |
|---------|----------------------------|---------------------|
| AI Model | ✅ Gemini 2.0 Flash | ✅ Gemini 2.0 Flash |
| Memory | ✅ Dual memory system | ✅ Dual memory system |
| Chat Interface | ✅ Basic Gradio UI | ✅ Modern React UI |
| Real-time Updates | ❌ | ✅ |
| Connection Status | ❌ | ✅ |
| Mobile Responsive | ⚠️ Limited | ✅ |
| Production Ready | ❌ | ✅ |
| Modular Architecture | ❌ | ✅ |
| Error Handling | ⚠️ Basic | ✅ Comprehensive |
| Deployment | ❌ Notebook only | ✅ Full deployment |

## 🔍 Key Improvements

1. **Production Architecture**: Separated backend and frontend with proper API design
2. **Modern UI**: Beautiful, responsive React interface with professional styling
3. **Better Error Handling**: Comprehensive error handling and user feedback
4. **Real-time Features**: Connection status, typing indicators, and live updates
5. **Modular Code**: Clean, maintainable code structure with proper separation of concerns
6. **Configuration Management**: Environment-based configuration for different deployment scenarios
7. **Enhanced UX**: Loading states, auto-scroll, timestamps, and better message formatting

## 🐛 Troubleshooting

### Common Issues

1. **Backend not starting**: Check if port 5001 is available and Google API key is set
2. **Frontend can't connect**: Ensure backend is running and CORS is properly configured
3. **API key errors**: Verify your Google API key is valid and has Gemini access
4. **Memory issues**: Adjust `CONVERSATION_WINDOW_SIZE` for better performance

### Logs

- Backend logs are printed to console when running in debug mode
- Frontend errors appear in browser developer console
- Check network tab for API request/response details

## 📄 License

This project is provided as-is for educational and development purposes.

## 🤝 Contributing

This is a converted project from Jupyter Notebook to production application. Feel free to extend and improve the codebase following the established patterns.

---

**BitBraniac** - Your AI-powered CS tutor, now in production! 🚀

