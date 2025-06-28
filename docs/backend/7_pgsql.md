# LangGraph × PostgreSQL 완전 가이드

> **참조:**  
> • LangGraph Persistence Docs – Checkpointer Libraries: <https://langchain-ai.github.io/langgraph/concepts/persistence/#checkpointer-libraries>  
> • `langgraph-checkpoint-postgres` PyPI: <https://pypi.org/project/langgraph-checkpoint-postgres/>  
> • pgvector 공식 문서: <https://github.com/pgvector/pgvector>

LangGraph는 Checkpointer·Store·Streaming 같은 핵심 기능을 **DB-독립적 인터페이스**로 추상화합니다. 이 문서에서는 **PostgreSQL**을 활용하여

1. **Checkpoint**(그래프 상태) 영구 저장  
2. **스트리밍** 응답 제공  
3. **Vector DB** + 시멘틱 검색

을 구현하는 방법을 정리합니다.

---

## 1. 왜 PostgreSQL인가?

| 항목 | 장점 | 비고 |
|------|------|------|
| 신뢰성 | ACID 트랜잭션, WAL 복구 | 운영 경험 풍부 |
| 확장성 | 파티셔닝·리플리카·클러스터링 | 다중 인스턴스 RDS, CloudSQL 등 |
| JSON 지원 | `JSONB` 컬럼으로 체크포인트 구조 저장 | 🚀 |
| 벡터 검색 | `pgvector` 확장으로 내장 벡터 인덱싱 | Top-K Cosine/L2/Inner |

---

## 2. 패키지 설치

```bash
pip install langgraph-checkpoint-postgres psycopg2-binary pgvector
```

> `pgvector` 파이썬 패키지는 선택적이지만, 예제에서 편의상 사용합니다.

---

## 3. Checkpoint를 PostgreSQL에 저장하기

### 3-1. 데이터베이스 준비

```sql
-- DB 접속 후 단 한번 실행
CREATE EXTENSION IF NOT EXISTS pgcrypto; -- UUID 생성용 (선택)
```

LangGraph는 자체적으로 테이블/인덱스를 생성하므로 별도 스키마 준비가 없습니다.

### 3-2. 코드 예시

```python
from langgraph.graph import StateGraph
from langgraph.checkpoint.postgres import PostgresSaver
import os

PG_URL = os.getenv("POSTGRES_URL", "postgresql://user:pass@localhost:5432/db")

checkpointer = PostgresSaver.from_conn_string(PG_URL)
checkpointer.setup()  # ⚠️ 최초 1회 인덱스 생성

builder = StateGraph(int)
builder.add_node("add_one", lambda x: x + 1)
builder.set_entry_point("add_one")

graph = builder.compile(checkpointer=checkpointer)

config = {"configurable": {"thread_id": "thread-1"}}
print(graph.invoke(1, config))  # 2
```

### 3-3. TTL·암호화·비동기

| 기능 | 방법 |
|------|------|
| **TTL** | `PostgresSaver(ttl={"default_ttl": 1440})` (분 단위) |
| **AES 암호화** | `serde=EncryptedSerializer.from_pycryptodome_aes()` 전달 |
| **Async** | `AsyncPostgresSaver` 사용 + `await graph.ainvoke()` |

---

## 4. FastAPI 스트리밍과 PostgreSQL

PostgreSQL은 **스트리밍 로직과 완전히 분리**됩니다. LLM 토큰이 생성되는 즉시 FastAPI `StreamingResponse`로 클라이언트에 전달되고, 체크포인터는 슈퍼스텝 종료 후 한번만 DB에 기록합니다.

```python
from fastapi.responses import StreamingResponse

@router.post("/chat/stream")
async def chat_stream(req: ChatRequest):
    cfg = {"configurable": {"thread_id": req.thread_id}}
    gen = graph.stream({"messages": req.to_messages()}, cfg, stream_mode="updates")
    return StreamingResponse((json.dumps(e) for e in gen), media_type="text/event-stream")
```

> 실시간 UX가 중요한 경우 PostgreSQL → 애플리케이션 → 클라이언트 사이의 버퍼를 최소화하도록 `psycopg2` `autocommit` 또는 커넥션 풀(eg. `asyncpg`) 튜닝을 권장합니다.

---

## 5. PostgreSQL을 Vector DB로 활용 (pgvector)

### 5-1. 확장 활성화

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

### 5-2. 테이블 스키마 예시

```sql
CREATE TABLE semantic_docs (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  content text,
  embedding vector(768)  -- OpenAI Ada: 1536, MiniLM: 384 등
);

-- HNSW 인덱스 (Cosine)
CREATE INDEX ON semantic_docs USING hnsw (embedding vector_cosine_ops);
```

### 5-3. 파이썬 삽입/검색

```python
import openai, psycopg2, numpy as np

def embed(text: str) -> list[float]:
    return openai.Embedding.create(model="text-embedding-3-small", input=text)["data"][0]["embedding"]

with psycopg2.connect(PG_URL) as conn, conn.cursor() as cur:
    # 삽입
    cur.execute("INSERT INTO semantic_docs (content, embedding) VALUES (%s, %s)",
                ("휴대용 블루투스 스피커", np.array(embed("휴대용 블루투스 스피커"))))
    # 검색 (Top-K)
    cur.execute("SELECT content FROM semantic_docs ORDER BY embedding <=> %s LIMIT 5", (np.array(embed("가성비 스피커")),))
    print(cur.fetchall())
```

### 5-4. LangGraph Store로 래핑하기

아직 공식 PostgresStore 구현은 없지만, `BaseStore` 프로토콜을 구현해 `search/put/get` 메서드에서 위 SQL을 호출하면 LangGraph 노드에서 동일한 API로 사용 가능합니다.

```python
from langgraph.store.base import BaseStore, Item
from uuid import uuid4

class PgVectorStore(BaseStore):
    def __init__(self, conn_str: str):
        self.conn_str = conn_str

    def put(self, namespace: tuple[str, ...], key: str, value: dict, **kwargs):
        # namespace → 테이블 or 추가 컬럼 활용
        ...

    def search(self, namespace, query: str, limit: int = 5):
        ...  # pgvector <=> 연산자 사용
```

---

## 6. 운영 팁

1. **커넥션 풀** – `asyncpg.pool` 또는 SQLAlchemy `AsyncSession`으로  DB 연결 수 제한.  
2. **마이그레이션** – `alembic`으로 Checkpointer 테이블 외 사용자 테이블(리포트, 벡터) 스키마 관리.  
3. **모니터링** – `pg_stat_activity`, `auto_explain` 로 장기 실행 쿼리 추적.  
4. **백업** – WAL-G, pg_dump, 관리형 RDS snapshot 활용.

---

## 7. 요약

| 기능 | PostgreSQL 적용 방법 | 비고 |
|------|--------------------|------|
| **Checkpoint** | `PostgresSaver` / `AsyncPostgresSaver` | JSONB + 인덱스 자동 생성 |
| **Streaming** | FastAPI `StreamingResponse` & `graph.stream()` | DB와 독립적, 실시간 토큰 전송 |
| **Semantic Search** | `pgvector` 확장 + HNSW 인덱스 | Store 래퍼 구현 가능 |

PostgreSQL 하나로 **영속성·검색·확장성**을 모두 충족시킬 수 있으므로, 별도 Redis 없이도 서비스 운영이 가능합니다.
