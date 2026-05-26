import streamlit as st
import streamlit.components.v1 as components

# Sayfa Ayarları
st.set_page_config(page_title="🐍 Global Skorlu Yılan Oyunu", page_icon="🐍", layout="centered")

st.title("🐍 Dünyanın En Rekabetçi Yılan Oyunu")
st.write("🏆 Adınızı yazın, rekoru kırın ve adınızı tüm dünyaya duyurun!")

# --- OYUNUN HTML, CSS VE JAVASCRIPT KODLARI ---
# Not: kvdb.io servisi ile tüm oyuncuların skorları ortak bir havuzda tutulur.
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
        
        /* Ekran Yönetimi */
        .ekran { display: none; width: 100%; max-width: 400px; text-align: center; }
        .aktif { display: flex; flex-direction: column; align-items: center; }

        /* Giriş ve Bitiş Ekranı Tasarımları */
        h2 { color: #4CAF50; margin-top: 10px; }
        input {
            padding: 12px;
            font-size: 16px;
            border: 2px solid #4CAF50;
            border-radius: 8px;
            background-color: #222;
            color: white;
            margin-bottom: 15px;
            width: 80%;
            text-align: center;
        }
        button {
            padding: 12px 25px;
            font-size: 16px;
            font-weight: bold;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            box-shadow: 0 4px #2e7d32;
        }
        button:active { transform: translateY(2px); box-shadow: 0 2px #2e7d32; }

        /* Global Skor Tablosu Stili */
        .skor-tablosu {
            width: 90%;
            background-color: #2a2a2a;
            border-radius: 10px;
            padding: 15px;
            margin-top: 20px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.3);
        }
        .skor-satir {
            display: flex;
            justify-content: space-between;
            padding: 8px 10px;
            border-bottom: 1px solid #3d3d3d;
            font-size: 16px;
        }
        .skor-satir:last-child { border-bottom: none; }
        .derece-1 { color: #FFD700; font-weight: bold; } /* Altın */
        .derece-2 { color: #C0C0C0; font-weight: bold; } /* Gümüş */
        .derece-3 { color: #CD7F32; font-weight: bold; } /* Bronz */

        /* Oyun İçi Skor Barı */
        .oyun-skor-bar {
            display: flex;
            justify-content: space-between;
            width: 100%;
            max-width: 400px;
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 5px;
            color: #4CAF50;
        }

        /* Canvas */
        canvas {
            border: 4px solid #4CAF50;
            background-color: #000;
            max-width: 90vw;
            height: auto;
        }

        /* D-PAD (Mobil Butonlar) */
        .dpad { display: flex; flex-direction: column; align-items: center; margin-top: 15px; width: 100%; max-width: 220px; }
        .dpad-row { display: flex; justify-content: center; width: 100%; }
        .dpad-btn {
            width: 60px; height: 50px; margin: 4px; background-color: #333; color: white;
            border: 2px solid #555; border-radius: 12px; font-size: 22px;
            display: flex; justify-content: center; align-items: center; box-shadow: 0 4px #222; cursor: pointer;
        }
        .dpad-btn:active { box-shadow: 0 0 #222; transform: translateY(4px); background-color: #4CAF50; }
        .dpad-spacer { width: 60px; height: 50px; margin: 4px; }
    </style>
</head>
<body>

    <div id="ekran-giris" class="ekran aktif">
        <h2>🏆 ŞAMPİYONLAR LİGİ</h2>
        <input type="text" id="oyuncu-adi" placeholder="Adınızı Yazın..." maxlength="12">
        <button onclick="oyunuBaslat()">Oyuna Başla 🎮</button>
        
        <div class="skor-tablosu">
            <h3 style="margin-top:0; color:#FFD700;">🌍 DÜNYA REKORLARI (TOP 5)</h3>
            <div id="kuresel-skorlar-giris">Yükleniyor...</div>
        </div>
    </div>

    <div id="ekran-oyun" class="ekran">
        <div class="oyun-skor-bar">
            <div>Oyuncu: <span id="bar-isim" style="color:white;">-</span></div>
            <div>Skor: <span id="bar-skor">0</span></div>
        </div>
        <canvas id="gameCanvas" width="400" height="400"></canvas>
        
        <div class="dpad">
            <div class="dpad-row"><div class="dpad-btn" onclick="yonDegistir('UP')">▲</div></div>
            <div class="dpad-row">
                <div class="dpad-btn" onclick="yonDegistir('LEFT')">◀</div>
                <div class="dpad-spacer"></div>
                <div class="dpad-btn" onclick="yonDegistir('RIGHT')">▶</div>
            </div>
            <div class="dpad-row"><div class="dpad-btn" onclick="yonDegistir('DOWN')">▼</div></div>
        </div>
    </div>

    <div id="ekran-bitis" class="ekran">
        <h2 style="color:#ff4d4d;">💀 OYUN BİTTİ!</h2>
        <p style="font-size:20px;">Skorunuz: <span id="bitis-skor" style="color:#4CAF50; font-weight:bold;">0</span></p>
        <button onclick="yenidenOyna()">Yeniden Dene 🔄</button>

        <div class="skor-tablosu">
            <h3 style="margin-top:0; color:#FFD700;">🌍 GÜNCEL DÜNYA REKORLARI</h3>
            <div id="kuresel-skorlar-bitis">Skorunuz kaydediliyor...</div>
        </div>
    </div>

    <script>
        // Veritabanı Ayarı (Senin projene özel benzersiz bir bulut odası oluşturduk)
        const DB_URL = "https://kvdb.io/efernolcr_snake_shared_v1/leaderboard";

        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");
        
        const grid = 20;
        let count = 0;
        let skor = 0;
        let oyuncuAdi = "Anonim";
        let oyunDongusu;
        
        let yilan = { x: 160, y: 160, dx: grid, dy: 0, cells: [], maxCells: 4 };
        let elma = { x: 320, y: 320 };

        // Sayfa ilk açıldığında dünya skorlarını getir
        dunyaSkorlariniGetir();

        async function dunyaSkorlariniGetir() {
            let skorlar = [];
            try {
                let response = await fetch(DB_URL);
                if (response.ok) { skorlar = await response.json(); }
            } catch(e) { console.log("Henüz kayıt yok veya hata oluştu."); }
            tabloyuCiz(skorlar);
        }

        function tabloyuCiz(skorlar) {
            let htmlIcerik = "";
            if (skorlar.length === 0) {
                htmlIcerik = "<div class='skor-satir'>Henüz rekor kıran yok! İlk sen ol!</div>";
            }
            skorlar.forEach((item, index) => {
                htmlIcerik += `<div class='skor-satir derece-${index+1}'>
                    <span>${index+1}. ${item.name}</span>
                    <span>${item.score} Puan</span>
                </div>`;
            });
            document.getElementById("kuresel-skorlar-giris").innerHTML = htmlIcerik;
            document.getElementById("kuresel-skorlar-bitis").innerHTML = htmlIcerik;
        }

        async function skoruBulutaKaydet(isim, alinanSkor) {
            let skorlar = [];
            try {
                let response = await fetch(DB_URL);
                if (response.ok) { skorlar = await response.json(); }
            } catch(e) {}

            // Yeni skoru ekle, büyükten küçüğe sırala ve sadece ilk 5 kişiyi tut
            skorlar.push({ name: isim, score: alinanSkor });
            skorlar.sort((a, b) => b.score - a.score);
            skorlar = skorlar.slice(0, 5);

            try {
                await fetch(DB_URL, { method: 'POST', body: JSON.stringify(skorlar) });
            } catch(e) {}
            
            tabloyuCiz(skorlar);
        }

        function ekranDegistir(ekranId) {
            document.querySelectorAll('.ekran').forEach(e => e.classList.remove('aktif'));
            document.getElementById(ekranId).classList.add('aktif');
        }

        function oyunuBaslat() {
            let girilenIsim = document.getElementById("oyuncu-adi").value.trim();
            if (girilenIsim !== "") { oyuncuAdi = girilenIsim; }
            
            document.getElementById("bar-isim").textContent = oyuncuAdi;
            ekranDegistir("ekran-oyun");
            
            // Oyunu sıfırla ve başlat
            skor = 0;
            document.getElementById("bar-skor").textContent = skor;
            yilan = { x: 160, y: 160, dx: grid, dy: 0, cells: [{x:160,y:160}], maxCells: 4 };
            elmaYerlestir();
            
            if(!oyunDongusu) { loop(); }
        }

        function elmaYerlestir() {
            elma.x = Math.floor(Math.random() * 20) * grid;
            elma.y = Math.floor(Math.random() * 20) * grid;
        }

        function loop() {
            oyunDongusu = requestAnimationFrame(loop);

            if (++count < 11) { return; } // Hız dengesi
            count = 0;

            ctx.clearRect(0,0,canvas.width,canvas.height);

            yilan.x += yilan.dx;
            yilan.y += yilan.dy;

            // Duvarlardan geçiş telesportasyonu
            if (yilan.x < 0) yilan.x = canvas.width - grid;
            else if (yilan.x >= canvas.width) yilan.x = 0;
            if (yilan.y < 0) yilan.y = canvas.height - grid;
            else if (yilan.y >= canvas.height) yilan.y = 0;

            yilan.cells.unshift({x: yilan.x, y: yilan.y});
            if (yilan.cells.length > yilan.maxCells) { yilan.cells.pop(); }

            // Elma Çizimi
            ctx.fillStyle = '#ff4d4d';
            ctx.beginPath();
            ctx.arc(elma.x + grid/2, elma.y + grid/2, grid/2 - 1, 0, 2 * Math.PI);
            ctx.fill();

            // Yılan Çizimi
            yilan.cells.forEach(function(cell, index) {
                ctx.fillStyle = (index === 0) ? '#81C784' : '#4CAF50';
                ctx.fillRect(cell.x, cell.y, grid-1, grid-1);  

                // Elma yendi mi?
                if (cell.x === elma.x && cell.y === elma.y) {
                    yilan.maxCells++;
                    skor += 10;
                    document.getElementById("bar-skor").textContent = skor;
                    elmaYerlestir();
                }

                // Kendine çarpma ölme kontrolü
                for (let i = index + 1; i < yilan.cells.length; i++) {
                    if (cell.x === yilan.cells[i].x && cell.y === yilan.cells[i].y) {
                        oyunBitti();
                    }
                }
            });
        }

        function oyunBitti() {
            cancelAnimationFrame(oyunDongusu);
            oyunDongusu = null;
            document.getElementById("bitis-skor").textContent = skor;
            document.getElementById("kuresel-skorlar-bitis").innerHTML = "Skorunuz dünya liderliğine kaydediliyor...";
            ekranDegistir("ekran-bitis");
            skoruBulutaKaydet(oyuncuAdi, skor);
        }

        function yenidenOyna() {
            dunyaSkorlariniGetir();
            ekranDegistir("ekran-giris");
        }

        function yonDegistir(yon) {
            if (yon === 'LEFT' && yilan.dx === 0) { yilan.dx = -grid; yilan.dy = 0; }
            else if (yon === 'UP' && yilan.dy === 0) { yilan.dy = -grid; yilan.dx = 0; }
            else if (yon === 'RIGHT' && yilan.dx === 0) { yilan.dx = grid; yilan.dy = 0; }
            else if (yon === 'DOWN' && yilan.dy === 0) { yilan.dy = grid; yilan.dy = 0; }
        }

        document.addEventListener('keydown', function(e) {
            if([37, 38, 39, 40].indexOf(e.keyCode) > -1) e.preventDefault();
            if (e.which === 37) yonDegistir('LEFT');
            else if (e.which === 38) yonDegistir('UP');
            else if (e.which === 39) yonDegistir('RIGHT');
            else if (e.which === 40) yonDegistir('DOWN');
        });
    </script>
</body>
</html>
"""

# Mobil butonların rahat sığması için yüksekliği artırdık
components.html(oyun_html, height=700)
