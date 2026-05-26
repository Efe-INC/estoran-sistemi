import streamlit as st
import streamlit.components.v1 as components

# Sayfa Ayarları
st.set_page_config(page_title="🐍 Mobil Yılan Oyunu", page_icon="🐍", layout="centered")

st.title("🐍 Mobil Uyumlu Yılan Oyunu")
st.write("📱 **Bilgisayardan:** Yön tuşlarını kullanabilir veya ekrandaki butonlara tıklayabilirsiniz.")
st.write("📱 **Telefondan:** Oyunu başlatmak için önce siyah alana dokunun, ardından aşağıdaki yön butonlarını kullanın!")

# --- OYUNUN HTML, CSS VE JAVASCRIPT KODLARI ---
oyun_html = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
        body {
            display: flex;
            flex-direction: column;
            align-items: center;
            background-color: #1e1e1e;
            color: white;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            user-select: none;
            touch-action: manipulation;
        }
        
        /* Skor Tablosu Tasarımı */
        .skor-konteyner {
            display: flex;
            justify-content: space-between;
            width: 100%;
            max-width: 400px;
            font-size: 20px;
            font-weight: bold;
            margin-bottom: 10px;
        }
        #aktif-skor { color: #4CAF50; }
        #en-yuksek-skor { color: #FFD700; } /* Altın sarısı */

        /* Mobil Uyumlu Oyun Ekranı */
        canvas {
            border: 4px solid #4CAF50;
            background-color: #000;
            box-shadow: 0px 0px 20px rgba(76, 175, 80, 0.3);
            max-width: 90vw; /* Telefon ekranına sığması için esnek genişlik */
            height: auto;
            cursor: pointer;
        }

        /* D-PAD (Mobil Yön Butonları) Tasarımı */
        .dpad {
            display: flex;
            flex-direction: column;
            align-items: center;
            margin-top: 20px;
            width: 100%;
            max-width: 220px;
        }
        .dpad-row {
            display: flex;
            justify-content: center;
            width: 100%;
        }
        .dpad-btn {
            width: 65px;
            height: 55px;
            margin: 5px;
            background-color: #333;
            color: white;
            border: 2px solid #555;
            border-radius: 12px;
            font-size: 24px;
            font-weight: bold;
            display: flex;
            justify-content: center;
            align-items: center;
            box-shadow: 0 4px #222;
            cursor: pointer;
            transition: 0.1s;
        }
        .dpad-btn:active {
            box-shadow: 0 0 #222;
            transform: translateY(4px);
            background-color: #4CAF50;
        }
        .dpad-spacer {
            width: 65px;
            height: 55px;
            margin: 5px;
        }
    </style>
