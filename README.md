# Kanzyou-Bunseki

Azure AI Language(旧 Text Analytics)の感情分析APIを試すためのお試しリポジトリ。

`reviews.json` に書いたテキストをまとめてAPIに投げ、結果を **Excel(.xlsx)** に書き出します。100件以上でも一覧で確認しやすいよう、ドキュメント単位・文単位・オピニオンマイニングの3シートに分けて出力します。

## 構成

| ファイル | 役割 |
| --- | --- |
| `sentiment.py` | 感情分析+オピニオンマイニングを実行し、結果を Excel に書き出す |
| `reviews.json` | 解析対象テキスト(言語とレビュー配列) |
| `output/` | 解析結果の Excel ファイル出力先(自動生成、`.gitignore` 済み) |
| `requirements.txt` | Python依存パッケージ |
| `.env.example` | 環境変数のテンプレート |

## 前提

- Python 3.12+
- Azure サブスクリプション(Free tier F0 でOK)

## セットアップ

### 1. Azure リソースを作成

Azure Portal で **Language service** リソースを作成 → 「キーとエンドポイント」からキーとエンドポイントURLを控える。

### 2. venv と依存パッケージ

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 3. .env を作成

```powershell
Copy-Item .env.example .env
```

`.env` を編集してキーとエンドポイントを設定:

```
AZURE_LANGUAGE_ENDPOINT=https://<your-resource-name>.cognitiveservices.azure.com/
AZURE_LANGUAGE_KEY=<your-key>
```

`.env` は `.gitignore` 済み。

## 使い方

`reviews.json` に解析したいテキストを書いて、`sentiment.py` を実行するだけ。

```powershell
.\.venv\Scripts\python.exe sentiment.py
```

実行すると `output/sentiment_<timestamp>.xlsx` が生成されます。コンソールには件数の内訳サマリだけ出ます。

### Excel の構成

| シート | 内容 |
| --- | --- |
| `summary` | 1行=1レビュー。全体の感情・positive/neutral/negative スコア・文の数・オピニオン数 |
| `sentences` | 1行=1文。文ごとの感情とスコア |
| `opinions` | 1行=対象語+評価語のペア。オピニオンマイニング結果(例:「コーヒー→最高」) |

感情のセルは色分け(positive=緑/negative=赤/mixed=黄/neutral=灰)してあるので、ざっと眺めて気になる行だけ深掘れます。

### reviews.json の編集

```json
{
  "language": "ja",
  "reviews": [
    "このカフェのコーヒーは香りがよくて最高でした。",
    "新しいスマートフォンはバッテリー持ちが悪い。"
  ]
}
```

`reviews` 配列に文字列を追加・差し替えれば、そのまま解析対象が変わります。`language` を `"en"` にすれば英語モード。

## 参考

- [Azure AI Language - Sentiment analysis 公式ドキュメント](https://learn.microsoft.com/azure/ai-services/language-service/sentiment-opinion-mining/overview)
