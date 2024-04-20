import yaml
import anthropic
import os
from dotenv import load_dotenv
from graphviz import Digraph  # graphvizモジュールをインポート

load_dotenv()  # .envファイルから環境変数を読み込む

anthropic.api_key = os.getenv("ANTHROPIC_API_KEY")  # 環境変数からAPI keyを取得

def generate_syllabus(transcript):
    """
    文字起こし情報からカリキュラムを作成する関数
    
    Args:
        transcript (str): 文字起こし情報
        
    Returns:
        str: カリキュラム
    """
    client = anthropic.Anthropic(api_key=anthropic.api_key)
    
    prompt = f"""
    以下の文字起こし情報からカリキュラムを作成してください。
    カリキュラムはyaml形式で出力してください。
    文字起こし情報:
    {transcript}
    
    以下を例として（週はweek、月はmonth、年はyearなど考えて記述）
    - week: 1
     topics:
     - 
     lectures:
       - title: （複数）
       description: |
    - week: 2
     topics:
     - 
     lectures:
       - title: （複数）
       description: |
         
    """
    
    response = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=4000,
        temperature=0.5,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ]
    )
    
    syllabus_yaml = response.content[0].text.strip()
    syllabus_yaml = syllabus_yaml.replace("```yaml", "").replace("```", "")
    return syllabus_yaml

def generate_syllabus_ja(syllabus_yaml):
    """
    カリキュラムを日本語訳する
    """
    client = anthropic.Anthropic(api_key=anthropic.api_key)
    
    prompt = f"""
    以下のカリキュラムを忠実に日本語に訳してください。
    ただしキーは訳さずに原文のままにしてください。
    カリキュラムはyaml形式で出力してください。
    カリキュラム:
    {syllabus_yaml}
    """
    
    response = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=4000,
        temperature=0.7,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ]
    )
    
    syllabus_yaml_ja = response.content[0].text.strip()
    syllabus_yaml_ja = syllabus_yaml_ja.replace("```yaml", "").replace("```", "")
    return syllabus_yaml_ja

def generate_syllabus_graph():
    """
    syllabusの内容からグラフを生成する関数
    
    Args:
        syllabus (dict): syllabusの内容が入った辞書
        
    Returns:
        None
    """
    client = anthropic.Anthropic(api_key=anthropic.api_key)

    with open("./syllabus.yaml", "r") as file:
        syllabus_en = file.read()
    with open("./syllabus_ja.yaml", "r") as file:
        syllabus_ja = file.read()

    prompt = f"""
    syllabus_en:
    {syllabus_en}
    syllabus_ja:
    {syllabus_ja}

    上記の日英それぞれのシラバスから、
    以下のPythonコードを生成してください。

    以下の「週」に関してはyamlファイルを見て適宜変える、月、年、カテゴリーとか
    以下の処理を英語版・日本語版それぞれに対して行ってください。
    # syllabus.yaml, syllabus_ja.yaml からそれぞれデータ読み込み
    # syllabusデータの作成 （型：リスト[dict]）
    # Graphvizを使ってグラフを作成。コメントに'Syllabus Graph'を指定。
    # 週のボックスノードと講義サブボックスの作成
    # syllabusデータの各週について繰り返し処理
    # 週のインデックスを取得
    # 週の講義を取得し、カンマ区切りの文字列に変換
    # 週のノード名を作成（例: "Week 1\nIntroduction to Human-Canine Bonding"）
    # 週のノードを作成。ボックス形状、塗りつぶし、水色の背景色を指定。
    # 週ごとのサブグラフを作成
    # 講義をリストアップし、改行区切りの文字列に変換
    # サブグラフ内に講義一覧のノードを作成。ボックス形状、ラベルに講義一覧を指定。
    # 週のノードと講義一覧のノードを破線で接続
    # 週ボックスノードの下部（south）からエッジを始め、headport='sw'はサブグラフの左下（south-west）にエッジを接続するように指定
    # 週ごとの矢印の接続
    # syllabusデータの週の数-1回繰り返し処理
    # 現在の週のデータを取得
    # 次の週のデータを取得
    # 現在の週のノード名を作成
    # 次の週のノード名を作成
    # 現在の週のノードと次の週のノードを矢印で接続
    # グラフの保存と表示
    # グラフを'syllabus_graph_en.png', 'syllabus_graph_ja.png' という名前で保存する

    pythonのコードブロックのみ出力。その他説明は書かないこと。
    """
    
    response = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=4000,
        temperature=0.7,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ]
    )
    
    code = response.content[0].text.strip()
    
    code = code.replace("```python", "").replace("```", "")
    with open("generate_syllabus_graph.py", "w") as f:
        f.write(code)

    # codeを実行するコードを追記
    exec(code)
    
    
# from generate_syllabus_graph import generate_syllabus_graph

# 使用例
from tqdm import tqdm
import time

steps = [
    "📜 文字起こしデータの読み込み",
    "📝 シラバスの生成",
    "💾 シラバスのテキストファイルへの保存", 
    "📂 ファイル名変更",
    "📊 シラバスからグラフの生成"
]

for step in tqdm(steps):
    if step == "📜 文字起こしデータの読み込み":
        with open("./transcript.txt", "r") as f:
            transcript = f.read()  # transcript.txtファイルから文字起こし情報を読み込む
        print(f"{step}完了！")
    elif step == "📝 シラバスの生成":
        syllabus_en = generate_syllabus(transcript)
        syllabus_ja = generate_syllabus_ja(syllabus_en)
        print(f"{step}完了！")
    elif step == "💾 シラバスのテキストファイルへの保存":
        with open("syllabus_en.txt", "w") as f:
            f.write(syllabus_en)
        with open("syllabus_ja.txt", "w") as f:
            f.write(syllabus_ja)
        print(f"{step}完了!")
    elif step == "📂 ファイル名変更":
        os.rename("syllabus_en.txt", "syllabus.yaml")
        os.rename("syllabus_ja.txt", "syllabus_ja.yaml")
        print(f"{step}完了!")
    elif step == "📊 シラバスからグラフの生成":
        generate_syllabus_graph()
        print(f"{step}完了！")
    time.sleep(0.5)

print("✏️ シラバスの内容は syllabus.yaml を書き換えることで、ご自身の求めている形に変更できます。")
print("📜 syllabus.yamlのリンク: ./syllabus.yaml")
