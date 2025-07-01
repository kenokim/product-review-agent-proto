import time
import uuid
import logging
from typing import Dict, Any, List
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import HumanMessage

from app.graph.graph import graph, invoke_with_logging
from app.schemas.chat_schema import ChatRequest, ChatResponse, SourceInfo
from app.core.config import settings

# 로거 설정
logger = logging.getLogger(__name__)

class ChatService:
    """채팅 서비스 클래스"""
    
    def __init__(self):
        self.graph = graph
    
    async def process_chat_request(self, request: ChatRequest) -> ChatResponse:
        """채팅 요청을 처리하고 응답을 반환합니다."""
        
        start_time = time.time()
        
        try:
            # 스레드 ID 생성 (없는 경우)
            thread_id = request.thread_id or f"thread-{uuid.uuid4()}"
            
            # 설정 구성
            config = self._create_config(request, thread_id)
            
            # 그래프 실행
            result = await self._execute_graph(request.message, config)

            # 응답 구성
            processing_time = time.time() - start_time
            return self._create_response(result, thread_id, processing_time)
            
        except Exception as e:
            # 에러 처리
            raise self._create_error_response(str(e), f"채팅 처리 중 오류 발생: {str(e)}")
    
    def _create_config(self, request: ChatRequest, thread_id: str) -> RunnableConfig:
        """그래프 실행을 위한 설정을 생성합니다."""
        
        # 기본 설정에서 시작
        configurable = {
            "validation_model": settings.validation_model,
            "search_model": settings.search_model,
            "analysis_model": settings.analysis_model,
            "max_search_queries": request.max_search_queries or settings.max_search_queries,
            "max_search_loops": request.max_search_loops or settings.max_search_loops,
            "thread_id": thread_id,  # Checkpointer가 인식할 수 있도록 추가
        }
        
        config = RunnableConfig(
            configurable=configurable,
            metadata={"thread_id": thread_id}
        )
        
        return config
    
    async def _execute_graph(self, message: str, config: RunnableConfig) -> Dict[str, Any]:
        """그래프를 실행하고 결과를 반환합니다."""
        
        # 초기 상태 설정
        initial_state = {
            "messages": [HumanMessage(content=message)]
        }
        
        # stream_log 기반 실행 (invoke_with_logging 사용)
        result = invoke_with_logging(initial_state, config)
        
        return result
    
    def _create_response(self, result: Dict[str, Any], thread_id: str, processing_time: float) -> ChatResponse:
        """그래프 결과를 API 응답 형태로 변환합니다."""
        
        # 메시지 추출
        messages = result.get("messages", [])
        last_message = ""
        if messages:
            # 마지막 assistant 메시지 찾기 (AIMessage 객체와 dict 모두 처리)
            for msg in reversed(messages):
                if hasattr(msg, 'content'):  # AIMessage 객체 처리
                    last_message = msg.content
                    break
                elif isinstance(msg, dict) and msg.get("role") == "assistant":  # dict 처리
                    last_message = msg.get("content", "")
                    break
        
        # 구체화 질문 여부 확인
        is_clarification = result.get("is_clarification_question", False)
        
        # 출처 정보 추출
        sources = self._extract_sources(result)
        
        # 사용된 검색어 추출
        search_queries_used = result.get("search_queries", [])
        if isinstance(search_queries_used, dict):
            search_queries_used = search_queries_used.get("queries", [])
        
        return ChatResponse(
            message=last_message or "응답을 생성할 수 없습니다.",
            thread_id=thread_id,
            sources=sources,
            processing_time=processing_time,
            search_queries_used=search_queries_used,
            is_clarification=is_clarification
        )
    
    def _extract_sources(self, result: Dict[str, Any]) -> List[SourceInfo]:
        """결과에서 출처 정보를 추출합니다."""
        
        try:
            sources = []
            sources_gathered = result.get("sources_gathered", [])
            
            if sources_gathered is None:
                sources_gathered = []
            
            for source in sources_gathered:
                if isinstance(source, dict):
                    title = source.get("title", "제목 없음")
                    url = source.get("url", "")
                    short_url = source.get("short_url")
                    
                    if url:  # URL이 있는 경우만 추가
                        sources.append(SourceInfo(
                            title=title,
                            url=url,
                            short_url=short_url
                        ))
            
            return sources
            
        except Exception as e:
            logger.error(f"출처 정보 추출 중 오류: {str(e)}")
            return []
    
    def _create_error_response(self, error_message: str, detail: str = None) -> Exception:
        """에러 응답을 생성합니다."""
        return Exception(f"{error_message}: {detail}" if detail else error_message) 