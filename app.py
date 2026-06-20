from flask import Flask, render_template, request, jsonify
import math
import requests
import os
import re  
from datetime import datetime  
from bs4 import BeautifulSoup  

app = Flask(__name__)

# 🌍 MEGA COĞRAFYA VERİ TABANI
world_countries = {
    "turkiye": {"b": "Ankara", "k": "Asya/Avrupa", "lat": 39.93, "lon": 32.85, "bilgi": "Asya ve Avrupa'yı birbirine bağlayan, üç tarafı denizlerle çevrili, şanlı bir tarihe sahip stratejik bir köprü ülkedir. En büyük şehri İstanbul'dur."},
    "hindistan": {"b": "Yeni Delhi", "k": "Asya", "lat": 28.61, "lon": 77.20, "bilgi": "Güney Asya'da yer alan, dünyanın en kalabalık nüfumuna sahip, Tac Mahal gibi devasa tarihi eserleri barındıran rengarenk bir kültür ülkesidir."},
    "kuba": {"b": "Havana", "k": "Karayipler", "lat": 23.11, "lon": -82.36, "bilgi": "Karayip Denizi'nde yer alan, kendine has müzikleri, puroları, klasik arabaları ve tarihi mimarisiyle ünlü bir ada devletidir."},
    "abd": {"b": "Washington D.C.", "k": "Kuzey Amerika", "lat": 38.90, "lon": -77.03, "bilgi": "Kuzey Amerika kıtasında bulunan, 50 eyaletten oluşan, ekonomik ve teknolojik açıdan küresel bir süper güçtür."},
    "amerika": {"b": "Washington D.C.", "k": "Kuzey Amerika", "lat": 38.90, "lon": -77.03, "bilgi": "Kuzey Amerika kıtasında bulunan küresel bir federal devlettir."},
    "rusya": {"b": "Moskova", "k": "Asya/Avrupa", "lat": 55.75, "lon": 37.61, "bilgi": "Yüzölçümü bakımından dünyanın en büyük ülkesidir. Devasa doğal gaz ve yer altı kaynaklarına sahip, iki kıtaya yayılmış bir devdir."},
    "almanya": {"b": "Berlin", "k": "Avrupa", "lat": 52.52, "lon": 13.40, "bilgi": "Orta Avrupa'da yer alan; Mercedes, BMW gibi markaları üreten, sanayisi, mühendisliği ve teknolojisi son derece gelişmiş bir Avrupa gücüdür."},
    "fransa": {"b": "Paris", "k": "Avrupa", "lat": 48.85, "lon": 2.35, "bilgi": "Batı Avrupa'da bulunan; sanat, moda, Eyfel Kulesi, gurme mutfağı ve köklü siyasi tarihiyle tanınan lider bir ülkedir."},
    "ingiltere": {"b": "Londra", "k": "Avrupa", "lat": 51.50, "lon": -0.12, "bilgi": "Büyük Britanya adasında yer alan, geçmişte 'üzerinde güneş batmayan imparatorluk' olarak bilinen köklü ve güçlü bir denizci ülkesidir."},
    "hollanda": {"b": "Amsterdam", "k": "Avrupa", "lat": 52.36, "lon": 4.90, "bilgi": "Topraklarının büyük kısmı deniz seviyesinin altında olan, bendlerle korunan, yel değirmenleri, kanalları ve laleleriyle ünlü Batı Avrupa ülkesidir."},
    "italya": {"b": "Roma", "k": "Avrupa", "lat": 41.90, "lon": 12.49, "bilgi": "Akdeniz'e uzanan çizme şeklindeki yarımadada kurulmuş; Pisa Kulesi, Kolezyum gibi eserlere sahip Roma İmparatorluğu'nun beşiğidir."},
    "japonya": {"b": "Tokyo", "k": "Asya", "lat": 35.67, "lon": 139.65, "bilgi": "Doğu Asya'da bir ada ülkesidir. Robotik teknolojisi, otomotiv sanayisi, anime kültürü ve köklü samuray gelenekleriyle tanınır."},
    "mısır": {"b": "Kahire", "k": "Afrika", "lat": 30.04, "lon": 31.23, "bilgi": "Kuzey Afrika ile Orta Doğu'yu bağlayan, insanlık tarihinin en eski medeniyetlerinden biri olan, Nil Nehri ve antik Gize Piramitleri'nin ev sahibidir."},
    "brezilya": {"b": "Brasilia", "k": "Güney Amerika", "lat": -15.79, "lon": -47.88, "bilgi": "Güney Amerika'nın en büyük ve en kalabalık ülkesidir. Dünyanın oksijen deposu olan Amazon Ormanları'na ve futbol kültürüne ev sahipliği yapar."},
    "azerbaycan": {"b": "Bakü", "k": "Asya", "lat": 40.40, "lon": 49.86, "bilgi": "Kafkasya'da yer alan, zengin petrol ve doğal gaz yataklarına sahip, Türkiye ile köklü bağları olan kardeş ülkedir."},
    "cin": {"b": "Pekin", "k": "Asya", "lat": 39.90, "lon": 116.40, "bilgi": "Doğu Asya'da devasa bir üretim gücüne ve milyarlık nüfusa sahip, dünyanın en uzun savunma duvarı olan Çin Seddi ile ünlü kadim bir ülkedir."},
    "kanada": {"b": "Ottava", "k": "Kuzey Amerika", "lat": 45.42, "lon": -75.69, "bilgi": "Dünyanın en geniş yüzölçümüne sahip ikinci ülkesidir. Soğuk iklimi, gölleri ve yüksek yaşam kalitesiyle bilinir."},
    "ispanya": {"b": "Madrid", "k": "Avrupa", "lat": 40.41, "lon": -3.70, "bilgi": "İber Yarımadası'nda yer alan; Endülüs İslam tarihi kalıntıları, mimarisi ve spor kültürüyle ünlü bir Akdeniz ülkesidir."},
    "guney afrika": {"b": "Pretoria", "k": "Afrika", "lat": -25.74, "lon": 28.18, "bilgi": "Afrika kıtasının en güney ucunda yer alan, maden kaynakları bakımından zengin ve çeşitliliğe sahip bir devlettir."},
    "avustralya": {"b": "Kanberra", "k": "Okyanusya", "lat": -35.28, "lon": 149.13, "bilgi": "Kendi başına bir kıta olan ada ülkesidir. Kendine has faunası ve yüksek gelişmişlik düzeyiyle tanınır."}
}

