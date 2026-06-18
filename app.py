from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# --- DEV KÜRESEL BİLGİ BANKASI ---
global_geography = {
    # Ülkeler & Şehirler
    "papua yeni gine": {"b": "Port Moresby", "m": "12.800 km", "k": "Okyanusya"},
    "hollanda": {"b": "Amsterdam", "m": "2.210 km", "k": "Avrupa"},
    "amsterdam": {"b": "Hollanda'nın başkentidir", "m": "2.210 km", "k": "Avrupa"},
    "fransa": {"b": "Paris", "m": "2.250 km", "k": "Avrupa"},
    "paris": {"b": "Fransa'nın başkentidir", "m": "2.250 km", "k": "Avrupa"},
    "almanya": {"b": "Berlin", "m": "1.740 km", "k": "Avrupa"},
    "ingiltere": {"b": "Londra", "m": "2.500 km", "k": "Avrupa"},
    "italya": {"b": "Roma", "m": "1.380 km", "k": "Avrupa"},
    "japonya": {"b": "Tokyo", "m": "8.900 km", "k": "Asya"},
    "rusya": {"b": "Moskova", "m": "1.750 km", "k": "Asya/Avrupa"},
    "mısır": {"b": "Kahire", "m": "1.200 km", "k": "Afrika"},
    "brezilya": {"b": "Brasilia", "m": "9.800 km", "k": "Güney Amerika"},
    "abd": {"b": "Washington D.C.", "m": "8.300 km", "k": "Kuzey Amerika"},
    "amerika": {"b": "Washington D.C.", "m": "8.300 km", "k": "Kuzey Amerika"},
    "azerbaycan": {"b": "Bakü", "m": "1.700 km", "k": "Asya"},
    "küba": {"b": "Havana", "m": "9.500 km", "k": "Karayipler"},
    "madagaskar": {"b": "Antananarivo", "m": "7.200 km", "k": "Afrika"},
    "ispanya": {"b": "Madrid", "m": "2.700 km", "k": "Avrupa"},
    "portekiz": {"b": "Lizbon", "m": "3.200 km", "k": "Avrupa"},
    "çin": {"b": "Pekin", "m": "7.000 km", "k": "Asya"},
    "hindistan": {"b": "Yeni Delhi", "m": "4.500 km", "k": "Asya"},
    "türkiye": {"b": "Ankara", "m": "Merkez Ülke 🇹🇷", "k": "Asya/Avrupa"}
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_message = request.json.get("message", "").lower().strip()
    
    # Kısaltma Çözücü (Geliştirildi)
    shortcuts = {
        "knk": "kanka", "slm": "selam", "mrb": "merhaba", "tr": "türkiye",
        "km": "kilometre", "baskent": "başkenti", "baskenti": "başkenti",
        "arasında": "arası", "mesafe": "arası", "dg": "dağı", "gl": "gölü",
        "ing": "ingilizce", "mat": "matematik", "tc": "türkçe", "sos": "sosyal"
    }
    for key, val in shortcuts.items():
        user_message = user_message.replace(f" {key} ", f" {val} ")
        if user_message.startswith(key): user_message = user_message.replace(key, val, 1)
        if user_message.endswith(key): user_message = user_message[:-len(key)] + val

    reply = ""
    math_chars = set("0123456789+-*/(). ")
    
    # 🔢 DİNAMİK MATEMATİK MOTORU
    if any(char in user_message for char in ['+', '-', '*', '/']) and set(user_message).issubset(math_chars):
        try:
            result = eval(user_message)
            reply = f'<span class="expert-badge badge-sayisal">Matematik Hesaplama</span><br><div class="formula-box">{user_message} = {result}</div><b>Sonuç:</b> {result}'
        except:
            reply = '<span class="expert-badge badge-sayisal">Hata</span><br>İşlem hesaplanamadı kanka.'
            
    # 📚 DERSLER VE COĞRAFYA MOTORU
    else:
        found_country = None
        for country in global_geography:
            if country in user_message:
                found_country = country
                break
                
        if found_country:
            data = global_geography[found_country]
            if "başkenti" in user_message or "nerenin" in user_message:
                reply = f'<span class="expert-badge badge-cografya">Küresel Coğrafya</span><br><b>Bölge:</b> {found_country.upper()}<br><b>Başkenti:</b> {data["b"]}<br><b>Bulunduğu Kıta:</b> {data["k"]}'
            elif "arası" in user_message or "km" in user_message or "kaç" in user_message:
                reply = f'<span class="expert-badge badge-cografya">Mesafe Analizi</span><br><b>Rota:</b> Türkiye ➔ {found_country.upper()}<br><b>Uzaklık:</b> {data["m"]}<br><b>Konum:</b> {data["k"]}'
            else:
                reply = f'<span class="expert-badge badge-cografya">Genel Bilgi</span><br><b>Bölge:</b> {found_country.upper()}<br><b>Başkent:</b> {data["b"]}<br><b>Mesafe:</b> {data["m"]}'
        
        # --- TÜRKÇE DERSİ MODÜLÜ ---
        elif "türkçe" in user_message or "mecaz" in user_message or "gerçek anlam" in user_message or "terim" in user_message:
            reply = ('<span class="expert-badge badge-sozel">Türkçe Dil Bilgisi</span><br>'
                     '• **Gerçek Anlam:** Kelimenin akla gelen ilk anlamıdır. (Örn: Çay çok sıcaktı.)<br>'
                     '• **Mecaz Anlam:** Kelimenin gerçek anlamından tamamen uzaklaşmasıdır. (Örn: Bize çok soğuk davrandı.)<br>'
                     '• **Terim Anlam:** Bilim, sanat, spor dallarına ait özel kelimelerdir. (Örn: Nota, Ofsayt, Zamir.)')
        
        # --- MATEMATİK GEOMETRİ FORMÜLLERİ ---
        elif "matematik formül" in user_message or "alan formül" in user_message or "çevre formül" in user_message:
            reply = ('<span class="expert-badge badge-sayisal">Matematik & Geometri Formülleri</span><br>'
                     '• **Alan Formülleri:** Kare = $a^2$ | Dikdörtgen = $a \cdot b$ | Üçgen = $\\frac{b \cdot h}{2}$<br>'
                     '• **Çevre Formülleri:** Kare = $4a$ | Dikdörtgen = $2(a+b)$ | Çember = $2\\pi r$')
        
        # --- FEN BİLİMLERİ MODÜLÜ ---
        elif "fen" in user_message or "hücre" in user_message or "organel" in user_message or "mitokondri" in user_message:
            reply = ('<span class="expert-badge badge-sayisal">Fen Bilimleri Laboratuvarı</span><br>'
                     '• **Hücre:** Hücre zarı (korur), Sitoplazma (yaşam döner), Çekirdek (yönetir).<br>'
                     '• **Organeller:** Mitokondri (Enerji ⚡), Kloroplast (Bitkide besin/oksijen 🌱), Ribozom (Protein sentezi).')
        
        # --- TARİH MODÜLÜ (İSTANBUL + DİĞERLERİ) ---
        elif "tarih" in user_message or "istanbul" in user_message or "kurtuluş savaşı" in user_message or "malazgirt" in user_message:
            if "istanbul" in user_message and "fetih" in user_message:
                reply = '<span class="expert-badge badge-sozel">Tarih Analizi</span><br><b>İstanbul\'un Fethi (1453):</b> Fatih Sultan Mehmet tarafından fethedildi. Yeni Çağ\'ı açan büyük askeri başarıdır.'
            elif "malazgirt" in user_message:
                reply = '<span class="expert-badge badge-sozel">Tarih Analizi</span><br><b>Malazgirt Savaşı (1071):</b> Sultan Alparslan komutasında Anadolu\'nun kapıları Türklere kesin olarak açılmıştır.'
            else:
                reply = ('<span class="expert-badge badge-sozel">Tarih Kronolojisi</span><br>'
                         '• **1071:** Malazgirt Savaşı (Anadolu kapısı açıldı)<br>'
                         '• **1453:** İstanbul\'un Fethi (Yeni Çağ başladı)<br>'
                         '• **1919:** 19 Mayıs Atatürk\'ün Samsun\'a çıkışı (Kurtuluş Savaşı başladı)<br>'
                         '• **1923:** 29 Ekim Cumhuriyet\'in İlanı 🇹🇷')

        # --- COĞRAFYA EK MODÜLÜ ---
        elif "coğrafya" in user_message or "iklim" in user_message or "yeryüzü" in user_message:
            reply = ('<span class="expert-badge badge-cografya">Coğrafya Co-Pilot</span><br>'
                     '• **İklimler:** Karadeniz (Her mevsim yağışlı), Akdeniz (Yazlar sıcak-kurak, kışlar ılık-yağışlı), Karasal (Kışlar karlı/soğuk).<br>'
                     '• **Yeryüzü Şekilleri:** Ova (Alçak düzlük), Plato (Yüksek düzlük), Dağ (Yüksek kütle).')

        # --- İNGİLİZCE MODÜLÜ ---
        elif "ingilizce" in user_message or "english" in user_message or "günler" in user_message:
            reply = ('<span class="expert-badge badge-sozel">English Time / İngilizce</span><br>'
                     '• **To Be:** I am | He/She/It is | You/We/They are<br>'
                     '• **Days (Günler):** Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday.<br>'
                     '• **Soru Kelimeleri:** What (Ne), Where (Nerede), Who (Kim), When (Ne zaman).')

        # --- FİZİK / HIZ FORMÜLÜ ---
        elif "hız" in user_message or "hiz" in user_message:
            reply = '<span class="expert-badge badge-sayisal">Fizik Analizi</span><br><div class="formula-box">V = x / t</div><b>V:</b> Hız, <b>x:</b> Yol, <b>t:</b> Zaman.'
            
        # --- SOHBET ŞABLONLARI ---
        elif "selam" in user_message or "merhaba" in user_message:
            reply = "Selam **TÜW**! **Aries 1. Sürüm** Python web sunucusu üzerinden aktif, seni dinliyorum."
        elif "kanka" in user_message or "naber" in user_message:
            reply = "İyidir kanka, sistemi Python ile canavara dönüştürdük! Arayüzümüz eski, sarsılmaz gücünde. Nereyi veya hangi dersi merak ediyorsun?"
        else:
            reply = "Aries Zeka Motoru veriyi Python arka planında taradı ancak eşleşme bulamadı. Bana matematik, fen, türkçe, tarih, coğrafya veya ingilizce ile ilgili bir kelime sorabilirsin!"

    return jsonify({"reply": reply})

if __name__ == '__main__':
    app.run(debug=True)
