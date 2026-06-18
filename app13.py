import streamlit as st
import streamlit.components.v1 as components
import os
import json

st.set_page_config(
    page_title="太鼓の達人風 Streamlitアプリ",
    layout="centered"
)

st.title("🥁 太鼓の達人風ミニゲーム")
st.write("曲ごとに独立した本格譜面ファイルを読み込んでプレイします！")

# 各種フォルダパスの取得
current_dir = os.path.dirname(__file__)
charts_dir = os.path.join(current_dir, "charts")
html_path = os.path.join(current_dir, "index.html")

# 選択肢となる楽曲リスト（ファイル名と対応）
song_list = {
    "千本桜 風 (おに難易度・完全書き下ろし)": "senbon.json"
}

st.sidebar.header("🎵 楽曲選択")
selected_title = st.sidebar.selectbox("プレイする曲を選んでください", list(song_list.keys()))
target_file_name = song_list[selected_title]

# chartsフォルダから選ばれた譜面ファイルを読み込む
target_json_path = os.path.join(charts_dir, target_file_name)

if os.path.exists(target_json_path):
    with open(target_json_path, "r", encoding="utf-8") as f:
        selected_chart = json.load(f)
else:
    st.error(f"譜面ファイル {target_file_name} が charts フォルダ内に見つかりません。")
    st.stop()

# HTMLファイルの読み込みとデータ埋め込み
if os.path.exists(html_path):
    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    
    chart_json = json.dumps(selected_chart)
    
    injected_script = f"""
    <script>
        window.CURRENT_SONG_KEY = "{target_file_name}";
        window.PYTHON_CHART_DATA = {chart_json};
    </script>
    """
    game_html = html_content.replace("<body>", f"<body>{injected_script}")
    
    components.html(game_html, height=340)
else:
    st.error("index.html が見つかりません。")
