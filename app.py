from flask import Flask, render_template, request, jsonify
import math
import requests
import os
from datetime import datetime  # Soruların zamanını kaydetmek için ekledik

app = Flask(__name__)

# [Yukarıdaki veri tabanları - world_countries, historical_events, religious_database aynı kalıyor]
world_countries = {
    "turkiye": {"b": "Ankara", "k": "Asya/Avrupa", "lat": 39.93, "lon": 32.85, "bilgi": "Asya ve Avrupa'yı birbirine bağlayan, üç tarafı denizlerle çevrili stratejik bir köprü ülkedir."},
    "hindistan": {"b": "Yeni Delhi", "k": "Asya", "lat": 28.61, "lon": 77.20, "bilgi": "Güney Asya'da yer alan, dünyanın en kalabalık nüfusuna sahip rengarenk bir kültür ülkesidir."},
    "kuba": {"b": "Havana", "k": "Karayipler", "lat": 23.11, "lon": -82.36, "bilgi": "Karayip Denizi'nde yer alan, müzikleri ve tarihi mimarisiyle ünlü bir ada devletidir."},
    "abd": {"b": "Washington D.C.", "k": "Kuzey Amerika", "lat": 38.90, "lon": -77.03, "bilgi": "Kuzey Amerika kıtasında bulunan, 50 eyaletten oluşan küresel bir güçtür."},
    "amerika": {"b": "Washington D.C.", "k": "Kuzey Amerika", "lat": 38.90, "lon": -77.03, "bilgi": "Kuzey Amerika kıtasında bulunan küresel bir federal devlettir."},
    "rusya": {"b": "Moskova", "k": "Asya/Avrupa", "lat": 55.75, "lon": 37.61, "bilgi": "Yüzölçümü bakımından dünyanın en büyük ülkesidir, iki kıtaya yayılmıştır."},
    "almanya": {"b": "Berlin", "k": "Avrupa", "lat": 52.52, "lon": 13.40, "bilgi": "Orta Avrupa'da yer alan, sanayisi ve teknolojisi son derece gelişmiş bir sanayi devidir."},
    "fransa": {"b": "Paris", "k": "Avrupa", "lat": 48.85, "lon": 2.35, "bilgi": "Batı Avrupa'da bulunan; sanat, moda, mutfak ve köklü siyasi tarihiyle bilinen bir ülkedir."},
    "ingiltere": {"b": "Londra", "k": "Avrupa", "lat": 51.50, "lon": -0.12, "bilgi": "Büyük Britanya adasında yer alan, coğrafi keşiflerin öncüsü köklü bir denizci ülkesidir."},
    "hollanda": {"b": "Amsterdam", "k": "Avrupa", "lat": 52.36, "lon": 4.90, "bilgi": "Topraklarının büyük kısmı deniz seviyesinin altında olan, yel değirmenleri ve laleleriyle ünlü Batı Avrupa ülkesidir."},
    "italya": {"b": "Roma", "k": "Avrupa", "lat": 41.90, "lon": 12.49, "bilgi": "Akdeniz'e uzanan çizme şeklindeki yarımadada kurulmuş, Roma İmparatorluğu'nun beşiği olan ülkedir."},
    "japonya": {"b": "Tokyo", "k": "Asya", "lat": 35.67, "lon": 139.65, "bilgi": "Doğu Asya'da bir ada ülkesidir, ileri teknolojisi ve köklü samuray/geleneksel kültürüyle tanınır."},
    "mısır": {"b": "Kahire", "k": "Afrika", "lat": 30.04, "lon": 31.23, "bilgi": "Kuzey Afrika ile Orta Doğu'yu bağlayan, Nil Nehri ve antik piramitlerin ev sahibidir."},
    "brezilya": {"b": "Brasilia", "k": "Güney Amerika", "lat": -15.79, "lon": -47.88, "bilgi": "Güney Amerika'nın en büyük ve en kalabalık ülkesidir, Amazon Ormanları burada yer alır."},
    "azerbaycan": {"b": "Bakü", "k": "Asya", "lat": 40.40, "lon": 49.86, "bilgi": "Kafkasya'da yer alan, Türkiye ile 'Tek millet, iki devlet' bağına sahip kardeş canı ülkedir."}
}