</head>
<body>

    <div class="skor-konteyner">
        <div>Skor: <span id="skor">0</span></div>
        <div>🏆 En Yüksek: <span id="yuksekSkor">0</span></div>
    </div>

    <canvas id="gameCanvas" width="400" height="400"></canvas>

    <div class="dpad">
        <div class="dpad-row">
            <div class="dpad-btn" onclick="yonDegistir('UP')">▲</div>
        </div>
        <div class="dpad-row">
            <div class="dpad-btn" onclick="yonDegistir('LEFT')">◀</div>
            <div class="dpad-spacer"></div>
            <div class="dpad-btn" onclick="yonDegistir('RIGHT')">▶</div>
        </div>
        <div class="dpad-row">
            <div class="dpad-btn" onclick="yonDegistir('DOWN')">▼</div>
        </div>
    </div>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");
        const skorElementi = document.getElementById("skor");
        const yuksekSkorElementi = document.getElementById("yuksekSkor");

        const grid = 20;
        let count = 0;
        let skor = 0;
        let oyunBasladi = false;
        
        // Tarayıcı hafızasından yüksek skoru yükle
        let yuksekSkor = localStorage.getItem("yilan_yuksek_skor") || 0;
        yuksekSkorElementi.textContent = yuksekSkor;
        
        let yilan = {
            x: 160,
            y: 160,
            dx: 0,
            dy: 0,
            cells: [{x: 160, y: 160}, {x: 140, y: 160}],
            maxCells: 4
        };
        
        let elma = { x: 320, y: 320 };

        function rastgeleSayi(min, max) {
            return Math.floor(Math.random() * (max - min) + min);
        }

        function elmaYerlestir() {
            elma.x = rastgeleSayi(0, 20) * grid;
            elma.y = rastgeleSayi(0, 20) * grid;
        }

        function loop() {
            requestAnimationFrame(loop);

            if (++count < 12) { return; }
            count = 0;

            ctx.clearRect(0,0,canvas.width,canvas.height);

            if (oyunBasladi) {
                yilan.x += yilan.dx;
                yilan.y += yilan.dy;
            }

            if (yilan.x < 0) { yilan.x = canvas.width - grid; }
            else if (yilan.x >= canvas.width) { yilan.x = 0; }
            
            if (yilan.y < 0) { yilan.y = canvas.height - grid; }
            else if (yilan.y >= canvas.height) { yilan.y = 0; }

            if (oyunBasladi) {
                yilan.cells.unshift({x: yilan.x, y: yilan.y});
                if (yilan.cells.length > yilan.maxCells) {
                    yilan.cells.pop();
                }
            }

            // Elmayı çiz (Yuvarlak ve tatlı bir elma olsun)
            ctx.fillStyle = '#ff4d4d';
            ctx.beginPath();
            ctx.arc(elma.x + grid/2, elma.y + grid/2, grid/2 - 1, 0, 2 * Math.PI);
            ctx.fill();

            // Yılanı çiz
            yilan.cells.forEach(function(cell, index) {
                if (index === 0) ctx.fillStyle = '#81C784'; // Kafa
                else ctx.fillStyle = '#4CAF50'; // Gövde
                
                ctx.fillRect(cell.x, cell.y, grid-1, grid-1);  

                if (cell.x === elma.x && cell.y === elma.y) {
                    yilan.maxCells++;
                    skor += 10;
                    skorElementi.textContent = skor;
                    elmaYerlestir();
                    
                    // Anlık olarak yüksek skor kontrolü yap
                    if (skor > yuksekSkor) {
                        yuksekSkor = skor;
                        yuksekSkorElementi.textContent = yuksekSkor;
                        localStorage.setItem("yilan_yuksek_skor", yuksekSkor);
                    }
                }

                for (let i = index + 1; i < yilan.cells.length; i++) {
                    if (cell.x === yilan.cells[i].x && cell.y === yilan.cells[i].y && oyunBasladi) {
                        // Oyun Bittiğinde Sıfırla
                        yilan.x = 160; yilan.y = 160;
                        yilan.cells = [{x: 160, y: 160}, {x: 140, y: 160}];
                        yilan.maxCells = 4;
                        yilan.dx = 0; yilan.dy = 0;
                        skor = 0;
                        oyunBasladi = false;
                        skorElementi.textContent = skor;
                        elmaYerlestir();
                    }
                }
            });
        }

        // D-Pad Buton Fonksiyonu (Mobil için)
        function yonDegistir(yon) {
            oyunBasladi = true;
            
            if (yon === 'LEFT' && yilan.dx === 0) {
                yilan.dx = -grid; yilan.dy = 0;
            }
            else if (yon === 'UP' && yilan.dy === 0) {
                yilan.dy = -grid; yilan.dx = 0;
            }
            else if (yon === 'RIGHT' && yilan.dx === 0) {
                yilan.dx = grid; yilan.dy = 0;
            }
            else if (yon === 'DOWN' && yilan.dy === 0) {
                yilan.dy = grid; yilan.dx = 0;
            }
        }

        // Klavye Kontrolleri (Bilgisayar için)
        document.addEventListener('keydown', function(e) {
            if([37, 38, 39, 40].indexOf(e.keyCode) > -1) {
                e.preventDefault();
            }

            if (e.which === 37) yonDegistir('LEFT');
            else if (e.which === 38) yonDegistir('UP');
            else if (e.which === 39) yonDegistir('RIGHT');
            else if (e.which === 40) yonDegistir('DOWN');
        });

        elmaYerlestir();
        requestAnimationFrame(loop);
    </script>
</body>
</html>
"""

# HTML Bileşeni (Butonlar da sığsın diye yüksekliği 680 yaptık)
components.html(oyun_html, height=680)
