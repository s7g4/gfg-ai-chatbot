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
        const res = await axios.post("https://your-backend-url.com/chat", {
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
        const res = await axios.post("https://your-backend-url.com/login", {
        username: "testuser",
        password: "password123",
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
    <div className="flex flex-col items-center justify-center min-h-screen p-6 bg-gray-900 text-white">
    <h1 className="text-5xl font-extrabold mb-6 text-blue-400">AI Chatbot</h1>
    {!token ? (
        <motion.button 
        whileHover={{ scale: 1.1 }}
        className="bg-green-500 px-4 py-2 rounded-lg shadow-lg text-lg"
        onClick={login}
        >
        Login
        </motion.button>
        ) : (
        <motion.button 
        whileHover={{ scale: 1.1 }}
        className="bg-red-500 px-4 py-2 rounded-lg shadow-lg text-lg"
        onClick={logout}
        >
        Logout
        </motion.button>
        )}
        <motion.textarea
        initial={{ scale: 0.9 }}
        animate={{ scale: 1 }}
        transition={{ duration: 0.2 }}
        className="border p-3 mt-5 w-96 h-28 bg-gray-800 text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="Type your message..."

        />
        <motion.button
        whileHover={{ scale: 1.1 }}
        whileTap={{ scale: 0.9 }}
        className="bg-blue-500 text-white px-5 py-2 mt-3 rounded-lg shadow-lg hover:bg-blue-600"
        onClick={sendMessage}
        >
        Send
        </motion.button>
        {loading && <div className="mt-4 animate-spin rounded-full h-8 w-8 border-t-2 border-white"></div>}
        {response && (
        <motion.p 
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.5 }}
        className="mt-4 bg-gray-700 p-4 rounded-lg shadow-lg text-lg text-blue-300"
        >
        {response}
        </motion.p>
        )}
    </div>
    );
}