# 📜 UPUPUZUN TARİH VERİ TABANI
historical_events = {
    "istanbulun fethi": "<b>1453 - İstanbul'un Fethi:</b> Fatih Sultan Mehmed liderliğindeki Osmanlı ordusu Bizans İmparatorluğu'nu yıkarak şehri fethetti. Bu olayla Orta Çağ kapanmış, Yeni Çağ başlamıştır.",
    "cumhuriyetin ilani": "<b>29 Ekim 1923 - Cumhuriyetin İlanı:</b> Gazi Mustafa Kemal Atatürk önderliğinde kazanılan Kurtuluş Savaşı'nın ardından Türkiye Cumhuriyeti resmen kurulmuş ve egemenlik kayıtsız şartsız millete geçmiştir. 🇹🇷",
    "malazgirt": "<b>1071 - Malazgirt Meydan Muharebesi:</b> Büyük Selçuklu Sultanı Alparslan komutasındaki Türk ordusu, Bizans ordusunu mağlup ederek Anadolu'nun kapılarını açmıştır.",
    "buyuk taarruz": "<b>30 Ağustos 1922 - Büyük Taarruz:</b> Başkomutanlık Meydan Muharebesi ile işgalci ordular bozguna uğratılmış ve Anadolu toprakları tamamen bağımsızlığına kavuşmuştur.",
    "1 dunya savasi": "<b>1914 - 1918 (I. Dünya Savaşı):</b> İtilaf ve İttifak devletleri arasında gerçekleşen, Osmanlı İmparatorluğu'nun Çanakkale Cephesi'nde tarihi bir savunma gerçekleştirdiği küresel savaştır.",
    "2 dunya savasi": "<b>1939 - 1945 (II. Dünya Savaşı):</b> Mihver ve Müttefik devletler arasında geçen, nükleer silahların kullanıldığı insanlık tarihinin en büyük küresel çatışmasıdır.",
    "fransiz ihtilali": "<b>1789 - Fransız İhtilali:</b> Fransa'da mutlak monarşinin yıkılmasıyla sonuçlanan; dünyaya milliyetçilik, hürriyet ve eşitlik fikirlerini yayarak Yakın Çağ'ı başlatan tarihi olaydır.",
    "ronesans": "<b>14. - 17. Yüzyıl (Rönesans):</b> İtalya'da başlayan; bilim, sanat ve felsefede yeniden doğuşu simgeleyen, modern Avrupa'nın temelini atan dönemdir.",
    "cografi kesifler": "<b>15. ve 16. Yüzyıl - Coğrafi Keşifler:</b> Avrupalı denizcilerin yeni ticaret yolları ve kıtalar bulmak amacıyla başlattığı büyük keşif hareketleridir.",
    "reform": "<b>16. Yüzyıl - Reform Dönemi:</b> Avrupa'da dini kurumlara karşı gelişen, eğitim ve düşüncenin kilise baskısından kurtulmasını sağlayan yenilik hareketidir."
}

