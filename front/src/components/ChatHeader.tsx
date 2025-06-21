
import { Bot } from "lucide-react";

const ChatHeader = () => {
  return (
    <div className="bg-white border-b border-gray-200 px-6 py-3 flex items-center space-x-3">
      <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
        <Bot className="w-5 h-5 text-blue-600" />
      </div>
      <div>
        <h2 className="text-lg font-semibold text-gray-900">AI 어시스턴트</h2>
        <p className="text-xs text-gray-500">제품 추천을 도와드립니다</p>
      </div>
    </div>
  );
};

export default ChatHeader;
