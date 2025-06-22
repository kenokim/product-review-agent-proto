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

### 4. LangGraph 개발 서버 실행
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

# 특정 제품 케이스만 테스트
pytest -k "earphones" -v
```

### 테스트 커버리지 확인
```bash
pytest --cov=app --cov-report=html
```

## 📁 구조
- `app/graph/graph.py`: 제품 추천 그래프 구현
- `app/graph/state.py`: 상태 정의 및 설정
- `app/graph/prompts.py`: 프롬프트 템플릿
- `app/graph/tools_and_schemas.py`: 구조화된 출력 스키마
- `test_graph.py`: 노드별 단위 테스트
- `requirements.txt`: 필요한 패키지 목록

## 🔧 주요 기능
- 사용자 요청 검증 및 구체화
- 병렬 웹 검색 (Gemini API)
- 검색 결과 평가 및 추가 검색
- 마크다운 형식 응답 생성