historical_events = {
    "istanbulun fethi": "<b>1453 - İstanbul'un Fethi:</b> Fatih Sultan Mehmed liderliğindeki Osmanlı ordusu Bizans'ı yıktı. Orta Çağ kapandı, Yeni Çağ başladı.",
    "cumhuriyetin ilani": "<b>29 Ekim 1923 - Cumhuriyetin İlanı:</b> Gazi Mustafa Kemal Atatürk önderliğinde Türkiye Cumhuriyeti resmen kuruldu ve egemenlik kayıtsız şartsız millete geçti. 🇹🇷",
    "malazgirt": "<b>1071 - Malazgirt Meydan Muharebesi:</b> Sultan Alparslan komutasındaki Büyük Selçuklu ordusu, Bizans'ı yenerek Anadolu'nun kapılarını Türklere sonsuza dek açtı.",
    "büyük taarruz": "<b>1922 - Büyük Taarruz (Başkomutanlık Meydan Muharebesi):</b> Türk Kurtuluş Savaşı'nın son evresi. Yunan ordusu bozguna uğratılarak Anadolu düşman işgalinden tamamen temizlendi.",
    "1 dunya savasi": "<b>1914 - 1918 (I. Dünya Savaşı):</b> İtilaf ve İttifak devletleri arasında küresel savaş.",
    "2 dunya savasi": "<b>1939 - 1945 (II. Dünya Savaşı):</b> Mihver ve Müttefik devletler arasında insanlık tarihinin en kanlı küresel savaşı.",
    "fransiz ihtilali": "<b>1789 - Fransız İhtilali:</b> Dünyada milliyetçilik, adalet, eşitlik ve özgürlük akımlarının yayılmasına sebep oldu. Yakın Çağ başladı.",
    "rönesans": "<b>14. - 17. Yüzyıl:</b> İtalya'da başlayan; bilim, sanat, edebiyat ve felsefede yeniden doğuşu simgeleyen dönemdir."
}

religious_database = {
    "hicret": "<b>Hicret (622):</b> Hz. Muhammed (s.a.v.) ve Müslümanların Mekke'den Medine'ye göç etmesidir. Hicri takvimin başlangıcı olmuştur.",
    "bedir savasi": "<b>Bedir Savaşı (624):</b> Müslümanlar ile Mekkeli müşrikler arasındaki ilk büyük savaştır. Müslümanlar zafer kazanmıştır.",
    "uhud savasi": "<b>Uhud Savaşı (625):</b> Müşriklerle yapıldı. Okçuların yerini terk etmesi sonucu Müslümanlar zor anlar yaşadı ve Hz. Hamza şehit düştü.",
    "hendek savasi": "<b>Hendek Savaşı (627):</b> Medine'nin etrafına derin hendekler kazılarak yapılan efsanevi bir savunma savaşıdır.",
    "mekkenin fethi": "<b>Mekke'deki Fetih (630):</b> Hz. Muhammed liderliğindeki İslam ordusu kan dökmeden Mekke'ye girdi.",
    "dört halife": "<b>Dört Halife Dönemi:</b> Sırasıyla yöneten adalet timsalleridir:<br>1. Hz. Ebubekir<br>2. Hz. Ömer<br>3. Hz. Osman<br>4. Hz. Ali",
    "fıkıh": "<b>Fıkıh:</b> İslam hukukudur. Günlük hayatın dini kurallarını ve amel detaylarını inceleyen ilim dalıdır.",
    "tefsir": "<b>Tefsir:</b> Kur'an-ı Kerim'in ayetlerini detaylıca açıklayan ve yorumlayan ilim dalıdır.",
    "hadis": "<b>Hadis:</b> Peygamber Efendimiz Hz. Muhammed'in (s.a.v.) söylediği mübarek sözler and davranışların bütüdür.",
    "kelam": "<b>Kelam:</b> İslam inanç esaslarını akli ve nakli delillerle savunup açıklayan ilim dalıdır.",
    "akait": "<b>Akait:</b> İslam dininde inanılması zorunlu olan iman esaslarının kurallarıdır."
}