# 🕋 UPUPUZUN DİNİ TERİMLER VERİ TABANI
religious_database = {
    "hicret": "<b>Hicret (622):</b> Hz. Muhammed (s.a.v.) ve Müslümanların, Mekke'deki baskılar nedeniyle Medine'ye göç etmesidir. İslam devletinin kuruluş temeli ve Hicri takvimin başlangıcıdır.",
    "bedir savasi": "<b>Bedir Savaşı (624):</b> Müslümanlar ile Mekkeli müşrikler arasındaki ilk büyük savaştır. Müslüman ordusunun zaferiyle sonuçlanmış ve İslam'ın askeri gücünü kanıtlamıştır.",
    "uhud savasi": "<b>Uhud Savaşı (625):</b> Stratejik mevkideki okçuların yerlerini terk etmesi sonucu Müslüman ordusunun zor anlar yaşadığı ve Hz. Hamza'nın şehit düştüğü savaştır.",
    "hendek savasi": "<b>Hendek Savaşı (627):</b> Medine çevresine hendekler kazılarak gerçekleştirilen, askeri strateji ve sabır odaklı başarılı bir savunma savaşıdır.",
    "mekkenin fethi": "<b>Meke'nin Fethi (630):</b> İslam ordusunun kan dökmeden, büyük bir barış ve merhametle Mekke'ye girmesi ve Kabe'yi putlardan temizlemesi olayıdır.",
    "dort halife": "<b>Dört Halife Dönemi:</b> Hz. Muhammed'den sonra İslam devletini sırasıyla yöneten mübarek liderlerdir:<br>1. Hz. Ebubekir<br>2. Hz. Ömer<br>3. Hz. Osman<br>4. Hz. Ali",
    "fikih": "<b>Fıkıh İlmi:</b> İslam'ın ibadet, sosyal ve hukuki kurallarını delilleriyle birlikte inceleyen İslam hukuku bilim dalıdır.",
    "tefsir": "<b>Tefsir İlmi:</b> Kur'an-ı Kerim ayetlerinin anlamlarını, iniş sebeplerini ve inceliklerini açıklayan bilim dalıdır.",
    "hadis": "<b>Hadis-i Şerif:</b> Hz. Muhammed'in (s.a.v.) sözleri, davranışları ve ashabının uygulamalarına verdiği onayların bütününü ifade eder.",
    "kelam": "<b>Kelam İlmi:</b> İslam dininin inanç esaslarını akli ve nakli delillerle açıklayan ve savunan ilim dalıdır.",
    "akait": "<b>Akait:</b> İslam dininde inanılması zorunlu olan temel iman esaslarının (Amentü esasları) bütünüdür.",
    "siyer": "<b>Siyer Bilimi:</b> Peygamberimiz Hz. Muhammed'in (s.a.v.) hayatını, şahsiyetini ve mücadelelerini kronolojik olarak inceleyen bilim dalıdır."
}

