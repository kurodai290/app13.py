import streamlit as st
import streamlit.components.v1 as components
import os
import json

st.set_page_config(
    page_title="太鼓の達人風 Streamlitアプリ",
    layout="centered"
)

st.title("🥁 太鼓の達人風ミニゲーム")
st.write("Streamlitのメニューから曲を切り替えて遊べます。")

# 各種ファイルのパス取得
current_dir = os.path.dirname(__file__)
json_path = os.path.join(current_dir, "songs.json")
html_path = os.path.join(current_dir, "index.html")

# 1. 譜面データの読み込み
if os.path.exists(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        songs_data = json.load(f)
else:
    st.error("songs.json が見つかりません。")
    st.stop()

# 2. Streamlitのサイドバーで曲を選択
st.sidebar.header("🎵 楽曲選択")
song_options = {data["title"]: key for key, data in songs_data.items()}
selected_title = st.sidebar.selectbox("プレイする曲を選んでください", list(song_options.keys()))
selected_key = song_options[selected_title]

# 選択された譜面データを取得
selected_chart = songs_data[selected_key]["chart"]

# 3. HTMLファイルの読み込みとデータ埋め込み
if os.path.exists(html_path):
    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    
    # HTML内の特定の目印（__CHART_DATA__）を選んだ譜面データ（JSON文字列）に置き換える
    game_html = html_content.replace("__CHART_DATA__", json.dumps(selected_chart))
    
    # 型エラーを引き起こす原因となっていた `key=` 引数を削除し、安全に表示
    components.html(game_html, height=340)
else:
    st.error("index.html が見つかりません。")
