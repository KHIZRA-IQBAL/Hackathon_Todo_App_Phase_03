"use client";

import { useState, useRef, useEffect } from "react";
import { PaperAirplaneIcon } from "@heroicons/react/24/outline";
import { sendChatMessage } from "@/lib/api";

interface Message {
  role: "user" | "assistant" | "error";
  content: string;
}

interface ChatWidgetProps {
  token: string | null;
}

export default function ChatWidget({ token }: ChatWidgetProps) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [conversationId, setConversationId] = useState<number | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async () => {
    if (input.trim() === "" || isLoading || !token) {
      if (!token) {
        setMessages((prev) => [
          ...prev,
          { role: "error", content: "Authentication token is missing. Please log in again." },
        ]);
      }
      return;
    }

    const userMessage: Message = { role: "user", content: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);

    try {
      const response = await sendChatMessage(input, conversationId);
      
      const assistantMessage: Message = {
        role: "assistant",
        content: response.response,
      };
      setMessages((prev) => [...prev, assistantMessage]);
      
      if (response.conversation_id) {
        setConversationId(response.conversation_id);
      }

    } catch (error: any) {
      const errorMessage: Message = {
        role: "error",
        content: `Failed to get response: ${error.message || 'Unknown error'}`,
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-[600px] w-full max-w-2xl mx-auto bg-white rounded-lg shadow-lg">
      <div className="p-4 border-b">
        <h2 className="text-xl font-bold">AI Assistant</h2>
      </div>
      <div className="flex-1 p-4 overflow-y-auto">
        {messages.map((msg, index) => (
          <div
            key={index}
            className={`flex my-2 ${
              msg.role === "user" ? "justify-end" : "justify-start"
            }`}
          >
            <div
              className={`p-3 rounded-lg ${
                msg.role === "user"
                  ? "bg-blue-500 text-white"
                  : msg.role === "assistant"
                  ? "bg-gray-200 text-gray-800"
                  : "bg-red-100 text-red-700" // Error message style
              }`}
            >
              <p>{msg.content}</p>
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="flex justify-start">
            <div className="p-3 rounded-lg bg-gray-200 text-gray-500">
              <p>Typing...</p>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>
      <div className="p-4 border-t">
        <div className="flex items-center">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === "Enter" && handleSendMessage()}
            placeholder="Type your message..."
            className="flex-1 p-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            disabled={isLoading || !token}
          />
          <button
            onClick={handleSendMessage}
            className="p-2 ml-2 text-white bg-blue-500 rounded-lg hover:bg-blue-600 disabled:bg-blue-300"
            disabled={isLoading || !token}
          >
            <PaperAirplaneIcon className="w-6 h-6" />
          </button>
        </div>
        {!token && (
            <p className="text-xs text-red-500 mt-2">
                You must be logged in to use the chat.
            </p>
        )}
      </div>
    </div>
  );
}
