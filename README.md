<center>

# YouTube Chat Bot

[![python](https://img.shields.io/badge/-Python_3.10_%7C_3.11_%7C_3.12-blue?logo=python&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![uv](https://img.shields.io/badge/-uv_dependency_management-2C5F2D?logo=python&logoColor=white)](https://docs.astral.sh/uv/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![tests](https://github.com/Mai0313/youtubechatbot/actions/workflows/test.yml/badge.svg)](https://github.com/Mai0313/youtubechatbot/actions/workflows/test.yml)
[![code-quality](https://github.com/Mai0313/youtubechatbot/actions/workflows/code-quality-check.yml/badge.svg)](https://github.com/Mai0313/youtubechatbot/actions/workflows/code-quality-check.yml)
[![license](https://img.shields.io/badge/License-MIT-green.svg?labelColor=gray)](https://github.com/Mai0313/youtubechatbot/tree/master?tab=License-1-ov-file)
[![PRs](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/Mai0313/youtubechatbot/pulls)
[![contributors](https://img.shields.io/github/contributors/Mai0313/youtubechatbot.svg)](https://github.com/Mai0313/youtubechatbot/graphs/contributors)

</center>

🤖 **A powerful YouTube live chat bot that can monitor live stream chat messages and automatically respond to viewers**

Monitor YouTube live streams, analyze chat messages in real-time, and engage with your audience through automated responses.

**Other Languages**: [English](README.md) | [繁體中文](README_cn.md)

## ✨ Features

### 🟢 **Live Chat Monitoring**

- **Real-time chat tracking**: Monitor YouTube live stream chat messages as they appear
- **Multiple stream support**: Connect to different YouTube live streams
- **Message filtering**: Filter and process specific types of messages
- **Author identification**: Track message authors and their details

### 🤖 **Automated Response System**

- **Smart replies (example)**: Example assistant in `youtubechatbot.cli` uses OpenAI to compose a reply and post it back
- **OAuth authentication**: Secure authentication with YouTube API
- **Custom logic**: Extend `YoutubeStream` to implement your own reply logic
- **Rate limiting**: Respect YouTube API rate limits (add throttling in your loop)

### ⚙️ **Easy Configuration**

- **Environment variables**: Simple setup with `.env` file
- **YouTube Data API**: Integration with YouTube Data API v3
- **OpenAI integration**: Ready for AI-powered responses (future feature)
- **CLI entry points**: `youtubechatbot` and `cli` invoke the example assistant

### 🛡️ **Modern Development**

- **Type safety**: Full type hints with Pydantic models
- **Error handling**: Robust error handling and logging
- **Testing support**: Comprehensive testing framework
- **Code quality**: Pre-commit hooks and code formatting

## 🚀 Quick Start

### Prerequisites

1. **YouTube Data API Key**: Get your API key from [Google Cloud Console](https://console.cloud.google.com/)
2. **OAuth 2.0 Credentials**: Download `client_secret.json` for chat posting functionality
3. **Python 3.10+**: Make sure you have Python 3.10 or later installed

### Installation

1. **Clone the repository**:

    ```bash
    git clone https://github.com/Mai0313/youtubechatbot.git
    cd youtubechatbot
    ```

2. **Install dependencies**:

    ```bash
    make uv-install  # Install uv if not already installed
    uv sync          # Install project dependencies
    ```

3. **Set up environment variables**:

    Create a `.env` file in the project root and add your keys:

    ```env
    YOUTUBE_DATA_API_KEY=your_youtube_data_api_key_here
    OPENAI_API_KEY=your_openai_api_key_here  # optional
    ```

4. **Configure OAuth (for sending messages)**:

    - Download `client_secret.json` from Google Cloud Console
    - Place it at `./data/client_secret.json` (create the `data/` folder if missing)

### Basic Usage (Library)

#### Monitor Live Chat Messages

```python
from youtubechatbot import YoutubeStream

# Create a stream instance
stream = YoutubeStream(url="https://www.youtube.com/watch?v=YOUR_VIDEO_ID")

# Fetch a page of recent chat messages as a single string
chat_history = stream.get_chat_messages()
print(chat_history)
```

#### Send a Message to Chat

```python
# Reply to the chat
stream.reply_to_chat("Hello everyone! 👋")
```

#### Command Line Usage (Example Assistant)

```bash
youtubechatbot  # runs the example assistant with the default URL inside `cli.py`

python -m youtubechatbot.cli  # equivalent
```

## 📁 Project Structure

```
├── .devcontainer/          # VS Code Dev Container configuration
├── .github/
│   ├── workflows/          # CI/CD workflows
│   └── copilot-instructions.md
├── docker/                 # Docker configurations
├── docs/                   # MkDocs documentation
├── scripts/                # Automation scripts
├── src/
│   └── youtubechatbot/     # Main bot package
│       ├── __init__.py
│       └── cli.py          # Core bot functionality
├── tests/                  # Test suite
├── client_secret.json      # OAuth credentials (not in repo)
├── .env                    # Environment variables (not in repo)
├── pyproject.toml          # Project configuration
├── Makefile               # Development commands
└── README.md
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
YOUTUBE_DATA_API_KEY=your_youtube_data_api_key_here
OPENAI_API_KEY=your_openai_api_key_here  # Optional, for future AI features
```

### OAuth Setup for Sending Messages

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable YouTube Data API v3
4. Create OAuth 2.0 credentials
5. Download the JSON file and rename it to `client_secret.json`
6. Place it at `./data/client_secret.json` (create the `data/` folder if missing)

### API Rate Limits

- **YouTube Data API**: 10,000 units per day (default)
- **Chat messages**: ~1 unit per message retrieved
- **Sending messages**: ~50 units per message sent

Monitor your usage in Google Cloud Console to avoid hitting limits.

## 🛠️ Available Commands

```bash
# Development
make clean          # Clean autogenerated files
make format         # Run pre-commit hooks
make test           # Run all tests
make gen-docs       # Generate documentation

# Dependencies
make uv-install     # Install uv dependency manager
uv add <package>    # Add production dependency
uv add <package> --dev  # Add development dependency

# Example Assistant
youtubechatbot
python -m youtubechatbot.cli
```

## 🔧 Advanced Usage

### Custom Message Processing

```python
from youtubechatbot import YoutubeStream


class CustomChatBot(YoutubeStream):
    def run_once(self) -> None:
        page = self.get_chat_messages()
        for line in page.splitlines():
            if ":" not in line:
                continue
            author, message = line.split(":", 1)
            if "hello" in message.lower():
                self.reply_to_chat(f"Hello {author.strip()}! 👋")
            elif "help" in message.lower():
                self.reply_to_chat("Available commands: !help, !info, !time")


# Use your custom bot
bot = CustomChatBot(url="https://www.youtube.com/watch?v=YOUR_VIDEO_ID")
bot.get_chat_messages()
```

### Integration with AI Services (Example)

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

## 🎯 Use Cases

### Content Creator Engagement

- **Auto-greetings**: Welcome new viewers automatically
- **FAQ responses**: Answer common questions instantly
- **Moderation**: Filter and respond to inappropriate content
- **Stream interaction**: Create interactive games and polls

### Business Applications

- **Customer support**: Provide instant responses during live events
- **Product launches**: Engage with audience during announcements
- **Educational content**: Answer student questions during live classes
- **Community building**: Foster engagement in live communities

## 🔎 Keyword Registration Utility

Use `get_registered_accounts(target_word)` to collect unique users who mentioned a keyword in the latest page of messages:

```python
users = stream.get_registered_accounts(target_word="!join")
print(users)
```

## 🔒 Security and Privacy

- **OAuth 2.0**: Secure authentication with YouTube
- **API key management**: Environment-based credential storage
- **Rate limiting**: Respects YouTube API quotas
- **Error handling**: Graceful handling of API failures

## 🚨 Troubleshooting

### Common Issues

**Bot not receiving messages:**

- Verify the YouTube URL is for a live stream
- Check if the stream has chat enabled
- Ensure your API key has proper permissions

**Cannot send messages:**

- Verify `client_secret.json` is properly configured
- Check OAuth permissions include chat posting
- Ensure the bot account can post in the chat

**API quota exceeded:**

- Monitor your API usage in Google Cloud Console
- Implement message batching for high-volume streams
- Consider upgrading your API quota if needed

## 🤝 Contributing

We welcome contributions! Please feel free to:

- **Report bugs**: Open issues for any problems you encounter
- **Request features**: Suggest new functionality for the bot
- **Submit improvements**: Create pull requests for enhancements
- **Share use cases**: Tell us how you're using the bot

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes and add tests
4. Run tests: `make test`
5. Format code: `make format`
6. Commit changes: `git commit -m 'Add amazing feature'`
7. Push to branch: `git push origin feature/amazing-feature`
8. Open a Pull Request

## 📖 Documentation

For detailed documentation and API reference, visit: [https://mai0313.github.io/youtubechatbot/](https://mai0313.github.io/youtubechatbot/)

## 👥 Contributors

[![Contributors](https://contrib.rocks/image?repo=Mai0313/youtubechatbot)](https://github.com/Mai0313/youtubechatbot/graphs/contributors)

Made with [contrib.rocks](https://contrib.rocks)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Happy streaming! 🎥✨**
