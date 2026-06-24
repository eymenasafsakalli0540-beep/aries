from flask import Flask, render_template, request, jsonify

import math

import requests

import os

import re  

from datetime import datetime  



app = Flask(__name__)



# 🌍 COĞRAFYA VERİ TABANI

world_countries = {

    "turkiye": {"b": "Ankara", "k": "Asya/Avrupa", "lat": 39.93, "lon": 32.85, "bilgi": "Asya ve Avrupa'yı birbirine bağlayan stratejik bir köprü ülkedir."},

    "hindistan": {"b": "Yeni Delhi", "k": "Asya", "lat": 28.61, "lon": 77.20, "bilgi": "Güney Asya'da yer alan, dünyanın en kalabalık nüfusuna sahip ülkesidir."},

    "kuba": {"b": "Havana", "k": "Karayipler", "lat": 23.11, "lon": -82.36, "bilgi": "Karayip Denizi'nde yer alan bir ada devletidir."},

    "abd": {"b": "Washington D.C.", "k": "Kuzey Amerika", "lat": 38.90, "lon": -77.03, "bilgi": "50 eyaletten oluşan küresel bir güçtür."},

    "rusya": {"b": "Moskova", "k": "Asya/Avrupa", "lat": 55.75, "lon": 37.61, "bilgi": "Yüzölçümü bakımından dünyanın en büyük ülkesidir."},

    "almanya": {"b": "Berlin", "k": "Avrupa", "lat": 52.52, "lon": 13.40, "bilgi": "Orta Avrupa'da yer alan sanayi devidir."},

    "fransa": {"b": "Paris", "k": "Avrupa", "lat": 48.85, "lon": 2.35, "bilgi": "Batı Avrupa'da bulunan; sanat ve moda merkezidir."},

    "ingiltere": {"b": "Londra", "k": "Avrupa", "lat": 51.50, "lon": -0.12, "bilgi": "Büyük Britanya adasında yer alan köklü bir ülkedir."},

    "azerbaycan": {"b": "Bakü", "k": "Asya", "lat": 40.40, "lon": 49.86, "bilgi": "Kafkasya'da yer alan kardeş canı ülkedir."}

}



# 📜 TARİH VERİ TABANI

historical_events = {

    "istanbulun fethi": "<b>1453 - İstanbul'un Fethi:</b> Fatih Sultan Mehmed liderliğindeki Osmanlı ordusu Bizans'ı yıktı. Orta Çağ kapandı, Yeni Çağ başladı.",

    "cumhuriyetin ilani": "<b>29 Ekim 1923 - Cumhuriyetin İlanı:</b> Gazi Mustafa Kemal Atatürk önderliğinde Türkiye Cumhuriyeti resmen kuruldu. 🇹🇷",

    "malazgirt": "<b>1071 - Malazgirt Meydan Muharebesi:</b> Sultan Alparslan komutasındaki Büyük Selçuklu ordusu, Anadolu'nun kapılarını Türklere açtı.",

    "buyuk taarruz": "<b>1922 - Büyük Taarruz:</b> Türk Kurtuluş Savaşı'nın son evresi. Anadolu düşman işgalinden tamamen temizlendi."

}



# 🕋 DİNİ TERİMLER VERİ TABANI

religious_database = {

    "hicret": "<b>Hicret (622):</b> Hz. Muhammed (s.a.v.) ve Müslümanların Mekke'den Medine'ye göç etmesidir. Hicri takvimin başlangıcıdır.",

    "bedir savasi": "<b>Bedir Savaşı (624):</b> Müslümanlar ile Mekkeli müşrikler arasındaki ilk büyük savaştır. Müslümanlar zafer kazanmıştır.",

    "mekkenin fethi": "<b>Mekke'nin Fethi (630):</b> Hz. Muhammed liderliğindeki İslam ordusu kan dökmeden Mekke'ye girdi.",

    "siyer": "<b>Siyer:</b> Peygamber Efendimiz Hz. Muhammed'in (s.a.v.) hayatını inceleyen bilim dalıdır."

}



# 🧬 YENİ: ANATOMİ VE FEN VERİ TABANI

