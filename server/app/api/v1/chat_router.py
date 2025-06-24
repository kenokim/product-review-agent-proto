from fastapi import APIRouter, HTTPException, status
import logging

from app.schemas.chat_schema import ChatRequest, ChatResponse, ErrorResponse
from app.services.chat_service import ChatService

# 로거 설정
logger = logging.getLogger(__name__)

# 라우터 생성
router = APIRouter()

# 채팅 서비스 인스턴스
chat_service = ChatService()

@router.post(
    "/chat", 
    response_model=ChatResponse,
    responses={
        400: {"model": ErrorResponse, "description": "잘못된 요청"},
        500: {"model": ErrorResponse, "description": "서버 오류"}
    },
    summary="채팅 메시지 처리",
    description="사용자의 채팅 메시지를 받아 제품 추천 AI 에이전트로 처리하고 응답을 반환합니다."
)
async def chat(request: ChatRequest) -> ChatResponse:
    """
    채팅 메시지를 처리합니다.
    
    - **message**: 사용자 메시지 (필수)
    - **thread_id**: 대화 스레드 ID (선택, 없으면 자동 생성)
    - **max_search_queries**: 최대 검색어 수 (선택, 기본값: 3)
    - **max_search_loops**: 최대 검색 루프 수 (선택, 기본값: 2)
    """
    try:
        logger.info(f"채팅 요청 처리 시작: {request.message[:50]}...")
        
        # 채팅 서비스를 통해 요청 처리
        response = await chat_service.process_chat_request(request)
        
        # 응답 결과 로깅
        logger.info(f"=== API 응답 결과 (thread_id: {response.thread_id}) ===")
        logger.info(f"응답 메시지: {response.message[:100]}{'...' if len(response.message) > 100 else ''}")
        logger.info(f"처리 시간: {response.processing_time:.2f}초")
        logger.info(f"사용된 검색어: {response.search_queries_used}")
        logger.info(f"출처 개수: {len(response.sources)}")
        logger.info(f"구체화 질문 여부: {response.is_clarification}")
        
        for i, source in enumerate(response.sources):
            logger.info(f"출처 {i+1}: {source.title} - {source.url}")
        
        logger.info(f"채팅 요청 처리 완료: thread_id={response.thread_id}")
        
        return response
        
    except ValueError as e:
        logger.error(f"입력 검증 오류: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"입력 검증 오류: {str(e)}"
        )
    except Exception as e:
        logger.error(f"채팅 처리 중 오류 발생: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"채팅 처리 중 오류가 발생했습니다: {str(e)}"
        )

 