def calculate_haversine(lat1, lon1, lat2, lon2):
    R = 6371
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    a = math.sin(d_lat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(d_lon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(R * c)

def fetch_country_from_api(country_name):
    try:
        url = f"https://restcountries.com/v3.1/name/{country_name}"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()[0]
            name_tr = data.get("translations", {}).get("tur", {}).get("common", country_name).upper()
            capital = data.get("capital", ["Bilinmiyor"])[0]
            region = data.get("continents", ["Bilinmiyor"])[0]
            population = data.get("population", 0)
            flag = data.get("flag", "🌐")
            latlng = data.get("latlng", [0, 0])
            return {
                "name": name_tr, "b": capital, "k": region, "lat": latlng[0], "lon": latlng[1],
                "bilgi": f"{flag} {name_tr}, {region} kıtasında yer alan, yaklaşık {population:,} nüfuslu bir world_countries ülkesidir."
            }
    except:
        pass
    return None

@app.route('/')
def home():
    return render_template('index.html')

# 🔐 AKILLI VE GÜVENLİ LOG API ROTASI (TEMİZLEME DESTEKLİ)
@app.route('/api/get-logs', methods=['POST', 'OPTIONS'])
def get_logs():
    response_headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type"
    }
    
    if request.method == 'OPTIONS':
        return jsonify({"success": True}), 200, response_headers

    data = request.json or {}
    password = data.get('password', '')
    action = data.get('action', 'get')  # 'clear' veya 'get' komutunu yakalar
    
    if password != "F89B2A.ey": 
        return jsonify({"success": False, "message": "Hatalı şifre girdin kanka!"}), 403, response_headers

    # 🗑️ PANELDEKİ SİLME TUŞUNA BASILDIYSA DOSYAYI SIFIRLA
    if action == 'clear':
        try:
            with open("sorular.txt", "w", encoding="utf-8") as file:
                file.write("")  # İçeriği tamamen kazıdık kanka
            return jsonify({"success": True, "logs": []}), 200, response_headers
        except Exception as e:
            return jsonify({"success": False, "message": str(e)}), 500, response_headers

    # 🔄 NORMAL ŞARTLARDA VERİLERİ ÇEK VE GÖNDER
    try:
        with open("sorular.txt", "r", encoding="utf-8") as file:
            logs = file.readlines()
        
        # Eğer dosya içi boşsa düzgün mesaj dönelim
        if not logs or len(logs) == 0:
            return jsonify({"success": True, "logs": ["Henüz hiç soru sorulmadı kanka."]}), 200, response_headers
            
        return jsonify({"success": True, "logs": list(reversed(logs))}), 200, response_headers
    except FileNotFoundError:
        return jsonify({"success": True, "logs": ["Henüz hiç soru sorulmadı kanka."]}), 200, response_headers

@app.route('/ask', methods=['POST'])
def ask():
    user_message = request.json.get("message", "").lower().strip()
    raw_message = request.json.get("message", "").strip() 

    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    user_ip = request.remote_addr  
    
    # Yardımcı log fonksiyonu
    def save_log(status_msg):
        with open("sorular.txt", "a", encoding="utf-8") as file:
            file.write(f"[{current_time}] IP: {user_ip} | DURUM: {status_msg} -> Soru: {raw_message}\n")

    # Metin Normalizasyonu
    norm_msg = user_message.replace("ı", "i").replace("ğ", "g").replace("ü", "u").replace("ş", "s").replace("ö", "o").replace("ç", "c")
    norm_msg = norm_msg.replace("'", "").replace("-", "").replace("’", "")

    is_buddy_mode = "kanka" in norm_msg or "knk" in norm_msg

    shortcuts = {"tr": "türkiye", "km": "kilometre", "baskent": "başkenti"}
    for key, val in shortcuts.items():
        user_message = user_message.replace(f" {key} ", f" {val} ")

    # Geliştirici ve Kimlik Kontrolü
    if any(x in norm_msg for x in ["kim yapti", "yapimcin", "kim gelistirdi", "kurucun", "sahibin", "sen kimsin", "adini kim verdi"]):
        save_log("CEVAPLANDI")
        if is_buddy_mode:
            return jsonify({"reply": '<span class="expert-badge badge-sozel">Sistem Çekirdeği</span><br>Beni tam bir dahi olmam için <b>TÜW</b> geliştirdi kanka! Adım <b>ARIES AI</b>, yaratıcım ve tek liderim <b>TÜW</b>\'dür. 🚀'})
        return jsonify({"reply": '<span class="expert-badge badge-sozel">Sistem Çekirdeği</span><br>Ben, <b>TÜW</b> tarafından geliştirilmiş resmi bir yapay zeka asistanıyım. Yapay zeka ismim <b>ARIES AI</b> olup, tüm haklarım geliştiricim <b>TÜW</b>\'e aittir.'})

    # Matematik Motoru
    math_message = user_message.replace(",", ".")
    math_chars = set("0123456789+-*/(). ")
    if any(char in math_message for char in ['+', '-', '*', '/']) and set(math_message).issubset(math_chars):
        try:
            result = eval(math_message)
            if isinstance(result, float):
                result = round(result, 4)
            save_log("CEVAPLANDI")
            return jsonify({"reply": f'<span class="expert-badge badge-sayisal">Matematiksel Analiz</span><br><div class="formula-box">{user_message} = {result}</div><b>Sonuç:</b> {result}'})
        except:
            save_log("HATA")
            msg = 'Hesaplanamadı kanka, işlemi kontrol et.' if is_buddy_mode else 'Girilen matematiksel işlem hesaplanamadı. Lütfen kontrol ediniz.'
            return jsonify({"reply": f'<span class="expert-badge badge-sayisal">Hata</span><br>{msg}'})

    # Dini Terimler Motoru
    for key, response in religious_database.items():
        norm_key = key.replace("ı", "i").replace("ğ", "g").replace("ü", "u").replace("ş", "s").replace("ö", "o").replace("ç", "c")
        if norm_key in norm_msg or key in user_message:
            save_log("CEVAPLANDI")
            return jsonify({"reply": f'<span class="expert-badge badge-sozel" style="background-color:#9c27b0;">İslami Analiz & Tarih</span><br>{response}'})

    # Tarih Motoru
    for key, response in historical_events.items():
        norm_key = key.replace("ı", "i").replace("ğ", "g").replace("ü", "u").replace("ş", "s").replace("ö", "o").replace("ç", "c")
        if norm_key in norm_msg or key in user_message:
            save_log("CEVAPLANDI")
            return jsonify({"reply": f'<span class="expert-badge badge-sozel">Tarih & Genel Kültür</span><br>{response}'})

    # Coğrafya Motoru
    matched_countries = []
    for country, data in world_countries.items():
        norm_country = country.replace("ı", "i").replace("ğ", "g").replace("ü", "u").replace("ş", "s").replace("ö", "o").replace("ç", "c")
        if norm_country in norm_msg or country in user_message:
            matched_countries.append({
                "name": country.upper(), "b": data["b"], "k": data["k"], "lat": data["lat"], "lon": data["lon"], "bilgi": data["bilgi"]
            })

    if len(matched_countries) == 0:
        words = user_message.split()
        for word in words:
            if len(word) > 3:
                api_data = fetch_country_from_api(word)
                if api_data:
                    matched_countries.append(api_data)
                    break

    if len(matched_countries) >= 2:
        c1 = matched_countries[0]
        c2 = matched_countries[1]
        distance = calculate_haversine(c1["lat"], c1["lon"], c2["lat"], c2["lon"])
        reply = (f'<span class="expert-badge badge-cografya">Küresel Rota Analitiği</span><br>'
                 f'<b>Başlangıç:</b> {c1["name"]}<br>'
                 f'<b>Varış:</b> {c2["name"]}<br>'
                 f'📐 <b>Mesafe:</b> ~{distance} Kilometre<br>'
                 f'🌐 <b>Bölgeler:</b> {c1["k"]} ➔ {c2["k"]}')
        save_log("CEVAPLANDI")
        return jsonify({"reply": reply})

    elif len(matched_countries) == 1:
        c = matched_countries[0]
        save_log("CEVAPLANDI")
        if "baskent" in norm_msg:
            return jsonify({"reply": f'<span class="expert-badge badge-cografya">Küresel Coğrafya</span><br><b>Ülke:</b> {c["name"]}<br><b>Resmi Başkenti:</b> {c["b"]}'})
        return jsonify({"reply": f'<span class="expert-badge badge-cografya">Coğrafi Analiz</span><br><b>Ülke:</b> {c["name"]}<br><b>Kıta:</b> {c["k"]}<br><b>Başkent:</b> {c["b"]}<br><br>ℹ️ {c["bilgi"]}'})

    if any(x in norm_msg for x in ["selam", "merhaba", "slm", "mrb"]):
        save_log("CEVAPLANDI")
        if is_buddy_mode:
            return jsonify({"reply": "Selam kanka! **ARIES AI** emirlerini bekliyor, ne yapıyoruz bugün?"})
        return jsonify({"reply": "Merhaba. **ARIES AI** sistemi, hizmete hazırdır."})

    if is_buddy_mode:
        save_log("CEVAPLANDI")
        return jsonify({"reply": "Efendim kanka? Mekaniğin sahibi **TÜW**'ün izniyle buradayım, ne istersen sorabilirsin!"})

    # Hiçbir eşleşme olmazsa çalışacak yer (Cevaplanamadı)
    save_log("CEVAPLANAMADI")
    return jsonify({"reply": "ARIES Yapay Zeka Motoru talebinizi analiz etti ancak tam bir esleşme bulamadı. Lütfen coğrafya, dini ilimler, genel kültür veya matematik alanında bir soru yöneltiniz."})

if __name__ == '__main__':
    app.run(debug=True)
