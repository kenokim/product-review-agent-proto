from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class ChatMessage(BaseModel):
    """채팅 메시지 스키마"""
    role: str = Field(..., description="메시지 역할 (user, assistant)")
    content: str = Field(..., description="메시지 내용")

class ChatRequest(BaseModel):
    """채팅 요청 스키마"""
    message: str = Field(..., description="사용자 메시지", min_length=1)
    thread_id: Optional[str] = Field(None, description="대화 스레드 ID")
    
    # 선택적 설정 오버라이드
    max_search_queries: Optional[int] = Field(None, description="최대 검색어 수", ge=1, le=10)
    max_search_loops: Optional[int] = Field(None, description="최대 검색 루프 수", ge=1, le=5)
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "가성비 좋은 무선 이어폰 추천해주세요",
                "thread_id": "user-123-session-456"
            }
        }

class SourceInfo(BaseModel):
    """출처 정보"""
    title: str = Field(..., description="출처 제목")
    url: str = Field(..., description="출처 URL")
    short_url: Optional[str] = Field(None, description="단축 URL")

class ChatResponse(BaseModel):
    """채팅 응답 스키마"""
    message: str = Field(..., description="AI 응답 메시지")
    thread_id: str = Field(..., description="대화 스레드 ID")
    sources: List[SourceInfo] = Field(default=[], description="참조한 출처 목록")
    
    # 메타데이터
    processing_time: Optional[float] = Field(None, description="처리 시간 (초)")
    search_queries_used: List[str] = Field(default=[], description="사용된 검색어 목록")
    is_clarification: bool = Field(False, description="구체화 질문 여부")
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "다음과 같은 가성비 좋은 무선 이어폰을 추천드립니다...",
                "thread_id": "user-123-session-456",
                "sources": [
                    {
                        "title": "2024년 최고의 가성비 무선 이어폰 추천",
                        "url": "https://example.com/review"
                    }
                ],
                "processing_time": 5.23,
                "search_queries_used": ["가성비 무선 이어폰", "무선 이어폰 추천 2024"],
                "is_clarification": False
            }
        }

class ErrorResponse(BaseModel):
    """에러 응답 스키마"""
    error: str = Field(..., description="에러 메시지")
    detail: Optional[str] = Field(None, description="상세 에러 정보")
    timestamp: datetime = Field(default_factory=datetime.now, description="에러 발생 시간")
    
    class Config:
        json_schema_extra = {
            "example": {
                "error": "Invalid request",
                "detail": "검색어 생성에 실패했습니다.",
                "timestamp": "2024-12-23T07:30:00"
            }
        } 