# 🧬 UPUPUZUN ANATOMİ VE FEN VERİ TABANI
science_database = {
    "kalp": "<b>Anatomi - Kalp:</b> Göğüs boşluğunda yer alan, kaslı yapısıyla kanı tüm vücuda pompalamakla görevli hayati organdır. 2 kulakçık ve 2 karıncık olmak üzere 4 odacıktan oluşur.",
    "akciyer": "<b>Anatomi - Akciğer:</b> Solunum sisteminin ana organıdır. Havadan alınan oksijenin kana geçmesini, kandaki karbondioksitin ise dışarı atılmasını sağlar.",
    "karaciyer": "<b>Anatomi - Karaciğer:</b> Vücudun en büyük iç organıdır. Toksinleri arındırır, safra üretir, glikoz depolar ve metabolik faaliyetlerin merkezidir.",
    "mide": "<b>Anatomi - Mide:</b> Sindirim sisteminin kaslı organıdır. Salgıladığı güçlü asit ve enzimlerle besinleri kimyasal ve mekanik olarak parçalar.",
    "beyin": "<b>Anatomi - Beyin:</b> Merkezi sinir sisteminin yönetim merkezidir. Hafıza, düşünme, duyular ve tüm organların koordinasyonunu kontrol eder.",
    "hucre": "<b>Fen Bilgisi - Hücre:</b> Canlılığın en küçük yapı taşıdır. Hücre zarı, sitoplazma ve yönetim merkezi olan çekirdek (DNA) olmak üzere 3 ana kısımdan oluşur.",
    "fotosentez": "<b>Fen Bilgisi - Fotosentez:</b> Klorofil taşıyan canlıların ışık enerjisi yardımıyla karbondioksit (CO2) ve su (H2O) kullanarak kendi besinlerini ve oksijen (O2) üretmesi olayıdır.",
    "mitokondri": "<b>Fen Bilgisi - Mitokondri:</b> Hücrenin enerji santralidir. Oksijenli solunum yoluyla hücrenin hayati faaliyetlerinde ihtiyaç duyduğu ATP moleküllerini sentezler."
}

# ⚡ UPUPUZUN FİZİK VE GEOMETRİ VERİ TABANI
physics_geometry_database = {
    "yercekimi": "<b>Fizik - Yerçekimi Kuvveti:</b> Büyük kütleli cisimlerin etrafındaki nesnelere uyguladığı çekim kuvvetidir. Dünya yüzeyindeki ivmesi g = 9.81 m/s2 kabul edilir. Formülü F = m * g şeklindedir.",
    "surtunme": "<b>Fizik - Sürtünme Kuvveti:</b> Temas halindeki iki yüzey arasında harekete karşı oluşan direnç kuvvetidir. Kinetik enerjiyi ısı enerjisine dönüştürür. Formülü: Fs = k * N şeklindedir.",
    "ohm kanunu": "<b>Fizik - Ohm Kanunu:</b> Bir elektrik devresindeki gerilim (V), akım (I) ve direnç (R) arasındaki ilişkiyi belirtir. Temel formülü V = I * R şeklindedir.",
    "ucgen": "<b>Geometri - Üçgen:</b> Doğrusal olmayan üç noktanın birleşmesiyle oluşan kapalı geometrik şekildir. İç açılarının toplamı 180 derece, dış açılarının toplamı 360 derecedir. Alanı: (Taban * Yükseklik) / 2 şeklindedir.",
    "kare": "<b>Geometri - Kare:</b> Tüm kenarları eşit ve iç açıları 90 derece olan düzgün dörtgendir. Bir kenarı 'a' ise Çevresi: 4 * a, Alanı ise Alan = a * a formülüyle hesaplanır.",
    "dikdortgen": "<b>Geometri - Dikdörtgen:</b> Karşılıklı kenarları eşit ve paralel, iç açıları 90 derece olan dörtgendir. Kenarları 'a' ve 'b' ise Çevresi: 2 * (a + b), Alanı: a * b şeklindedir.",
    "daire": "<b>Geometri - Daire:</b> Çember ve iç bölgesinin oluşturduğu alandır. Yarıçapı 'r' ise Çevresi: 2 * pi * r, Alanı ise Alan = pi * r * r formülüyle bulunur."
}

