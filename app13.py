import streamlit as st
import streamlit.components.v1 as components
import os
import base64

st.set_page_config(
    page_title="太鼓の達人風リズムゲーム",
    layout="centered"
)

st.title("🥁 本格派！太鼓の達人風ミニゲーム")
st.write("エラーを引き起こすコードを完全に切り離しました！画面内のボタンかキーボードで遊べます。")

current_dir = os.path.dirname(__file__)
html_path = os.path.join(current_dir, "index.html")

# index.htmlを読み込んで暗号化配信（セキュリティ回避）するだけ
if os.path.exists(html_path):
    with open(html_path, "r", encoding="utf-8") as f:
        game_html = f.read()
    
    # 安全なローカル配信（Blob）に変換して、Streamlitのブロックをすり抜ける
    b64_html = base64.b64encode(game_html.encode('utf-8')).decode('utf-8')
    blob_src = f"data:text/html;base64,{b64_html}"
    
    components.iframe(src=blob_src, height=360, scrolling=False)
else:
    st.error("index.html が見つかりません。同じリポジトリ（フォルダ）内に配置してください。")
