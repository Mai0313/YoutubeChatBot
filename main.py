import time
from typing import TYPE_CHECKING, Any
from urllib.parse import urlparse

import dotenv
from pydantic import Field, computed_field
from rich.console import Console
from pydantic_settings import BaseSettings
from googleapiclient.discovery import Resource, build

if TYPE_CHECKING:
    from googleapiclient.http import HttpRequest


dotenv.load_dotenv()
console = Console()


class Config(BaseSettings):
    youtube_data_api_key: str = Field(..., validation_alias="YOUTUBE_DATA_API_KEY")
    openai_api_key: str = Field(..., validation_alias="OPENAI_API_KEY")


class YoutubeStream(Config):
    url: str

    @computed_field
    @property
    def youtube(self) -> Resource:
        youtube: Resource = build(
            serviceName="youtube", version="v3", developerKey=self.youtube_data_api_key
        )
        return youtube

    @computed_field
    @property
    def video_id(self) -> str:
        parsed_url = urlparse(url=self.url)
        video_id = parsed_url.query.split("=")[-1]
        return video_id

    def get_chat_id(self) -> str:
        video_info: HttpRequest = self.youtube.videos().list(
            part="liveStreamingDetails", id=self.video_id
        )
        response = video_info.execute()
        chat_id: str = response["items"][0]["liveStreamingDetails"]["activeLiveChatId"]
        return chat_id

    def get_live_messages(self) -> None:
        live_chat_id = self.get_chat_id()
        next_token = None
        while True:
            live_messages: HttpRequest = self.youtube.liveChatMessages().list(
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


if __name__ == "__main__":
    youtube_stream = YoutubeStream(url="https://www.youtube.com/watch?v=cE4nBa0xjgc")
    youtube_stream.get_live_messages()
