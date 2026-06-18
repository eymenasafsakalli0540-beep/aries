from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Küresel Coğrafya Veri Tabanı
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
        "mat": "matematik", "ing": "ingilizce", "fen": "fen bilimleri", "sos": "sosyal"
    }
    for key, val in shortcuts.items():
        user_message = user_message.replace(f" {key} ", f" {val} ")
        if user_message.startswith(key): user_message = user_message.replace(key, val, 1)
        if user_message.endswith(key): user_message = user_message[:-len(key)] + val

    reply = ""
    math_chars = set("0123456789+-*/(). ")
    
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
        
        elif any(x in user_message for x in ["fen", "hücre", "organel", "mitokondri", "dna", "element", "asit", "baz"]):
            reply = ('<span class="expert-badge badge-sayisal">Fen Bilimleri Laboratuvarı</span><br>'
                     '• <b>Hücre Yapısı:</b> Hücre zarı (korur), Sitoplazma (yaşamsal faaliyetler), Çekirdek (yönetim merkezidir).<br>'
                     '• <b>Enerji Odası (Mitokondri):</b> Hücrenin besinleri enerjiye (ATP) dönüştürdüğü yerdir. 🌱 Kloroplast ise bitkilerde fotosentez yapar.<br>'
                     '• <b>Kritik Kimya:</b> Asitlerin pH değeri 0-7 arasıdır (ekşidir), Bazların pH değeri 7-14 arasıdır (acıdır ve ele kayganlık verir).')

        elif any(x in user_message for x in ["matematik", "geometri", "formül", "alan", "çevre", "üçgen", "kare"]):
            reply = ('<span class="expert-badge badge-sayisal">Geometri & Matematik Formülleri</span><br>'
                     '• <b>Alan Hesaplama:</b> Kare = a², Dikdörtgen = a × b, Üçgen = (Taban × Yükseklik) / 2<br>'
                     '• <b>Çevre Hesaplama:</b> Kare = 4a, Dikdörtgen = 2(a+b), Çember = 2πr<br>'
                     '• <b>Bilinmesi Gerekenler:</b> Bir üçgenin iç açıları toplamı her zaman 180° derecedir.')

        elif any(x in user_message for x in ["türkçe", "mecaz", "gerçek anlam", "deyim", "atasözü", "zamir", "sıfat"]):
            reply = ('<span class="expert-badge badge-sozel">Türkçe Dil Bilgisi</span><br>'
                     '• <b>Gerçek Anlam:</b> Sözcüğün akla gelen ilk anlamıdır. (Örn: "Kuru odunları yaktık.")<br>'
                     '• <b>Mecaz Anlam:</b> Gerçek anlamından tamamen uzaklaşmış yeni anlamdır. (Örn: "Bize çok kuru davrandı.")<br>'
                     '• <b>Sözcük Türleri:</b> Sıfatlar isimlerin önüne gelerek onları niteler (Örn: Kırmızı araba). Zamirler ise ismin yerini tutar (Örn: O, bunu, şunlar).')

        elif any(x in user_message for x in ["sosyal", "tarih", "coğrafya", "istanbul", "fetih", "malazgirt", "cumhuriyet", "iklim"]):
            if "istanbul" in user_message and "fetih" in user_message:
                reply = '<span class="expert-badge badge-sozel">Tarih Analizi</span><br><b>İstanbul\'un Fethi (1453):</b> Fatih Sultan Mehmet komutasında yapılmıştır. Bizans İmparatorluğu yıkılmış, Orta Çağ kapanıp Yeni Çağ başlamıştır.'
            elif "malazgirt" in user_message:
                reply = '<span class="expert-badge badge-sozel">Tarih Analizi</span><br><b>Malazgirt Savaşı (1071):</b> Büyük Selçuklu Hükümdarı Sultan Alparslan\'ın Bizans\'ı yendiği ve Anadolu\'nun kapılarını Türklere açtığı tarihi zaferdir.'
            else:
                reply = ('<span class="expert-badge badge-cografya">Sosyal Bilgiler Çekirdeği</span><br>'
                         '• <b>Kronoloji:</b> 1071 Malazgirt ➔ 1453 İstanbul\'un Fethi ➔ 1919 Kurtuluş Savaşı Başlangıcı ➔ 1923 Cumhuriyet\'in İlanı 🇹🇷<br>'
                         '• <b>İklim Tipleri:</b> Akdeniz (Yazlar sıcak/kurak), Karadeniz (Her mevsim yağışlı), Karasal (Kışlar soğuk/karlı).')

        elif any(x in user_message for x in ["ingilizce", "english", "tense", "kelime", "günler"]):
            reply = ('<span class="expert-badge badge-sozel">English Language Core</span><br>'
                     '• <b>Simple Present (Geniş Zaman):</b> I/You/We/They + Verb | He/She/It + Verb(-s). (Örn: She likes coding.)<br>'
                     '• <b>Soru Kalıpları:</b> What (Ne), Who (Kim), Where (Nerede), When (Ne zaman), Why (Neden), How (Nasıl).<br>'
                     '• <b>Days of the Week:</b> Monday (Pzt), Tuesday (Sal), Wednesday (Çar), Thursday (Per), Friday (Cum), Saturday (Cmt), Sunday (Paz).')

        elif "hız" in user_message or "hiz" in user_message:
            reply = '<span class="expert-badge badge-sayisal">Fizik Analizi</span><br><div class="formula-box">V = x / t</div><b>V:</b> Hız (m/s), <b>x:</b> Alınan Yol (metre), <b>t:</b> Zaman (saniye).'
            
        elif "selam" in user_message or "merhaba" in user_message:
            reply = "Selam **TÜW**! **ARIES AI** dahi eğitim ve analiz çekirdeğiyle aktif, seni dinliyorum."
        elif "kanka" in user_message or "naber" in user_message:
            reply = "Harikayım kanka! Sistemi tamamen yeniledik; Fen, Matematik, Türkçe, Sosyal ve İngilizce derslerinde bir dehayım artık. Ne analiz etmemi istersin?"
        else:
            reply = "ARIES Zeka Motoru veriyi yerel veri tabanında taradı ancak tam eşleşme bulamadı. Bana matematik, fen, türkçe, tarih, coğrafya veya ingilizce ile ilgili dilediğin terimi sorabilirsin Kaptan!"

    return jsonify({"reply": reply})

if __name__ == '__main__':
    app.run(debug=True)
