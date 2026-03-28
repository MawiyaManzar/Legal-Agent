import React, { useState, useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Send, User, Bot, Upload, FileText } from 'lucide-react';

interface Message {
  id: number;
  text: string;
  isUser: boolean;
  timestamp: Date;
}

interface UploadResponse {
  message?: string;
  error?: string;
}

interface AskResponse {
  answer?: string;
  error?: string;
}

type UploadStatus = 'idle' | 'uploading' | 'success' | 'error';

const ChatPage = () => {
  const navigate = useNavigate();
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 1,
      text: "Hello! I'm WakeelSahab, your AI legal assistant. Please upload a PDF document to get started with your legal research.",
      isUser: false,
      timestamp: new Date()
    }
  ]);
  const [inputText, setInputText] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [uploadStatus, setUploadStatus] = useState<UploadStatus>('idle');
  const [uploadMessage, setUploadMessage] = useState<string>('');
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  // API configuration
  const API_BASE_URL = 'http://localhost:8000';

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      if (file.type === 'application/pdf') {
        setSelectedFile(file);
        setUploadStatus('idle');
        setUploadMessage('');
      } else {
        setUploadStatus('error');
        setUploadMessage('Please select a PDF file');
      }
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) return;

    setUploadStatus('uploading');
    setUploadMessage('Uploading...');

    try {
      const formData = new FormData();
      formData.append('file', selectedFile);

      const response = await fetch(`${API_BASE_URL}/upload_pdf`, {
        method: 'POST',
        body: formData,
      });

      const data: UploadResponse = await response.json();

      if (!response.ok || data.error) {
        throw new Error(data.error || 'Upload failed');
      }

      setUploadStatus('success');
      setUploadMessage(data.message || 'PDF uploaded successfully');
      
      // Update bot greeting after successful upload
      setMessages(prev => [{
        id: 1,
        text: `Hello! I'm WakeelSahab, your AI legal assistant. I've loaded your document "${selectedFile.name}". How can I help you with your legal research today?`,
        isUser: false,
        timestamp: new Date()
      }, ...prev.slice(1)]);
    } catch (error) {
      console.error('Upload failed:', error);
      setUploadStatus('error');
      setUploadMessage(error instanceof Error ? error.message : 'Failed to upload PDF. Please try again.');
    }
  };

  const callAskAPI = async (query: string): Promise<AskResponse> => {
    try {
      const response = await fetch(`${API_BASE_URL}/ask`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: query
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data: AskResponse = await response.json();
      return data;
    } catch (error) {
      console.error('API call failed:', error);
      throw error;
    }
  };

  const handleSendMessage = async () => {
    if (inputText.trim() === '' ) return;

    const userMessage = inputText;
    setInputText('');
    setIsTyping(true);

    // Add user message
    setMessages(prev => [...prev, {
      id: Date.now(),
      text: userMessage,
      isUser: true,
      timestamp: new Date()
    }]);

    try {
      const response = await callAskAPI(userMessage);
      
      let aiResponse = '';
      if (response.error) {
        aiResponse = `Error: ${response.error}`;
      } else if (response.answer) {
        aiResponse = response.answer;
      } else {
        aiResponse = "I apologize, but I couldn't process your request. Please try rephrasing your question.";
      }

      // Add AI response
      setMessages(prev => [...prev, {
        id: Date.now(),
        text: aiResponse,
        isUser: false,
        timestamp: new Date()
      }]);

    } catch (error) {
      // Add error message
      setMessages(prev => [...prev, {
        id: Date.now(),
        text: error instanceof Error ? `I'm sorry, I encountered an error: ${error.message}` : "I'm sorry, I encountered an error while processing your request. Please try again later.",
        isUser: false,
        timestamp: new Date()
      }]);
    } finally {
      setIsTyping(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const isInputDisabled =  isTyping;

  return (
    <div className="min-h-screen bg-black text-white flex flex-col">
      {/* Header */}
      <header className="bg-black/95 backdrop-blur-sm border-b border-gray-900 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            {/* Logo */}
            <div className="flex items-center">
              <span className="text-xl font-semibold text-white">WakeelSahab</span>
            </div>

            {/* Home Link */}
            <button 
              onClick={() => navigate('/')}
              className="bg-gray-800 hover:bg-gray-700 text-white px-4 py-2 rounded-lg transition-colors border border-gray-700"
            >
              Back to Home
            </button>
          </div>
        </div>
      </header>

      {/* Chat Area */}
      <div className="flex-1 flex flex-col max-w-4xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-8">
        {/* Messages Container */}
        <div className="flex-1 overflow-y-auto space-y-6">
          {messages.map((message) => (
            <div
              key={message.id}
              className={`flex ${message.isUser ? 'justify-end' : 'justify-start'}`}
            >
              <div className={`flex items-start space-x-3 max-w-3xl ${message.isUser ? 'flex-row-reverse space-x-reverse' : ''}`}>
                {/* Avatar */}
                <div className={`w-10 h-10 rounded-full flex items-center justify-center flex-shrink-0 ${
                  message.isUser 
                    ? 'bg-blue-600' 
                    : 'bg-gray-800'
                }`}>
                  {message.isUser ? (
                    <User className="w-5 h-5" />
                  ) : (
                    <Bot className="w-5 h-5" />
                  )}
                </div>

                {/* Message Bubble */}
                <div className={`rounded-2xl px-6 py-4 ${
                  message.isUser
                    ? 'bg-gradient-to-r from-yellow-400 to-yellow-500 text-black'
                    : 'bg-gray-900/50 text-gray-100 border border-gray-800'
                }`}>
                  <p className="leading-relaxed">{message.text}</p>
                  <p className={`text-xs mt-2 ${
                    message.isUser ? 'text-blue-100' : 'text-gray-400'
                  }`}>
                    {message.timestamp.toLocaleTimeString([], { 
                      hour: '2-digit', 
                      minute: '2-digit' 
                    })}
                  </p>
                </div>
              </div>
            </div>
          ))}

          {/* Typing Indicator */}
          {isTyping && (
            <div className="flex justify-start">
              <div className="flex items-start space-x-3 max-w-3xl">
                <div className="w-10 h-10 rounded-full bg-gray-800 flex items-center justify-center flex-shrink-0">
                  <Bot className="w-5 h-5" />
                </div>
                <div className="bg-gray-900 border border-gray-700 rounded-2xl px-6 py-4">
                  <div className="flex space-x-1">
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                  </div>
                </div>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Upload Area */}
        <div className="border-t border-gray-900 py-4">
          <div className="flex items-center gap-4 flex-wrap">
            <input
              ref={fileInputRef}
              type="file"
              accept=".pdf"
              onChange={handleFileSelect}
              className="hidden"
            />
            <button
              onClick={() => fileInputRef.current?.click()}
              className="flex items-center gap-2 bg-gray-800 hover:bg-gray-700 text-white px-4 py-2 rounded-lg transition-colors border border-gray-700"
            >
              <FileText className="w-4 h-4" />
              Select PDF
            </button>
            
            {selectedFile && (
              <span className="text-sm text-gray-400 truncate max-w-xs">
                {selectedFile.name}
              </span>
            )}
            
            <button
              onClick={handleUpload}
              disabled={!selectedFile || uploadStatus === 'uploading' || uploadStatus === 'success'}
              className="flex items-center gap-2 bg-gradient-to-r from-yellow-400 to-yellow-500 hover:from-yellow-500 hover:to-yellow-600 disabled:bg-gray-800 disabled:cursor-not-allowed text-black px-4 py-2 rounded-lg transition-all duration-300"
            >
              <Upload className="w-4 h-4" />
              Upload PDF
            </button>

            {/* Upload Status Badge */}
            {uploadStatus !== 'idle' && (
              <div className={`flex items-center gap-2 px-3 py-1 rounded-full text-xs font-medium ${
                uploadStatus === 'uploading'
                  ? 'bg-blue-500/20 text-blue-400 border border-blue-500/30'
                  : uploadStatus === 'success'
                  ? 'bg-green-500/20 text-green-400 border border-green-500/30'
                  : 'bg-red-500/20 text-red-400 border border-red-500/30'
              }`}>
                {uploadStatus === 'uploading' && (
                  <div className="w-2 h-2 bg-blue-400 rounded-full animate-pulse"></div>
                )}
                {uploadStatus === 'success' && (
                  <span>✓</span>
                )}
                {uploadStatus === 'error' && (
                  <span>✗</span>
                )}
                <span>{uploadMessage || (uploadStatus === 'uploading' ? 'Uploading...' : uploadStatus === 'success' ? 'Uploaded' : 'Error')}</span>
              </div>
            )}
          </div>
        </div>

        {/* Input Area */}
        <div className="border-t border-gray-900 py-6">
          <div className="flex items-end space-x-4">
            <div className="flex-1 relative">
              <input
                ref={inputRef}
                type="text"
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder={"Ask me about legal research, case law, statutes..."}
                className="w-full bg-gray-900/50 border border-gray-800 rounded-xl px-4 py-3 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-yellow-500 focus:border-transparent resize-none disabled:opacity-50 disabled:cursor-not-allowed"
                disabled={isInputDisabled}
              />
            </div>
            <button
              onClick={handleSendMessage}
              disabled={inputText.trim() === '' || isInputDisabled}
              className="bg-gradient-to-r from-yellow-400 to-yellow-500 hover:from-yellow-500 hover:to-yellow-600 disabled:bg-gray-800 disabled:cursor-not-allowed text-black p-3 rounded-xl transition-all duration-300 flex items-center justify-center"
            >
              <Send className="w-5 h-5" />
            </button>
          </div>
          
          {/* Disclaimer */}
          <p className="text-xs text-gray-500 mt-3 text-center">
            WakeelSahab provides legal research assistance. Always consult with a qualified attorney for legal advice.
          </p>
        </div>
      </div>
    </div>
  );
};

export default ChatPage;