import os
import re
import json
import stanza
import pandas as pd
from tqdm import tqdm
from dotenv import load_dotenv
import anthropic

load_dotenv()  # .envファイルから環境変数を読み込む

class WordListGenerator:
    def __init__(self):
        self.nlp = stanza.Pipeline('en', processors='tokenize,pos,lemma')
        self.client = anthropic.Anthropic(
            api_key=os.environ.get("ANTHROPIC_API_KEY"),  # 環境変数からAPI keyを取得。os.getenvではなくos.environ.getを使う 🔑
        )

    def get_target_files(self, book_dir):
        target_files = []
        for root, dirs, files in os.walk(book_dir):
            for file in files:
                if file.endswith(".md") and os.path.basename(root).startswith("week") and "example" not in root:
                    target_files.append(os.path.join(root, file))
        return target_files

    def analyze_text(self, text):
        doc = self.nlp(text)
        lemma_dict = {}
        for sentence in doc.sentences:
            for word in sentence.words:
                if word.upos not in ["PUNCT", "NUM", "PROPN"] and word.text.isalpha():
                    lemma = (word.lemma.lower(), word.upos)
                    lemma_dict[lemma] = lemma_dict.get(lemma, 0) + 1
        return lemma_dict

    def filter_easy_words(self, lemma_dict):
        df = pd.read_csv("data/CEFR-J.csv")
        easy_words = set(df[df['CEFR'].isin(['A1', 'A2', 'B1'])]['headword'])
        filtered_dict = {k: v for k, v in lemma_dict.items() if k[0] not in easy_words}
        return filtered_dict

    def generate_translations(self, text, lemma_list):
        prompt = f"以下の英文に出てくる単語のうち、リストにある単語の日本語訳を教えてください。\n\n英文:\n{text}\n\n単語リスト:\n{', '.join([lemma for lemma, _ in lemma_list])}\n\n単語の一般的な意味ではなく、英文に実際に出てきた意味を日本語で挙げてください。日本語訳を英語に訳したら、元の単語になるようにしてください。日本語訳はできるだけ簡潔にしてください。英文で使われている品詞と日本語訳の品詞が一致するようにしてください。\n\n出力は以下のJSON形式だけにしてください。JSON以外のものは返さないでください。\n[{{\"lemma\": \"\", \"translation\": \"\"}}]"

        response = self.client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=2000,
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

        json_text = response.content[0].text.strip()
        translations = json.loads(json_text)
        return translations

    def generate_word_list(self, input_file):
        with open(input_file, "r") as f:
            text = f.read()

        print(f"Analyzing {input_file}...")
        lemma_dict = self.analyze_text(text)
        print("Filtering easy words...")
        filtered_dict = self.filter_easy_words(lemma_dict)
        print("Generating translations...")
        translations = self.generate_translations(text, list(filtered_dict.keys()))

        output_file = os.path.join(os.path.dirname(input_file), f"words_{os.path.basename(input_file)}")
        # Create a dictionary to store lemma and count pairs
        lemma_to_count = {}
        for tr in translations:
            lemma = tr["lemma"]
            count = sum(value for key, value in filtered_dict.items() if key[0] == lemma)
            lemma_to_count[lemma] = (count, tr['translation'])

        # Sort the dictionary by count in descending order and convert to list of tuples
        sorted_lemma_counts = sorted(lemma_to_count.items(), key=lambda x: x[1][0], reverse=True)

        with open(output_file, "w") as f:
            for lemma, (count, translation) in sorted_lemma_counts:
                f.write(f"{lemma} ({count}回) - {translation}\n")

        print(f"Word list generated: {output_file}")

    def run(self):
        book_dir = "book"
        target_files = self.get_target_files(book_dir)

        for file in tqdm(target_files, desc="Generating word lists"):
            self.generate_word_list(file)

if __name__ == "__main__":
    generator = WordListGenerator()
    generator.run()
