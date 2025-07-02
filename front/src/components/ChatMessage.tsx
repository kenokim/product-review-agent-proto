import { Bot, User } from "lucide-react";
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import SourcesList from "./SourcesList";
import { Source } from "@/lib/api";

interface ChatMessageProps {
  message: string;
  isBot: boolean;
  timestamp: string;
  sources?: Source[];
}

// 변환 함수: [라벨] (URL) -> [라벨](URL)
function normalizeLinks(text: string): string {
  // 정규식: 대괄호 안 라벨 + 공백? + 괄호 속 URL
  return text.replace(/\[([^\]]+)]\s*\((https?:\/\/[^)\s]+)\)/g, '[$1]($2)');
}

const ChatMessage = ({ message, isBot, timestamp, sources }: ChatMessageProps) => {
  const processedMessage = normalizeLinks(message);

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
          {isBot ? (
            <div className="text-sm prose prose-sm max-w-none">
              <ReactMarkdown
                remarkPlugins={[remarkGfm]}
                components={{
                  // 링크 컴포넌트 커스터마이징
                  a: ({ href, children, ...props }) => (
                    <a
                      href={href}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-blue-600 hover:text-blue-800 underline font-medium"
                      title={href}
                      {...props}
                    >
                      {children}
                    </a>
                  ),
                  // 헤딩 스타일링
                  h1: ({ children }) => <h1 className="text-lg font-bold text-gray-800 mb-2">{children}</h1>,
                  h2: ({ children }) => <h2 className="text-base font-bold text-gray-800 mb-2">{children}</h2>,
                  h3: ({ children }) => <h3 className="text-sm font-bold text-gray-800 mb-1">{children}</h3>,
                  // 리스트 스타일링
                  ul: ({ children }) => <ul className="list-disc list-inside space-y-1 text-gray-800 ml-4">{children}</ul>,
                  ol: ({ children }) => <ol className="list-decimal list-inside space-y-1 text-gray-800 ml-4">{children}</ol>,
                  li: ({ children }) => <li className="text-gray-800">{children}</li>,
                  // 강조 텍스트
                  strong: ({ children }) => <strong className="font-bold text-gray-900">{children}</strong>,
                  em: ({ children }) => <em className="italic text-gray-800">{children}</em>,
                  // 코드 블록
                  code: ({ children, className }) => {
                    const isBlock = className?.includes('language-');
                    return isBlock ? (
                      <pre className="bg-gray-100 p-2 rounded text-xs font-mono text-gray-800 overflow-x-auto">
                        <code>{children}</code>
                      </pre>
                    ) : (
                      <code className="bg-gray-100 px-1 py-0.5 rounded text-xs font-mono text-gray-800">
                        {children}
                      </code>
                    );
                  },
                  // 문단
                  p: ({ children }) => <p className="text-gray-800 mb-2 last:mb-0">{children}</p>,
                  // 인용문
                  blockquote: ({ children }) => (
                    <blockquote className="border-l-4 border-blue-200 pl-4 italic text-gray-700 my-2">
                      {children}
                    </blockquote>
                  ),
                  // 테이블
                  table: ({ children }) => (
                    <table className="min-w-full border-collapse border border-gray-300 my-2">
                      {children}
                    </table>
                  ),
                  th: ({ children }) => (
                    <th className="border border-gray-300 px-2 py-1 bg-gray-100 font-bold text-gray-800">
                      {children}
                    </th>
                  ),
                  td: ({ children }) => (
                    <td className="border border-gray-300 px-2 py-1 text-gray-800">
                      {children}
                    </td>
                  ),
                }}
              >
                {processedMessage}
              </ReactMarkdown>
            </div>
          ) : (
            <p className="text-sm whitespace-pre-wrap text-white">
              {processedMessage}
            </p>
          )}
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
