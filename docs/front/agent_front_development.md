# LangGraph 에이전트 프론트엔드 개발 가이드

## 1. 개요

본 문서는 LangGraph를 백엔드로 사용하는 AI 에이전트의 프론트엔드를 개발할 때 주의해야 할 핵심 사항들을 정리합니다. LangGraph의 특성과 에이전트 워크플로우를 고려한 효과적인 UI/UX 설계 방법을 제시합니다.

## 2. LangGraph 에이전트 특성 이해

### 2.1. 에이전트 실행 플로우
```
사용자 입력 → 검증 → 검색어 생성 → 웹 검색 (병렬) → 반성/평가 → 추가 검색 (필요시) → 최종 답변
```

### 2.2. 핵심 특징
- **비동기 처리**: 웹 검색과 LLM 호출로 인한 긴 처리 시간 (5-30초)
- **중간 결과 스트리밍**: 각 노드 실행 과정을 실시간으로 확인 가능
- **동적 병렬 처리**: 여러 검색어를 동시에 실행
- **반복적 개선**: 검색 결과가 부족하면 추가 검색 수행
- **출처 추적**: 모든 답변에 웹 출처 정보 포함

## 3. 프론트엔드 아키텍처 선택

### 3.1. LangGraph SDK 사용 (권장)
```typescript
import { useStream } from "@langchain/langgraph-sdk/react";

const thread = useStream<StateType>({
  apiUrl: "http://localhost:8000",
  assistantId: "agent",
  messagesKey: "messages",
  onUpdateEvent: (event) => {
    // 중간 결과 처리
  },
  onError: (error) => {
    // 에러 처리
  }
});
```

**장점:**
- 실시간 스트리밍 지원
- 자동 상태 관리
- 타입 안전성
- LangGraph와의 완벽한 호환성

### 3.2. REST API 직접 사용
```typescript
const response = await fetch('/api/v1/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    message: userInput,
    thread_id: threadId
  })
});
```

**장점:**
- 단순한 구현
- 기존 API 패턴과 일치
- 최종 결과만 필요한 경우 적합

## 4. 핵심 UI/UX 고려사항

### 4.1. 로딩 상태 표시

#### 단계별 진행 표시
```typescript
interface ProcessedEvent {
  title: string;
  data: string;
  timestamp?: Date;
}

const ActivityTimeline = ({ events }: { events: ProcessedEvent[] }) => (
  <div className="activity-timeline">
    {events.map((event, index) => (
      <div key={index} className="timeline-item">
        <h4>{event.title}</h4>
        <p>{event.data}</p>
      </div>
    ))}
  </div>
);
```

#### 예시 단계들
- "사용자 요청 검증 중..."
- "검색어 생성 중... (3개 생성됨)"
- "웹 검색 진행 중... (병렬 처리)"
- "검색 결과 분석 중..."
- "추가 검색 필요성 판단 중..."
- "최종 답변 생성 중..."

### 4.2. 처리 시간 관리

```typescript
const [processingTime, setProcessingTime] = useState<number>(0);
const [estimatedTime, setEstimatedTime] = useState<string>("약 10-30초");

useEffect(() => {
  if (thread.isLoading) {
    const interval = setInterval(() => {
      setProcessingTime(prev => prev + 1);
    }, 1000);
    return () => clearInterval(interval);
  }
}, [thread.isLoading]);
```

### 4.3. 사용자 기대치 관리

#### 초기 안내 메시지
```typescript
const WelcomeMessage = () => (
  <div className="welcome-guide">
    <h3>AI 에이전트가 다음과 같이 도움을 드립니다:</h3>
    <ul>
      <li>🔍 여러 검색어로 웹에서 정보 수집</li>
      <li>🧠 수집된 정보를 분석하고 평가</li>
      <li>📊 부족한 정보가 있으면 추가 검색</li>
      <li>📝 종합적인 답변과 출처 제공</li>
    </ul>
    <p className="processing-note">
      ⏱️ 답변 생성에 보통 10-30초 정도 소요됩니다.
    </p>
  </div>
);
```

