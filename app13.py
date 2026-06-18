import streamlit as st
import streamlit.components.v1 as components
import os
import json

st.set_page_config(
    page_title="太鼓の達人風 Streamlitアプリ",
    layout="centered"
)

st.title("🥁 太鼓の達人風ミニゲーム")
st.write("サイドバーから曲を切り替えると、譜面が自動でパッと切り替わります！")

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

# 2. サイドバーで曲を選択
st.sidebar.header("🎵 楽曲選択")
song_options = {data["title"]: key for key, data in songs_data.items()}
selected_title = st.sidebar.selectbox("プレイする曲を選んでください", list(song_options.keys()))
selected_key = song_options[selected_title]

# 3. HTMLファイルの読み込みとデータ更新
if os.path.exists(html_path):
    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    
    # 選択された曲のデータと、現在の識別キーをHTMLの中に埋め込む
    chart_json = json.dumps(songs_data[selected_key]["chart"])
    
    # JavaScript側に現在の曲を強制認識させるスクリプトを注入
    injected_script = f"""
    <script>
        window.CURRENT_SONG_KEY = "{selected_key}";
        window.PYTHON_CHART_DATA = {chart_json};
    </script>
    """
    game_html = html_content.replace("<body>", f"<body>{injected_script}")
    
    # エラーを引き起こす key 引数を使わずに表示
    components.html(game_html, height=340)
else:
    st.error("index.html が見つかりません。")
