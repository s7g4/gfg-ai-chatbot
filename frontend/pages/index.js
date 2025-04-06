import { useState, useEffect } from "react";
import axios from "axios";
import { motion } from "framer-motion";

export default function Home() {
    const [message, setMessage] = useState("");
    const [response, setResponse] = useState("");
    const [loading, setLoading] = useState(false);
    const [token, setToken] = useState(null);
    useEffect(() => {
    const savedToken = localStorage.getItem("jwt");
    if (savedToken) setToken(savedToken);
}, []);
const sendMessage = async () => {
    if (!token) {
        alert("Please login first");
        return;
    }
    setLoading(true);
    try {
        const res = await axios.post("http://localhost:8000/chat", {
        user_input: message,
    }, {
        headers: { 
            Authorization: `Bearer ${token}`,
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, GET, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, Authorization"
        },
    });
    setResponse(res.data.ai_response);
    } catch (error) {
        console.error("Error sending message", error);
    }
    setLoading(false);
};
const login = async () => {
    try {
        const res = await axios.post("http://localhost:8000/login", {
        username: "test",
        password: "secret",
    });
    localStorage.setItem("jwt", res.data.token);
    setToken(res.data.token);
    alert("Login successful");
    } catch (error) {
        console.error("Login error", error);
    }
};
const logout = () => {
    localStorage.removeItem("jwt");
    setToken(null);
    alert("Logged out");
};
return (
    <div className="flex flex-col min-h-screen bg-gray-900 text-gray-100">
      {/* Header */}
      <header className="bg-gray-800 border-b border-gray-700 p-4">
        <div className="max-w-4xl mx-auto flex justify-between items-center">
          <h1 className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-purple-500">
            AI Assistant
          </h1>
          {token ? (
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="px-4 py-2 bg-red-500 rounded-md text-sm font-medium"
              onClick={logout}
            >
              Logout
            </motion.button>
          ) : (
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="px-4 py-2 bg-green-500 rounded-md text-sm font-medium"
              onClick={login}
            >
              Login
            </motion.button>
          )}
        </div>
      </header>

      {/* Chat Container */}
      <main className="flex-1 overflow-hidden flex flex-col max-w-4xl mx-auto w-full p-4">
        {/* Messages Area */}
        <div className="flex-1 overflow-y-auto space-y-4 mb-4">
          {response && (
            <div className="space-y-4">
              {/* User Message */}
              <div className="flex justify-end">
                <div className="bg-blue-600 text-white rounded-lg py-2 px-4 max-w-[80%]">
                  {message}
                </div>
              </div>
              
              {/* AI Response */}
              <div className="flex justify-start">
                <div className="bg-gray-700 rounded-lg py-2 px-4 max-w-[80%]">
                  <p className="whitespace-pre-wrap">{response}</p>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Input Area */}
        <div className="bg-gray-800 rounded-lg p-4 border border-gray-700">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="flex space-x-2"
          >
            <motion.textarea
              initial={{ scale: 0.95 }}
              animate={{ scale: 1 }}
              transition={{ duration: 0.2 }}
              className="flex-1 bg-gray-700 border border-gray-600 rounded-full p-3 focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              placeholder="Message AI Assistant..."
              rows={1}
            />
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 text-white px-6 py-3 rounded-full shadow-lg self-end transition-all duration-300"
              onClick={sendMessage}
              disabled={loading}
            >
              {loading ? (
                <div className="flex items-center justify-center">
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                </div>
              ) : (
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-8.707l-3-3a1 1 0 00-1.414 1.414L10.586 9H7a1 1 0 100 2h3.586l-1.293 1.293a1 1 0 101.414 1.414l3-3a1 1 0 000-1.414z" clipRule="evenodd" />
                </svg>
              )}
            </motion.button>
          </motion.div>
        </div>
      </main>
    </div>
    );
}
