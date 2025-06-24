import { Bot, User } from "lucide-react";
import SourcesList from "./SourcesList";
import { Source } from "@/lib/api";

interface ChatMessageProps {
  message: string;
  isBot: boolean;
  timestamp: string;
  sources?: Source[];
}

const ChatMessage = ({ message, isBot, timestamp, sources }: ChatMessageProps) => {
  return (
    <div className={`flex space-x-3 ${isBot ? '' : 'flex-row-reverse space-x-reverse'} mb-6`}>
      <div className={`w-8 h-8 rounded-full flex items-center justify-center ${
        isBot ? 'bg-blue-100' : 'bg-green-100'
      }`}>
        {isBot ? (
          <Bot className="w-5 h-5 text-blue-600" />
        ) : (
          <User className="w-5 h-5 text-green-600" />
        )}
      </div>
      <div className={`max-w-2xl ${isBot ? '' : 'text-right'}`}>
        <div className={`px-4 py-3 rounded-2xl ${
          isBot 
            ? 'bg-white border border-gray-200' 
            : 'bg-blue-600 text-white'
        }`}>
          <p className={`text-sm whitespace-pre-wrap ${isBot ? 'text-gray-800' : 'text-white'}`}>
            {message}
          </p>
        </div>
        
        {isBot && sources && sources.length > 0 && (
          <SourcesList sources={sources} />
        )}
        
        <p className={`text-xs text-gray-500 mt-1 ${isBot ? '' : 'text-right'}`}>
          {timestamp}
        </p>
      </div>
    </div>
  );
};

export default ChatMessage;
