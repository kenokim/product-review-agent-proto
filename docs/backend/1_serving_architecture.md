# LangGraph 서빙 아키텍처 (간소화 버전)

## 1. 개요

본 문서는 Python과 LangGraph를 사용하여 최소한의 구성으로 AI 에이전트를 서빙하는 간소화된 아키텍처를 제안합니다. 복잡성을 줄이고 단일 데이터베이스(PostgreSQL) 중심으로 구성하는 것을 목표로 합니다.

- 상태 유지(Stateful) 관리: 사용자의 대화 상태를 PostgreSQL에 저장하고 관리합니다.
- 벡터 검색: `pgvector` 확장을 사용하여 PostgreSQL 내에서 벡터 검색(RAG) 기능을 수행합니다.
- 단일 애플리케이션: 웹 서버와 그래프 실행 로직이 하나의 애플리케이션 내에서 동작합니다.

## 2. 핵심 기술 스택

- Web Framework: `FastAPI` (Uvicorn으로 실행)
- Graph Orchestration: `LangGraph`
- Database & Vector Store: `PostgreSQL` (with `pgvector` extension)
- Containerization: `Docker`, `Docker Compose`
- LLM: OpenAI, Anthropic 등 외부 API 또는 자체 호스팅 모델

## 2.5. 패키지 구조 (예시)

```
/app
├── api/                  # API 엔드포인트 (라우터)
│   └── v1/
│       └── chat_router.py
├── core/                 # FastAPI 설정, DB 연결 등
│   └── config.py
├── graphs/               # LangGraph 정의 패키지
│   ├── __init__.py
│   └── product_recommender/
│       ├── __init__.py
│       ├── graph.py        # 그래프 구성
│       ├── state.py        # 그래프 상태 정의
│       └── tools.py        # 그래프에서 사용할 도구들
├── schemas/              # Pydantic 스키마 (요청/응답 모델)
│   └── chat_schema.py
├── services/             # 비즈니스 로직 (API와 그래프를 연결)
│   └── chat_service.py
└── main.py               # FastAPI 애플리케이션 초기화
```

## 3. 아키텍처 다이어그램

```mermaid
graph TD
    subgraph "클라이언트"
        A[User Application]
    end

    subgraph "서빙 애플리케이션 (Docker)"
        B["API 서버 (FastAPI)<br/>+<br/>LangGraph 실행 로직"]
    end

    subgraph "데이터베이스 (Docker)"
        C["PostgreSQL<br/>- 대화 상태 (Checkpointer)<br/>- 벡터 데이터 (pgvector)"]
    end

    subgraph "외부 서비스"
        D[LLM APIs<br/>(OpenAI, Anthropic...)]
    end

    A -- HTTP 요청 --> B
    B -- 상태 저장/조회<br/>(Checkpointer) --> C
    B -- 벡터 검색<br/>(RAG) --> C
    B -- LLM 호출 --> D
    B -- HTTP 응답 --> A
```

## 4. 컴포넌트별 상세 설명

### 4.1. 서빙 애플리케이션 (FastAPI + LangGraph)

- 역할: 클라이언트의 요청을 받아 LangGraph 로직을 동기적으로 실행하고 응답하는 단일 서비스입니다.
- 주요 기능:
    - API 엔드포인트: 클라이언트가 그래프를 실행하기 위한 HTTP 인터페이스를 제공합니다.
    - LangGraph 실행: 요청을 받으면 즉시 해당 스레드의 그래프를 인스턴스화하고 실행합니다. 모든 처리는 API 요청-응답 사이클 내에서 완료됩니다.
    - 상태 관리 연동: LangGraph의 `Checkpointer`가 PostgreSQL 데이터베이스에 대화 상태를 저장하고 불러오도록 설정합니다. `langgraph-postgres` 라이브러리를 사용할 수 있습니다.
    - RAG 연동: 필요시 `pgvector`를 사용하는 벡터 저장소(Vector Store)와 연동하여 관련 문서를 검색하고, 이를 프롬프트에 포함하여 LLM에 전달합니다.

- 주요 엔드포인트 예시:
    - `POST /graph/invoke`: 새로운 그래프 실행을 시작하거나 기존 대화를 이어가고, 처리 완료 후 최종 결과를 반환합니다.

### 4.2. 데이터베이스 (PostgreSQL with pgvector)

