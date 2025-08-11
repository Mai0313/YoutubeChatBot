<center>

# YouTube 聊天室機器人

[![python](https://img.shields.io/badge/-Python_3.10_%7C_3.11_%7C_3.12-blue?logo=python&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![uv](https://img.shields.io/badge/-uv_dependency_management-2C5F2D?logo=python&logoColor=white)](https://docs.astral.sh/uv/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![tests](https://github.com/Mai0313/youtubechatbot/actions/workflows/test.yml/badge.svg)](https://github.com/Mai0313/youtubechatbot/actions/workflows/test.yml)
[![code-quality](https://github.com/Mai0313/youtubechatbot/actions/workflows/code-quality-check.yml/badge.svg)](https://github.com/Mai0313/youtubechatbot/actions/workflows/code-quality-check.yml)
[![license](https://img.shields.io/badge/License-MIT-green.svg?labelColor=gray)](https://github.com/Mai0313/youtubechatbot/tree/master?tab=License-1-ov-file)
[![PRs](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/Mai0313/youtubechatbot/pulls)
[![contributors](https://img.shields.io/github/contributors/Mai0313/youtubechatbot.svg)](https://github.com/Mai0313/youtubechatbot/graphs/contributors)

</center>

🤖 **功能強大的 YouTube 直播聊天室機器人，可以監控直播聊天訊息並自動回覆觀眾**

即時監控 YouTube 直播聊天室，分析聊天訊息，並透過自動回覆與您的觀眾互動。

**其他語言版本**: [English](README.md) | [繁體中文](README_cn.md)

## ✨ 功能特色

### 🟢 **即時聊天室監控**

- **即時聊天追蹤**: 即時監控 YouTube 直播聊天室訊息
- **多直播支援**: 連接到不同的 YouTube 直播串流
- **訊息過濾**: 過濾和處理特定類型的訊息
- **用戶識別**: 追蹤訊息作者及其詳細資訊

### 🤖 **自動回覆系統**

- **智慧回覆（示例）**: `youtubechatbot.cli` 中的示例助理使用 OpenAI 產生回覆並發送
- **OAuth 驗證**: 與 YouTube API 的安全驗證
- **自訂邏輯**: 繼承 `YoutubeStream` 實作您自己的回覆邏輯
- **速率限制**: 請在您的輪詢邏輯中加入節流以遵守 API 限制

### ⚙️ **簡易配置**

- **環境變數**: 使用 `.env` 檔案進行簡單設定
- **YouTube Data API**: 整合 YouTube Data API v3
- **OpenAI 整合**: 為 AI 驅動的回覆做好準備（未來功能）
- **CLI 入口**: `youtubechatbot` 與 `cli` 會啟動示例助理

### 🛡️ **現代化開發**

- **類型安全**: 使用 Pydantic 模型的完整類型提示
- **錯誤處理**: 強大的錯誤處理和日誌記錄
- **測試支援**: 完整的測試框架
- **程式碼品質**: Pre-commit hooks 和程式碼格式化

## 🚀 快速開始

### 預備條件

1. **YouTube Data API 金鑰**: 從 [Google Cloud Console](https://console.cloud.google.com/) 取得您的 API 金鑰
2. **OAuth 2.0 憑證**: 下載 `client_secret.json` 以使用聊天室發訊功能
3. **Python 3.10+**: 確保您安裝了 Python 3.10 或更新版本

### 安裝步驟

1. **複製儲存庫**:

    ```bash
    git clone https://github.com/Mai0313/youtubechatbot.git
    cd youtubechatbot
    ```

2. **安裝依賴套件**:

    ```bash
    make uv-install  # 如果尚未安裝 uv
    uv sync          # 安裝專案依賴
    ```

3. **設定環境變數**:

    在專案根目錄建立 `.env` 並加入：

    ```env
    YOUTUBE_DATA_API_KEY=您的youtube_data_api金鑰
    OPENAI_API_KEY=您的openai_api金鑰  # 可選
    ```

4. **配置 OAuth（用於發送訊息）**:

    - 從 Google Cloud Console 下載 `client_secret.json`
    - 放置於 `./data/client_secret.json`（若無 `data/` 請自行建立）

### 基本使用方式（函式庫）

#### 監控直播聊天室訊息

```python
from youtubechatbot import YoutubeStream

# 建立串流實例
stream = YoutubeStream(url="https://www.youtube.com/watch?v=您的影片ID")

# 取得一頁最近的聊天室訊息（具型別）
resp = stream.get_chat_messages()
for item in resp.items:
    author = item.author_details.display_name if item.author_details else "Unknown"
    print(f"{author}: {item.snippet.display_message}")
```

#### 發送訊息到聊天室

```python
# 回覆聊天室
stream.reply_to_chat("大家好！ 👋")
```

#### 命令列使用方式（示例助理）

```bash
youtubechatbot  # 執行 `cli.py` 內建的示例助理（使用預設 URL）

python -m youtubechatbot.cli  # 等效
```

## 📁 專案結構

```
├── .devcontainer/          # VS Code Dev Container 配置
├── .github/
│   ├── workflows/          # CI/CD 工作流程
│   └── copilot-instructions.md
├── data/
│   └── client_secret.json  # OAuth 憑證（不在儲存庫中）
├── docker/                 # Docker 配置
├── docs/                   # MkDocs 文檔
├── scripts/                # 自動化腳本
├── src/
│   └── youtubechatbot/     # 主要機器人套件
│       ├── __init__.py
│       └── cli.py          # 核心機器人功能
├── tests/                  # 測試套件
├── .env                    # 環境變數（不在儲存庫中）
├── pyproject.toml          # 專案配置
├── Makefile               # 開發命令
└── README.md
```

## ⚙️ 配置設定

### 環境變數

在專案根目錄建立 `.env` 檔案：

```env
YOUTUBE_DATA_API_KEY=您的youtube_data_api金鑰
OPENAI_API_KEY=您的openai_api金鑰  # 可選，用於未來的 AI 功能
```

### OAuth 設定用於發送訊息

1. 前往 [Google Cloud Console](https://console.cloud.google.com/)
2. 建立新專案或選擇現有專案
3. 啟用 YouTube Data API v3
4. 建立 OAuth 2.0 憑證
5. 下載 JSON 檔案並重新命名為 `client_secret.json`
6. 放置於 `./data/client_secret.json`（若無 `data/` 請自行建立）

### API 速率限制

- **YouTube Data API**: 每日 10,000 單位（預設）
- **聊天訊息**: 每則訊息約 1 個單位
- **發送訊息**: 每則訊息約 50 個單位

在 Google Cloud Console 監控您的使用量以避免達到限制。

## 🛠️ 可用命令

```bash
# 開發相關
make clean          # 清理自動生成的檔案
make format         # 執行 pre-commit hooks
make test           # 執行所有測試
make gen-docs       # 生成文檔

# 依賴管理
make uv-install     # 安裝 uv 依賴管理器
uv add <套件名稱>    # 添加生產依賴
uv add <套件名稱> --dev  # 添加開發依賴

# 示例助理
youtubechatbot
python -m youtubechatbot.cli
```

## 🔧 進階使用

### 自訂訊息處理

```python
from youtubechatbot import YoutubeStream


class CustomChatBot(YoutubeStream):
    def run_once(self) -> None:
        page = self.get_chat_messages()
        for line in page.splitlines():
            if ":" not in line:
                continue
            author, message = line.split(":", 1)
            if "你好" in message or "hello" in message.lower():
                self.reply_to_chat(f"哈囉 {author.strip()}！ 👋")
            elif "幫助" in message or "help" in message.lower():
                self.reply_to_chat("可用指令：!help, !info, !time")


# 使用您的自訂機器人
bot = CustomChatBot(url="https://www.youtube.com/watch?v=您的影片ID")
bot.get_chat_messages()
```

### 與 AI 服務整合（示例）

```python
from openai import OpenAI
from youtubechatbot import YoutubeStream


class AIChatBot(YoutubeStream):
    def generate_ai_response(self, message: str) -> str:
        client = OpenAI()
        response = client.chat.completions.create(
            model="gpt-4.1", messages=[{"role": "user", "content": message}]
        )
        return response.choices[0].message.content
```

## 🎯 使用案例

### 內容創作者互動

- **自動問候**: 自動歡迎新觀眾
- **FAQ 回應**: 即時回答常見問題
- **內容管理**: 過濾並回應不當內容
- **串流互動**: 建立互動遊戲和投票

### 商業應用

- **客戶支援**: 在直播活動中提供即時回應
- **產品發表**: 在產品發表會期間與觀眾互動
- **教育內容**: 在直播課程中回答學生問題
- **社群建設**: 在直播社群中促進參與

## 🔎 關鍵字登記工具

使用 `get_registered_accounts(target_word)` 收集最近一頁訊息中有提及關鍵字的唯一用戶：

```python
users = stream.get_registered_accounts(target_word="!join")
print(users)
```

## 🔒 安全性與隱私

- **OAuth 2.0**: 與 YouTube 的安全驗證
- **API 金鑰管理**: 基於環境變數的憑證儲存
- **速率限制**: 遵守 YouTube API 配額
- **錯誤處理**: 優雅處理 API 故障

## 🚨 疑難排解

### 常見問題

**機器人無法接收訊息:**

- 確認 YouTube 網址是直播串流
- 檢查串流是否啟用聊天室
- 確保您的 API 金鑰有適當權限

**無法發送訊息:**

- 確認 `client_secret.json` 正確配置
- 檢查 OAuth 權限包含聊天室發文權限
- 確保機器人帳戶可以在聊天室發文

**API 配額超出:**

- 在 Google Cloud Console 監控您的 API 使用量
- 為高流量串流實作訊息批次處理
- 如需要可考慮升級您的 API 配額

## 🤝 貢獻

我們歡迎貢獻！請隨時：

- **回報錯誤**: 為您遇到的任何問題開啟 issue
- **請求功能**: 為機器人建議新功能
- **提交改進**: 為增強功能建立 pull requests
- **分享使用案例**: 告訴我們您如何使用機器人

### 開發設定

1. Fork 此儲存庫
2. 建立功能分支: `git checkout -b feature/amazing-feature`
3. 進行變更並添加測試
4. 執行測試: `make test`
5. 格式化程式碼: `make format`
6. 提交變更: `git commit -m 'Add amazing feature'`
7. 推送到分支: `git push origin feature/amazing-feature`
8. 開啟 Pull Request

## 📖 文檔

詳細文檔和 API 參考，請訪問：[https://mai0313.github.io/youtubechatbot/](https://mai0313.github.io/youtubechatbot/)

## 👥 貢獻者

[![Contributors](https://contrib.rocks/image?repo=Mai0313/youtubechatbot)](https://github.com/Mai0313/youtubechatbot/graphs/contributors)

Made with [contrib.rocks](https://contrib.rocks)

## 📄 授權

本專案採用 MIT 授權 - 詳見 [LICENSE](LICENSE) 檔案。

---

**祝您直播愉快！ 🎥✨**
