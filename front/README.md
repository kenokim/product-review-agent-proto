# Welcome to your Lovable project

## Project info

**URL**: https://lovable.dev/projects/86d9711e-e0a7-49a0-b733-811651c17530

## API 연결 설정

이 프론트엔드는 백엔드 API 서버와 연결됩니다.

### 1. 백엔드 서버 실행
```sh
# 백엔드 서버 디렉토리로 이동
cd ../server

# 서버 실행 (FastAPI)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. 프론트엔드 실행
```sh
# 프론트엔드 디렉토리에서
npm run dev
```

### 3. API 설정
- 기본 API URL: `http://localhost:8000/api/v1`
- 환경 변수로 변경 가능: `VITE_API_BASE_URL`

### 4. 기능
- 🤖 AI 제품 추천 채팅
- 🔍 실시간 웹 검색
- 📚 출처 정보 표시
- 💬 대화 스레드 관리

## How can I edit this code?

There are several ways of editing your application.

**Use Lovable**

Simply visit the [Lovable Project](https://lovable.dev/projects/86d9711e-e0a7-49a0-b733-811651c17530) and start prompting.

Changes made via Lovable will be committed automatically to this repo.

**Use your preferred IDE**

If you want to work locally using your own IDE, you can clone this repo and push changes. Pushed changes will also be reflected in Lovable.

The only requirement is having Node.js & npm installed - [install with nvm](https://github.com/nvm-sh/nvm#installing-and-updating)

Follow these steps:

```sh
# Step 1: Clone the repository using the project's Git URL.
git clone <YOUR_GIT_URL>

# Step 2: Navigate to the project directory.
cd <YOUR_PROJECT_NAME>

# Step 3: Install the necessary dependencies.
npm i

# Step 4: Start the development server with auto-reloading and an instant preview.
npm run dev
```

**Edit a file directly in GitHub**

- Navigate to the desired file(s).
- Click the "Edit" button (pencil icon) at the top right of the file view.
- Make your changes and commit the changes.

**Use GitHub Codespaces**

- Navigate to the main page of your repository.
- Click on the "Code" button (green button) near the top right.
- Select the "Codespaces" tab.
- Click on "New codespace" to launch a new Codespace environment.
- Edit files directly within the Codespace and commit and push your changes once you're done.

## What technologies are used for this project?

This project is built with:

- Vite
- TypeScript
- React
- shadcn-ui
- Tailwind CSS

## How can I deploy this project?

Simply open [Lovable](https://lovable.dev/projects/86d9711e-e0a7-49a0-b733-811651c17530) and click on Share -> Publish.

## Can I connect a custom domain to my Lovable project?

Yes, you can!

To connect a domain, navigate to Project > Settings > Domains and click Connect Domain.

Read more here: [Setting up a custom domain](https://docs.lovable.dev/tips-tricks/custom-domain#step-by-step-guide)
