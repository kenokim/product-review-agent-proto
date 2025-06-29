# Server `app` 코드 리뷰 및 LangGraph 활용 개선 설계

> **리뷰 대상 경로:** `server/app/*`
>
> **주요 기능:** FastAPI 백엔드 + LangGraph 기반 제품 추천 에이전트

---

## 1. 아키텍처 요약

| 계층 | 주요 모듈 | 역할 |
|------|-----------|------|
| **API** | `api/v1/chat_router.py` | HTTP 요청 수신, 서비스 레이어 호출 |
| **Service** | `services/chat_service.py` | 그래프 실행, 응답 가공, 로깅 |
| **Domain / Graph** | `graph/*.py` | LangGraph 노드·프롬프트·상태 정의 |
| **Infra** | `core/config.py`, `graph/utils.py` | 설정, 공통 유틸 |

현재 구조는 **클린 아키텍처** 패턴(Controller–Service–Domain)과 유사하여 가독성이 좋습니다. 다만 LangGraph 고급 기능(메모리, Checkpointer, Store, Streaming 등)을 적극 활용하면 다음과 같은 개선 여지가 있습니다.

---

## 2. 전반적인 강점

1. **계층 분리**: API ↔︎ Service ↔︎ Graph 로 명확히 분리해 유지보수 용이.
2. **Pydantic 스키마 활용**: `schemas/chat_schema.py`를 통해 데이터 모델이 명확.
3. **세분화된 로깅**: 각 노드 단위 로그로 디버깅 편의성 확보.

---

## 3. 개선 제안 (LangGraph 사용성 중심)