def google_gibi_ara(sorgu):
    try:
        url = f"https://html.duckduckgo.com/html/?q={sorgu}"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        response = requests.get(url, headers=headers, timeout=5)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            result = soup.find('a', class_='result__snippet')
            if result:
                return result.text.strip()
    except:
        pass
    return None

def fetch_country_from_api(country_name):
    try:
        url = f"https://restcountries.com/v3.1/name/{country_name}"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()[0]
            name_tr = data.get("translations", {}).get("tur", {}).get("common", country_name).upper()
            capital = data.get("capital", ["Bilinmiyor"])[0]
            region = data.get("continents", ["Bilinmiyor"])[0]
            return {"name": name_tr, "b": capital, "k": region, "bilgi": f"🌐 {name_tr}, {region} kıtasında yer alan bir ülkedir."}
    except:
        pass
    return None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/get-logs', methods=['POST', 'OPTIONS'])
def get_logs():
    response_headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type"
    }
    if request.method == 'OPTIONS': return jsonify({"success": True}), 200, response_headers

    data = request.json or {}
    password = data.get('password', '')
    action = data.get('action', 'get')
    
    if password != "F89B2A.ey": 
        return jsonify({"success": False, "message": "Hatalı şifre!"}), 403, response_headers

    if action == 'clear':
        if os.path.exists("sorular.txt"): os.remove("sorular.txt")
        return jsonify({"success": True, "logs": []}), 200, response_headers

    if os.path.exists("sorular.txt"):
        with open("sorular.txt", "r", encoding="utf-8") as file: logs = file.readlines()
        clean_logs = [line.strip() for line in logs if line.strip()]
        return jsonify({"success": True, "logs": list(reversed(clean_logs)) if clean_logs else ["Soru geçmişi temiz."]}), 200, response_headers
    return jsonify({"success": True, "logs": ["Soru geçmişi temiz."]}), 200, response_headers

