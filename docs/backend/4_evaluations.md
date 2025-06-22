# LangGraph 노드별 테스트 및 평가 가이드

## 개요

LangGraph 애플리케이션의 품질을 보장하기 위해서는 체계적인 테스트 전략이 필요합니다. 이 문서는 노드별 테스트 방법과 평가 기법을 제공합니다.

## 테스트 피라미드 (Test Pyramid)

### Level 0: 단위 테스트 (Unit Tests)
- **목적**: 개별 노드 함수의 로직 검증
- **특징**: LLM 호출 모킹, 빠른 실행, 비용 효율적
- **범위**: 모든 엣지 케이스 커버

### Level 1: 그래프 라우팅 테스트
- **목적**: 노드 간 연결과 조건부 엣지 검증
- **특징**: 노드는 모킹하되 라우팅 로직은 실제 사용
- **범위**: 워크플로 흐름의 모든 경로

### Level 2: 통합/E2E 테스트
- **목적**: 전체 플로우의 실제 동작 검증
- **특징**: 모델 출력 캐싱으로 비용 절약
- **범위**: 주요 시나리오만 커버

## 노드별 테스트 방법

### 1. 개별 노드 직접 테스트

```python
# 방법 1: 컴파일된 그래프에서 노드 접근
graph = create_product_recommendation_graph()
result = graph.nodes["validate_request"].invoke(state)

# 방법 2: 노드 함수 직접 호출
from app.graph.graph import validate_request
result = validate_request(state)
```

### 2. 모킹을 활용한 단위 테스트

```python
def test_validate_request_node():
    with patch('app.graph.graph.genai') as mock_genai:
        mock_genai.GenerativeModel.return_value.generate_content.return_value.text = '''
        {
            "is_specific": true,
            "extracted_requirements": {"category": "smartphone"},
            "clarification_question": ""
        }
        '''
        
        graph = create_product_recommendation_graph()
        state = {"messages": [{"role": "user", "content": "아이폰 추천해주세요"}]}
        
        result = graph.nodes["validate_request"].invoke(state)
        
        assert "request_validation" in result
        assert result["request_validation"]["is_specific"] == True
```

### 3. 그래프 흐름 테스트

```python
def test_graph_routing():
    with patch('app.graph.graph.genai') as mock_genai:
        # 각 노드의 응답을 순서대로 설정
        mock_genai.GenerativeModel.return_value.generate_content.side_effect = [
            MagicMock(text='{"is_specific": true, ...}'),  # validate_request
            MagicMock(text='{"queries": ["test"]}'),       # generate_queries
            MagicMock(text='search results'),               # web_search
            MagicMock(text='{"needs_more_search": false}'), # reflection
            MagicMock(text='final answer')                  # format_response
        ]
        
        graph = create_product_recommendation_graph()
        state = {"messages": [{"role": "user", "content": "아이폰 추천"}]}
        
        # 실행 경로 추적
        events = []
        for event in graph.stream(state):
            events.append(list(event.keys())[0])
        
        expected_path = ["validate_request", "generate_queries", "web_search", "reflection", "format_response"]
        assert events == expected_path
```

## 테스트 시나리오

### 1. 정상 시나리오
- 구체적인 요청 → 전체 플로우 실행
- 모호한 요청 → 구체화 질문 반환
- 추가 검색 필요 → reflection 루프 실행

### 2. 에러 시나리오
- LLM API 호출 실패
- 잘못된 JSON 응답
- 네트워크 타임아웃
- 상태 검증 실패

### 3. 엣지 케이스
- 빈 검색 결과
- 매우 긴 사용자 입력
- 특수 문자 포함 요청
- 다국어 입력

## 성능 테스트

### 1. 노드 실행 시간 측정

```python
def test_node_performance():
    import time
    
    graph = create_product_recommendation_graph()
    state = {"messages": [{"role": "user", "content": "테스트"}]}
    
    start_time = time.time()
    result = graph.nodes["validate_request"].invoke(state)
    end_time = time.time()
    
    # 1초 이내 완료 확인
    assert (end_time - start_time) < 1.0
```

### 2. 메모리 사용량 모니터링

