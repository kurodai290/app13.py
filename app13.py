import streamlit as st
import streamlit.components.v1 as components

# ページの設定
st.set_page_config(
    page_title="太鼓の達人風 Streamlitアプリ",
    layout="centered"
)

# Streamlitのタイトルと説明文
st.title("🥁 太鼓の達人風ミニゲーム")
st.write("140ノーツ超えのロング譜面を搭載しました！フルコンボを目指しましょう。")

# 埋め込むHTML/JavaScriptコード
game_html = """<!DOCTYPE html>
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

        // --- 140ノーツ以上の本格的なロング譜面データ ---
        const chartData = [
            { frame: 80, type: 'don' }, { frame: 100, type: 'don' }, { frame: 120, type: 'don' }, { frame: 140, type: 'don' },
            { frame: 160, type: 'don' }, { frame: 180, type: 'don' }, { frame: 200, type: 'ka' }, { frame: 220, type: 'ka' },
            { frame: 240, type: 'don' }, { frame: 260, type: 'ka' }, { frame: 280, type: 'don' }, { frame: 300, type: 'ka' },
            { frame: 320, type: 'don' }, { frame: 330, type: 'don' }, { frame: 340, type: 'don' }, { frame: 360, type: 'ka' },

            { frame: 400, type: 'don' }, { frame: 420, type: 'don' }, { frame: 440, type: 'ka' }, { frame: 460, type: 'don' },
            { frame: 480, type: 'don' }, { frame: 500, type: 'ka' }, { frame: 520, type: 'ka' }, { frame: 540, type: 'don' },
            { frame: 560, type: 'don' }, { frame: 570, type: 'don' }, { frame: 580, type: 'ka' }, { frame: 600, type: 'don' },
            { frame: 620, type: 'ka' }, { frame: 630, type: 'ka' }, { frame: 640, type: 'don' }, { frame: 660, type: 'ka' },

            { frame: 700, type: 'don' }, { frame: 710, type: 'don' }, { frame: 730, type: 'ka' },
            { frame: 750, type: 'don' }, { frame: 760, type: 'don' }, { frame: 780, type: 'ka' },
            { frame: 800, type: 'ka' }, { frame: 810, type: 'ka' }, { frame: 830, type: 'don' },
            { frame: 850, type: 'don' }, { frame: 860, type: 'ka' }, { frame: 870, type: 'don' }, { frame: 890, type: 'ka' },
            { frame: 910, type: 'don' }, { frame: 920, type: 'don' }, { frame: 930, type: 'don' }, { frame: 940, type: 'don' },
            { frame: 950, type: 'ka' }, { frame: 960, type: 'ka' }, { frame: 970, type: 'ka' }, { frame: 980, type: 'ka' },
            { frame: 1000, type: 'don' }, { frame: 1010, type: 'don' }, { frame: 1020, type: 'don' }, { frame: 1030, type: 'don' },
            { frame: 1040, type: 'ka' }, { frame: 1050, type: 'ka' }, { frame: 1060, type: 'don' }, { frame: 1080, type: 'don' },

            { frame: 1120, type: 'don' }, { frame: 1140, type: 'ka' }, { frame: 1160, type: 'don' }, { frame: 1170, type: 'don' }, { frame: 1180, type: 'ka' },
            { frame: 1200, type: 'don' }, { frame: 1220, type: 'ka' }, { frame: 1240, type: 'don' }, { frame: 1250, type: 'ka' }, { frame: 1260, type: 'don' },
            { frame: 1280, type: 'ka' }, { frame: 1300, type: 'ka' }, { frame: 1320, type: 'don' }, { frame: 1330, type: 'ka' }, { frame: 1340, type: 'don' },
            { frame: 1360, type: 'don' }, { frame: 1370, type: 'don' }, { frame: 1380, type: 'ka' }, { frame: 1400, type: 'don' },

            { frame: 1440, type: 'don' }, { frame: 1450, type: 'don' }, { frame: 1460, type: 'ka' },
            { frame: 1480, type: 'don' }, { frame: 1490, type: 'don' }, { frame: 1510, type: 'ka' }, { frame: 1520, type: 'ka' }, { frame: 1530, type: 'don' },
            { frame: 1550, type: 'don' }, { frame: 1560, type: 'ka' }, { frame: 1570, type: 'don' }, { frame: 1590, type: 'ka' },
            { frame: 1610, type: 'don' }, { frame: 1620, type: 'don' }, { frame: 1630, type: 'don' }, { frame: 1650, type: 'ka' },
            { frame: 1670, type: 'ka' }, { frame: 1680, type: 'ka' }, { frame: 1690, type: 'ka' }, { frame: 1710, type: 'don' },

            { frame: 1750, type: 'don' }, { frame: 1760, type: 'ka' }, { frame: 1770, type: 'don' },
            { frame: 1790, type: 'ka' }, { frame: 1800, type: 'don' }, { frame: 1810, type: 'ka' },
            { frame: 1830, type: 'don' }, { frame: 1840, type: 'don' }, { frame: 1850, type: 'ka' }, { frame: 1860, type: 'ka' },
            { frame: 1880, type: 'don' }, { frame: 1890, type: 'ka' }, { frame: 1900, type: 'don' }, { frame: 1910, type: 'ka' },
            { frame: 1930, type: 'don' }, { frame: 1940, type: 'don' }, { frame: 1950, type: 'don' }, { frame: 1960, type: 'don' },
            { frame: 1970, type: 'ka' }, { frame: 1980, type: 'ka' }, { frame: 1990, type: 'ka' }, { frame: 2000, type: 'ka' },

            { frame: 2040, type: 'don' }, { frame: 2050, type: 'don' }, { frame: 2060, type: 'don' }, { frame: 2070, type: 'don' },
            { frame: 2080, type: 'ka' }, { frame: 2090, type: 'ka' }, { frame: 2100, type: 'ka' }, { frame: 2110, type: 'ka' },
            { frame: 2130, type: 'don' }, { frame: 2140, type: 'ka' }, { frame: 2150, type: 'don' }, { frame: 2160, type: 'ka' },
            { frame: 2180, type: 'don' }, { frame: 2190, type: 'don' }, { frame: 2200, type: 'don' }, { frame: 2210, type: 'don' },
            { frame: 2220, type: 'ka' }, { frame: 2230, type: 'ka' }, { frame: 2240, type: 'ka' }, { frame: 2250, type: 'ka' },
            { frame: 2280, type: 'don' }, { frame: 2290, type: 'don' }, { frame: 2300, type: 'ka' }, { frame: 2310, type: 'ka' },
            { frame: 2330, type: 'don' }, { frame: 2340, type: 'ka' }, { frame: 2350, type: 'don' }, { frame: 2360, type: 'ka' },
            { frame: 2420, type: 'don' }
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
