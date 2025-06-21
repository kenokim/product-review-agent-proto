
import { Bot, User } from "lucide-react";

interface ChatMessageProps {
  message: string;
  isBot: boolean;
  timestamp?: string;
}

const ChatMessage = ({ message, isBot, timestamp }: ChatMessageProps) => {
  return (
    <div className={`flex space-x-3 ${isBot ? '' : 'flex-row-reverse space-x-reverse'} mb-6`}>
      <div className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 ${
        isBot ? 'bg-blue-100' : 'bg-gray-100'
      }`}>
        {isBot ? (
          <Bot className="w-5 h-5 text-blue-600" />
        ) : (
          <User className="w-5 h-5 text-gray-600" />
        )}
      </div>
      <div className={`max-w-xs lg:max-w-md ${isBot ? '' : 'text-right'}`}>
        <div className={`px-4 py-3 rounded-2xl ${
          isBot 
            ? 'bg-gray-100 text-gray-900' 
            : 'bg-blue-600 text-white'
        }`}>
          <p className="text-sm whitespace-pre-wrap">{message}</p>
        </div>
        {timestamp && (
          <p className="text-xs text-gray-500 mt-1 px-2">{timestamp}</p>
        )}
      </div>
    </div>
  );
};

export default ChatMessage;
