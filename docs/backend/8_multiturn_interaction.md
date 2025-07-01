# LangGraph 대화 관리 메커니즘: Persistence

LangGraph는 **Persistence(영속성)** 레이어를 통해 여러 턴에 걸친 대화의 맥락을 유지하고 관리합니다. 이 메커니즘 덕분에 개발자는 복잡한 상태 관리 로직을 직접 구현할 필요 없이, 대화형 챗봇이나 에이전트를 손쉽게 구축할 수 있습니다.

> **주요 출처:**
> - **[LangGraph Docs: Persistence](https://langchain-ai.github.io/langgraph/concepts/persistence/)**
> - **[LangGraph How-To: Manage Conversation History](https://langchain-ai.github.io/langgraph/how-tos/memory/manage-conversation-history/)**

---

## 1. 핵심 구성 요소

LangGraph의 대화 관리 메커니즘은 다음 세 가지 핵심 요소로 이루어집니다.

### 1.1. Checkpointer (체크포인터)

- **역할**: 그래프의 **상태(State)** 를 물리적인 저장소(DB, 파일 등)에 저장하고 불러오는 **엔진**입니다.
- **설명**: `graph.compile()` 시점에 `checkpointer` 객체를 넘겨주면, LangGraph가 모든 상태 관리를 이 체크포인터에 위임합니다. 어떤 저장소를 쓸지에 따라 다양한 구현체를 선택할 수 있습니다.
- **종류**:
    - `MemorySaver`: 인메모리에 상태를 저장 (테스트 및 개발용)
    - `SqliteSaver`: SQLite DB에 상태를 저장 (간단한 로컬 환경용)
    - `PostgresSaver`: PostgreSQL DB에 상태를 저장 (프로덕션 환경용)

### 1.2. Thread (스레드)

- **역할**: 개별 **대화 세션(Conversation Session)** 을 의미합니다.
- **설명**: 각 대화는 고유한 `thread_id` (문자열)를 가집니다. 사용자와 챗봇이 주고받는 모든 메시지와 그로 인해 변경되는 중간 상태값들은 모두 이 `thread_id`에 연결되어 저장됩니다. 즉, `thread_id`는 특정 대화의 전체 기록을 식별하는 고유한 키입니다.

### 1.3. Checkpoint (체크포인트)

- **역할**: 특정 시점의 **그래프 상태 스냅샷(State Snapshot)** 입니다.
- **설명**: 그래프가 한 단계(노드) 실행될 때마다, 그 직후의 상태가 하나의 `Checkpoint`로 생성되어 저장소에 기록됩니다. 각 체크포인트는 `thread_id`에 속하며, 시간 순서대로 쌓입니다. 따라서 하나의 `Thread`는 여러 개의 `Checkpoint`로 구성된 시퀀스라고 볼 수 있습니다.

---

## 2. 대화 관리 동작 흐름

`Checkpointer`가 연결된 그래프를 `invoke` 또는 `stream`으로 호출할 때, 내부적으로 다음과 같은 과정이 자동으로 처리됩니다.

1.  **`thread_id` 식별**: 클라이언트는 API를 호출할 때 `configurable` 딕셔너리에 `{"thread_id": "some-unique-id"}`를 포함하여 요청합니다.

2.  **상태 불러오기 (Load)**: LangGraph는 `thread_id`를 이용해 **Checkpointer**에게 해당 대화의 **가장 마지막 Checkpoint**를 요청합니다.

3.  **상태 복원**: Checkpointer는 저장소에서 마지막 체크포인트 데이터를 찾아 그래프의 현재 상태를 복원합니다. 만약 해당 `thread_id`로 저장된 기록이 없다면, 초기 상태에서 시작합니다.

4.  **그래프 실행**: 복원된 상태에서부터 입력받은 메시지를 처리하며 그래프의 노드들을 실행합니다.

5.  **상태 저장 (Save)**: 그래프의 각 노드 실행이 끝날 때마다, **Checkpointer**는 변경된 최신 상태를 새로운 **Checkpoint**로 만들어 저장소에 기록합니다. 이 새 체크포인트는 같은 `thread_id`에 연결됩니다.

6.  **결과 반환**: 그래프 실행이 모두 끝나면 최종 결과를 클라이언트에게 반환합니다.

---

## 3. 요약

LangGraph의 **Persistence** 메커니즘은 `Checkpointer`를 통해 `thread_id`로 식별되는 대화의 상태(`Checkpoint`의 연속)를 자동으로 저장하고 불러옵니다. 이 덕분에 개발자는 세션 관리나 대화 기록 저장 로직을 직접 코딩할 필요 없이, 오직 그래프의 비즈니스 로직에만 집중하여 강력하고 상태 저장(stateful)이 가능한 애플리케이션을 만들 수 있습니다. 

---

## 4. 실전 예제: MessagesState + MemorySaver로 멀티턴 챗봇 구현

아래 코드는 `docs/backend/chatbot.md` 튜토리얼에서 발췌한 **가장 단순한 멀티턴 챗봇** 예제입니다. 핵심은 두 가지입니다.

1. `MessagesState`를 사용하여 대화 기록을 누적한다.
2. `MemorySaver`(인메모리 Checkpointer)를 붙여서 `thread_id` 별 상태를 자동 저장·복원한다.

```python
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langgraph.graph import START, MessagesState, StateGraph
from langgraph.checkpoint.memory import MemorySaver

# 1) LLM 준비
model = ChatOpenAI(model="gpt-4o-mini")

# 2) 그래프 정의
workflow = StateGraph(state_schema=MessagesState)

def call_model(state: MessagesState):
    """마지막 사용자 메시지를 포함한 전체 대화 기록을 모델에 전달"""
    response = model.invoke(state["messages"])
    return {"messages": [response]}

workflow.add_node("model", call_model)
workflow.add_edge(START, "model")

# 3) 멀티턴 메모리 활성화
memory = MemorySaver()                # 인메모리 Checkpointer
bot = workflow.compile(checkpointer=memory)

# 4) 대화 실행 예시
config = {"configurable": {"thread_id": "chat-123"}}  # 고유 대화 ID

# 첫 번째 턴
msg1 = [HumanMessage(content="Hi! I'm Bob")]
print(bot.invoke({"messages": msg1}, config)["messages"][-1].content)

# 두 번째 턴 (같은 thread_id 사용: 이전 대화 자동 로드)
msg2 = [HumanMessage(content="What did I just tell you?")]
print(bot.invoke({"messages": msg2}, config)["messages"][-1].content)
```

### 동작 요약

- **`MessagesState`**: `{"messages": [...]} ` 형태의 단일 채널 상태로, 각 노드가 반환한 메시지가 자동 누적됩니다.
- **`MemorySaver`**: `thread_id` 별로 체크포인트를 인메모리에 저장하므로, 같은 `thread_id`로 호출하면 이전 대화가 이어집니다.
- **확장성**: 프로덕션 환경에서는 `SqliteSaver`나 `PostgresSaver`로 교체해도 코드 변경은 `checkpointer` 부분뿐입니다.

이 예제는 가장 기본적인 형태이므로, **커스텀 State**(추가 파라미터), **프롬프트 템플릿**, **메시지 트리밍** 등 고급 기능은 `docs/backend/chatbot.md`를 참고하세요. 

---

## 5. 다중 턴 대화를 가능하게 하는 두 축: **State + Checkpointer**

멀티턴 기능이 동작하려면 **두 가지**가 모두 갖춰져야 합니다.

| 구성 요소 | 무엇을 담당하나? | 핵심 포인트 |
|-----------|-----------------|-------------|
| **State 스키마**<br/>(예: `messages: Annotated[list, add_messages]`) | • **누적 방식** 정의<br/>• 그래프 한 번 실행(1 러닝 사이클) 안에서<br/>메시지가 계속 **append** 되도록 함 | `add_messages` 리듀서가 새 메시지를 리스트에 붙입니다. 만약 `messages` 채널이 없거나 리듀서가 없는 단순 타입이면, 이전 메시지가 덮어써져 버려 멀티턴이 불가능합니다. |
| **Checkpointer**<br/>(예: `MemorySaver`, `SqliteSaver`, `PostgresSaver`) | • **영속성** 담당<br/>• `thread_id` 별로 Checkpoint를 저장/로드 | 요청이 새로 올 때마다 `thread_id`에 대응하는 **마지막 Checkpoint**를 불러오고, 실행 후 새 상태를 저장합니다. Checkpointer가 없으면 매 호출이 "새 그래프"로 시작하여 기록이 이어지지 않습니다. |

### 작동 순서 요약

1. 클라이언트가 `thread_id`를 지정해 `graph.invoke()` 호출
2. Checkpointer가 해당 `thread_id`의 마지막 상태를 **로드**
3. 노드 실행 중 `messages` 채널이 `add_messages`로 **누적**
4. 실행 종료 시 Checkpointer가 새로운 Checkpoint를 **저장**
5. 같은 `thread_id`로 다음 호출 시 ② 단계부터 반복 ⇒ 대화 맥락 유지

따라서 "**State + Checkpointer**"가 모두 있어야 진정한 멀티턴 대화가 구현됩니다. 한쪽이라도 빠지면 대화 기록이 이어지지 않으니 구현 시 두 부분을 모두 확인하세요. 