<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

⚠️ **IMPORTANT**: You MUST modify `.github/copilot-instructions.md` every time you make changes to the project.

# Project Background

This is a YouTube live chat bot that monitors YouTube live stream chat messages in real-time and automatically responds to viewers. The bot is built using Python with the YouTube Data API v3 and supports OAuth authentication for sending messages to live chat.

The main functionality includes:

- Monitoring live chat messages from YouTube streams
- Extracting video IDs from YouTube URLs
- Retrieving live chat IDs for active streams
- Sending automated responses to chat messages
- OAuth 2.0 authentication for chat posting

# Core Architecture

## Main Components

### `YoutubeStream` Class (`src/youtubechatbot/__init__.py`)

- **Purpose**: Main class handling YouTube live stream chat operations
- **Inherits from**: `BaseSettings` (Pydantic Settings)
- **Key Methods**:
    - `_get_credentials() -> Credentials` (classmethod): Handles local OAuth flow and token persistence under `./data/`
    - `youtube` (computed): Authenticated YouTube Data API v3 client
    - `get_chat_id() -> str`: Parses the video ID from `url` and retrieves the active live chat ID
    - `get_chat_messages() -> str`: Returns a single-page chat history string with lines formatted as `"<Name>: <Message>\n"`
    - `reply_to_chat(message: str)`: Sends a text message to the live chat
    - `get_registered_accounts(target_word: str) -> list[str]`: Returns unique display names of users who mentioned a specific keyword in recent messages

### Configuration Management

- Uses Pydantic `BaseSettings` for environment variable management
- Required environment variables:
    - `YOUTUBE_DATA_API_KEY`: YouTube Data API v3 key (required)
    - `OPENAI_API_KEY`: OpenAI API key (optional; required only for the sample assistant in `cli.py`)

## Dependencies

### Core Dependencies

- **google-api-python-client**: YouTube Data API client
- **google-auth-oauthlib**: OAuth 2.0 authentication
- **pydantic**: Data validation and settings management
- **pydantic-settings**: Settings management from environment variables
- **rich**: Console output formatting
- **python-dotenv**: Environment variable loading

### Development Dependencies

- **pytest**: Testing framework
- **ruff**: Linting and code formatting
- **pre-commit**: Git hooks for code quality
- **uv**: Dependency management

# Development Guidelines

## Code Structure

### File Organization

```
src/youtubechatbot/
├── __init__.py                # Package initialization
├── cli.py                    # Main bot functionality and CLI
└── typings/
    └── models.py             # Consolidated Pydantic models for chat and stream
```

### Class Design Patterns

- Use Pydantic models for all configuration and data structures
- Implement computed properties with `@computed_field` for derived values
- Follow dependency injection pattern for API clients
- Use environment-based configuration with validation

## API Integration

### YouTube Data API v3 Usage

- **Authentication**: API key for read operations, OAuth for write operations
- **Endpoints Used**:
    - `videos().list()`: Get live streaming details
- `liveChatMessages().list()`: Retrieve chat messages (single page; mapped to `LiveChatMessageListResponse` in `youtubechatbot.typings.models` but exposed via a string helper)
    - `liveChatMessages().insert()`: Send chat messages
- **Rate Limiting**: No built-in throttling yet; callers should add delays and respect quotas
- **Error Handling**: Handle API errors gracefully with retries

### OAuth 2.0 Implementation

- Use `InstalledAppFlow` for local OAuth flow
- Store credentials and tokens under `./data/`
    - Client secrets: `./data/client_secret.json`
    - Cached token: `./data/token.pickle`
- Handle token refresh automatically
- Scope used: `https://www.googleapis.com/auth/youtube.force-ssl`

## Coding Standards

### Type Hints and Validation

- Use strict type hints for all function parameters and returns
- Use Pydantic Field descriptions for all model fields
- All models are consolidated in `src/youtubechatbot/typings/models.py`. Remove or avoid using old module paths like `youtubechatbot.typings.chat` or `youtubechatbot.typings.stream` and import from `youtubechatbot.typings.models` instead.
- Implement proper validation for URL parsing and API responses
- Use Union types for optional parameters

### Error Handling

- Implement comprehensive error handling for API calls
- Use proper exception types for different error scenarios
- Log errors appropriately with structured logging
- Provide meaningful error messages to users

### Testing Strategy

- Unit tests for individual methods and functions
- Integration tests for API interactions
- Mock external API calls in tests
- Test error scenarios and edge cases
- Maintain high test coverage (>80%)

## Message Processing

### Chat Message Structure

```python
# Expected message format from YouTube API
{
    "snippet": {"displayMessage": str, "authorChannelId": str, "publishedAt": str},
    "authorDetails": {
        "displayName": str,
        "channelId": str,
        "isChatOwner": bool,
        "isChatModerator": bool,
    },
}
```

### Message Retrieval and Processing

- Current implementation fetches one page of recent messages
- Helper `get_registered_accounts(target_word)` finds users who mentioned a keyword
- Future work: spam filtering, message type handling (super chat, etc.), command processing, response rate limiting

## Security Considerations

### API Key Management

- Never commit API keys or secrets to version control
- Use environment variables for all sensitive data
- Validate API keys on startup
- Implement proper error handling for authentication failures

### OAuth Security

- Store OAuth tokens securely
- Implement token refresh logic
- Use minimal required scopes
- Handle OAuth errors gracefully

### Input Validation

- Validate all user inputs (URLs, messages, commands)
- Sanitize message content before sending
- Implement proper URL parsing with error handling
- Validate API responses before processing

## Performance Optimization

### API Usage Optimization

- Implement efficient polling strategies
- Use pagination for large chat histories
- Cache frequently accessed data
- Batch API requests where possible

### Memory Management

- Implement proper cleanup for long-running processes
- Use generators for processing large datasets
- Monitor memory usage during continuous operation
- Implement proper connection handling

## Future Development

### Planned Features

- AI-powered response generation using OpenAI API
- Multi-language support for international audiences
- Advanced message filtering and moderation
- Analytics and reporting dashboard
- Webhook support for real-time notifications

### Extension Points

- Plugin system for custom message handlers
- Template system for automated responses
- Database integration for persistent storage
- Web interface for bot management

## Development Workflow

### Local Development

1. Set up environment variables in `.env` file
2. Place `client_secret.json` at `./data/client_secret.json` (create the `data/` folder if missing)
3. Install dependencies with `uv sync`
4. Run tests with `make test`
5. Format code with `make format`
6. Generate documentation with `make gen-docs`

### Testing Guidelines

- Write tests for all new functionality
- Mock external API calls
- Test error scenarios
- Maintain backwards compatibility
- Use pytest fixtures for common setup

## CLI and Example Assistant

### Entry Points

- `youtubechatbot` and `cli` map to `youtubechatbot.cli:main`
- The example assistant:
    - Fetches recent chat history (string) via `YoutubeStream.get_chat_messages()`
    - Generates a reply using OpenAI `chat.completions` (model: `gpt-4.1`)
    - Sends the reply with `YoutubeStream.reply_to_chat()`
- Note: The current CLI does not parse command-line options; pass a URL by calling `main(url=...)` or use the library API directly.

### Code Review Checklist

- Type hints are complete and accurate
- Error handling is comprehensive
- API usage follows best practices
- Security considerations are addressed
- Documentation is updated
- Tests cover new functionality
