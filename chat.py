import os
import sys
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("エラー: .env に OPENAI_API_KEY が設定されていません。")
    sys.exit(1)

client = OpenAI(api_key=api_key)
messages = [
    {
        "role": "system",
        "content": "あなたは優秀なエンジニアリングアシスタントです。簡潔かつ的確に回答してください。",
    }
]

print("=== OpenAI Terminal Chat (終了: 'exit' または 'quit') ===\n")

while True:
    try:
        user_input = input("You > ").strip()
        if not user_input:
            continue
        if user_input.lower() in ["exit", "quit"]:
            print("終了します。")
            break

        messages.append({"role": "user", "content": user_input})

        print("\nAI > ", end="", flush=True)

        response_stream = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            stream=True,
        )

        full_response = ""
        for chunk in response_stream:
            content = chunk.choices[0].delta.content or ""
            print(content, end="", flush=True)
            full_response += content
        print("\n")

        messages.append({"role": "assistant", "content": full_response})

    except KeyboardInterrupt:
        print("\n終了します。")
        break
    except Exception as e:
        print(f"\nエラーが発生しました: {e}\n")