@app.route('/ask', methods=['POST'])
def ask():
    user_message = request.json.get("message", "").lower().strip()
    raw_message = request.json.get("message", "").strip() 
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    user_ip = request.remote_addr  
    
    def save_log(status_msg):
        with open("sorular.txt", "a", encoding="utf-8") as file:
            file.write(f"[{current_time}] IP: {user_ip} | DURUM: {status_msg} -> Soru: {raw_message}\n")

    # Dinamik Üslup Motoru: Kullanıcı "kanka" dedi mi?
    is_kanka_mode = "kanka" in user_message or "knk" in user_message
    suffix = " kanka." if is_kanka_mode else "."

    user_message = re.sub(r'[.,\?!;\(\)"\'’\-]', '', user_message)
    norm_msg = user_message.replace("ı", "i").replace("ğ", "g").replace("ü", "u").replace("ş", "s").replace("ö", "o").replace("ç", "c")

    typo_rules = {
        "nber": "naber", "nbr": "naber", "slm": "selam", "mrb": "merhaba", 
        "mrhb": "merhaba", "knk": "kanka", "kgo": "coğrafya", "mat": "matematik",
        "fzk": "fizik", "gmt": "geometri", "antm": "anatomi", "akciger": "akciyer"
    }
    words = norm_msg.split()
    fixed_words = [typo_rules.get(w, w) for w in words]
    norm_msg = " ".join(fixed_words)

    if any(x in norm_msg for x in ["kim yapti", "yapimcin", "kim gelistirdi", "kurucun", "sahibin", "sen kimsin", "adini kim verdi"]):
        save_log("CEVAPLANDI")
        msg = f"Sistem mimarisi <b>TÜW</b> tarafından geliştirilmiştir{suffix} İsmim <b>ARIES AI</b>{suffix} 🚀"
        return jsonify({"reply": f'<span class="expert-badge badge-sozel">Sistem Çekirdeği</span><br>{msg}'})

    # Matematik Motoru
    math_message = user_message.replace(",", ".")
    math_chars = set("0123456789+-*/(). ")
    if any(char in math_message for char in ['+', '-', '*', '/']) and set(math_message).issubset(math_chars):
        try:
            result = eval(math_message)
            save_log("CEVAPLANDI")
            return jsonify({"reply": f'<span class="expert-badge badge-sayisal">Matematiksel Analiz</span><br><div class="formula-box">{user_message} = {result}</div>'})
        except:
            save_log("HATA")
            return jsonify({"reply": f"Matematiksel işlem hesaplanamadı{suffix}"})

    # Veri tabanı kontrolleri
    for key, response in science_database.items():
        if key in norm_msg:
            save_log("CEVAPLANDI")
            return jsonify({"reply": f'<span class="expert-badge badge-sayisal" style="background-color:#00e676; color:black;">Fen Bilimleri & Anatomi</span><br>{response}'})

    for key, response in physics_geometry_database.items():
        if key in norm_msg:
            save_log("CEVAPLANDI")
            return jsonify({"reply": f'<span class="expert-badge badge-sayisal" style="background-color:#ff9100; color:black;">Fizik & Geometri</span><br>{response}'})

    for key, response in religious_database.items():
        if key in norm_msg:
            save_log("CEVAPLANDI")
            return jsonify({"reply": f'<span class="expert-badge badge-sozel" style="background-color:#9c27b0;">İslami Tarih & İlim</span><br>{response}'})

    for key, response in historical_events.items():
        if key.replace("ı", "i").replace("ğ", "g") in norm_msg:
            save_log("CEVAPLANDI")
            return jsonify({"reply": f'<span class="expert-badge badge-sozel">Tarih Bilgisi</span><br>{response}'})

    matched_countries = []
    for country, data in world_countries.items():
        if country in norm_msg:
            matched_countries.append({"name": country.upper(), "b": data["b"], "k": data["k"], "bilgi": data["bilgi"]})

    if len(matched_countries) == 0:
        for word in words:
            if len(word) > 3:
                api_data = fetch_country_from_api(word)
                if api_data:
                    matched_countries.append(api_data)
                    break

    if len(matched_countries) == 1:
        save_log("CEVAPLANDI")
        return jsonify({"reply": f'<span class="expert-badge badge-cografya">Coğrafya Analizi</span><br><b>Ülke:</b> {matched_countries[0]["name"]}<br><b>Başkent:</b> {matched_countries[0]["b"]}<br><br>ℹ️ {matched_countries[0]["bilgi"]}'})

    if any(x in norm_msg for x in ["selam", "merhaba"]):
        save_log("CEVAPLANDI")
        msg = f"Bağlantı başarılı{suffix} ARIES AI aktif ve analiz süreçlerine hazır{suffix}"
        return jsonify({"reply": msg})

    # Canlı Arama Motoru
    canli_sonuc = google_gibi_ara(raw_message)
    if canli_sonuc:
        save_log("CEVAPLANDI (CANLI)")
        return jsonify({"reply": f'<span class="expert-badge badge-sozel" style="background-color:#00bcd4;">Canlı İnternet Sonucu</span><br>{canli_sonuc}'})

    save_log("CEVAPLANAMADI")
    return jsonify({"reply": f"Sorgu derinliği analiz edildi fakat veri tabanında eşleşme sağlanamadı{suffix}"})

if __name__ == '__main__':
    app.run(debug=True)
