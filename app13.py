import streamlit as st
import streamlit.components.v1 as components
import os
import json

st.set_page_config(
    page_title="太鼓の達人風 Streamlitアプリ",
    layout="centered"
)

st.title("🥁 太鼓の達人風ミニゲーム")
st.write("曲の展開に合わせた本格的な譜面です！フルコンボを目指しましょう。")

# --- 外部ファイルを無くし、Python内に直接セット（非ループの書き下ろし譜面） ---
songs_data = {
    "senbon": {
        "title": "千本桜 風 (おに難易度・完全書き下ろし)",
        "chart": [
            {"frame": 60, "type": "don"}, {"frame": 80, "type": "don"}, {"frame": 100, "type": "don"}, {"frame": 120, "type": "don"},
            {"frame": 140, "type": "ka"}, {"frame": 160, "type": "ka"}, {"frame": 180, "type": "ka"}, {"frame": 200, "type": "ka"},
            {"frame": 220, "type": "don"}, {"frame": 230, "type": "don"}, {"frame": 240, "type": "ka"}, {"frame": 260, "type": "don"},
            {"frame": 280, "type": "ka"}, {"frame": 290, "type": "ka"}, {"frame": 300, "type": "don"}, {"frame": 320, "type": "don"},
            {"frame": 340, "type": "don"}, {"frame": 360, "type": "ka"}, {"frame": 380, "type": "don"}, {"frame": 400, "type": "ka"},
            {"frame": 420, "type": "don"}, {"frame": 430, "type": "don"}, {"frame": 440, "type": "don"}, {"frame": 460, "type": "ka"},
            {"frame": 480, "type": "don"}, {"frame": 500, "type": "don"}, {"frame": 520, "type": "ka"}, {"frame": 540, "type": "ka"},
            {"frame": 560, "type": "don"}, {"frame": 570, "type": "don"}, {"frame": 580, "type": "ka"}, {"frame": 600, "type": "don"},
            {"frame": 640, "type": "don"}, {"frame": 660, "type": "ka"}, {"frame": 680, "type": "don"}, {"frame": 700, "type": "ka"},
            {"frame": 720, "type": "don"}, {"frame": 730, "type": "don"}, {"frame": 740, "type": "ka"}, {"frame": 760, "type": "don"},
            {"frame": 780, "type": "ka"}, {"frame": 790, "type": "ka"}, {"frame": 800, "type": "don"}, {"frame": 820, "type": "don"},
            {"frame": 840, "type": "ka"}, {"frame": 860, "type": "ka"}, {"frame": 880, "type": "don"}, {"frame": 900, "type": "ka"},
            {"frame": 920, "type": "don"}, {"frame": 930, "type": "don"}, {"frame": 940, "type": "ka"}, {"frame": 960, "type": "don"},
            {"frame": 980, "type": "don"}, {"frame": 990, "type": "don"}, {"frame": 1000, "type": "ka"}, {"frame": 1020, "type": "don"},
            {"frame": 1040, "type": "ka"}, {"frame": 1050, "type": "ka"}, {"frame": 1060, "type": "don"}, {"frame": 1080, "type": "ka"},
            {"frame": 1100, "type": "don"}, {"frame": 1120, "type": "don"}, {"frame": 1140, "type": "ka"}, {"frame": 1160, "type": "don"},
            {"frame": 1200, "type": "don"}, {"frame": 1210, "type": "don"}, {"frame": 1220, "type": "ka"}, {"frame": 1240, "type": "don"},
            {"frame": 1260, "type": "ka"}, {"frame": 1270, "type": "ka"}, {"frame": 1280, "type": "don"}, {"frame": 1300, "type": "don"},
            {"frame": 1320, "type": "don"}, {"frame": 1340, "type": "ka"}, {"frame": 1360, "type": "don"}, {"frame": 1380, "type": "ka"},
            {"frame": 1400, "type": "don"}, {"frame": 1410, "type": "don"}, {"frame": 1420, "type": "don"}, {"frame": 1440, "type": "ka"},
            {"frame": 1460, "type": "don"}, {"frame": 1480, "type": "don"}, {"frame": 1500, "type": "ka"}, {"frame": 1520, "type": "ka"},
            {"frame": 1540, "type": "don"}, {"frame": 1550, "type": "don"}, {"frame": 1560, "type": "ka"}, {"frame": 1580, "type": "don"},
            {"frame": 1620, "type": "don"}, {"frame": 1630, "type": "don"}, {"frame": 1640, "type": "don"}, {"frame": 1660, "type": "ka"},
            {"frame": 1680, "type": "don"}, {"frame": 1690, "type": "ka"}, {"frame": 1700, "type": "don"}, {"frame": 1720, "type": "ka"},
            {"frame": 1740, "type": "don"}, {"frame": 1750, "type": "don"}, {"frame": 1760, "type": "ka"}, {"frame": 1780, "type": "don"},
            {"frame": 1800, "type": "ka"}, {"frame": 1810, "type": "ka"}, {"frame": 1820, "type": "don"}, {"frame": 1840, "type": "don"},
            {"frame": 1860, "type": "don"}, {"frame": 1880, "type": "ka"}, {"frame": 1900, "type": "don"}, {"frame": 1920, "type": "ka"},
            {"frame": 1940, "type": "don"}, {"frame": 1950, "type": "don"}, {"frame": 1960, "type": "don"}, {"frame": 1980, "type": "ka"},
            {"frame": 2000, "type": "don"}, {"frame": 2020, "type": "don"}, {"frame": 2040, "type": "ka"}, {"frame": 2060, "type": "ka"},
            {"frame": 2080, "type": "don"}, {"frame": 2090, "type": "don"}, {"frame": 2100, "type": "ka"}, {"frame": 2120, "type": "don"},
            {"frame": 2160, "type": "don"}, {"frame": 2170, "type": "don"}, {"frame": 2180, "type": "don"}, {"frame": 2200, "type": "ka"},
            {"frame": 2220, "type": "don"}, {"frame": 2230, "type": "ka"}, {"frame": 2240, "type": "don"}, {"frame": 2260, "type": "ka"},
            {"frame": 2280, "type": "don"}, {"frame": 2290, "type": "don"}, {"frame": 2300, "type": "ka"}, {"frame": 2320, "type": "don"},
            {"frame": 2340, "type": "ka"}, {"frame": 2350, "type": "ka"}, {"frame": 2360, "type": "don"}, {"frame": 2380, "type": "don"},
            {"frame": 2400, "type": "don"}, {"frame": 2420, "type": "ka"}, {"frame": 2440, "type": "don"}, {"frame": 2460, "type": "ka"},
            {"frame": 2480, "type": "don"}, {"frame": 2490, "type": "don"}, {"frame": 2500, "type": "don"}, {"frame": 2520, "type": "ka"},
            {"frame": 2540, "type": "don"}, {"frame": 2560, "type": "don"}, {"frame": 2580, "type": "ka"}, {"frame": 2600, "type": "ka"},
            {"frame": 2620, "type": "don"}, {"frame": 2630, "type": "don"}, {"frame": 2640, "type": "ka"}, {"frame": 2660, "type": "don"},
            {"frame": 2700, "type": "don"}, {"frame": 2710, "type": "don"}, {"frame": 2720, "type": "don"}, {"frame": 2740, "type": "ka"},
            {"frame": 2760, "type": "don"}, {"frame": 2770, "type": "ka"}, {"frame": 2780, "type": "don"}, {"frame": 2800, "type": "ka"},
            {"frame": 2820, "type": "don"}, {"frame": 2830, "type": "don"}, {"frame": 2840, "type": "ka"}, {"frame": 2860, "type": "don"},
            {"frame": 2880, "type": "ka"}, {"frame": 2890, "type": "ka"}, {"frame": 2900, "type": "don"}, {"frame": 2920, "type": "don"},
            {"frame": 2940, "type": "don"}, {"frame": 2960, "type": "ka"}, {"frame": 2980, "type": "don"}, {"frame": 3000, "type": "ka"},
            {"frame": 3020, "type": "don"}, {"frame": 3030, "type": "don"}, {"frame": 3040, "type": "don"}, {"frame": 3060, "type": "ka"},
            {"frame": 3080, "type": "don"}, {"frame": 3100, "type": "don"}, {"frame": 3120, "type": "ka"}, {"frame": 3140, "type": "ka"},
            {"frame": 3160, "type": "don"}, {"frame": 3170, "type": "don"}, {"frame": 3180, "type": "ka"}, {"frame": 3200, "type": "don"},
            {"frame": 3240, "type": "don"}, {"frame": 3250, "type": "don"}, {"frame": 3260, "type": "don"}, {"frame": 3280, "type": "ka"},
            {"frame": 3300, "type": "don"}, {"frame": 3310, "type": "ka"}, {"frame": 3320, "type": "don"}, {"frame": 3340, "type": "ka"},
            {"frame": 3360, "type": "don"}, {"frame": 3370, "type": "don"}, {"frame": 3380, "type": "ka"}, {"frame": 3400, "type": "don"},
            {"frame": 3420, "type": "ka"}, {"frame": 3430, "type": "ka"}, {"frame": 3440, "type": "don"}, {"frame": 3460, "type": "don"},
            {"frame": 3480, "type": "don"}, {"frame": 3500, "type": "ka"}, {"frame": 3520, "type": "don"}, {"frame": 3540, "type": "ka"},
            {"frame": 3560, "type": "don"}, {"frame": 3570, "type": "don"}, {"frame": 3580, "type": "don"}, {"frame": 3600, "type": "ka"},
            {"frame": 3620, "type": "don"}, {"frame": 3640, "type": "don"}, {"frame": 3660, "type": "ka"}, {"frame": 3680, "type": "ka"},
            {"frame": 3700, "type": "don"}, {"frame": 3710, "type": "don"}, {"frame": 3720, "type": "ka"}, {"frame": 3740, "type": "don"},
            {"frame": 3800, "type": "don"}
        ]
    }
}

# サイドバーで曲を選択
st.sidebar.header("🎵 楽曲選択")
song_options = {data["title"]: key for key, data in songs_data.items()}
selected_title = st.sidebar.selectbox("プレイする曲を選んでください", list(song_options.keys()))
selected_key = song_options[selected_title]

selected_chart = songs_data[selected_key]["chart"]

current_dir = os.path.dirname(__file__)
html_path = os.path.join(current_dir, "index.html")

# 3. HTMLファイルの読み込みとデータ埋め込み
if os.path.exists(html_path):
    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    
    chart_json = json.dumps(selected_chart)
    
    # データを安全にJavaScriptへ注入
    injected_script = f"""
    <script>
        window.CURRENT_SONG_KEY = "{selected_key}";
        window.PYTHON_CHART_DATA = {chart_json};
    </script>
    """
    game_html = html_content.replace("<body>", f"<body>{injected_script}")
    
    # エラー回避のため高さを少し広げて表示
    components.html(game_html, height=360)
else:
    st.error("index.html が見つかりません。")
