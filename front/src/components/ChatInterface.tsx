import { useState, useRef, useEffect } from "react";
import { Send, Loader2, AlertCircle } from "lucide-react";
import ChatMessage from "./ChatMessage";
import { ChatAPI, ChatMessage as ChatMessageType } from "@/lib/api";

interface ChatInterfaceProps {
  onUserInteraction?: () => void;
}

const ChatInterface = ({ onUserInteraction }: ChatInterfaceProps) => {
  const [messages, setMessages] = useState<ChatMessageType[]>([
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
  const [error, setError] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    if (messages.length > 1) {
      scrollToBottom();
    }
  }, [messages]);

  const formatTimestamp = () => {
    const now = new Date();
    return now.toLocaleTimeString('ko-KR', { 
      hour: '2-digit', 
      minute: '2-digit' 
    });
  };

  const handleSendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;

    // 에러 상태 초기화
    setError(null);

    // 첫 번째 사용자 메시지일 때 사이드바 표시
    if (!hasInteracted) {
      setHasInteracted(true);
      onUserInteraction?.();
    }

    const userMessage: ChatMessageType = {
      id: Date.now(),
      message: inputValue,
      isBot: false,
      timestamp: formatTimestamp()
    };

    setMessages(prev => [...prev, userMessage]);
    const currentMessage = inputValue;
    setInputValue("");
    setIsLoading(true);

    try {
      // 실제 API 호출
      const response = await ChatAPI.sendMessage(currentMessage);
      
      console.log(response);

      const botMessage: ChatMessageType = {
        id: Date.now() + 1,
        message: response.message,
        isBot: true,
        timestamp: formatTimestamp(),
        sources: response.sources
      };

      setMessages(prev => [...prev, botMessage]);
      
      // 처리 시간과 검색어 정보를 콘솔에 로그
      console.log('🔍 검색어:', response.search_queries_used);
      console.log('⏱️ 처리 시간:', response.processing_time.toFixed(2) + '초');
      console.log('📚 출처 수:', response.sources.length);
      
    } catch (error) {
      console.error('메시지 전송 실패:', error);
      
      // 에러 메시지 설정
      const errorMessage = error instanceof Error ? error.message : '알 수 없는 오류가 발생했습니다.';
      setError(errorMessage);
      
      // 에러 응답 메시지 추가
      const errorBotMessage: ChatMessageType = {
        id: Date.now() + 1,
        message: `죄송합니다. 현재 서비스에 문제가 발생했습니다. 잠시 후 다시 시도해 주세요.\n\n오류: ${errorMessage}`,
        isBot: true,
        timestamp: formatTimestamp()
      };

      setMessages(prev => [...prev, errorBotMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const handleRetry = () => {
    setError(null);
    if (messages.length > 1) {
      // findLast 대신 reverse()와 find() 사용
      const lastUserMessage = [...messages].reverse().find(msg => !msg.isBot);
      if (lastUserMessage) {
        setInputValue(lastUserMessage.message);
      }
    }
  };

  return (
    <div className="flex-1 flex flex-col bg-gray-50">
      {/* 에러 알림 */}
      {error && (
        <div className="bg-red-50 border-l-4 border-red-400 p-4 mx-4 mt-4">
          <div className="flex">
            <div className="flex-shrink-0">
              <AlertCircle className="h-5 w-5 text-red-400" />
            </div>
            <div className="ml-3">
              <p className="text-sm text-red-700">
                연결에 문제가 발생했습니다. 서버가 실행 중인지 확인해 주세요.
              </p>
              <button
                onClick={handleRetry}
                className="mt-2 text-sm text-red-600 hover:text-red-500 underline"
              >
                다시 시도
              </button>
            </div>
          </div>
        </div>
      )}

      {/* 메시지 영역 */}
      <div className="flex-1 overflow-y-auto p-6 space-y-4">
        {messages.map((message) => (
          <ChatMessage
            key={message.id}
            message={message.message}
            isBot={message.isBot}
            timestamp={message.timestamp}
            sources={message.sources}
          />
        ))}
        
        {/* 로딩 상태 */}
        {isLoading && (
          <div className="flex space-x-3 mb-6">
            <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
              <Loader2 className="w-5 h-5 text-blue-600 animate-spin" />
            </div>
            <div className="bg-white border border-gray-200 px-4 py-3 rounded-2xl">
              <p className="text-sm text-gray-600">
                <span className="inline-flex items-center">
                  검색 중
                  <span className="ml-1 animate-pulse">...</span>
                </span>
              </p>
              <p className="text-xs text-gray-400 mt-1">
                Thread ID: {ChatAPI.getThreadId()}
              </p>
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
            {isLoading ? (
              <Loader2 className="w-4 h-4 animate-spin" />
            ) : (
              <Send className="w-4 h-4" />
            )}
          </button>
        </div>
        
        {/* 상태 정보 */}
        <div className="mt-2 text-xs text-gray-500 text-center">
          {isLoading ? (
            <span>AI가 최적의 제품을 찾고 있습니다...</span>
          ) : (
            <span>Enter 키를 눌러 메시지를 보내세요</span>
          )}
        </div>
      </div>
    </div>
  );
};

export default ChatInterface;