```python
import psutil
import os

def test_memory_usage():
    process = psutil.Process(os.getpid())
    initial_memory = process.memory_info().rss
    
    # 그래프 실행
    graph = create_product_recommendation_graph()
    result = graph.invoke({"messages": [{"role": "user", "content": "테스트"}]})
    
    final_memory = process.memory_info().rss
    memory_increase = final_memory - initial_memory
    
    # 메모리 증가량이 100MB 이하인지 확인
    assert memory_increase < 100 * 1024 * 1024
```

## 평가 지표

### 1. 기능적 지표
- **정확성**: 올바른 제품 추천 여부
- **완전성**: 필요한 정보 모두 포함 여부
- **관련성**: 사용자 요구사항과의 일치도

### 2. 성능 지표
- **응답 시간**: 각 노드별 실행 시간
- **처리량**: 단위 시간당 처리 가능한 요청 수
- **메모리 사용량**: 실행 중 메모리 소비량

### 3. 품질 지표
- **일관성**: 동일 입력에 대한 안정적 출력
- **견고성**: 예외 상황 처리 능력
- **확장성**: 부하 증가 시 성능 유지

## 테스트 자동화

### 1. CI/CD 파이프라인 통합

```yaml
# .github/workflows/test.yml
name: Test
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      - name: Run tests
        run: |
          pytest -v --cov=app
```

### 2. 테스트 데이터 관리

```python
# test_data.py
TEST_SCENARIOS = {
    "specific_request": {
        "input": {"messages": [{"role": "user", "content": "아이폰 15 추천해주세요"}]},
        "expected_path": ["validate_request", "generate_queries", "web_search", "reflection", "format_response"]
    },
    "vague_request": {
        "input": {"messages": [{"role": "user", "content": "뭔가 추천해주세요"}]},
        "expected_path": ["validate_request", "format_response"]
    }
}
```

## 모니터링 및 로깅

### 1. 테스트 결과 추적

```python
import logging

# 테스트 로그 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('test_results.log'),
        logging.StreamHandler()
    ]
)

def test_with_logging():
    logger = logging.getLogger(__name__)
    logger.info("Starting test execution")
    
    try:
        # 테스트 실행
        result = run_test()
        logger.info(f"Test passed: {result}")
    except Exception as e:
        logger.error(f"Test failed: {e}")
        raise
```

### 2. 메트릭 수집

```python
import time
from collections import defaultdict

class TestMetrics:
    def __init__(self):
        self.execution_times = defaultdict(list)
        self.success_rates = defaultdict(int)
        self.error_counts = defaultdict(int)
    
    def record_execution_time(self, node_name, duration):
        self.execution_times[node_name].append(duration)
    
    def record_success(self, test_name):
        self.success_rates[test_name] += 1
    
    def record_error(self, test_name, error_type):
        self.error_counts[f"{test_name}_{error_type}"] += 1
    
    def get_average_execution_time(self, node_name):
        times = self.execution_times[node_name]
        return sum(times) / len(times) if times else 0
```

## 베스트 프랙티스

### 1. 테스트 작성 원칙
- **독립성**: 각 테스트는 서로 독립적으로 실행
- **반복성**: 동일한 결과를 항상 생성
- **명확성**: 테스트 의도가 명확히 드러남
- **속도**: 빠른 피드백을 위한 효율적 실행

### 2. 모킹 전략
- **최소 모킹**: 필요한 부분만 모킹
- **현실적 응답**: 실제 API 응답과 유사한 모킹 데이터
- **에러 시뮬레이션**: 다양한 실패 상황 테스트

### 3. 데이터 관리
- **테스트 데이터 분리**: 프로덕션 데이터와 완전 분리
- **데이터 정리**: 테스트 후 임시 데이터 정리
- **버전 관리**: 테스트 데이터의 버전 관리

## 실행 방법

### 1. 전체 테스트 실행
```bash
cd server
pytest -v
```

### 2. 특정 테스트 실행
```bash
# 단위 테스트만 실행
pytest -m unit

# 특정 노드 테스트만 실행
pytest -k "validate_request"

# 커버리지 포함 실행
pytest --cov=app --cov-report=html
```

### 3. 성능 테스트 실행
```bash
# 느린 테스트 포함
pytest -m slow

# 병렬 실행
pytest -n auto
```

이 가이드를 통해 LangGraph 애플리케이션의 품질을 체계적으로 관리하고, 안정적인 제품 추천 서비스를 구축할 수 있습니다.