| # | 개선 항목 | 제안 내용 | 기대 효과 |
|---|-----------|-----------|-----------|
| 1 | **Checkpointer 다양화** | 현재 인메모리 기반 → `SqliteSaver`(로컬) or `PostgresSaver`(프로덕션) 선택 가능하도록 DI 패턴 적용.<br/> `graph.create_product_recommendation_graph(checkpointer=...)` 형태로 의존성 주입 지원 | 재시작·복구·Time-Travel 기능 강화, 다중 인스턴스 확장성 확보 ([공식문서](https://langchain-ai.github.io/langgraph/concepts/persistence/#checkpointer-libraries)) |
| 2 | **Store(메모리) 도입** | 사용자별 장기 기억을 위해 `InMemoryStore`→향후 `RedisStore` 도입.<br/> 예) `namespace=(user_id,"memories")` 패턴 ([예시](https://langchain-ai.github.io/langgraph/concepts/persistence/#memory-store)) | 개인화 추천 정확도 향상, 세션 간 컨텍스트 유지 |
| 3 | **Streaming API** | 그래프 `stream()` 사용 및 FastAPI의 `StreamingResponse`로 토큰 스트리밍 지원.<br/> Service 레이어에서 `graph.stream(..., stream_mode="updates")` 사용 | UX 개선(대기시간 체감), 장시간 작업도 실시간 피드백 ([Streaming 가이드](https://langchain-ai.github.io/langgraph/how-tos/streaming_responses/)) |
| 4 | **LangSmith 통합** | `LANGCHAIN_TRACING_V2=true` + `LANGCHAIN_API_KEY` 설정 후 `graph.compile(tracer=...)` | 실행 경로 시각화·오류 분석·성능 모니터링 강화 |
| 5 | **프롬프트/노드 모듈화** | `prompts.py`가 커짐 → 노드별 프롬프트 클래스로 분리 (`prompt/validation.py` 등) | 변경 영향 범위 축소, 테스트 용이 |
| 6 | **에러 복구 전략** | 노드 실패 시 `graph.resume()` 활용 및 Pending Writes 저장 → 자동 재시도 or 사용자 개입 | 안정성 향상, 중단 시점부터 재실행 ([Fault-tolerance](https://langchain-ai.github.io/langgraph/concepts/persistence/#fault-tolerance)) |
| 7 | **ConfigurableBuilder 패턴** | 사용자 요구(모델, 검색어 수 등)를 `ProductRecommendationConfig`에 추가하고 FastAPI 쿼리로 노출 | A/B 테스트, 하이퍼파라미터 튜닝 용이 |
| 8 | **테스트 커버리지 확대** | `pytest`로 노드 단위·그래프 단위·API 단위 테스트 추가.<br/> 특히 `graph.test_graph.py` 샘플처럼 `StateGraph.testing()` 사용 | 회귀 방지, 리팩터링 안전성 확보 |
| 9 | **CI/CD 파이프라인** | GitHub Actions: 테스트→Docker 빌드→배포 자동화 | 빠른 피드백, 배포 일관성 |

---

## 4. 샘플 구현 스케치

```python
# graph/__init__.py
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.checkpoint.postgres import PostgresSaver

def get_checkpointer(env: str = "local"):
    if env == "local":
        return SqliteSaver.from_conn_string("checkpoint.db")
    if env == "prod":
        return PostgresSaver.from_conn_string(os.getenv("POSTGRES_URL"))
    return InMemorySaver()
```

```python
# services/chat_service.py (발췌)
checkpointer = get_checkpointer(os.getenv("ENV", "local"))
app_graph = create_product_recommendation_graph(checkpointer=checkpointer)
```

FastAPI 스트리밍 예시:
```python
from fastapi.responses import StreamingResponse

async def chat_endpoint(request: ChatRequest):
    config = {"configurable": {"thread_id": request.thread_id}}
    event_stream = app_graph.stream({"messages": request.to_messages()}, config, stream_mode="updates")
    return StreamingResponse((json.dumps(evt) for evt in event_stream), media_type="text/event-stream")
```

---

## 5. 결론

현재 코드베이스는 기본적인 계층화와 LangGraph 통합이 잘 이루어져 있습니다. 위 개선안을 도입하면

* **지속성**과 **확장성** 확보 (Checkpointer/Store)
* **사용자 경험** 개선 (Streaming, Memory)
* **운영/품질** 강화 (LangSmith, 테스트, CI/CD)

을 단기간에 달성할 수 있습니다. 앞으로의 스케일업을 고려해 설계 유연성을 높이는 것을 권장드립니다.

---

## 6. 개인화(단일 사용자) 및 리포트 게시판 설계

> **전제:** 로그인 X, `user_id="default_user"` 고정. 에이전트가 생성한 *리포트(제품 추천 결과)*를 저장·조회할 수 있는 게시판이 필요.

### 6.1 저장 전략

| 항목 | 설계 | 비고 |
|------|------|------|
| 저장소 | **LangGraph Store** (`InMemoryStore` → `RedisStore` 전환 가능) | Vector 검색 대비 `dims` 설정 가능 |
| 네임스페이스 | `(user_id, "reports")` | 단일 사용자이므로 `user_id="default_user"` 고정 |
| key | `uuid4()` | 각 리포트의 고유 ID |
| value(예시) | `{ "title": "3만원대 가성비 이어폰", "content": "...", "created_at": "2025-06-26" }` | 추가 메타데이터(태그 등) 확장 가능 |

### 6.2 노드 통합

1. **answer_generation** 노드 종료 시:
   ```python
   store.put(("default_user", "reports"), str(uuid.uuid4()), {
       "title": extract_title(final_content),
       "content": final_content,
       "created_at": datetime.utcnow().isoformat()
   })
   ```
2. 필요 시 리포트 요약본(title)만 별도 채널에 저장해 빠른 목록 조회 지원.

### 6.3 API 설계

| Method | Path | 설명 |
|--------|------|------|
| `GET` | `/api/v1/reports` | 모든 리포트 목록(title, id, created_at) 반환 |
| `GET` | `/api/v1/reports/{report_id}` | 특정 리포트 상세 조회 |
| `DELETE` | `/api/v1/reports/{report_id}` | 리포트 삭제(옵션) |

**FastAPI 예시**
```python
@router.get("/reports")
async def list_reports():
    ns = ("default_user", "reports")
    items = store.search(ns, limit=100)  # 최신순
    return [{"id": i.key, **i.value} for i in items]

@router.get("/reports/{report_id}")
async def get_report(report_id: str):
    ns = ("default_user", "reports")
    item = store.get(ns, report_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Not found")
    return item.value
```

### 6.4 프론트엔드(게시판 뷰)

* `ReportsList` 컴포넌트: `/api/v1/reports` 호출 → 리스트 렌더링
* `ReportDetail` 페이지: `/api/v1/reports/{id}` 호출 → 마크다운 렌더링
* Shadcn/ui `Card`, `Table` 사용으로 간단 구현

### 6.5 기대 효과

* **개인화 히스토리**: 한 사용자가 과거 생성한 리포트를 쉽게 다시 확인·공유 가능.
* **재활용**: 오래된 리포트 기반 추가 질문 시, 기존 리포트 내용을 `messages`에 삽입해 컨텍스트 강화.
* **확장성**: 추후 다중 사용자 요구 시 `user_id`를 쿼리 파라미터/헤더로 받아 네임스페이스만 확장하면 됨.

> **참고 문서**
> * LangGraph Memory Store 예시: <https://langchain-ai.github.io/langgraph/concepts/persistence/#memory-store>
