from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import logging

from app.api.v1.chat_router import router as chat_router
from app.core.config import settings

# 환경 변수 로드
load_dotenv()

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # 콘솔 출력
    ]
)

# FastAPI 앱 초기화
app = FastAPI(
    title="Product Recommendation Agent",
    description="LangGraph 기반 제품 추천 AI 에이전트",
    version="1.0.0"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 프로덕션에서는 구체적인 도메인 지정
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API 라우터 등록
app.include_router(chat_router, prefix="/api/v1", tags=["chat"])

@app.get("/")
async def root():
    """헬스 체크 엔드포인트"""
    return {"message": "Product Recommendation Agent API", "status": "running"}

@app.get("/health")
async def health_check():
    """헬스 체크"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    ) 