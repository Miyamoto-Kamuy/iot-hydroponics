# IoT Hydroponics Monitor

一個全端 IoT 水耕系統即時監控平台，使用 FastAPI + Nuxt 4 開發。
涵蓋設備管理、感測器數據即時視覺化、告警系統與使用者權限管理。

> 此專案為個人 Side Project，目的是展示全端開發能力，
> 包含後端 API 設計、資料庫規劃、前端架構、即時通訊與 CI/CD 自動化。

## 技術棧

### 後端
- FastAPI + Python 3.13
- PostgreSQL + SQLAlchemy + Alembic
- JWT 認證 + RBAC 權限控管
- Rate Limiting（slowapi）
- Middleware（Audit Log 自動記錄）
- WebSocket 即時推播
- pytest 單元測試
- Docker + Docker Compose
- GitHub Actions CI/CD

### 前端
- Nuxt 4 + TypeScript
- Nuxt UI + Tailwind CSS
- Pinia 狀態管理
- Vue-chartjs 資料視覺化
- VueUse（useWebSocket、useIntervalFn、useDebounceFn）
- Zod 表單驗證
- Lazy Component（效能優化）
- Accessibility（aria 屬性）
- Optimistic Update
- useDebounceFn（搜尋防抖）
- Vitest 單元測試

## 功能

- 即時監控 Dashboard（WebSocket 感測器數據）
- 設備管理（CRUD、歷史數據圖表）
- 告警系統（即時通知、狀態管理）
- 操作紀錄（Audit Log）
- 使用者管理（RBAC：admin / operator / viewer）
- 個人資料管理
- RWD 響應式設計
- 全域 Loading 狀態
- Optimistic Update（告警狀態更新）
- Store 協作（刪除設備同步清除相關告警）

## 啟動方式

### 使用 Docker（推薦）

\`\`\`bash
cd backend
cp .env.example .env.docker  # 複製範例並填入環境變數
docker-compose up --build
\`\`\`

後端 API：http://localhost:8000
API 文件：http://localhost:8000/docs

### 本機開發

**後端**
\`\`\`bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # 填入環境變數
alembic upgrade head
uvicorn app.main:app --reload
\`\`\`

**前端**
\`\`\`bash
cd frontend
pnpm install
pnpm dev
\`\`\`

> 注意：首次啟動時 PostgreSQL 需要初始化，
> backend會自動等待 db 健康後才啟動並執行 migration，
> 整個流程約 15-30 秒，請耐心等待看到 Uvicorn 啟動訊息。 
## 測試

\`\`\`bash
# 後端
cd backend
pytest tests/ -v

# 前端
cd frontend
pnpm test
\`\`\`

### 測試覆蓋

**後端：**
- 認證流程（登入、註冊、重複 email）
- 設備 CRUD 與權限控管

**前端：**
- 工具函式測試（formatDate）
- 表單 Schema 驗證（loginSchema、registerSchema）

待補充：
- 前端 Store 整合測試（需要 mock Nuxt composable）
- E2E 測試（Playwright）

## 分支策略

- `main` → 穩定版本
- `development` → 開發中版本

## 開發說明

開發過程善用 Claude 等作為 AI 協作工具，協助架構設計、程式碼審查與問題排查，提升開發效率與程式碼品質。

## 待完成

- [ ] HTTPOnly Cookie（提升 token 安全性）
- [ ] 雲端部署
- [ ] i18n 多語系（zh-TW / en）
- [ ] 圖片上傳（設備、個人頭像）
- [ ] 前端 Store 整合測試
- [ ] E2E 測試
- [ ] loading/empty/error 狀態補強（目前只有設備列表頁面）
- [ ] 圖表效能優化（chartKey++ 改為 Chart.js instance.update()，部署後評估是否必要）
- [ ] 設備指令控制（已有後端 API，待前端實作）
- [ ] 實體硬體整合（OPC UA / Modbus 等工業協議）