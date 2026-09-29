# 商談支援AIエージェント（MVP/PoC）

営業担当者が商談メモを入力すると、TODO（やることリスト）・関連ナレッジ（過去事例要約）、フォローアップメール文案をAIが自動生成するアプリです。

## 起動方法

1. 必要ライブラリをインストール
    ```
    pip install streamlit openai python-dotenv
    ```
2. `.env` ファイルへ下記のようにAPIキーを記載
    ```
    OPENAI_API_KEY=sk-XXXXXXXXXXXXXXX
    ```

3. アプリを起動
    ```
    streamlit run streamlit_main.py
    ```

## 使用技術

- Python
- Streamlit
- OpenAI API
- python-dotenv
- Markdown（ナレッジファイル）

## 必要な環境変数

- `OPENAI_API_KEY`

## 動作確認方法

1. .envファイルを用意しAPIキー設定
2. Streamlitで起動
3. 商談メモ入力 → 「分析実行」 → 結果3つ（TODO・ナレッジ・メール文）を確認

## 注意
- .envなど機密情報は公開リポジトリに**含めないでください**
- サンプルナレッジファイル(past_proposals.md)入り
