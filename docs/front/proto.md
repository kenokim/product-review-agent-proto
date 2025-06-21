# 프론트엔드 기술 분석 리포트

## 📋 프로젝트 개요
- **프로젝트명**: Product Review Agent Proto - Frontend
- **타입**: 제품 비교 플랫폼의 프론트엔드 애플리케이션
- **주요 기능**: AI 기반 제품 비교 및 추천 시스템

## 🛠 기술 스택

### 핵심 프레임워크 & 라이브러리
- **React 18.3.1**: 메인 UI 프레임워크
- **TypeScript 5.5.3**: 타입 안전성을 위한 정적 타입 언어
- **Vite 5.4.1**: 번들러 및 개발 서버 (빠른 HMR 지원)
- **React Router DOM 6.26.2**: 클라이언트 사이드 라우팅

### UI/UX 컴포넌트 시스템
- **shadcn/ui**: 모던 React 컴포넌트 라이브러리
- **Radix UI**: 접근성 최적화된 헤드리스 UI 컴포넌트
  - Dialog, Dropdown, Tooltip, Select 등 다양한 컴포넌트 활용
- **Tailwind CSS 3.4.11**: 유틸리티 퍼스트 CSS 프레임워크
- **Lucide React**: 아이콘 라이브러리

### 상태 관리 & 데이터 페칭
- **TanStack Query (React Query) 5.56.2**: 서버 상태 관리 및 데이터 페칭
- **React Hook Form 7.53.0**: 폼 상태 관리 및 유효성 검사
- **Zod 3.23.8**: 스키마 검증 라이브러리

### 스타일링 & 테마
- **Tailwind CSS**: 반응형 디자인 및 다크모드 지원
- **CSS Variables**: 동적 테마 시스템
- **next-themes**: 테마 토글 기능

### 개발 도구
- **ESLint**: 코드 품질 관리
- **TypeScript**: 타입 체크
- **Vite**: 개발 서버 및 번들링
- **SWC**: 빠른 컴파일링

## 🏗 프로젝트 구조

```
front/
├── src/
│   ├── components/          # 재사용 가능한 컴포넌트
│   │   ├── ui/             # shadcn/ui 기반 기본 컴포넌트
│   │   ├── ChatHeader.tsx   # 채팅 헤더
│   │   ├── ChatInterface.tsx # 메인 채팅 인터페이스
│   │   ├── ChatMessage.tsx  # 채팅 메시지 컴포넌트
│   │   └── RelatedProducts.tsx # 관련 제품 추천
│   ├── pages/              # 페이지 컴포넌트
│   │   ├── Index.tsx       # 메인 페이지
│   │   └── NotFound.tsx    # 404 페이지
│   ├── hooks/              # 커스텀 훅
│   ├── lib/                # 유틸리티 함수
│   ├── App.tsx             # 메인 앱 컴포넌트
│   └── main.tsx           # 엔트리 포인트
├── public/                 # 정적 파일
├── package.json           # 의존성 관리
├── vite.config.ts         # Vite 설정
├── tailwind.config.ts     # Tailwind 설정
└── components.json        # shadcn/ui 설정
```

## 🚀 실행 방법

### 1. 개발 환경 실행
```bash
# 의존성 설치
npm install

# 개발 서버 실행 (포트 8080)
npm run dev
```

### 2. 빌드 및 배포
```bash
# 프로덕션 빌드
npm run build

# 개발 모드 빌드
npm run build:dev

# 빌드 결과 미리보기
npm run preview

# 코드 품질 검사
npm run lint
```

### 3. 접속 정보
- **개발 서버**: http://localhost:8080
- **호스트**: :: (모든 네트워크 인터페이스)

## 🎯 주요 기능

### 메인 애플리케이션 기능
1. **제품 비교 플랫폼**: AI 기반 제품 비교 서비스
2. **탭 기반 네비게이션**: 
   - AI 제품 비교
   - 인기 비교
   - 카테고리별 비교
3. **실시간 채팅 인터페이스**: 사용자와 AI 간의 대화형 인터페이스
4. **관련 제품 추천**: 동적 사이드바로 관련 제품 표시

### UI/UX 특징
- **반응형 디자인**: 모바일, 태블릿, 데스크톱 지원
- **다크모드 지원**: 테마 토글 기능
- **접근성 최적화**: Radix UI 기반 컴포넌트
- **모던 디자인**: shadcn/ui 디자인 시스템

## 🔧 개발 설정

### TypeScript 설정
- **앱용**: `tsconfig.app.json` - 클라이언트 코드
- **Node용**: `tsconfig.node.json` - 빌드 도구
- **통합**: `tsconfig.json` - 전체 프로젝트

### Vite 설정 특징
- **React SWC**: 빠른 컴파일링
- **Path Alias**: `@` -> `./src` 매핑
- **포트**: 8080 (IPv6 지원)
- **개발용 태거**: lovable-tagger 플러그인

### Tailwind 설정
- **다크모드**: 클래스 기반 토글
- **CSS Variables**: 동적 색상 시스템
- **커스텀 테마**: 확장된 색상 팔레트
- **애니메이션**: accordion, fade 등

## 📦 주요 의존성 분석

### 프로덕션 의존성 (48개)
- **React 생태계**: react, react-dom, react-router-dom
- **UI 컴포넌트**: @radix-ui/* (20개 패키지)
- **상태 관리**: @tanstack/react-query, react-hook-form
- **유틸리티**: clsx, tailwind-merge, date-fns
- **검증**: zod, @hookform/resolvers

### 개발 의존성 (16개)
- **TypeScript**: typescript, @types/*
- **빌드 도구**: vite, @vitejs/plugin-react-swc
- **CSS**: tailwindcss, autoprefixer, postcss
- **린터**: eslint, typescript-eslint

## 🌟 프로젝트 특징

### 장점
1. **최신 기술 스택**: React 18, TypeScript 5, Vite 5
2. **확장성**: 모듈화된 컴포넌트 구조
3. **성능 최적화**: SWC 컴파일러, Vite 번들러
4. **접근성**: Radix UI 기반 접근성 최적화
5. **개발자 경험**: 타입 안전성, HMR, 린팅

### 개선 포인트
1. **테스트 코드**: Jest/Vitest 기반 테스트 환경 추가 필요
2. **상태 관리**: 복잡한 상태의 경우 Zustand/Redux 고려
3. **국제화**: i18n 지원 추가 고려
4. **PWA**: 오프라인 지원 및 PWA 기능 추가 가능

## 💡 기술 결정 배경

### Vite 선택 이유
- **빠른 개발 서버**: ES 모듈 네이티브 지원
- **플러그인 생태계**: React, TypeScript 완벽 지원
- **최적화된 빌드**: Rollup 기반 프로덕션 빌드

### shadcn/ui 선택 이유
- **커스터마이징**: 소스 코드 복사 방식으로 완전한 제어
- **접근성**: Radix UI 기반으로 WCAG 준수
- **타입 안전성**: TypeScript 완벽 지원

### TanStack Query 선택 이유
- **서버 상태 관리**: 캐싱, 동기화, 에러 처리
- **개발자 도구**: 강력한 디버깅 도구
- **성능**: 자동 백그라운드 업데이트
