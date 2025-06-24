# 프론트엔드 프로젝트 분석 (React + TypeScript)

## 🏗️ 프로젝트 개요

### 기본 정보
- **프로젝트명**: AI 제품 추천 플랫폼
- **기술 스택**: React 18 + TypeScript + Vite
- **UI 프레임워크**: shadcn/ui + Tailwind CSS
- **상태 관리**: React Query (TanStack Query)
- **라우팅**: React Router DOM

### 주요 기능
- 🤖 AI 기반 제품 추천 채팅
- 🔍 실시간 웹 검색 결과 표시
- 📚 출처 정보 및 링크 제공
- 💬 실시간 채팅 인터페이스
- 📱 반응형 디자인

## 📁 프로젝트 구조

```
front/
├── src/
│   ├── components/          # React 컴포넌트
│   │   ├── ui/             # shadcn/ui 컴포넌트 라이브러리
│   │   ├── ChatInterface.tsx    # 메인 채팅 인터페이스
│   │   ├── ChatMessage.tsx      # 개별 메시지 컴포넌트
│   │   ├── SourcesList.tsx      # 출처 정보 표시
│   │   ├── ChatHeader.tsx       # 채팅 헤더
│   │   └── RelatedProducts.tsx  # 관련 제품 추천
│   ├── lib/                # 유틸리티 및 서비스
│   │   ├── api.ts          # API 호출 서비스
│   │   └── utils.ts        # 공통 유틸리티
│   ├── pages/              # 페이지 컴포넌트
│   │   ├── Index.tsx       # 메인 페이지
│   │   └── NotFound.tsx    # 404 페이지
│   ├── hooks/              # 커스텀 React 훅
│   │   ├── use-mobile.tsx  # 모바일 감지
│   │   └── use-toast.ts    # 토스트 알림
│   ├── App.tsx             # 루트 앱 컴포넌트
│   ├── main.tsx            # 앱 엔트리 포인트
│   └── index.css           # 전역 스타일
├── public/                 # 정적 파일
├── package.json            # 의존성 관리
├── vite.config.ts          # Vite 설정
├── tailwind.config.ts      # Tailwind CSS 설정
├── tsconfig.json           # TypeScript 설정
└── README.md               # 프로젝트 문서
```

## 🧩 주요 컴포넌트 분석

### 1. **App.tsx** - 루트 컴포넌트
```typescript
- QueryClient 설정 (React Query)
- Router 설정 (React Router)
- 전역 UI 프로바이더 (Tooltip, Toast)
- 라우팅 구조: "/" (Index), "*" (NotFound)
```

### 2. **pages/Index.tsx** - 메인 페이지
```typescript
구조:
- 상단 헤더 (제목, 설명)
- 탭 메뉴 (AI 제품 추천, 카테고리)
- 메인 컨텐츠 영역
  - ChatInterface (채팅 인터페이스)
  - RelatedProducts (사이드바)

특징:
- Tabs 컴포넌트로 섹션 구분
- 반응형 레이아웃 (lg:block으로 사이드바 제어)
- 고정 높이 설정 (calc(100vh-180px))
```

### 3. **ChatInterface.tsx** - 핵심 채팅 컴포넌트
```typescript
주요 기능:
- 실제 API 호출 (ChatAPI.sendMessage)
- 실시간 메시지 교환
- 로딩 상태 관리
- 에러 처리 및 재시도
- 자동 스크롤
- 타임스탬프 표시

상태 관리:
- messages: 채팅 메시지 배열
- inputValue: 입력창 텍스트
- isLoading: 로딩 상태
- error: 에러 상태
- hasInteracted: 사용자 상호작용 여부

핵심 로직:
- handleSendMessage(): API 호출 및 응답 처리
- formatTimestamp(): 시간 포맷팅
- handleRetry(): 에러 시 재시도
```

### 4. **ChatMessage.tsx** - 메시지 표시 컴포넌트
```typescript
기능:
- 사용자/봇 메시지 구분 렌더링
- 아바타 표시 (User/Bot 아이콘)
- 출처 정보 표시 (SourcesList 컴포넌트)
- 반응형 메시지 버블

특징:
- isBot에 따른 스타일 분기
- 최대 너비 제한 (max-w-2xl)
- 출처는 봇 메시지에만 표시
```

### 5. **SourcesList.tsx** - 출처 정보 컴포넌트
```typescript
기능:
- API 응답의 sources 배열 렌더링
- 외부 링크로 출처 표시
- ExternalLink 아이콘 포함

스타일:
- 회색 배경에 파란색 왼쪽 보더
- 호버 효과 (underline)
- 새 창에서 링크 열기 (target="_blank")
```

## 🔧 기술적 구현 세부사항

### API 통신 (`lib/api.ts`)
```typescript
주요 클래스: ChatAPI

기능:
- sendMessage(): POST /api/v1/chat 호출
- 스레드 ID 자동 관리
- 에러 처리 및 로깅
- 환경 변수 지원 (VITE_API_BASE_URL)

인터페이스:
- ChatRequest: 요청 데이터 타입
- ChatResponse: 응답 데이터 타입
- ChatMessage: 메시지 타입
- Source: 출처 정보 타입
```

### 상태 관리 전략
```typescript
컴포넌트 레벨:
- useState로 로컬 상태 관리
- useRef로 DOM 참조 (자동 스크롤)
- useEffect로 사이드 이펙트 처리

전역 상태:
- React Query로 서버 상태 관리
- Context API 없이 prop drilling 최소화
```

