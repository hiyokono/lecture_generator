import os
import anthropic
from tqdm import tqdm
from dotenv import load_dotenv

load_dotenv()  # .envファイルから環境変数を読み込む

def generate_wordlist():
    """
    """
    client = anthropic.Anthropic(
        api_key=os.getenv("ANTHROPIC_API_KEY"),  # 環境変数からAPI keyを取得
    )

    with open("AIdocs/単語一覧生成AI.md", "r") as f:
        book_prompt = f.read()

    with open("llms/claude.txt", "r") as f:
        claude_code = f.read()

    message = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=4000,
        temperature=0.5,
        system="",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"""

要件定義書:
{book_prompt}

上記の要件定義書をもとにして、Pythonのコードブロックのみ出力してください。

クラス内でh2は以下の関数で適宜呼び出し。

from dotenv import load_dotenv
load_dotenv()  # .envファイルから環境変数を読み込む

利用LLM:
{claude_code}
    model="claude-3-haiku-20240307",
    max_tokens=2000,
    temperature=0.5,

注意点:
- [ ] プログラムの進捗がわかるようなprintのコメントと、進捗バーを記載すること
"""
                    }
                ]
            }
        ]
    )
    return message.content[0].text



print("📚 単語一覧の生成コードを生成中...")
code = generate_wordlist()
code = code.replace("```python", "").replace("```", "")
with open("generate_wordlist.py", "w") as f:
    f.write(code)
print("✅ 単語一覧の生成コードを生成完了！")

print("📖 単語一覧の生成コードを実行中...")
# codeを実行するコードを追記
exec(code)
print("🎉 単語一覧の生成が完了しました！")