- 역할: 애플리케이션의 모든 데이터를 저장하는 중앙 저장소입니다.
- 주요 기능:
    1.  대화 상태 저장 (Checkpointer Backend): LangGraph의 `Checkpointer`를 위한 백엔드 역할을 합니다. 각 대화 스레드(`thread_id`)의 상태(메시지, 중간 결과 등)를 테이블에 저장하여 대화의 연속성을 보장합니다.
    2.  벡터 데이터 저장 (Vector Store): `pgvector` 확장을 활성화하여 텍스트 임베딩 벡터를 저장하고, 코사인 유사도와 같은 벡터 검색 쿼리를 효율적으로 처리합니다. RAG(Retrieval-Augmented Generation) 파이프라인의 핵심 요소입니다.

## 5. 데이터 흐름

1.  요청: 클라이언트가 특정 `thread_id`와 사용자 입력을 담아 FastAPI 서버의 엔드포인트를 호출합니다.
2.  상태 로드: FastAPI는 `thread_id`를 사용하여 PostgreSQL에서 해당 대화의 마지막 상태를 `Checkpointer`를 통해 로드합니다.
3.  그래프 실행: 로드된 상태와 사용자 입력을 바탕으로 LangGraph가 실행됩니다.
4.  RAG (필요시): 그래프 내 노드가 RAG를 수행해야 할 경우, PostgreSQL(`pgvector`)에 벡터 검색 쿼리를 실행하여 관련 문서를 가져옵니다.
5.  LLM 호출: 검색된 문서와 대화 기록을 바탕으로 프롬프트를 구성하여 외부 LLM API를 호출합니다.
6.  상태 저장: LLM 응답을 포함한 그래프의 최종 상태를 다시 `Checkpointer`를 통해 PostgreSQL에 저장합니다.
7.  응답: 최종 결과를 클라이언트에게 HTTP 응답으로 반환합니다.

## 6. 배포

- 컨테이너화: `FastAPI 애플리케이션`과 `PostgreSQL`을 각각 Docker 컨테이너로 구성합니다.
- 실행: `docker-compose.yml`을 사용하여 두 컨테이너를 한번에 실행합니다. 이 방식은 로컬 개발 및 소규모 프로덕션 환경에 적합합니다.

## 7. 장단점

### 장점
- 단순성: 아키텍처가 매우 단순하여 이해하고 관리하기 쉽습니다.
- 최소 구성 요소: Redis, Celery 등 추가적인 미들웨어가 필요 없어 운영 부담이 적습니다.
- 통합된 데이터 관리: 대화 상태와 벡터 데이터를 하나의 PostgreSQL 데이터베이스에서 관리할 수 있습니다.

### 단점
- 동기식 처리: LLM 호출과 같이 오래 걸리는 작업이 완료될 때까지 API 응답이 지연됩니다. (타임아웃 발생 가능)
- 확장성 한계: 트래픽이 증가할 경우, 데이터베이스가 병목 지점이 되거나 애플리케이션 서버를 확장하는 데 한계가 있습니다.
- 실시간 응답 불가: 중간 결과를 스트리밍하기 어렵고, 모든 처리가 끝난 후에만 최종 결과를 받을 수 있습니다.

## 8. 아키텍처 확장: Redis와 Celery 도입의 장점

현재의 간소화된 아키텍처는 초기 개발 및 소규모 트래픽에 적합하지만, 서비스가 성장함에 따라 Redis와 Celery를 추가하여 다음과 같은 장점을 얻을 수 있습니다.

- 응답 시간 단축: LLM 호출과 같은 오래 걸리는 작업을 Celery 워커에 위임(비동기 처리)함으로써, API 서버는 즉시 사용자에게 응답을 반환할 수 있습니다. 사용자는 더 이상 작업이 끝날 때까지 기다릴 필요가 없습니다.
- 안정성 및 신뢰성 향상: 만약 작업 처리 중 서버에 문제가 발생해도, 작업은 Celery 큐에 안전하게 남아있어 서버가 복구된 후 재처리할 수 있습니다.
- 실시간 스트리밍 지원: Redis Pub/Sub과 WebSocket을 연동하여, LLM이 생성하는 토큰이나 중간 처리 결과를 클라이언트에 실시간으로 전송할 수 있어 사용자 경험(UX)이 크게 향상됩니다.
- 유연한 확장성: API 서버와 워커를 독립적으로 확장할 수 있습니다. 예를 들어, AI 모델 처리량이 많아지면 워커 수만 늘리고, API 요청이 많아지면 API 서버 수만 늘리는 등 유연한 대응이 가능합니다.
