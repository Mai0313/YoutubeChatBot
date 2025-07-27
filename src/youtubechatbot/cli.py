import pickle
from pathlib import Path
from functools import cached_property
from urllib.parse import urlparse

import dotenv
from openai import OpenAI
from pydantic import Field, computed_field
from rich.console import Console
from pydantic_settings import BaseSettings
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import Resource, build
from google.auth.transport.requests import Request

from youtubechatbot.typings.chat import LiveChatMessageItem, LiveChatMessageListResponse
from youtubechatbot.typings.stream import VideoListResponse

dotenv.load_dotenv()
console = Console()


class Config(BaseSettings):
    youtube_data_api_key: str = Field(..., validation_alias="YOUTUBE_DATA_API_KEY")
    openai_api_key: str = Field(..., validation_alias="OPENAI_API_KEY")


class YoutubeStream(Config):
    url: str

    @computed_field
    @property
    def video_id(self) -> str:
        parsed_url = urlparse(url=self.url)
        video_id = parsed_url.query.split("=")[-1]
        return video_id

    @computed_field
    @property
    def client(self) -> OpenAI:
        client = OpenAI(api_key=self.openai_api_key)
        return client

    @computed_field
    @cached_property
    def youtube(self) -> Resource:
        credentials = self.get_credentials()
        youtube = build(
            serviceName="youtube",
            version="v3",
            developerKey=self.youtube_data_api_key,
            credentials=credentials,
        )
        return youtube

    def get_credentials(self) -> Credentials:
        token_file = Path("./data/token.pickle")
        if token_file.exists():
            with open(token_file, "rb") as token:
                credentials: Credentials = pickle.load(token)  # noqa: S301
        else:
            credentials = None
        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                try:
                    credentials.refresh(Request())
                except Exception:
                    credentials = None

            if not credentials:
                console.print("🔐 需要重新授權...")
                flow = InstalledAppFlow.from_client_secrets_file(
                    client_secrets_file="./data/client_secret.json",
                    scopes=["https://www.googleapis.com/auth/youtube.force-ssl"],
                )
                credentials = flow.run_local_server(port=8080, open_browser=True)
                console.print("✅ 授權完成")

            with open(token_file, "wb") as token:
                pickle.dump(credentials, token)
                console.print("💾 憑證已保存")
        return credentials

    def get_oai_response(self, message: str) -> str:
        messages = [
            {"role": "user", "content": f"Here is all chat history:\n{message}"},
            {"role": "user", "content": "請假扮 Mai 代替他回應聊天室, 你只能回應一句話"},
        ]
        response = self.client.chat.completions.create(
            messages=messages, model="gpt-4.1", max_tokens=50
        )
        return response.choices[0].message.content

    def reply_to_chat(self, message: str) -> None:
        live_chat_id = self.get_chat_id()
        live_message = self.youtube.liveChatMessages()

        chat = live_message.insert(
            part="snippet",
            body={
                "snippet": {
                    "liveChatId": live_chat_id,
                    "type": "textMessageEvent",
                    "textMessageDetails": {"messageText": message},
                }
            },
        ).execute()
        chat = LiveChatMessageItem(**chat)

        console.print(f"📤 已發送: {message}")

    def get_chat_id(self) -> str:
        video_list = self.youtube.videos().list(part="liveStreamingDetails", id=self.video_id)
        response_dict = video_list.execute()
        response = VideoListResponse(**response_dict)
        chat_id = response.items[0].live_streaming_details.active_live_chat_id
        return chat_id

    def get_chat_messages(self) -> str:
        live_chat_id = self.get_chat_id()
        live_message = self.youtube.liveChatMessages()
        live_messages = live_message.list(
            liveChatId=live_chat_id, part="snippet,authorDetails", pageToken=None
        )
        response = LiveChatMessageListResponse(**live_messages.execute())

        chat_history = ""
        for item in response.items:
            name = item.author_details.display_name
            message = item.snippet.display_message
            chat_history += f"{name}: {message}\n"
        return chat_history


def main() -> None:
    youtube_stream = YoutubeStream(url="https://www.youtube.com/watch?v=AiuBogDGqYE")
    message = youtube_stream.get_chat_messages()
    response = youtube_stream.get_oai_response(message=message)
    youtube_stream.reply_to_chat(message=response)


if __name__ == "__main__":
    main()
