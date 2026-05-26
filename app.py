import streamlit as st
import streamlit.components.v1 as components

# Sayfa Ayarları
st.set_page_config(page_title="🐍 Yılan Oyunu", page_icon="🐍", layout="centered")

st.title("🐍 Python & Web Yılan Oyunu")
st.write("👉 **ÖNEMLİ:** Oyunu oynamak için önce aşağıdaki siyah alana **FAREYLE BİR KEZ TIKLAYIN**, ardından yön tuşlarıyla yılanı hareket ettirin.")

# --- OYUNUN HTML VE JAVASCRIPT KODLARI ---
oyun_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body {
            display: flex;
            flex-direction: column;
            align-items: center;
            background-color: #1e1e1e;
            color: white;
            font-family: Arial, sans-serif;
            margin: 0;
            user-select: none;
        }
        canvas {
            border: 4px solid #4CAF50;
            background-color: #000;
            box-shadow: 0px 0px 20px rgba(76, 175, 80, 0.5);
            cursor: pointer;
        }
        #skor-tablosu {
            font-size: 24px;
            margin: 10px 0;
            font-weight: bold;
            color: #4CAF50;
        }
    </style>
</head>
<body>
    <div id="skor-tablosu">Skor: <span id="skor">0</span></div>
    <canvas id="gameCanvas" width="400" height="400"></canvas>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");
        const skorElementi = document.getElementById("skor");

        const grid = 20;
        let count = 0;
        let skor = 0;
        let oyunBasladi = false;
        
        let yilan = {
            x: 160,
            y: 160,
            dx: 0,  // Başlangıçta sağa gitmesin, dursun (0 yaptık)
            dy: 0,  // Başlangıçta duruyor
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

            // HIZ AYARI: 6 olan değeri 12 yaptık, böylece oyun 2 kat yavaşladı!
            if (++count < 12) { return; }
            count = 0;

            ctx.clearRect(0,0,canvas.width,canvas.height);

            // Yılanı sadece yön tuşuna basıldıysa ilerlet
            if (oyunBasladi) {
                yilan.x += yilan.dx;
                yilan.y += yilan.dy;
            }

            // Duvarlardan geçiş
            if (yilan.x < 0) { yilan.x = canvas.width - grid; }
            else if (yilan.x >= canvas.width) { yilan.x = 0; }
            
            if (yilan.y < 0) { yilan.y = canvas.height - grid; }
            else if (yilan.y >= canvas.height) { yilan.y = 0; }

            // Yılanın gövdesi
            if (oyunBasladi) {
                yilan.cells.unshift({x: yilan.x, y: yilan.y});
                if (yilan.cells.length > yilan.maxCells) {
                    yilan.cells.pop();
                }
            }

            // Elmayı çiz
            ctx.fillStyle = '#ff4d4d';
            ctx.fillRect(elma.x, elma.y, grid-1, grid-1);

            // Yılanı çiz
            yilan.cells.forEach(function(cell, index) {
                if (index === 0) ctx.fillStyle = '#81C784'; // Kafa
                else ctx.fillStyle = '#4CAF50'; // Gövde
                
                ctx.fillRect(cell.x, cell.y, grid-1, grid-1);  

                // Elma yeme kontrolü
                if (cell.x === elma.x && cell.y === elma.y) {
                    yilan.maxCells++;
                    skor += 10;
                    skorElementi.textContent = skor;
                    elmaYerlestir();
                }

                // Kendine çarpma kontrolü
                for (let i = index + 1; i < yilan.cells.length; i++) {
                    if (cell.x === yilan.cells[i].x && cell.y === yilan.cells[i].y && oyunBasladi) {
                        // Oyunu sıfırla
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

        // Tuş Kontrolleri
        document.addEventListener('keydown', function(e) {
            // Sayfa kaymasını engelle
            if([37, 38, 39, 40].indexOf(e.keyCode) > -1) {
                e.preventDefault();
                oyunBasladi = true; // Herhangi bir yön tuşuna basılınca hareket başlasın
            }

            // Sola Dönüş (Eğer sağa gitmiyorsa veya oyun henüz başlamadıysa)
            if (e.which === 37 && (yilan.dx === 0 || yilan.cells.length === 2)) {
                yilan.dx = -grid; yilan.dy = 0;
            }
            // Yukarı Dönüş
            else if (e.which === 38 && (yilan.dy === 0 || yilan.cells.length === 2)) {
                yilan.dy = -grid; yilan.dx = 0;
            }
            // Sağa Dönüş
            else if (e.which === 39 && (yilan.dx === 0 || yilan.cells.length === 2)) {
                yilan.dx = grid; yilan.dy = 0;
            }
            // Aşağı Dönüş
            else if (e.which === 40 && (yilan.dy === 0 || yilan.cells.length === 2)) {
                yilan.dy = grid; yilan.dx = 0;
            }
        });

        elmaYerlestir();
        requestAnimationFrame(loop);
    </script>
</body>
</html>
"""

# HTML Kodunu Entegre Etme
components.html(oyun_html, height=500)

st.write("---")
st.info("By Efe Eren ÖLÇER")