### 스타일링 시스템
```typescript
Tailwind CSS:
- 유틸리티 클래스 기반
- 반응형 디자인 (sm:, md:, lg:)
- 다크모드 지원 준비

shadcn/ui:
- Radix UI 기반 컴포넌트
- 접근성 최적화
- 커스터마이징 가능한 디자인 시스템
```

## 📦 의존성 분석

### 핵심 의존성
```json
프레임워크:
- react: ^18.3.1
- react-dom: ^18.3.1
- typescript: ^5.5.3
- vite: ^5.4.1

라우팅:
- react-router-dom: ^6.26.2

상태 관리:
- @tanstack/react-query: ^5.56.2

UI 라이브러리:
- @radix-ui/*: 다양한 UI 컴포넌트
- lucide-react: ^0.462.0 (아이콘)
- tailwindcss: ^3.4.11

폼 관리:
- react-hook-form: ^7.53.0
- @hookform/resolvers: ^3.9.0
- zod: ^3.23.8 (스키마 검증)

기타:
- class-variance-authority: ^0.7.1 (스타일 변형)
- clsx: ^2.1.1 (조건부 클래스)
- tailwind-merge: ^2.5.2 (클래스 병합)
```

### 개발 도구
```json
빌드 도구:
- @vitejs/plugin-react-swc: ^3.5.0
- lovable-tagger: ^1.1.7

린팅:
- eslint: ^9.9.0
- typescript-eslint: ^8.0.1

스타일링:
- autoprefixer: ^10.4.20
- postcss: ^8.4.47
- @tailwindcss/typography: ^0.5.15
```

## 🔄 데이터 플로우

### 채팅 플로우
1. **사용자 입력** → `ChatInterface.tsx`
2. **API 호출** → `lib/api.ts` → `ChatAPI.sendMessage()`
3. **서버 응답** → 백엔드 AI 에이전트
4. **응답 처리** → `ChatInterface.tsx`에서 메시지 상태 업데이트
5. **UI 렌더링** → `ChatMessage.tsx`로 메시지 표시
6. **출처 표시** → `SourcesList.tsx`로 참고 자료 렌더링

### 컴포넌트 통신
```
App.tsx
└── BrowserRouter
    └── Routes
        └── Index.tsx
            ├── ChatInterface.tsx
            │   └── ChatMessage.tsx
            │       └── SourcesList.tsx
            └── RelatedProducts.tsx
```

## 🎨 UI/UX 특징

### 디자인 시스템
- **색상**: 주로 회색 계열 (gray-50, gray-100, etc.)
- **액센트**: 파란색 (blue-600, blue-700)
- **타이포그래피**: 시스템 폰트 스택
- **간격**: Tailwind의 스페이싱 시스템

### 반응형 디자인
- **모바일 우선**: 기본적으로 모바일 레이아웃
- **데스크톱**: `lg:` 브레이크포인트에서 사이드바 표시
- **유연한 그리드**: Flexbox 기반 레이아웃

### 접근성
- **키보드 네비게이션**: Enter 키로 메시지 전송
- **ARIA 라벨**: Radix UI 컴포넌트를 통한 접근성
- **의미론적 HTML**: 적절한 태그 사용

## 🚀 성능 최적화

### 코드 분할
- React.lazy() 사용 준비 (현재는 소규모로 미적용)
- 동적 import 지원

### 번들 최적화
- Vite의 빠른 HMR
- SWC 컴파일러 사용
- Tree shaking 지원

### 런타임 최적화
- React.memo 적용 가능한 컴포넌트 식별
- useCallback, useMemo 최적화 여지

## 🔮 확장 가능성

### 추가 가능한 기능
1. **사용자 인증**: 로그인/회원가입
2. **대화 기록**: 채팅 히스토리 저장
3. **제품 즐겨찾기**: 북마크 기능
4. **다국어 지원**: i18n 구현
5. **PWA**: Progressive Web App 변환
6. **실시간 알림**: WebSocket 통신

### 아키텍처 개선 방향
1. **상태 관리**: Zustand 또는 Redux Toolkit 도입
2. **테스팅**: Jest + React Testing Library
3. **스토리북**: 컴포넌트 문서화
4. **CI/CD**: 자동화된 배포 파이프라인
5. **모니터링**: 에러 추적 및 성능 모니터링

## 📝 개발 가이드라인

### 코딩 컨벤션
- TypeScript strict 모드 사용
- ESLint 규칙 준수
- 컴포넌트명은 PascalCase
- 파일명은 PascalCase (.tsx)

### 폴더 구조 규칙
- 컴포넌트별 단일 파일
- UI 컴포넌트는 `components/ui/`
- 비즈니스 로직은 `lib/`
- 페이지는 `pages/`

### Git 워크플로우
- 기능별 브랜치 생성
- PR 기반 코드 리뷰
- 커밋 메시지 컨벤션 준수

## 🎯 현재 상태 요약

### ✅ 완성된 기능
- 기본 채팅 인터페이스
- 실제 API 통신
- 출처 정보 표시
- 에러 처리
- 반응형 디자인

### 🚧 개선 필요 사항
- 컴포넌트 테스트 추가
- 성능 최적화
- 접근성 개선
- SEO 최적화
- 로딩 상태 UX 개선

### 📈 기술적 우수점
- 현대적인 React 패턴 사용
- TypeScript로 타입 안정성 확보
- shadcn/ui로 일관성 있는 디자인
- Vite로 빠른 개발 환경
- 모듈화된 코드 구조

이 프론트엔드는 확장 가능하고 유지보수가 용이한 구조로 설계되어 있으며, 현대적인 React 개발 패턴을 잘 따르고 있습니다.
