import streamlit as st
import streamlit.components.v1 as components
import os

# ページの設定
st.set_page_config(
    page_title="太鼓の達人風 Streamlitアプリ",
    layout="centered"
)

st.title("🥁 太鼓の達人風ミニゲーム")
st.write("140ノーツ超えのロング譜面を搭載しました！フルコンボを目指しましょう。")

# 同一階層にある index.html を読み込む
html_path = os.path.join(os.path.dirname(__file__), "index.html")

if os.path.exists(html_path):
    with open(html_path, "r", encoding="utf-8") as f:
        game_html = f.read()
    
    # Streamlit上にHTMLを表示
    components.html(game_html, height=320)
else:
    st.error("index.html が見つかりません。同じリポジトリ内に配置してください。")

# サイドバー機能
st.sidebar.header("📊 ゲーム設定")
st.sidebar.info("「おに」レベルの140ノーツ譜面がロードされています。")