science_database = {

    "kalp": "<b>Anatomi - Kalp:</b> Göğüs boşluğunda yer alan, kaslı bir pompadır. Vücuda kan pompalar. Üstte iki kulakçık, altta iki karıncık olmak üzere 4 odacıktan oluşur.",

    "akciyer": "<b>Anatomi - Akciğerler:</b> Solunum sisteminin ana organıdır. Göğüs kafesinde sağ ve sol olmak üzere iki adettir. Kana oksijen sağlar, karbondioksiti dışarı atar.",

    "karaciyer": "<b>Anatomi - Karaciğer:</b> Vücudun en büyük iç organıdır ve adeta bir kimya fabrikası gibi çalışır. Safra üretir, toksinleri temizler ve glikoz depolar.",

    "hucre": "<b>Fen Bilgisi - Hücre:</b> Canlıların canlılık özelliği gösteren en küçük yapı taşıdır. Hücre zarı, sitoplazma ve çekirdek olmak üzere üç temel kısımdan oluşur.",

    "fotosentez": "<b>Fen Bilgisi - Fotosentez:</b> Bitkilerin kloroplast organelinde, güneş ışığı yardımıyla su ve karbondioksiti birleştirerek besin (glikoz) ve oksijen üretmesi olayıdır.",

    "mitokondri": "<b>Fen Bilgisi - Mitokondri:</b> Hücrenin enerji santralidir. Oksijenli solunum yaparak hücre için gerekli olan ATP (enerji) molekülünü üretir."

}



# ⚡ YENİ: FİZİK VE GEOMETRİ VERİ TABANI

physics_geometry_database = {

    "yercekimi": "<b>Fizik - Yerçekimi Kuvveti:</b> Kütlesi olan cisimlerin birbirini çekmesidir. Dünyadaki yerçekimi ivmesi yaklaşık olarak $g = 9.81 m/s^2$ kabul edilir. Keşfeden bilim insanı Isaac Newton'dır.",

    "surtunme": "<b>Fizik - Sürtünme Kuvveti:</b> Harekete karşı koyan zorlayıcı kuvvettir. Temas eden yüzeyler arasında oluşur ve kinetik enerjiyi ısı enerjisine dönüştürür.",

    "ohm kanunu": "<b>Fizik - Ohm Kanunu:</b> Bir elektrik devresinde gerilim (V), akım (I) ve direnç (R) arasındaki ilişkiyi açıklar. Formülü: $V = I \\cdot R$ şeklindedir.",

    "ucgen": "<b>Geometri - Üçgen:</b> Üç doğrunun kesişmesiyle oluşan kapalı şekildir. İç açılarının toplamı her zaman **180°**, dış açılarının toplamı ise **360°**'dir.",

    "kare": "<b>Geometri - Kare:</b> Tüm kenarları birbirine eşit ve tüm iç açıları **90°** olan düzgün bir dörtgendir. Alanı bir kenarının karesidir ($A = a^2$).",

    "dikdortgen": "<b>Geometri - Dikdörtgen:</b> Karşılıklı kenarları eşit ve paralel, tüm iç açıları **90°** olan dörtgendir. Çevresi: $2(a+b)$, Alanı: $a \\cdot b$ formülüyle bulunur."

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

                "bilgi": f"{flag} {name_tr}, {region} kıtasında yer alan bir ülkedir."

            }

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

    

    if password != "4235": 

        return jsonify({"success": False, "message": "Hatalı şifre!"}), 403, response_headers



    if action == 'clear':

        if os.path.exists("sorular.txt"): os.remove("sorular.txt")

        return jsonify({"success": True, "logs": []}), 200, response_headers



    if os.path.exists("sorular.txt"):

        with open("sorular.txt", "r", encoding="utf-8") as file: logs = file.readlines()

        clean_logs = [line.strip() for line in logs if line.strip()]

        return jsonify({"success": True, "logs": list(reversed(clean_logs)) if clean_logs else ["Henüz hiç soru sorulmadı kanka."]}), 200, response_headers

    return jsonify({"success": True, "logs": ["Henüz hiç soru sorulmadı kanka."]}), 200, response_headers



@app.route('/ask', methods=['POST'])

