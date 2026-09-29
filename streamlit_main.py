import streamlit as st
import openai
import os

def load_knowledge(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

st.title("商談Next Action支援AIエージェント PoC")
st.write("""
商談メモ（テキスト）を入力すると、TODO/NextAction抽出、関連ナレッジ提示、
フォローアップメール案を自動生成します。
""")

memo_input = st.text_area("商談メモ入力", height=200, placeholder="例: 本日A社とミーティング。B製品の詳細資料要望...etc")
submit = st.button("分析実行")

past_knowledge = load_knowledge("past_proposals.md")

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error(".env または環境変数に OPENAI_API_KEY をセットしてください。")
    st.stop()

# 新しいOpenAIクライアント(API v1.0+)
client = openai.OpenAI(api_key=api_key)

if submit and memo_input:
    with st.spinner("AIが分析しています..."):
        # 1. TODO抽出
        todo_prompt = f"""
あなたは営業支援AIです。以下の商談メモから具体的にやるべきTODO、Next Actionを日本語でリストアップしてください。

--- 商談メモ ---
{memo_input}
---
箇条書きリスト:
"""
        # 1. TODO抽出（新APIに対応）
        todo_resp = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": todo_prompt}]
        )
        todo_list = todo_resp.choices[0].message.content
        
        # 2. ナレッジRAG
        rag_prompt = f"""
次に、下記商談メモと、事例ナレッジ(--- Knowledge ---以降)をもとに、
商談内容に特に関係しそうな知見を2点、日本語で簡潔に要約して出してください。
--- 商談メモ ---
{memo_input}
--- Knowledge ---
{past_knowledge}
---
関連ありそうな知見:
"""
        rag_resp = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": rag_prompt}]
        )
        related_knowledge = rag_resp.choices[0].message.content

        # 3. メール生成
        mail_prompt = f"""
あなたはビジネスメールを作るAIです。
以下の商談メモに基づき、顧客への丁寧なフォローアップメール文の文案を作ってください。
顧客名や要望点も反映してください。日本語で。

--- 商談メモ ---
{memo_input}
---
メール文案:
"""
        mail_resp = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": mail_prompt}]
        )
        mail_draft = mail_resp.choices[0].message.content

    st.subheader("1. TODO/Next Actionリスト")
    st.write(todo_list)

    st.subheader("2. 関連ナレッジ・過去提案の要点")
    st.write(related_knowledge)

    st.subheader("3. フォローアップメール文案")
    st.write(mail_draft)
