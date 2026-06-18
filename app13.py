import streamlit as st
import time

st.set_page_config(
    page_title="太鼓の達人風アプリ",
    layout="centered"
)

st.title("🥁 太鼓の達人風・リズム叩きゲーム")
st.write("Pythonだけで構築した安全・確実版です。下の大きなボタンを押して叩いてください！")

# --- ゲーム状態の管理（StreamlitのSessionStateを使用） ---
if "score" not in st.session_state:
    st.session_state.score = 0
if "combo" not in st.session_state:
    st.session_state.combo = 0
if "max_combo" not in st.session_state:
    st.session_state.max_combo = 0
if "perfects" not in st.session_state:
    st.session_state.perfects = 0
if "misses" not in st.session_state:
    st.session_state.misses = 0
if "current_target" not in st.session_state:
    st.session_state.current_target = "ドン（赤）" # 最初のターゲット
if "last_judgment" not in st.session_state:
    st.session_state.last_judgment = "ボタンを押してスタート！"

# --- 叩いたときの判定ロジック ---
def hit_drum(player_input):
    if player_input == st.session_state.current_target:
        st.session_state.score += 100
        st.session_state.combo += 1
        st.session_state.perfects += 1
        st.session_state.last_judgment = "良 (Perfect! 🎉)"
        if st.session_state.combo > st.session_state.max_combo:
            st.session_state.max_combo = st.session_state.combo
    else:
        st.session_state.combo = 0
        st.session_state.misses += 1
        st.session_state.last_judgment = "不可 (Miss 😢)"
    
    # 次のノーツをランダムで決定（本物の譜面のように展開）
    import random
    st.session_state.current_target = random.choice(["ドン（赤）", "カッ（青）"])

# --- リセット機能 ---
def reset_game():
    st.session_state.score = 0
    st.session_state.combo = 0
    st.session_state.max_combo = 0
    st.session_state.perfects = 0
    st.session_state.misses = 0
    st.session_state.current_target = "ドン（赤）"
    st.session_state.last_judgment = "新しく演奏を開始しました！"

# --- サイドバーの設定 ---
st.sidebar.header("📊 プレイデータ")
st.sidebar.metric("最大コンボ数", f"{st.session_state.max_combo} 回")
st.sidebar.metric("「良」の数", f"{st.session_state.perfects} 打")
st.sidebar.metric("「不可」の数", f"{st.session_state.misses} 打")
if st.sidebar.button("スコアをリセットして最初から", on_click=reset_game):
    pass

# --- メイン画面のビジュアル表示 ---
# 現在叩くべきターゲットを大きく目立たせる演出
st.markdown("### 👇 次に流れてくる音符はこれだ！")

if st.session_state.current_target == "ドン（赤）":
    st.markdown(
        "<h1 style='text-align: center; color: white; background-color: #ff4757; padding: 30px; border-radius: 50px; font-size: 50px; box-shadow: 0 10px #cc2e2e;'>🔴 ドン 🔴</h1>", 
        unsafe_allow_html=True
    )
else:
    st.markdown(
        "<h1 style='text-align: center; color: white; background-color: #1e90ff; padding: 30px; border-radius: 50px; font-size: 50px; box-shadow: 0 10px #1070cc;'>🔵 カッ 🔵</h1>", 
        unsafe_allow_html=True
    )

st.write("")

# リアルタイム判定メッセージの表示
if "良" in st.session_state.last_judgment:
    st.markdown(f"<p style='font-size: 24px; font-weight: bold; color: #fffa65; text-align: center;'>{st.session_state.last_judgment}</p>", unsafe_allow_html=True)
else:
    st.markdown(f"<p style='font-size: 24px; font-weight: bold; color: #ff4d4d; text-align: center;'>{st.session_state.last_judgment}</p>", unsafe_allow_html=True)

# スコアと現在のコンボ表示
col1, col2 = st.columns(2)
with col1:
    st.subheader(f"🏆 スコア: {st.session_state.score}")
with col2:
    st.subheader(f"🔥 現在: {st.session_state.combo} コンボ")

st.write("---")
st.write("【操作】画面に表示された色に合わせて、タイミングよく下の正しいボタンを連打してください！")

# --- プレイヤーが叩くための巨大な和太鼓ボタン ---
btn_col1, btn_col2 = st.columns(2)

with btn_col1:
    if st.button("🔴 ドンを叩く（面）", use_container_width=True, type="primary"):
        hit_drum("ドン（赤）")
        st.rerun()

with btn_col2:
    if st.button("🔵 カッを叩く（フチ）", use_container_width=True):
        hit_drum("カッ（青）")
        st.rerun()
