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
    # Türkçe karakter hatalarını ve yazım esnekliklerini normalize etme
    user_message = request.json.get("message", "").lower().strip()
    
    # Harf ve Karakter Normalizasyonu (Hatalı yazımları yumuşatır)
    norm_msg = user_message.replace("ı", "i").replace("ğ", "g").replace("ü", "u").replace("ş", "s").replace("ö", "o").replace("ç", "c")
    norm_msg = norm_msg.replace("'", "").replace("-", "").replace("’", "")

    # Kısaltma ve Sık Yapılan Hata Çözücü
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
        # Ülke isimlerindeki yazım hatalarını yakalama
        found_country = None
        for country in global_geography:
            norm_country = country.replace("ı", "i").replace("ğ", "g").replace("ü", "u").replace("ş", "s").replace("ö", "o").replace("ç", "c")
            if norm_country in norm_msg or country in user_message:
                found_country = country
                break
                
        if found_country:
            data = global_geography[found_country]
            if "baskent" in norm_msg or "neren" in norm_msg:
                reply = f'<span class="expert-badge badge-cografya">Küresel Coğrafya</span><br><b>Bölge:</b> {found_country.upper()}<br><b>Başkenti:</b> {data["b"]}<br><b>Bulunduğu Kıta:</b> {data["k"]}'
            elif "aras" in norm_msg or "km" in norm_msg or "kac" in norm_msg:
                reply = f'<span class="expert-badge badge-cografya">Mesafe Analizi</span><br><b>Rota:</b> Türkiye ➔ {found_country.upper()}<br><b>Uzaklık:</b> {data["m"]}<br><b>Konum:</b> {data["k"]}'
            else:
                reply = f'<span class="expert-badge badge-cografya">Genel Bilgi</span><br><b>Bölge:</b> {found_country.upper()}<br><b>Başkent:</b> {data["b"]}<br><b>Mesafe:</b> {data["m"]}'
        
        # --- ⏳ ULTRA TARİH ANALİZ MOTORU (Yazım Hatası Korumalı) ---
        elif any(x in norm_msg for x in ["tarih", "savas", "osmanli", "kurtulus", "ataturk", "cumhuriyet", "dunya savas", "antlasma", "fetih", "malazgirt"]):
            if "istanbul" in norm_msg and ("fet" in norm_msg or "fih" in norm_msg):
                reply = '<span class="expert-badge badge-sozel">Tarih: Osmanlı Dönemi</span><br><b>İstanbul\'un Fethi (1453):</b> II. Mehmed (Fatih) tarafından Bizans\'a son verildi. Orta Çağ bitti, Yeni Çağ başladı. İpek Yolu kontrolü Osmanlı\'ya geçti.'
            elif "malazgirt" in norm_msg or "malasgirt" in norm_msg:
                reply = '<span class="expert-badge badge-sozel">Tarih: Selçuklu Dönemi</span><br><b>Malazgirt Savaşı (1071):</b> Sultan Alparslan komutasındaki Büyük Selçuklu Devleti, Bizans\'ı mağlup etti. Anadolu\'nun kapıları Türklere tamamen açıldı.'
            elif "kurtulus" in norm_msg or "milli mucadele" in norm_msg:
                reply = '<span class="expert-badge badge-sozel">Tarih: Milli Mücadele</span><br><b>Kurtuluş Savaşı (1919-1922):</b> Mustafa Kemal Paşa\'nın 19 Mayıs 1919\'da Samsun\'a çıkmasıyla başladı. Başkomutanlık Meydan Muharebesi ile düşman Anadolu\'dan temizlendi ve Lozan Antlaşması ile taçlandı.'
            elif "osmanli" in norm_msg and ("kurul" in norm_msg or "osman bey" in norm_msg):
                reply = '<span class="expert-badge badge-sozel">Tarih: Osmanlı Devleti</span><br><b>Kuruluş (1299):</b> Osman Bey tarafından Söğüt ve Domaniç çevresinde bir beylik olarak kuruldu. Kısa sürede büyüyerek cihan imparatorluğuna dönüştü.'
            elif "dunya savas" in norm_msg:
                reply = '<span class="expert-badge badge-sozel">Tarih: Yakın Çağ</span><br>• <b>I. Dünya Savaşı (1914-1918):</b> İttifak ve İtilaf devletleri arasında oldu. Osmanlı bu savaşta yer aldı.<br>• <b>II. Dünya Savaşı (1939-1945):</b> Mihver (Almanya, İtalya, Japonya) ve Müttefik (İngiltere, SSCB, ABD) güçleri arasında yaşandı.'
            else:
                reply = ('<span class="expert-badge badge-sozel">Gelişmiş Tarih Arşivi</span><br>'
                         '• <b>1071:</b> Malazgirt Savaşı (Anadolu\'nun kapısı açıldı)<br>'
                         '• <b>1453:</b> İstanbul\'un Fethi (Cihan imparatorluğu dönemi)<br>'
                         '• <b>1919:</b> 19 Mayıs Atatürk\'ün Samsun\'a çıkışı<br>'
                         '• <b>1923:</b> 29 Ekim Cumhuriyet\'in İlanı 🇹🇷')

        # --- 🌍 ULTRA COĞRAFYA ANALİZ MOTORU (Yazım Hatası Korumalı) ---
        elif any(x in norm_msg for x in ["cografya", "iklim", "dag", "bogaz", "ova", "nehir", "harita", "olcek", "kesif"]):
            if "bogaz" in norm_msg or "kanal" in norm_msg:
                reply = ('<span class="expert-badge badge-cografya">Coğrafya: Stratejik Geçitler</span><br>'
                         '• <b>İstanbul ve Çanakkale Boğazları:</b> Karadeniz\'i Akdeniz\'e bağlayan en kritik su yollarıdır.<br>'
                         '• <b>Süveyş Kanalı:</b> Mısır\'da yer alır, Akdeniz ile Kızıldeniz\'i birleştirerek ticaret rotalarını kısaltır.<br>'
                         '• <b>Cebelitarık Boğazı:</b> Akdeniz\'i Atlas Okyanusu\'na bağlar.')
            elif "dag" in norm_msg or "ova" in norm_msg:
                reply = ('<span class="expert-badge badge-cografya">Coğrafya: Yer Şekilleri</span><br>'
                         '• <b>En Yüksek Noktalar:</b> Dünyada Everest Dağı (8.848 m), Türkiye\'de ise Ağrı Dağı (5.137 m) zirvedir.<br>'
                         '• <b>Ova ve Delta:</b> Türkiye\'nin en büyük delta ovası Çukurova\'dır. Seyhan ve Ceyhan nehirleri tarafından beslenir.')
            elif "iklim" in norm_msg:
                reply = ('<span class="expert-badge badge-cografya">Coğrafya: İklim Bilimi</span><br>'
                         '• <b>Akdeniz İklimi:</b> Yazlar sıcak ve kurak, kışlar ılık ve yağışlıdır. Bitki örtüsü makidir.<br>'
                         '• <b>Karasal İklim:</b> Kışlar çok soğuk ve karlı, yazlar sıcak geçer. Bitki örtüsü bozkırdır.<br>'
                         '• <b>Ekvatoral İklim:</b> Her mevsim sıcak ve her mevsim bol yağışlıdır.')
            else:
                reply = ('<span class="expert-badge badge-cografya">Gelişmiş Coğrafya Modülü</span><br>'
                         '• <b>Ölçek:</b> Haritalardaki küçültme oranıdır. Ölçek büyüdükçe ayrıntı artar.<br>'
                         '• <b>Paralel ve Meridyenler:</b> 180 paralel, 360 meridyen yayı bulunur. İki meridyen arası zaman farkı 4 dakikadır.')

        # --- 🧪 FEN BİLİMLERİ MODÜLÜ (Yazım Hatası Korumalı) ---
        elif any(x in norm_msg for x in ["fen", "hucre", "organel", "mitokondri", "dna", "element", "asit", "baz", "kloroplast"]):
            reply = ('<span class="expert-badge badge-sayisal">Fen Bilimleri Laboratuvarı</span><br>'
                     '• <b>Hücre Yapısı:</b> Hücre zarı (korur), Sitoplazma (yaşamsal faaliyetler), Çekirdek (yönetim merkezidir).<br>'
                     '• <b>Enerji Odası (Mitokondri):</b> Hücrenin besinleri enerjiye (ATP) dönüştürdüğü yerdir. 🌱 Kloroplast ise bitkilerde fotosentez yapar.<br>'
                     '• <b>Kritik Kimya:</b> Asitlerin pH değeri 0-7 arasıdır (ekşidir), Bazların pH değeri 7-14 arasıdır (acıdır).')

        # --- 🧮 MATEMATİK & GEOMETRİ FORMÜLLERİ (Yazım Hatası Korumalı) ---
        elif any(x in norm_msg for x in ["matematik", "matamatik", "geometri", "formul", "alan", "cevre", "ucgen", "kare"]):
            reply = ('<span class="expert-badge badge-sayisal">Geometri & Matematik Formülleri</span><br>'
                     '• <b>Alan Hesaplama:</b> Kare = a², Dikdörtgen = a × b, Üçgen = (Taban × Yükseklik) / 2<br>'
                     '• <b>Çevre Hesaplama:</b> Kare = 4a, Dikdörtgen = 2(a+b), Çember = 2πr')

        # --- 📝 TÜRKÇE DİL BİLGİSİ MODÜLÜ (Yazım Hatası Korumalı) ---
        elif any(x in norm_msg for x in ["turkce", "mecaz", "gercek anlam", "deyim", "atasozu", "zamir", "sifat"]):
            reply = ('<span class="expert-badge badge-sozel">Türkçe Dil Bilgisi</span><br>'
                     '• <b>Gerçek Anlam:</b> Sözcüğün akla gelen ilk anlamıdır.<br>'
                     '• <b>Mecaz Anlam:</b> Gerçek anlamından tamamen uzaklaşmış yeni anlamdır.<br>'
                     '• <b>Sözcük Türleri:</b> Sıfatlar isimlerin önüne gelerek onları niteler. Zamirler ise ismin yerini tutar.')

        # --- 🇬🇧 İNGİLİZCE MODÜLÜ (Yazım Hatası Korumalı) ---
        elif any(x in norm_msg for x in ["ingilizce", "english", "tense", "kelime", "gunler"]):
            reply = ('<span class="expert-badge badge-sozel">English Language Core</span><br>'
                     '• <b>Simple Present (Geniş Zaman):</b> I/You/We/They + Verb | He/She/It + Verb(-s).<br>'
                     '• <b>Days of the Week:</b> Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday.')

        # --- ⚡ FİZİK / HIZ FORMÜLÜ ---
        elif "hiz" in norm_msg or "hız" in norm_msg:
            reply = '<span class="expert-badge badge-sayisal">Fizik Analizi</span><br><div class="formula-box">V = x / t</div><b>V:</b> Hız (m/s), <b>x:</b> Alınan Yol (metre), <b>t:</b> Zaman (saniye).'
            
        # --- SOHBET ŞABLONLARI ---
        elif "selam" in norm_msg or "merhaba" in norm_msg or "slm" in norm_msg:
            reply = "Selam **TÜW**! **ARIES AI** gelişmiş esnek analiz çekirdeğiyle aktif, harf hatalarını dert etme dinliyorum."
        elif "kanka" in norm_msg or "naber" in norm_msg or "knk" in norm_msg:
            reply = "İyidir kanka! Artık 'matamatik' veya 'corafya' yazsan bile şak diye ne demek istediğini anlayan dahi bir sistemim var. Ne sormak istersin?"
        else:
            reply = "ARIES Zeka Motoru girdiyi filtreledi ancak tam eşleşme bulamadı. Bana matematik, fen, türkçe, tarih, coğrafya veya ingilizce ile ilgili dilediğin konuyu sorabilirsin Kaptan!"

    return jsonify({"reply": reply})

if __name__ == '__main__':
    app.run(debug=True)
