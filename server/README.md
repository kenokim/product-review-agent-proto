# Product Recommendation Server

LangGraph 기반 제품 추천 AI 에이전트

## 🚀 빠른 시작

### 1. 가상환경 설정
```bash
# 가상환경 생성
python -m venv venv

# 가상환경 활성화
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 2. 의존성 설치
```bash
pip install -r requirements.txt
```

### 3. 환경변수 설정
```bash
# .env 파일 생성
GEMINI_API_KEY=your_gemini_api_key_here
```

### 4. 서버 실행

#### 방법 1: FastAPI 서버 실행 (권장)
```bash
# FastAPI 서버 시작
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# 또는 Python으로 직접 실행
python app/main.py
```

#### 방법 2: LangGraph 개발 서버 실행
```bash
# LangGraph CLI 설치
pip install -U "langgraph-cli[inmem]"

# 개발 서버 시작
langgraph dev
```

### 5. 사용 예시
```python
from app.graph.graph import run_product_recommendation_sync

# 제품 추천 실행
result = run_product_recommendation_sync("10만원 이하 가성비 좋은 게이밍 키보드 추천해줘")
print(result)
```

## 🧪 테스트 실행

### 전체 테스트 실행
```bash
pytest -v
```

### 특정 노드 테스트
```bash
# validate_request 노드만 테스트
pytest -k "validate_request" -v

# 자동화된 API 테스트 실행
cd eval
python test_query_sender.py
```

### 테스트 커버리지 확인
```bash
pytest --cov=app --cov-report=html
```

## 📁 구조

### FastAPI 애플리케이션
- `app/main.py`: FastAPI 애플리케이션 진입점
- `app/api/v1/chat_router.py`: 채팅 API 라우터
- `app/services/chat_service.py`: 비즈니스 로직 서비스
- `app/schemas/chat_schema.py`: API 요청/응답 스키마
- `app/core/config.py`: 애플리케이션 설정

### LangGraph 그래프
- `app/graph/graph.py`: 제품 추천 그래프 구현
- `app/graph/state.py`: 상태 정의 및 설정
- `app/graph/prompts.py`: 프롬프트 템플릿
- `app/graph/tools_and_schemas.py`: 구조화된 출력 스키마
- `app/graph/utils.py`: 유틸리티 함수

### 기타
- `test_graph.py`: 노드별 단위 테스트
- `requirements.txt`: 필요한 패키지 목록

## 🔧 주요 기능
- 사용자 요청 검증 및 구체화
- 병렬 웹 검색 (Gemini API)
- 검색 결과 평가 및 추가 검색
- 마크다운 형식 응답 생성
