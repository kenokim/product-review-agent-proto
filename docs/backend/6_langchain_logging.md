# LangChain/LangGraph 노드 로깅 가이드

## 개요

LangChain과 LangGraph에서 제공하는 다양한 로깅 및 디버깅 방법을 소개합니다. 복잡한 에이전트나 체인에서 실행 과정을 추적하고 디버깅하는 것은 매우 중요합니다.

## 1. LangSmith를 통한 트레이싱

### 1.1 환경 변수 설정

```bash
export LANGCHAIN_TRACING_V2="true"
export LANGCHAIN_API_KEY="your-api-key"
```

또는 Python 코드에서:

```python
import getpass
import os

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = getpass.getpass()
```

### 1.2 LangSmith의 장점

- **전체 실행 과정 시각화**: 각 노드의 입력/출력을 시각적으로 확인
- **성능 모니터링**: 각 단계별 실행 시간 측정
- **에러 추적**: 실패한 지점과 원인 파악
- **A/B 테스트**: 다양한 프롬프트나 모델 비교

## 2. 그래프 노드별 커스텀 로깅

### 2.1 기본 로깅 패턴

```python
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def my_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """노드 실행 함수에서 로깅 구현"""
    
    # 노드 시작 로깅
    logger.info(f"=== 노드 실행 시작: {__name__} ===")
    logger.info(f"입력 상태: {state.keys()}")
    
    try:
        # 실제 노드 로직
        result = process_logic(state)
        
        # 성공 로깅
        logger.info(f"노드 실행 완료: {len(result)} 항목 처리됨")
        
        return {"result": result}
        
    except Exception as e:
        # 에러 로깅
        logger.error(f"노드 실행 실패: {str(e)}")
        raise
```

### 2.2 상태 기반 로깅

```python
def log_state_changes(before_state: Dict, after_state: Dict, node_name: str):
    """상태 변화를 로깅하는 헬퍼 함수"""
    
    logger.info(f"=== {node_name} 상태 변화 ===")
    
    # 새로 추가된 키들
    new_keys = set(after_state.keys()) - set(before_state.keys())
    if new_keys:
        logger.info(f"새로 추가된 키: {new_keys}")
    
    # 변경된 키들
    for key in before_state.keys() & after_state.keys():
        if before_state[key] != after_state[key]:
            logger.info(f"변경된 키 '{key}': {type(before_state[key])} -> {type(after_state[key])}")

def search_node(state: Dict[str, Any]) -> Dict[str, Any]:
    before_state = state.copy()
    
    # 검색 로직 실행
    search_results = perform_search(state["query"])
    
    after_state = {**state, "search_results": search_results}
    
    # 상태 변화 로깅
    log_state_changes(before_state, after_state, "search_node")
    
    return after_state
```

## 3. 구조화된 로깅

### 3.1 JSON 형태 로깅

```python
import json
from datetime import datetime

def structured_log(node_name: str, event_type: str, data: Dict[str, Any]):
    """구조화된 로그 출력"""
    
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "node": node_name,
        "event": event_type,
        "data": data
    }
    
    logger.info(json.dumps(log_entry, ensure_ascii=False, indent=2))

def analysis_node(state: Dict[str, Any]) -> Dict[str, Any]:
    # 노드 시작 로깅
    structured_log("analysis_node", "start", {
        "input_keys": list(state.keys()),
        "message_count": len(state.get("messages", []))
    })
    
    # 분석 실행
    analysis_result = analyze_content(state)
    
    # 노드 완료 로깅
    structured_log("analysis_node", "complete", {
        "analysis_type": analysis_result.get("type"),
        "confidence": analysis_result.get("confidence"),
        "processing_time": analysis_result.get("processing_time")
    })
    
    return {**state, "analysis": analysis_result}
```

### 3.2 성능 측정 로깅

```python
import time
from functools import wraps

def log_execution_time(func):
    """노드 실행 시간을 측정하는 데코레이터"""
    
    @wraps(func)
    def wrapper(state: Dict[str, Any]) -> Dict[str, Any]:
        start_time = time.time()
        node_name = func.__name__
        
        logger.info(f"[{node_name}] 실행 시작")
        
        try:
            result = func(state)
            execution_time = time.time() - start_time
            
            logger.info(f"[{node_name}] 실행 완료 - {execution_time:.2f}초")
            
            return result
            
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"[{node_name}] 실행 실패 - {execution_time:.2f}초, 오류: {str(e)}")
            raise
    
    return wrapper

@log_execution_time
def web_search_node(state: Dict[str, Any]) -> Dict[str, Any]:
    # 웹 검색 로직
    return perform_web_search(state)
```

