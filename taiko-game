import streamlit as st
import streamlit.components.v1 as components

# ページの設定
st.set_page_config(
    page_title="太鼓の達人風 Streamlitアプリ",
    layout="centered"
)

# Streamlitのタイトルと説明文
st.title("🥁 太鼓の達人風ミニゲーム")
st.write("Streamlit上で動くリズムゲームです。画面をクリックして開始してください。")

# 埋め込むHTML/JavaScriptコード
game_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body {
            background-color: #111;
            color: #fff;
            font-family: 'Helvetica Neue', Arial, sans-serif;
            text-align: center;
            margin: 0;
            padding: 10px;
            overflow: hidden;
        }
        #gameContainer { position: relative; width: 100%; max-width: 800px; margin: 0 auto; }
        canvas {
            background-color: #222;
            border: 3px solid #ff4b4b;
            border-radius: 8px;
            width: 100%;
            height: auto;
        }
        #instructions { margin-top: 10px; font-size: 14px; color: #aaa; line-height: 1.6; }
        .key { background: #444; padding: 2px 6px; border-radius: 4px; border: 1px solid #666; color: #fff; }
    </style>
</head>
<body>
    <div id="gameContainer">
        <canvas id="gameCanvas" width="800" height="200"></canvas>
    </div>
    <div id="instructions">
        【操作方法】<br>
        <span class="key">F</span> または <span class="key">J</span> : <strong>ドン（面・赤）</strong> / 
        <span class="key">D</span> または <span class="key">K</span> : <strong>カッ（フチ・青）</strong><br>
        ※ ゲームが動かない場合は、一度ゲーム画面（Canvas内）をクリックしてください。
    </div>

    <script>
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');

        let score = 0, combo = 0, maxCombo = 0, currentFrame = 0, judgmentTimer = 0;
        let gameActive = false, lastJudgment = "";
        let notes = [];
        
        const TARGET_X = 150, TARGET_Y = 100, TARGET_RADIUS = 30, NOTE_SPEED = 5;

        // 譜面データ
        const chartData = [
            { frame: 80, type: 'don' }, { frame: 120, type: 'don' }, { frame: 160, type: 'ka' },
            { frame: 200, type: 'don' }, { frame: 240, type: 'ka' }, { frame: 260, type: 'ka' },
            { frame: 300, type: 'don' }, { frame: 320, type: 'don' }, { frame: 340, type: 'don' },
            { frame: 380, type: 'ka' }, { frame: 420, type: 'don' }, { frame: 440, type: 'ka' },
            { frame: 460, type: 'don' }, { frame: 520, type: 'don' }, { frame: 540, type: 'don' },
            { frame: 560, type: 'ka' }, { frame: 580, type: 'ka' }, { frame: 620, type: 'don' }
        ];

        function initGame() {
            score = 0; combo = 0; maxCombo = 0; currentFrame = 0;
            notes = []; lastJudgment = ""; gameActive = true;
        }

        window.addEventListener('keydown', (e) => {
            if (!gameActive) return;
            let inputType = "";
            if (e.key === 'f' || e.key === 'j' || e.key === 'F' || e.key === 'J') inputType = "don";
            else if (e.key === 'd' || e.key === 'k' || e.key === 'D' || e.key === 'K') inputType = "ka";
            if (inputType !== "") checkHit(inputType);
        });

        canvas.addEventListener('click', () => { if (!gameActive) initGame(); });

        function checkHit(type) {
            if (notes.length === 0) return;
            let closestNote = notes[0];
            let distance = Math.abs(closestNote.x - TARGET_X);

            if (distance < 50) {
                if (closestNote.type === type) {
                    if (distance <= 15) { lastJudgment = "良 (Perfect!)"; score += 100; combo++; }
                    else { lastJudgment = "可 (Good)"; score += 50; combo++; }
                    if (combo > maxCombo) maxCombo = combo;
                } else { lastJudgment = "不可 (Miss)"; combo = 0; }
                judgmentTimer = 30;
                notes.shift();
            }
        }

        function gameLoop() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            ctx.fillStyle = '#333';
            ctx.fillRect(0, 50, canvas.width, 100);

            ctx.beginPath();
            ctx.arc(TARGET_X, TARGET_Y, TARGET_RADIUS, 0, Math.PI * 2);
            ctx.strokeStyle = '#666';
            ctx.lineWidth = 4;
            ctx.stroke();

            if (gameActive) {
                currentFrame++;
                chartData.forEach(item => {
                    if (item.frame === currentFrame) notes.push({ x: canvas.width + 20, type: item.type });
                });

                for (let i = notes.length - 1; i >= 0; i--) {
                    notes[i].x -= NOTE_SPEED;
                    ctx.beginPath();
                    ctx.arc(notes[i].x, TARGET_Y, TARGET_RADIUS - 5, 0, Math.PI * 2);
                    ctx.fillStyle = notes[i].type === 'don' ? '#ff4757' : '#1e90ff';
                    ctx.fill();
                    ctx.strokeStyle = '#fff';
                    ctx.lineWidth = 2;
                    ctx.stroke();

                    if (notes[i].x < TARGET_X - 60) {
                        notes.splice(i, 1);
                        lastJudgment = "不可 (Miss)";
                        combo = 0;
                        judgmentTimer = 30;
                    }
                }

                const lastItem = chartData[chartData.length - 1];
                if (currentFrame > lastItem.frame + 100 && notes.length === 0) gameActive = false;
            }

            ctx.fillStyle = '#fff';
            ctx.font = 'bold 18px Arial';
            ctx.fillText(`スコア: ${score}`, 20, 35);
            ctx.fillText(`最大コンボ: ${maxCombo}`, 200, 35);

            if (combo > 0) {
                ctx.fillStyle = '#ffa500';
                ctx.font = 'italic bold 24px Arial';
                ctx.fillText(`${combo} コンボ`, TARGET_X - 40, TARGET_Y - 45);
            }

            if (judgmentTimer > 0) {
                ctx.font = 'bold 20px Arial';
                ctx.fillStyle = lastJudgment.includes('良') ? '#fffa65' : (lastJudgment.includes('可') ? '#fff' : '#ff4d4d');
                ctx.fillText(lastJudgment, TARGET_X - 40, TARGET_Y + 65);
                judgmentTimer--;
            }

            if (!gameActive) {
                ctx.fillStyle = 'rgba(0, 0, 0, 0.8)';
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                ctx.fillStyle = '#fff';
                ctx.font = 'bold 24px Arial';
                ctx.textAlign = 'center';
                if (currentFrame === 0) {
                    ctx.fillText('クリックしてゲームスタート！', canvas.width / 2, canvas.height / 2 + 10);
                } else {
                    ctx.fillText('ゲーム終了！', canvas.width / 2, canvas.height / 2 - 20);
                    ctx.font = '20px Arial';
                    ctx.fillText(`最終スコア: ${score}  /  最大コンボ: ${maxCombo}`, canvas.width / 2, canvas.height / 2 + 20);
                }
                ctx.textAlign = 'left';
            }
            requestAnimationFrame(gameLoop);
        }
        gameLoop();
    </script>
</body>
</html>
"""

# Streamlit上にHTMLコンポーネントとしてレンダリング (高さを320pxに指定)
components.html(game_html, height=320)

# サイドバーにちょっとしたおまけ機能（Streamlitらしさ）
st.sidebar.header("📊 ゲーム設定（サンプル）")
difficulty = st.sidebar.selectbox("難易度選択 (見た目のみ)", ["かんたん", "ふつう", "むずかしい", "おに"])
st.sidebar.info(f"現在は「{difficulty}」が選択されています。Streamlitのボタン等とゲームの連動も可能です。")
