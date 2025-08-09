from openai import OpenAI

from youtubechatbot import YoutubeStream


def main(url: str = "https://www.youtube.com/watch?v=wksD4rYTxLg") -> None:
    yt = YoutubeStream(url=url)
    message = yt.get_chat_messages()
    client = OpenAI()
    response = client.chat.completions.create(
        messages=[
            {"role": "user", "content": f"Here is all chat history:\n{message}"},
            {"role": "user", "content": "你是 Mai 的助理 請代替他參與聊天"},
        ],
        model="gpt-4.1",
    )
    yt.reply_to_chat(message=response.choices[0].message.content)


if __name__ == "__main__":
    main()
