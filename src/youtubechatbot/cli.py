import time
from typing import Any
from urllib.parse import urlparse

import dotenv
from pydantic import Field, computed_field
from rich.console import Console
from pydantic_settings import BaseSettings
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from openai import OpenAI

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

    def get_chat_id(self) -> str:
        youtube = build(
            serviceName="youtube", version="v3", developerKey=self.youtube_data_api_key
        )
        response = youtube.videos().list(part="liveStreamingDetails", id=self.video_id).execute()
        chat_id: str = response["items"][0]["liveStreamingDetails"]["activeLiveChatId"]
        return chat_id

    def get_chat_messages(self) -> None:
        live_chat_id = self.get_chat_id()
        youtube = build(
            serviceName="youtube", version="v3", developerKey=self.youtube_data_api_key
        )
        next_token = None
        while True:
            live_messages = youtube.liveChatMessages().list(
                liveChatId=live_chat_id, part="snippet,authorDetails", pageToken=next_token
            )
            response: dict[str, dict[str, Any]] = live_messages.execute()

            for item in response["items"]:
                author = item["authorDetails"]["displayName"]
                message = item["snippet"]["displayMessage"]
                if isinstance(author, str) and isinstance(message, str):
                    console.print(f"{author}: {message}")

            next_token = response.get("nextPageToken")
            time.sleep(2000)

    def reply_to_chat(self, message: str) -> None:
        live_chat_id = self.get_chat_id()
        flow = InstalledAppFlow.from_client_secrets_file(
            client_secrets_file="./data/client_secret.json",
            scopes=["https://www.googleapis.com/auth/youtube.force-ssl"],
        )
        credentials = flow.run_local_server(port=8080, open_browser=True)

        youtube = build(serviceName="youtube", version="v3", credentials=credentials)

        youtube.liveChatMessages().insert(
            part="snippet",
            body={
                "snippet": {
                    "liveChatId": live_chat_id,
                    "type": "textMessageEvent",
                    "textMessageDetails": {"messageText": message},
                }
            },
        ).execute()


def main() -> None:
    youtube_stream = YoutubeStream(url="https://www.youtube.com/watch?v=ZcwMYFBNqd8")
    youtube_stream.reply_to_chat("潮主播是0")


if __name__ == "__main__":
    main()
