// API 서비스 파일
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';

export interface ChatMessage {
  id: number;
  message: string;
  isBot: boolean;
  timestamp: string;
  sources?: Source[];
}

export interface Source {
  title: string;
  url: string;
  short_url?: string;
}

export interface ChatRequest {
  message: string;
  thread_id?: string;
  max_search_queries?: number;
  max_search_loops?: number;
}

export interface ChatResponse {
  message: string;
  thread_id: string;
  sources: Source[];
  processing_time: number;
  search_queries_used: string[];
  is_clarification: boolean;
}

export class ChatAPI {
  private static threadId: string = `user-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;

  static async sendMessage(message: string): Promise<ChatResponse> {
    const request: ChatRequest = {
      message,
      thread_id: this.threadId,
      max_search_queries: 3,
      max_search_loops: 2
    };

    console.log('🚀 API 호출 시작:', { url: `${API_BASE_URL}/chat`, request });

    try {
      const response = await fetch(`${API_BASE_URL}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(request),
      });

      console.log('📡 응답 상태:', response.status, response.statusText);

      if (!response.ok) {
        const errorText = await response.text();
        console.error('❌ API 에러 응답:', errorText);
        throw new Error(`HTTP ${response.status}: ${response.statusText}\n${errorText}`);
      }

      const data: ChatResponse = await response.json();
      console.log('✅ API 응답 성공:', data);
      return data;
    } catch (error) {
      console.error('💥 API 호출 실패:', error);
      
      if (error instanceof TypeError && error.message.includes('fetch')) {
        throw new Error('서버에 연결할 수 없습니다. 서버가 실행 중인지 확인해 주세요.');
      }
      
      throw error;
    }
  }

  static getThreadId(): string {
    return this.threadId;
  }

  static resetThread(): void {
    this.threadId = `user-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    console.log('🔄 새 스레드 생성:', this.threadId);
  }

  static getApiUrl(): string {
    return API_BASE_URL;
  }
} 