## 4. 조건부 로깅

### 4.1 로그 레벨 관리

```python
def conditional_log(level: str, node_name: str, message: str, data: Any = None):
    """조건부 로깅 (개발/운영 환경 구분)"""
    
    if level == "DEBUG" and logger.isEnabledFor(logging.DEBUG):
        logger.debug(f"[{node_name}] {message}: {data}")
    elif level == "INFO":
        logger.info(f"[{node_name}] {message}")
    elif level == "ERROR":
        logger.error(f"[{node_name}] {message}: {data}")

def validation_node(state: Dict[str, Any]) -> Dict[str, Any]:
    # 디버그 레벨에서만 상세 로깅
    conditional_log("DEBUG", "validation_node", "입력 검증 시작", state)
    
    validation_result = validate_input(state)
    
    if validation_result["is_valid"]:
        conditional_log("INFO", "validation_node", "입력 검증 성공")
    else:
        conditional_log("ERROR", "validation_node", "입력 검증 실패", 
                       validation_result["errors"])
    
    return {**state, "validation": validation_result}
```

## 5. 통합 로깅 패턴

### 5.1 그래프 레벨 로깅

```python
class GraphLogger:
    """그래프 전체의 로깅을 관리하는 클래스"""
    
    def __init__(self, graph_name: str):
        self.graph_name = graph_name
        self.start_time = None
        self.node_times = {}
    
    def log_graph_start(self, initial_state: Dict[str, Any]):
        """그래프 실행 시작 로깅"""
        self.start_time = time.time()
        logger.info(f"=== {self.graph_name} 실행 시작 ===")
        logger.info(f"초기 상태: {list(initial_state.keys())}")
    
    def log_node_execution(self, node_name: str, before_state: Dict, after_state: Dict):
        """각 노드 실행 로깅"""
        node_start = time.time()
        
        # 노드별 실행 시간 기록
        if node_name not in self.node_times:
            self.node_times[node_name] = []
        
        execution_time = time.time() - node_start
        self.node_times[node_name].append(execution_time)
        
        logger.info(f"[{node_name}] 실행 완료 - {execution_time:.2f}초")
        
        # 상태 변화 요약
        new_keys = set(after_state.keys()) - set(before_state.keys())
        if new_keys:
            logger.info(f"[{node_name}] 새로운 상태 키: {new_keys}")
    
    def log_graph_complete(self, final_state: Dict[str, Any]):
        """그래프 실행 완료 로깅"""
        total_time = time.time() - self.start_time
        
        logger.info(f"=== {self.graph_name} 실행 완료 ===")
        logger.info(f"총 실행 시간: {total_time:.2f}초")
        logger.info(f"최종 상태: {list(final_state.keys())}")
        
        # 노드별 성능 요약
        for node_name, times in self.node_times.items():
            avg_time = sum(times) / len(times)
            logger.info(f"[{node_name}] 평균 실행 시간: {avg_time:.2f}초 ({len(times)}회 실행)")

# 사용 예시
graph_logger = GraphLogger("product_research_graph")

def execute_graph_with_logging(initial_state: Dict[str, Any]):
    graph_logger.log_graph_start(initial_state)
    
    # 그래프 실행 로직
    result = graph.invoke(initial_state)
    
    graph_logger.log_graph_complete(result)
    
    return result
```

## 6. 실제 적용 예시

### 6.1 제품 리서치 에이전트 로깅