## 5. 실시간 이벤트 처리

### 5.1. 이벤트 타입 정의
```typescript
interface GraphEvent {
  generate_query?: {
    search_queries: string[];
  };
  web_search?: {
    search_query: string;
    sources_gathered: Source[];
  };
  reflection?: {
    is_sufficient: boolean;
    additional_queries?: string[];
  };
  answer_generation?: {
    final_answer: string;
  };
}
```

### 5.2. 이벤트 처리 로직
```typescript
const handleGraphEvent = (event: GraphEvent) => {
  if (event.generate_query) {
    setCurrentStep("검색어 생성 완료");
    setSearchQueries(event.generate_query.search_queries);
  }
  
  if (event.web_search) {
    setCurrentStep(`웹 검색: "${event.web_search.search_query}"`);
    addSources(event.web_search.sources_gathered);
  }
  
  if (event.reflection) {
    if (event.reflection.is_sufficient) {
      setCurrentStep("검색 완료 - 답변 생성 중");
    } else {
      setCurrentStep("추가 검색 필요 - 새로운 검색어 생성");
    }
  }
};
```

## 6. 에러 처리 및 복구

### 6.1. 일반적인 에러 시나리오
- API 키 오류
- 네트워크 타임아웃
- 검색 결과 부족
- LLM 응답 파싱 실패

### 6.2. 에러 처리 전략
```typescript
const ErrorBoundary = ({ error, onRetry, onCancel }) => (
  <div className="error-container">
    <h3>처리 중 오류가 발생했습니다</h3>
    <p>{error.message}</p>
    <div className="error-actions">
      <button onClick={onRetry}>다시 시도</button>
      <button onClick={onCancel}>취소</button>
    </div>
  </div>
);
```

### 6.3. 부분 결과 보존
```typescript
const [partialResults, setPartialResults] = useState({
  searchQueries: [],
  sources: [],
  partialAnswer: ""
});

// 에러 발생 시에도 수집된 정보 표시
const showPartialResults = () => (
  <div className="partial-results">
    <h4>수집된 정보:</h4>
    <p>검색어: {partialResults.searchQueries.join(", ")}</p>
    <p>출처: {partialResults.sources.length}개</p>
  </div>
);
```

## 7. 출처 및 Citation 표시

### 7.1. 출처 정보 구조
```typescript
interface Source {
  title: string;
  url: string;
  short_url?: string;
  snippet?: string;
}
```

### 7.2. Citation 표시 컴포넌트
```typescript
const CitationList = ({ sources }: { sources: Source[] }) => (
  <div className="citations">
    <h4>참고 자료:</h4>
    {sources.map((source, index) => (
      <div key={index} className="citation-item">
        <a href={source.url} target="_blank" rel="noopener noreferrer">
          [{index + 1}] {source.title}
        </a>
        {source.snippet && <p className="snippet">{source.snippet}</p>}
      </div>
    ))}
  </div>
);
```

## 8. 결론

LangGraph 에이전트 프론트엔드 개발의 핵심은 **에이전트의 비동기적이고 반복적인 처리 과정을 사용자에게 투명하게 보여주는 것**입니다. 

### 주요 성공 요소:
1. **실시간 진행 상황 표시** - 사용자가 기다리는 동안 무엇이 일어나고 있는지 명확히 전달
2. **적절한 기대치 설정** - 처리 시간과 과정에 대한 사전 안내
3. **에러 처리 및 복구** - 문제 발생 시 사용자가 적절히 대응할 수 있도록 지원
4. **출처 투명성** - AI가 어떤 정보를 바탕으로 답변했는지 명확히 제시

이러한 원칙을 따르면 사용자가 AI 에이전트의 작업 과정을 이해하고 신뢰할 수 있는 프론트엔드를 구축할 수 있습니다.