def ask():

    user_message = request.json.get("message", "").lower().strip()

    raw_message = request.json.get("message", "").strip() 

    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    user_ip = request.remote_addr  

    

    def save_log(status_msg):

        with open("sorular.txt", "a", encoding="utf-8") as file:

            file.write(f"[{current_time}] IP: {user_ip} | DURUM: {status_msg} -> Soru: {raw_message}\n")



    # Noktalama temizliği

    user_message = re.sub(r'[.,\?!;\(\)"\'’\-]', '', user_message)

    norm_msg = user_message.replace("ı", "i").replace("ğ", "g").replace("ü", "u").replace("ş", "s").replace("ö", "o").replace("ç", "c")



    # 🛠️ YENİ: YANLIŞ YAZIM VE KISALTMA TOLERANS MOTORU (nber, slm, naber)

    typo_rules = {

        "nber": "naber", "nbr": "naber", "slm": "selam", "mrb": "merhaba", 

        "mrhb": "merhaba", "knk": "kanka", "kgo": "coğrafya", "mat": "matematik",

        "fzk": "fizik", "gmt": "geometri", "antm": "anatomi", "akciger": "akciyer"

    }

    words = norm_msg.split()

    fixed_words = [typo_rules.get(w, w) for w in words]

    norm_msg = " ".join(fixed_words)



    is_buddy_mode = "kanka" in norm_msg or "naber" in norm_msg



    # Yapımcı Kontrolü

    if any(x in norm_msg for x in ["kim yapti", "yapimcin", "kim gelistirdi", "kurucun", "sahibin", "sen kimsin", "adini kim verdi"]):

        save_log("CEVAPLANDI")

        return jsonify({"reply": '<span class="expert-badge badge-sozel">Sistem Çekirdeği</span><br>Beni tam bir dahi olmam için <b>TÜW</b> geliştirdi kanka! Adım <b>ARIES AI</b>. 🚀'})



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

            return jsonify({"reply": "İşlem hesaplanamadı kanka, kontrol et."})



    # 🧬 Anatomi ve Fen Bilgisi Kontrolü

    for key, response in science_database.items():

        if key in norm_msg:

            save_log("CEVAPLANDI")

            return jsonify({"reply": f'<span class="expert-badge badge-sayisal" style="background-color:#00e676; color:black;">Fen Bilimleri & Anatomi</span><br>{response}'})



    # ⚡ Fizik ve Geometri Kontrolü

    for key, response in physics_geometry_database.items():

        if key in norm_msg:

            save_log("CEVAPLANDI")

            return jsonify({"reply": f'<span class="expert-badge badge-sayisal" style="background-color:#ff9100; color:black;">Fizik & Geometri</span><br>{response}'})



    # 🕋 Dini Terimler Kontrolü

    for key, response in religious_database.items():

        if key in norm_msg:

            save_log("CEVAPLANDI")

            return jsonify({"reply": f'<span class="expert-badge badge-sozel" style="background-color:#9c27b0;">İslami Tarih</span><br>{response}'})



    # 📜 Tarih Kontrolü

    for key, response in historical_events.items():

        if key.replace("ı", "i").replace("ğ", "g") in norm_msg:

            save_log("CEVAPLANDI")

            return jsonify({"reply": f'<span class="expert-badge badge-sozel">Tarih Bilgisi</span><br>{response}'})



    # 🌍 Coğrafya Kontrolü

    matched_countries = []

    for country, data in world_countries.items():

        if country in norm_msg:

            matched_countries.append({"name": country.upper(), "b": data["b"], "k": data["k"], "lat": data["lat"], "lon": data["lon"], "bilgi": data["bilgi"]})



    if len(matched_countries) >= 2:

        distance = calculate_haversine(matched_countries[0]["lat"], matched_countries[0]["lon"], matched_countries[1]["lat"], matched_countries[1]["lon"])

        save_log("CEVAPLANDI")

        return jsonify({"reply": f'<span class="expert-badge badge-cografya">Rota Analizi</span><br>📐 <b>Mesafe:</b> ~{distance} Kilometre'})

    elif len(matched_countries) == 1:

        save_log("CEVAPLANDI")

        return jsonify({"reply": f'<span class="expert-badge badge-cografya">Coğrafya</span><br><b>Ülke:</b> {matched_countries[0]["name"]}<br><b>Başkent:</b> {matched_countries[0]["b"]}'})



    if any(x in norm_msg for x in ["selam", "merhaba"]):

        save_log("CEVAPLANDI")

        return jsonify({"reply": "Selam! ARIES AI hazır, ne soruyoruz?"})



    save_log("CEVAPLANAMADI")

    return jsonify({"reply": "ARIES bu soruyu analiz etti ama tam bir eşleşme bulamadı kanka. Matematik, fen, fizik, geometri, anatomi, tarih veya coğrafya sormayı dene!"})



if __name__ == '__main__':

    app.run(debug=True) 

