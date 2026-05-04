# Kanzyou-Bunseki

Azure AI Language(旧 Text Analytics)の感情分析APIを試すためのお試しリポジトリ。

## 構成

| ファイル | 役割 |
| --- | --- |
| `sentiment.py` | 感情分析+オピニオンマイニングを実行 |
| `reviews.json` | 解析対象テキスト(言語とレビュー配列) |
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

各レビューについて、全体の感情(positive/neutral/negative/mixed)、文単位の感情、オピニオンマイニング(対象語と評価語)が出力されます。

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
