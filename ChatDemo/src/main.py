# main.py

import streamlit as st
import os
from dotenv import load_dotenv
from document_loader import load_document
from chatbot import create_chatbot, get_response
from config import OPENAI_MODEL

# 環境変数を読み込む
load_dotenv()

# OpenAI APIキーを環境変数から取得
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    st.error("OpenAI APIキーが設定されていません。.envファイルまたは環境変数を確認してください。")
    st.stop()

st.set_page_config(page_title="社内FAQ AIチャットボット", page_icon=":robot_face:", layout="wide")

# CSSでUIをカスタマイズ
st.markdown("""
<style>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');

.stApp {
    max-width: 1200px;
    margin: 0 auto;
}
.chat-message {
    padding: 1.5rem;
    border-radius: 0.5rem;
    margin-bottom: 1rem;
    display: flex;
    align-items: flex-start;
}
.chat-message.user {
    justify-content: flex-end;
}
.chat-message.bot {
    justify-content: flex-start;
}
.chat-message .avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-right: 1rem;
    font-size: 20px;
}
.chat-message.user .avatar {
    background-color: #3498db;
    color: white;
    margin-left: 1rem;
    margin-right: 0;
    order: 1;
}
.chat-message.bot .avatar {
    background-color: #2ecc71;
    color: white;
}
.chat-message .content {
    max-width: 80%;
    padding: 1rem;
    border-radius: 0.5rem;
}
.chat-message.user .content {
    background-color: #3498db;
    color: white;
    text-align: right;
}
.chat-message.bot .content {
    background-color: white;
    color: black;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}
/* サイドバーのスタイル調整 */
.css-1d391kg {
    padding-top: 1rem;
    padding-right: 1rem;
    padding-left: 1rem;
}
.css-1d391kg .block-container {
    padding-top: 1rem;
}
/* ファイルアップローダーのスタイル調整 */
.stFileUploader {
    padding-bottom: 1rem;
}
</style>
""", unsafe_allow_html=True)

# 状態の初期化 (変更なし)
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'chatbot' not in st.session_state:
    st.session_state.chatbot = None
if 'user_input' not in st.session_state:
    st.session_state.user_input = ""
if 'last_user_input' not in st.session_state:
    st.session_state.last_user_input = ""

# サイドバー (変更なし)
with st.sidebar:
    st.markdown("<h1 style='font-size: 1.5em;'>社内FAQ AIチャットボット</h1>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("FAQファイルをアップロード (PDF or DOCX)", type=["pdf", "docx"])

    if uploaded_file and st.session_state.chatbot is None:
        with st.spinner("FAQファイルを処理中..."):
            st.session_state.chatbot = create_chatbot(uploaded_file, api_key, OPENAI_MODEL)
        st.success("FAQファイルが正常にアップロードされました。")

# メインコンテンツ
for message in st.session_state.messages:
    with st.container():
        st.markdown(f"""
        <div class="chat-message {message['role']}">
            <div class="avatar">
                <i class="fas fa-{'user' if message['role'] == 'user' else 'robot'}"></i>
            </div>
            <div class="content">
                {message['content']}
            </div>
        </div>
        """, unsafe_allow_html=True)

if st.session_state.chatbot:
    user_input = st.text_input("メッセージを入力してください...", key="user_input_widget", value=st.session_state.user_input)

    if user_input and user_input != st.session_state.last_user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.spinner("回答を生成中..."):
            response = get_response(st.session_state.chatbot, user_input, 
                                    [(msg['role'], msg['content']) for msg in st.session_state.messages if msg['role'] == 'user'])
        st.session_state.messages.append({"role": "bot", "content": response})
        st.session_state.user_input = ""  # 入力欄をクリア
        st.session_state.last_user_input = user_input  # 最後のユーザー入力を更新
        st.experimental_rerun()
else:
    st.info("FAQファイルをアップロードしてチャットを開始してください。")

# チャット履歴をクリアするボタン (変更なし)
if st.button("チャット履歴をクリア"):
    st.session_state.messages = []
    st.session_state.user_input = ""
    st.session_state.last_user_input = ""
    st.experimental_rerun()

# 入力欄をクリアするための追加のチェック (変更なし)
if st.session_state.user_input:
    st.session_state.user_input = ""
    st.experimental_rerun()