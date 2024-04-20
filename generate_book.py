
import os
import yaml
import anthropic
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()  # .envファイルから環境変数を読み込む

# aisディレクトリがなければ作成
if not os.path.exists("ais"):
    os.makedirs("ais")

class LectureGenerator:
    def __init__(self):
        self.client = anthropic.Anthropic(
            api_key=os.environ.get("ANTHROPIC_API_KEY"),  # 環境変数からAPI keyを取得。os.getenvではなくos.environ.getを使う 🔑
        )

    def generate_lecture_content(self, lecture_title, lecture_description, syllabus):
        with open("ais/講義資料生成AI.md", "r") as f:
            lecture_content_prompt = f.read().format(lecture_title=lecture_title, lecture_description=lecture_description, syllabus=syllabus)

        response = self.client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=2000,
            temperature=0.7,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": lecture_content_prompt
                        }
                    ]
                }
            ]
        )
        
        return response.content[0].text.strip()

class QuizGenerator:
    def __init__(self):
        self.client = anthropic.Anthropic(
            api_key=os.environ.get("ANTHROPIC_API_KEY"),  # 環境変数からAPI keyを取得。os.getenvではなくos.environ.getを使う 🔑
        )

    def generate_quiz_content(self, lecture_title, lecture_description, lecture_content, syllabus):
        with open("ais/問題生成AI.md", "r") as f:
            quiz_content_prompt = f.read().format(lecture_title=lecture_title, lecture_description=lecture_description, lecture_content=lecture_content, syllabus=syllabus)

        response = self.client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=2000, 
            temperature=0.7,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": quiz_content_prompt
                        }
                    ]
                }
            ]
        )
        
        return response.content[0].text.strip()

def main():
    print("📚 書籍生成AIを開始します...")

    # syllabus.yamlを読み込む
    with open("syllabus.yaml", "r") as f:
        syllabus = yaml.safe_load(f)

    # 講義資料生成AIと問題生成AIのインスタンスを作成
    lecture_generator = LectureGenerator()
    quiz_generator = QuizGenerator()

    # 大項目ごとに処理
    for week in tqdm(syllabus["schedule"], desc="📘 大項目の処理中"):
        week_dir = f'book/week{week["week"]}'
        os.makedirs(week_dir, exist_ok=True)  # 大項目のディレクトリを作成

        # 中項目ごとに処理
        for lecture in tqdm(week["lectures"], desc=f'📝 中項目の処理中 (Week {week["week"]})', leave=False):
            lecture_file = f'{week_dir}/{lecture["title"]}.md'

            # 講義資料を生成
            lecture_content = lecture_generator.generate_lecture_content(lecture["title"], lecture["description"], syllabus)

            # 問題を生成
            quiz_content = quiz_generator.generate_quiz_content(lecture["title"], lecture["description"], lecture_content, syllabus)

            # 講義資料と問題を中項目のファイルに書き込む
            with open(lecture_file, "w") as f:
                f.write(f'# {lecture["title"]}\n\n')
                f.write(lecture_content)
                f.write("\n\n")
                f.write(quiz_content)

    print("✅ 書籍の生成が完了しました！")

if __name__ == "__main__":
    main()
