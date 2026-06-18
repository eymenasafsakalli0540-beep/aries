from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Gelişmiş Küresel Coğrafya & Ülkeler Veri Tabanı
global_geography = {
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
    
    shortcuts = {
        "knk": "kanka", "slm": "selam", "mrb": "merhaba", "tr": "türkiye",
        "km": "kilometre", "baskent": "başkenti", "baskenti": "başkenti",
        "arasında": "arası", "mesafe": "arası", "dg": "dağı", "gl": "gölü",
        "mat": "matematik", "ing": "ingilizce", "fen": "fen bilimleri", "sos": "sosyal",
        "tar": "tarih", "cog": "coğrafya"
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
            reply = f'<span class="expert-badge badge-sayisal">Matematik Analizi</span><br><div class="formula-box">{user_message} = {result}</div><b>Sonuç:</b> {result}'
        except:
            reply = '<span class="expert-badge badge-sayisal">Hata</span><br>İşlem hesaplanamadı Kaptan.'
            
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
        
        # --- ⏳ ULTRA TARİH ANALİZ MOTORU ---
        elif any(x in user_message for x in ["tarih", "savaş", "osmanlı", "kurtuluş", "atatürk", "cumhuriyet", "dünya savaşı", "antlaşma"]):
            if "istanbul" in user_message and "fetih" in user_message:
                reply = '<span class="expert-badge badge-sozel">Tarih: Osmanlı Dönemi</span><br><b>İstanbul\'un Fethi (1453):</b> II. Mehmed (Fatih) tarafından Bizans\'a son verildi. Orta Çağ bitti, Yeni Çağ başladı. İpek Yolu kontrolü Osmanlı\'ya geçti.'
            elif "malazgirt" in user_message:
                reply = '<span class="expert-badge badge-sozel">Tarih: Selçuklu Dönemi</span><br><b>Malazgirt Savaşı (1071):</b> Sultan Alparslan komutasındaki Büyük Selçuklu Devleti, Bizans\'ı mağlup etti. Anadolu\'nun kapıları Türklere tamamen açıldı.'
            elif "kurtuluş" in user_message or "milli mücadele" in user_message:
                reply = '<span class="expert-badge badge-sozel">Tarih: Milli Mücadele</span><br><b>Kurtuluş Savaşı (1919-1922):</b> Mustafa Kemal Paşa\'nın 19 Mayıs 1919\'da Samsun\'ya çıkmasıyla başladı. Başkomutanlık Meydan Muharebesi ile düşman Anadolu\'dan temizlendi ve Lozan Antlaşması ile taçlandı.'
            elif "osmanlı" in user_message and ("kuruluş" in user_message or "kuruldu"):
                reply = '<span class="expert-badge badge-sozel">Tarih: Osmanlı Devleti</span><br><b>Kuruluş (1299):</b> Osman Bey tarafından Söğüt ve Domaniç çevresinde bir beylik olarak kuruldu. Kısa sürede büyüyerek cihan imparatorluğuna dönüştü.'
            elif "dünya savaşı" in user_message:
                reply = '<span class="expert-badge badge-sozel">Tarih: Yakın Çağ</span><br>• <b>I. Dünya Savaşı (1914-1918):</b> İttifak ve İtilaf devletleri arasında oldu. Osmanlı bu savaşta yer aldı.<br>• <b>II. Dünya Savaşı (1939-1945):</b> Mihver (Almanya, İtalya, Japonya) ve Müttefik (İngiltere, SSCB, ABD) güçleri arasında yaşandı, nükleer çağ başladı.'
            else:
                reply = ('<span class="expert-badge badge-sozel">Gelişmiş Tarih Arşivi</span><br>'
                         '• <b>1071:</b> Malazgirt Savaşı (Anadolu\'nun kapısı açıldı)<br>'
                         '• <b>1453:</b> İstanbul\'un Fethi (Cihan imparatorluğu dönemi)<br>'
                         '• <b>1919:</b> 19 Mayıs Atatürk\'ün Samsun\'a çıkışı<br>'
                         '• <b>1923:</b> 29 Ekim Cumhuriyet\'in İlanı 🇹🇷')

        # --- 🌍 ULTRA COĞRAFYA ANALİZ MOTORU ---
        elif any(x in user_message for x in ["coğrafya", "iklim", "dağ", "boğaz", "ova", "nehir", "harita", "ölçek", "keşif"]):
            if "boğaz" in user_message or "kanal" in user_message:
                reply = ('<span class="expert-badge badge-cografya">Coğrafya: Stratejik Geçitler</span><br>'
                         '• <b>İstanbul ve Çanakkale Boğazları:</b> Karadeniz\'i Akdeniz\'e bağlayan en kritik su yollarıdır.<br>'
                         '• <b>Süveyş Kanalı:</b> Mısır\'da yer alır, Akdeniz ile Kızıldeniz\'i birleştirerek ticaret rotalarını kısaltır.<br>'
                         '• <b>Cebelitarık Boğazı:</b> Akdeniz\'i Atlas Okyanusu\'na bağlar.')
            elif "dağ" in user_message or "ova" in user_message:
                reply = ('<span class="expert-badge badge-cografya">Coğrafya: Yer Şekilleri</span><br>'
                         '• <b>En Yüksek Noktalar:</b> Dünyada Everest Dağı (8.848 m), Türkiye\'de ise Ağrı Dağı (5.137 m) zirvedir.<br>'
                         '• <b>Ova ve Delta:</b> Türkiye\'nin en büyük delta ovası Çukurova\'dır. Seyhan ve Ceyhan nehirleri tarafından beslenir.')
            elif "iklim" in user_message:
                reply = ('<span class="expert-badge badge-cografya">Coğrafya: İklim Bilimi</span><br>'
                         '• <b>Akdeniz İklimi:</b> Yazlar sıcak ve kurak, kışlar ılık ve yağışlıdır. Bitki örtüsü makidir.<br>'
                         '• <b>Karasal İklim:</b> Kışlar çok soğuk ve karlı, yazlar sıcak geçer. Bitki örtüsü bozkırdır.<br>'
                         '• <b>Ekvatoral İklim:</b> Her mevsim sıcak ve her mevsim bol yağışlıdır.')
            else:
                reply = ('<span class="expert-badge badge-cografya">Gelişmiş Coğrafya Modülü</span><br>'
                         '• <b>Ölçek:</b> Haritalardaki küçültme oranıdır. Ölçek büyüdükçe ayrıntı artar.<br>'
                         '• <b>Paralel ve Meridyenler:</b> 180 paralel, 360 meridyen yayı bulunur. İki meridyen arası zaman farkı 4 dakikadır.<br>'
                         '• <b>Coğrafi Keşifler:</b> Pusulanın gelişmesiyle Macellan (Dünyayı dolaştı) ve Kristof Kolomb (Amerika\'ya ulaştı) gibi denizciler dünyayı yeniden şekillendirdi.')

        # --- 🧪 FEN BİLİMLERİ MODÜLÜ ---
        elif any(x in user_message for x in ["fen", "hücre", "organel", "mitokondri", "dna", "element", "asit", "baz"]):
            reply = ('<span class="expert-badge badge-sayisal">Fen Bilimleri Laboratuvarı</span><br>'
                     '• <b>Hücre Yapısı:</b> Hücre zarı (korur), Sitoplazma (yaşamsal faaliyetler), Çekirdek (yönetim merkezidir).<br>'
                     '• <b>Enerji Odası (Mitokondri):</b> Hücrenin besinleri enerjiye (ATP) dönüştürdüğü yerdir.<br>'
                     '• <b>Kritik Kimya:</b> Asitlerin pH değeri 0-7 arasıdır (ekşidir), Bazların pH değeri 7-14 arasıdır (acıdır).')

        # --- 🧮 MATEMATİK & GEOMETRİ FORMÜLLERİ ---
        elif any(x in user_message for x in ["matematik", "geometri", "formül", "alan", "çevre", "üçgen", "kare"]):
            reply = ('<span class="expert-badge badge-sayisal">Geometri & Matematik Formülleri</span><br>'
                     '• <b>Alan Hesaplama:</b> Kare = a², Dikdörtgen = a × b, Üçgen = (Taban × Yükseklik) / 2<br>'
                     '• <b>Çevre Hesaplama:</b> Kare = 4a, Dikdörtgen = 2(a+b), Çember = 2πr')

        # --- 📝 TÜRKÇE DİL BİLGİSİ MODÜLÜ ---
        elif any(x in user_message for x in ["türkçe", "mecaz", "gerçek anlam", "deyim", "atasözü", "zamir", "sıfat"]):
            reply = ('<span class="expert-badge badge-sozel">Türkçe Dil Bilgisi</span><br>'
                     '• <b>Gerçek Anlam:</b> Sözcüğün akla gelen ilk anlamıdır.<br>'
                     '• <b>Mecaz Anlam:</b> Gerçek anlamından tamamen uzaklaşmış yeni anlamdır.<br>'
                     '• <b>Sözcük Türleri:</b> Sıfatlar isimlerin önüne gelerek onları niteler. Zamirler ise ismin yerini tutar.')

        # --- 🇬🇧 İNGİLİZCE MODÜLÜ ---
        elif any(x in user_message for x in ["ingilizce", "english", "tense", "kelime", "günler"]):
            reply = ('<span class="expert-badge badge-sozel">English Language Core</span><br>'
                     '• <b>Simple Present (Geniş Zaman):</b> I/You/We/They + Verb | He/She/It + Verb(-s).<br>'
                     '• <b>Days of the Week:</b> Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday.')

        # --- ⚡ FİZİK / HIZ FORMÜLÜ ---
        elif "hız" in user_message or "hiz" in user_message:
            reply = '<span class="expert-badge badge-sayisal">Fizik Analizi</span><br><div class="formula-box">V = x / t</div><b>V:</b> Hız (m/s), <b>x:</b> Alınan Yol (metre), <b>t:</b> Zaman (saniye).'
            
        # --- SOHBET ŞABLONLARI ---
        elif "selam" in user_message or "merhaba" in user_message:
            reply = "Selam **TÜW**! **ARIES AI** genişletilmiş tarih, coğrafya ve bilim çekirdeğiyle aktif, seni dinliyorum."
        elif "kanka" in user_message or "naber" in user_message:
            reply = "Harikayım kanka! ARIES şu an tam bir tarih ve coğrafya dehası oldu. İstediğin savaşı, antlaşmayı, boğazı veya iklim tipini sorabilirsin, hemen analiz edeyim!"
        else:
            reply = "ARIES Zeka Motoru veriyi taradı ancak tam eşleşme bulamadı. Bana matematik, fen, türkçe, tarih, coğrafya veya ingilizce ile ilgili dilediğin konuyu sorabilirsin Kaptan!"

    return jsonify({"reply": reply})

if __name__ == '__main__':
    app.run(debug=True)
