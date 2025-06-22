import { useState, useRef, useEffect } from "react";
import { Send, Loader2 } from "lucide-react";
import ChatMessage from "./ChatMessage";

interface ChatInterfaceProps {
  onUserInteraction?: () => void;
}

const ChatInterface = ({ onUserInteraction }: ChatInterfaceProps) => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      message: "안녕하세요! AI 제품 추천 에이전트입니다. 어떤 제품을 추천해 드릴까요? 🛍️",
      isBot: true,
      timestamp: "방금 전"
    }
  ]);
  const [inputValue, setInputValue] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [hasInteracted, setHasInteracted] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    // 메시지가 2개 이상일 때만 스크롤 (초기 봇 메시지 1개는 제외)
    if (messages.length > 1) {
      scrollToBottom();
    }
  }, [messages]);

  const handleSendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;

    // 첫 번째 사용자 메시지일 때 사이드바 표시
    if (!hasInteracted) {
      setHasInteracted(true);
      onUserInteraction?.();
    }

    const userMessage = {
      id: messages.length + 1,
      message: inputValue,
      isBot: false,
      timestamp: "방금 전"
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue("");
    setIsLoading(true);

    // 시뮬레이션된 봇 응답
    setTimeout(() => {
      let botResponse = "";
      
      if (inputValue.toLowerCase().includes("키보드")) {
        botResponse = `키보드 추천을 원하시는군요! 더 구체적으로 알려주시면 도움이 될 것 같습니다:

• 가성비 좋은 키보드
• 게이밍용 키보드  
• 무소음 키보드
• 무선 키보드

어떤 특성을 원하시나요?`;
      } else if (inputValue.toLowerCase().includes("가성비")) {
        botResponse = `가성비 좋은 키보드 추천 목록입니다:

🏆 **추천 제품들**
• 독거미 K552 기계식 키보드
  - 가격: 약 45,000원
  - 출처: 네이버 블로그 리뷰
  - 리뷰: "이 가격에 이 품질이면 정말 만족"

• 로지텍 K380 무선키보드  
  - 가격: 약 35,000원
  - 쿠팡 평점: 4.5/5
  - 리뷰: "가성비 최고, 타건감도 괜찮음"

더 자세한 정보가 필요하시면 말씀해 주세요!`;
      } else {
        botResponse = `"${inputValue}"에 대해 검색해보겠습니다. 조금 더 구체적인 조건이 있으시면 더 정확한 추천을 도와드릴 수 있어요!

예를 들어:
• 예산 범위
• 사용 목적
• 선호하는 특징

어떤 부분을 중요하게 생각하시나요?`;
      }

      const botMessage = {
        id: messages.length + 2,
        message: botResponse,
        isBot: true,
        timestamp: "방금 전"
      };

      setMessages(prev => [...prev, botMessage]);
      setIsLoading(false);
    }, 1500);
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <div className="flex-1 flex flex-col bg-gray-50">
      {/* 메시지 영역 */}
      <div className="flex-1 overflow-y-auto p-6 space-y-4">
        {messages.map((message) => (
          <ChatMessage
            key={message.id}
            message={message.message}
            isBot={message.isBot}
            timestamp={message.timestamp}
          />
        ))}
        {isLoading && (
          <div className="flex space-x-3 mb-6">
            <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
              <Loader2 className="w-5 h-5 text-blue-600 animate-spin" />
            </div>
            <div className="bg-gray-100 px-4 py-3 rounded-2xl">
              <p className="text-sm text-gray-600">검색 중...</p>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* 입력 영역 */}
      <div className="border-t border-gray-200 bg-white p-4">
        <div className="flex space-x-3">
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="어떤 제품을 찾고 계시나요?"
            className="flex-1 px-4 py-3 border border-gray-300 rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            disabled={isLoading}
          />
          <button
            onClick={handleSendMessage}
            disabled={!inputValue.trim() || isLoading}
            className="px-6 py-3 bg-blue-600 text-white rounded-full hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 flex items-center space-x-2"
          >
            <Send className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
};

export default ChatInterface;
