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

## 5. LangSmith 없이 간단하게 로깅하기 (`stream_log`)

LangSmith 설정을 하지 않고도 LangGraph의 실행 흐름을 디버깅하고 싶을 때, `stream_log` 메서드를 사용하면 매우 간단하게 각 노드의 실행 과정을 추적할 수 있습니다.

`stream_log`는 그래프 실행의 모든 단계를 스트리밍으로 반환하며, 각 단계(op)의 이름, 경로(path), 그리고 노드의 최종 출력(final_output) 등을 포함한 로그 객체를 제공합니다.

### 5.1 사용 예제

아래는 `stream_log`를 사용하여 그래프의 실행 과정을 로깅하는 간단한 예제 코드입니다.

```python
import operator
from typing import Annotated, TypedDict

from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages

# 1. 그래프 상태 정의
class State(TypedDict):
    messages: Annotated[list, add_messages]

# 2. 그래프 및 노드 생성
graph_builder = StateGraph(State)

def greet(state: State):
    return {"messages": ["Hello!"]}

def ask_question(state: State):
    return {"messages": ["How can I help you?"]}

graph_builder.add_node("greeter", greet)
graph_builder.add_node("questioner", ask_question)
graph_builder.add_edge("greeter", "questioner")
graph_builder.set_entry_point("greeter")
graph_builder.set_finish_point("questioner")

graph = graph_builder.compile()

# 3. stream_log를 사용한 실행 및 로깅
async def run_and_log():
    async for log in graph.astream_log(
        {"messages": [HumanMessage(content="Start")]},
    ):
        print("---")
        print(f"OP: {log.op}")
        print(f"PATH: {log.path}")
        if 'final_output' in log.data:
            print(f"OUTPUT: {log.data['final_output']}")

# 실행
import asyncio
asyncio.run(run_and_log())
```

### 5.2 로그 출력 해석

위 코드를 실행하면 다음과 유사한 로그가 터미널에 출력됩니다. 이를 통해 어떤 노드가 어떤 순서로 실행되었고, 각 노드가 어떤 결과를 반환했는지 명확히 알 수 있습니다.

```
---
OP: add
PATH: /logs/greeter
OUTPUT: {'messages': ['Hello!']}
---
OP: add
PATH: /logs/questioner
OUTPUT: {'messages': ['How can I help you?']}
---
OP: add
PATH: /logs/__end__
OUTPUT: {'messages': [HumanMessage(content='Start'), 'Hello!', 'How can I help you?']}
```

이처럼 `stream_log`를 활용하면 외부 도구 없이도 print 문만으로 충분히 LangGraph의 동작을 디버깅하고 이해할 수 있습니다.

## 6. 베스트 프랙티스

### 6.1 로깅 가이드라인

1. **구조화된 로깅 사용**: JSON 형태로 일관된 로그 포맷 유지
2. **적절한 로그 레벨**: DEBUG, INFO, WARNING, ERROR 레벨을 적절히 활용
3. **성능 측정**: 각 노드의 실행 시간을 측정하여 병목 지점 파악
4. **에러 컨텍스트**: 에러 발생 시 충분한 컨텍스트 정보 포함
5. **민감 정보 보호**: 개인정보나 API 키 등은 로그에서 제외

### 6.2 운영 환경 고려사항

- **로그 레벨 조정**: 운영 환경에서는 INFO 레벨 이상만 출력
- **로그 로테이션**: 로그 파일 크기 관리
- **중앙 집중식 로깅**: ELK Stack, Fluentd 등 활용
- **알림 시스템**: 크리티컬 에러 발생 시 즉시 알림

## 결론

LangChain/LangGraph에서 효과적인 로깅은 시스템의 안정성과 디버깅 효율성을 크게 향상시킵니다. LangSmith를 통한 자동 트레이싱과 커스텀 로깅을 조합하여 사용하면 복잡한 에이전트 시스템도 효과적으로 모니터링하고 관리할 수 있습니다.
