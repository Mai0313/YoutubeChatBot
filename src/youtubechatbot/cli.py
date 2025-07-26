import time
import pickle
from pathlib import Path
from urllib.parse import urlparse

import dotenv
from openai import OpenAI
from pydantic import Field, computed_field
from rich.console import Console
from pydantic_settings import BaseSettings
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
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
            {"role": "user", "content": "請幫我想一句話參與聊天"},
            {"role": "user", "content": message},
        ]
        response = self.client.chat.completions.create(messages=messages, model="gpt-4.1")
        return response.choices[0].message.content

    def reply_to_chat(self, message: str) -> None:
        live_chat_id = self.get_chat_id()
        credentials = self.get_credentials()

        youtube = build(serviceName="youtube", version="v3", credentials=credentials)
        live_message = youtube.liveChatMessages()

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
        youtube = build(
            serviceName="youtube", version="v3", developerKey=self.youtube_data_api_key
        )
        video_list = youtube.videos().list(part="liveStreamingDetails", id=self.video_id)
        response = VideoListResponse(**video_list.execute())
        chat_id = response.items[0].live_streaming_details.active_live_chat_id
        return chat_id

    def get_chat_messages(self) -> None:
        live_chat_id = self.get_chat_id()
        youtube = build(
            serviceName="youtube", version="v3", developerKey=self.youtube_data_api_key
        )
        next_token = None
        live_message = youtube.liveChatMessages()
        live_messages = live_message.list(
            liveChatId=live_chat_id, part="snippet,authorDetails", pageToken=next_token
        )
        response = LiveChatMessageListResponse(**live_messages.execute())

        for item in response.items:
            name = item.author_details.display_name
            message = item.snippet.display_message
            console.print(f"{name}: {message}")


def main() -> None:
    youtube_stream = YoutubeStream(url="https://www.youtube.com/watch?v=ZcwMYFBNqd8")
    youtube_stream.get_chat_messages()


if __name__ == "__main__":
    main()