```python
def product_research_logging_example():
    """실제 제품 리서치 에이전트에서의 로깅 적용"""
    
    @log_execution_time
    def search_queries_generation_node(state: Dict[str, Any]) -> Dict[str, Any]:
        logger.info("=== 검색어 생성 노드 시작 ===")
        
        user_query = state.get("messages", [])[-1].get("content", "")
        logger.info(f"사용자 질의: {user_query}")
        
        # 검색어 생성 로직
        search_queries = generate_search_queries(user_query)
        
        logger.info(f"생성된 검색어 수: {len(search_queries)}")
        for i, query in enumerate(search_queries, 1):
            logger.info(f"검색어 {i}: {query}")
        
        return {**state, "search_queries": search_queries}
    
    @log_execution_time
    def web_search_node(state: Dict[str, Any]) -> Dict[str, Any]:
        logger.info("=== 웹 검색 노드 시작 ===")
        
        search_queries = state.get("search_queries", [])
        all_results = []
        
        for i, query in enumerate(search_queries, 1):
            logger.info(f"검색 {i}/{len(search_queries)}: {query}")
            
            try:
                results = perform_web_search(query)
                all_results.extend(results)
                logger.info(f"검색 결과: {len(results)}개 수집")
                
            except Exception as e:
                logger.error(f"검색 실패: {str(e)}")
        
        logger.info(f"총 수집된 결과: {len(all_results)}개")
        
        return {**state, "web_research_result": all_results}
    
    @log_execution_time
    def analysis_node(state: Dict[str, Any]) -> Dict[str, Any]:
        logger.info("=== 분석 노드 시작 ===")
        
        search_results = state.get("web_research_result", [])
        logger.info(f"분석할 결과 수: {len(search_results)}")
        
        # 분석 로직
        analysis = analyze_search_results(search_results)
        
        logger.info("분석 완료")
        logger.info(f"주요 키워드: {analysis.get('keywords', [])}")
        logger.info(f"신뢰도: {analysis.get('confidence', 0)}")
        
        return {**state, "analysis_result": analysis}
```

## 7. 모니터링 및 알림

### 7.1 실시간 모니터링

```python
import threading
from collections import defaultdict

class GraphMonitor:
    """그래프 실행 모니터링"""
    
    def __init__(self):
        self.execution_stats = defaultdict(list)
        self.error_count = defaultdict(int)
        self.lock = threading.Lock()
    
    def record_execution(self, node_name: str, execution_time: float, success: bool):
        with self.lock:
            self.execution_stats[node_name].append(execution_time)
            if not success:
                self.error_count[node_name] += 1
    
    def get_stats(self) -> Dict[str, Any]:
        with self.lock:
            stats = {}
            for node_name, times in self.execution_stats.items():
                stats[node_name] = {
                    "avg_time": sum(times) / len(times),
                    "min_time": min(times),
                    "max_time": max(times),
                    "total_executions": len(times),
                    "error_count": self.error_count[node_name]
                }
            return stats
    
    def check_health(self) -> bool:
        """시스템 상태 체크"""
        stats = self.get_stats()
        
        for node_name, node_stats in stats.items():
            # 에러율이 10% 이상이면 경고
            error_rate = node_stats["error_count"] / node_stats["total_executions"]
            if error_rate > 0.1:
                logger.warning(f"[{node_name}] 높은 에러율: {error_rate:.2%}")
                return False
            
            # 평균 실행 시간이 30초 이상이면 경고
            if node_stats["avg_time"] > 30:
                logger.warning(f"[{node_name}] 긴 실행 시간: {node_stats['avg_time']:.2f}초")
                return False
        
        return True

# 전역 모니터 인스턴스
graph_monitor = GraphMonitor()
```

## 8. 베스트 프랙티스

### 8.1 로깅 가이드라인

1. **구조화된 로깅 사용**: JSON 형태로 일관된 로그 포맷 유지
2. **적절한 로그 레벨**: DEBUG, INFO, WARNING, ERROR 레벨을 적절히 활용
3. **성능 측정**: 각 노드의 실행 시간을 측정하여 병목 지점 파악
4. **에러 컨텍스트**: 에러 발생 시 충분한 컨텍스트 정보 포함
5. **민감 정보 보호**: 개인정보나 API 키 등은 로그에서 제외

### 8.2 운영 환경 고려사항

- **로그 레벨 조정**: 운영 환경에서는 INFO 레벨 이상만 출력
- **로그 로테이션**: 로그 파일 크기 관리
- **중앙 집중식 로깅**: ELK Stack, Fluentd 등 활용
- **알림 시스템**: 크리티컬 에러 발생 시 즉시 알림

## 결론

LangChain/LangGraph에서 효과적인 로깅은 시스템의 안정성과 디버깅 효율성을 크게 향상시킵니다. LangSmith를 통한 자동 트레이싱과 커스텀 로깅을 조합하여 사용하면 복잡한 에이전트 시스템도 효과적으로 모니터링하고 관리할 수 있습니다.
