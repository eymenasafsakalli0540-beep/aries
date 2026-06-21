<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ARIES AI</title>
    <style>
        /* Temel yapı */
        body { margin: 0; background: #000; color: #fff; font-family: sans-serif; height: 100vh; display: flex; overflow: hidden; }
        
        /* Sol panel */
        #sidebar { width: 250px; border-right: 1px solid #111; padding: 20px; display: flex; flex-direction: column; justify-content: space-between; flex-shrink: 0; }
        .logo { color: #00e5ff; font-weight: bold; font-size: 24px; margin-bottom: 30px; }
        .yeni-analiz { background: #111; border: 1px solid #222; padding: 12px; border-radius: 8px; text-align: center; cursor: pointer; }
        
        /* Ana alan */
        #main { flex-grow: 1; position: relative; padding: 40px; display: flex; flex-direction: column; }
        .tatil-yazi { position: absolute; top: 30px; right: 40px; text-align: right; line-height: 1.2; font-size: 18px; font-weight: 500; }
        
        /* Mesaj */
        .mesaj-balonu { border: 1px solid #00e5ff; border-radius: 20px; padding: 15px 25px; width: fit-content; margin-top: 50px; }
        
        /* Giriş */
        .input-container { position: absolute; bottom: 40px; left: 40px; right: 40px; }
        input { width: 100%; background: #111; border: 1px solid #222; padding: 18px 20px; color: #fff; border-radius: 50px; outline: none; box-sizing: border-box; }
        
        /* Mobil ayar */
        @media (max-width: 768px) { #sidebar { display: none; } #main { padding: 20px; } }
    </style>
</head>
<body>

    <div id="sidebar">
        <div>
            <div class="logo">ARIES AI</div>
            <div class="yeni-analiz">Yeni Analiz</div>
        </div>
        <div style="font-size: 12px; color: #555;">DEVELOPER: TÜW</div>
    </div>

    <div id="main">
        <div class="tatil-yazi">Tatil Bitene<br>Kadar Yokuz</div>
        <div class="mesaj-balonu">ARIES AI: Merhaba TÜW. Seni dinliyorum kanka.</div>
        <div class="input-container">
            <input type="text" placeholder="Bir soru sorun...">
        </div>
    </div>

</body>
</html>
