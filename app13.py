import streamlit as st
import streamlit.components.v1 as components
import os
import json

st.set_page_config(
    page_title="太鼓の達人風 Streamlitアプリ",
    layout="centered"
)

st.title("🥁 太鼓の達人風ミニゲーム")
st.write("【音楽なし・超極長仕様】1曲あたり1,500ノーツ超え！演奏時間10分以上の超ロング譜面です。")

current_dir = os.path.dirname(__file__)
json_path = os.path.join(current_dir, "songs.json")
html_path = os.path.join(current_dir, "index.html")

if os.path.exists(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        songs_base = json.load(f)
else:
    st.error("songs.json が見つかりません。")
    st.stop()

st.sidebar.header("🎵 楽曲選択")
song_options = {data["title"]: key for key, data in songs_base.items()}
selected_title = st.sidebar.selectbox("プレイする曲を選んでください", list(song_options.keys()))
selected_key = song_options[selected_title]

# --- 1500ノーツ超えのマンモス譜面をPythonで自動生成 ---
generated_chart = []
pattern_type = songs_base[selected_key]["type"]

# 開始フレーム
frame = 80

# 1500ノーツに達するまでループ（約10分〜12分相当）
for i in range(1550):
    if pattern_type == "speed":
        # 千本桜風：高速でシンプルな連打が延々と続く（体力譜面）
        frame += 10 if i % 8 == 0 else 8
        note_type = "don" if i % 3 != 0 else "ka"
    elif pattern_type == "technical":
        # テーゼ風：複雑なハネリズムや偶数・奇数の混ざり（技術譜面）
        if i % 4 == 0:
            frame += 16
        elif i % 4 == 1:
            frame += 8
        else:
            frame += 6
        note_type = "don" if i % 5 < 3 else "ka"
    else:
        # 紅風：24分の狂った超高速高密度ラッシュが延々と襲いかかる（最凶難易度）
        if i % 16 < 8:
            frame += 5  # 超高速地帯
        else:
            frame += 10 # 繋ぎ地帯
        note_type = "don" if (i // 4) % 2 == 0 else "ka"
        
    generated_chart.append({"frame": frame, "type": note_type})

# 3. HTMLファイルの読み込みとデータ更新
if os.path.exists(html_path):
    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    
    chart_json = json.dumps(generated_chart)
    
    injected_script = f"""
    <script>
        window.CURRENT_SONG_KEY = "{selected_key}";
        window.PYTHON_CHART_DATA = {chart_json};
    </script>
    """
    game_html = html_content.replace("<body>", f"<body>{injected_script}")
    
    components.html(game_html, height=340)
else:
    st.error("index.html が見つかりません。")
