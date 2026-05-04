import json
import os
import sys
from pathlib import Path

from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv

REVIEWS_PATH = Path(__file__).parent / "reviews.json"


def build_client() -> TextAnalyticsClient:
    load_dotenv()
    endpoint = os.environ.get("AZURE_LANGUAGE_ENDPOINT")
    key = os.environ.get("AZURE_LANGUAGE_KEY")
    if not endpoint or not key:
        sys.exit("AZURE_LANGUAGE_ENDPOINT と AZURE_LANGUAGE_KEY を .env に設定してください")
    return TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(key))


def analyze(client: TextAnalyticsClient, documents: list[str], language: str = "ja") -> None:
    response = client.analyze_sentiment(
        documents=documents,
        language=language,
        show_opinion_mining=True,
    )
    for i, doc in enumerate(response):
        print(f"\n--- Document {i + 1} ---")
        print(f"Text     : {documents[i]}")
        if doc.is_error:
            print(f"Error    : {doc.error.code} - {doc.error.message}")
            continue
        print(f"Sentiment: {doc.sentiment}")
        scores = doc.confidence_scores
        print(f"Scores   : positive={scores.positive:.3f} neutral={scores.neutral:.3f} negative={scores.negative:.3f}")
        for s_idx, sentence in enumerate(doc.sentences):
            print(f"  Sentence {s_idx + 1}: {sentence.sentiment} | {sentence.text}")
            for mined in sentence.mined_opinions:
                target = mined.target
                assessments = ", ".join(f"{a.text}({a.sentiment})" for a in mined.assessments)
                print(f"    Opinion -> target='{target.text}' ({target.sentiment}) assessments=[{assessments}]")


def load_reviews(path: Path) -> tuple[list[str], str]:
    if not path.exists():
        sys.exit(f"レビューファイルが見つかりません: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    reviews = data.get("reviews", [])
    if not reviews:
        sys.exit(f"{path} の 'reviews' が空です")
    return reviews, data.get("language", "ja")


def main() -> None:
    reviews, language = load_reviews(REVIEWS_PATH)
    client = build_client()
    analyze(client, reviews, language=language)


if __name__ == "__main__":
    main()
