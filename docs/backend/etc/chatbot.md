# LangGraph로 챗봇 만들기: 한국어 요약 & 코드 분석

> 이 문서는 `chatbot.ipynb` 튜토리얼을 한국어로 정리한 것입니다. 단계별 코드와 함께 **LangGraph** 기반 챗봇을 구현하는 핵심 개념을 살펴봅니다.

---

## 1. 사전 준비

```bash
pip install langchain-core langgraph>=0.2.28
```

환경 변수(예: `OPENAI_API_KEY`)도 미리 설정해 두세요.

---

## 2. LLM 직접 호출하기

```python
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

model = ChatOpenAI(model="gpt-4o-mini")
print(model.invoke([HumanMessage(content="Hi! I'm Bob")]))
```

* LL​M만 호출하면 **대화 기록이 유지되지 않음** → 후속 질문에 답하지 못함.

---

## 3. LangGraph 기본 구조

### 3-1. MessagesState 사용 (가장 단순한 상태)

```python
from langgraph.graph import START, MessagesState, StateGraph
from langgraph.checkpoint.memory import MemorySaver

workflow = StateGraph(state_schema=MessagesState)

# 모델 호출 노드
def call_model(state: MessagesState):
    response = model.invoke(state["messages"])
    return {"messages": response}

workflow.add_edge(START, "model")     # START ➜ model
workflow.add_node("model", call_model) # 노드 등록

memory = MemorySaver()                 # 인메모리 체크포인터
app = workflow.compile(checkpointer=memory)
```

* `MessagesState`는 `{"messages": ...}` 단일 필드로 구성된 LangGraph 내장 상태.
* `MemorySaver` 덕분에 **다중 턴 대화**가 가능.

#### 실행 예시

```python
from langchain_core.messages import HumanMessage
config = {"configurable": {"thread_id": "abc123"}}

msg = [HumanMessage(content="Hi! I'm Bob")]  # 첫 질문
print(app.invoke({"messages": msg}, config)["messages"][-1].content)
```

### 3-2. MemorySaver 작동 원리 & 주의사항

| 환경 | MemorySaver 필요 여부 | 이유 |
|-------|---------------------|------|
| **로컬 파이썬 스크립트/서버** | **필수** | 실행이 끝나면 상태가 사라지므로 `MemorySaver` 등 체크포인터가 있어야 `thread_id`별 대화가 이어집니다. |
| **LangGraph Cloud / Runtime(local_dev)** | 선택 | 플랫폼이 내부적으로 Postgres 체크포인터를 제공하므로 `checkpointer`를 지정하지 않아도 상태가 자동 저장됩니다. 지정하면 경고가 뜹니다. |

*MemorySaver* 는 **프로세스 메모리**에만 기록하므로 서버가 재시작되면 데이터가 사라집니다. 영구 저장이 필요하면 `SqliteSaver`(로컬 파일)나 `PostgresSaver`(DB)로 교체하세요.

---

## 4. 프롬프트 템플릿 & 커스텀 State 추가

사용자 정의 입력(`language`)을 추가하려면 상태를 확장해야 합니다.

### 4-1. 커스텀 State 정의

```python
from typing import Sequence
from typing_extensions import Annotated, TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class State(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]  # 대화 기록
    language: str                                            # 추가 파라미터
```

### 4-2. 프롬프트 템플릿 작성

```python
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

prompt_template = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a helpful assistant. Answer all questions to the best of your ability in {language}.",
    ),
    MessagesPlaceholder(variable_name="messages"),
])
```

### 4-3. 그래프 구성

```python
workflow = StateGraph(state_schema=State)

def call_model(state: State):
    prompt = prompt_template.invoke(state)      # language & messages 포함
    response = model.invoke(prompt)
    return {"messages": [response]}

workflow.add_edge(START, "model")
workflow.add_node("model", call_model)
app = workflow.compile(checkpointer=MemorySaver())
```

### 4-4. 호출 예시

```python
config = {"configurable": {"thread_id": "abc456"}}
msg = [HumanMessage(content="Hi! I'm Bob.")]
print(app.invoke({"messages": msg, "language": "Spanish"}, config)["messages"][-1].content)
```

* 이후 턴에는 `language`를 생략해도 저장된 상태를 재사용.

---

## 5. 메시지 트리밍(문맥 관리)

대화가 길어지면 LLM 컨텍스트 한계를 초과할 수 있습니다. `trim_messages` 헬퍼로 메시지 길이를 관리합니다.

```python
from langchain_core.messages import trim_messages

trimmer = trim_messages(
    max_tokens=65,
    strategy="last",         # 최근 메시지 우선 보존
    token_counter=model,
    include_system=True,
)
```

노드 내부에서 사용:

```python
trimmed = trimmer.invoke(state["messages"])
prompt = prompt_template.invoke({"messages": trimmed, "language": state["language"]})
```

---

## 6. 스트리밍 응답

```python
for chunk, metadata in app.stream(
    {"messages": [HumanMessage("Tell me a joke")], "language": "English"},
    config,
    stream_mode="messages",   # 토큰 단위 스트림
):
    if chunk.role == "ai":
        print(chunk.content, end="|")
```

스트리밍으로 UX 개선 가능.

---

## 7. 핵심 정리

| 단계 | 핵심 기술 | 코드 포인트 |
|------|-----------|-------------|
| 대화 기록 | `MessagesState` | `state_schema=MessagesState` |
| 다중 턴 메모리 | `MemorySaver` | `app = workflow.compile(checkpointer=memory)` |
| 커스텀 입력 | 커스텀 `State` | `language` 필드 추가 |
| 프롬프트 제어 | `ChatPromptTemplate` | system + `MessagesPlaceholder` |
| 컨텍스트 관리 | `trim_messages` | `trimmer.invoke(...)` |
| 스트리밍 | `app.stream(..., stream_mode="messages")` | 토큰 실시간 출력 |

이렇게 LangGraph를 사용하면 **상태 관리, 메모리, 프롬프트 구성** 등 챗봇 개발의 필수 요소를 간결하게 구현할 수 있습니다.
