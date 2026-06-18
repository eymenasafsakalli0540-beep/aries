from flask import Flask, render_template, request, jsonify
import math

app = Flask(__name__)

# DÜNYADAKİ TÜM DEVLETLERİN VERİ TABANI (Enlem ve Boylam Odaklı Canlı Hesaplama Sistemi)
# Format: "ülke_adı": {"b": "Başkent", "k": "Kıta", "lat": Enlem, "lon": Boylam}
world_countries = {
    "turkiye": {"b": "Ankara", "k": "Asya/Avrupa", "lat": 39.93, "lon": 32.85},
    "hindistan": {"b": "Yeni Delhi", "k": "Asya", "lat": 28.61, "lon": 77.20},
    "kuba": {"b": "Havana", "k": "Karayipler", "lat": 23.11, "lon": -82.36},
    "abd": {"b": "Washington D.C.", "k": "Kuzey Amerika", "lat": 38.90, "lon": -77.03},
    "amerika": {"b": "Washington D.C.", "k": "Kuzey Amerika", "lat": 38.90, "lon": -77.03},
    "rusya": {"b": "Moskova", "k": "Asya/Avrupa", "lat": 55.75, "lon": 37.61},
    "almanya": {"b": "Berlin", "k": "Avrupa", "lat": 52.52, "lon": 13.40},
    "fransa": {"b": "Paris", "k": "Avrupa", "lat": 48.85, "lon": 2.35},
    "ingiltere": {"b": "Londra", "k": "Avrupa", "lat": 51.50, "lon": -0.12},
    "hollanda": {"b": "Amsterdam", "k": "Avrupa", "lat": 52.36, "lon": 4.90},
    "italya": {"b": "Roma", "k": "Avrupa", "lat": 41.90, "lon": 12.49},
    "japonya": {"b": "Tokyo", "k": "Asya", "lat": 35.67, "lon": 139.65},
    "mısır": {"b": "Kahire", "k": "Afrika", "lat": 30.04, "lon": 31.23},
    "brezilya": {"b": "Brasilia", "k": "Güney Amerika", "lat": -15.79, "lon": -47.88},
    "azerbaycan": {"b": "Bakü", "k": "Asya", "lat": 40.40, "lon": 49.86},
    "madagaskar": {"b": "Antananarivo", "k": "Afrika", "lat": -18.87, "lon": 47.50},
    "ispanya": {"b": "Madrid", "k": "Avrupa", "lat": 40.41, "lon": -3.70},
    "portekiz": {"b": "Lizbon", "k": "Avrupa", "lat": 38.72, "lon": -9.13},
    "cin": {"b": "Pekin", "m": "Asya", "lat": 39.90, "lon": 116.40},
    "arjantin": {"b": "Buenos Aires", "k": "Güney Amerika", "lat": -34.60, "lon": -58.38},
    "kanada": {"b": "Ottawa", "k": "Kuzey Amerika", "lat": 45.42, "lon": -75.69},
    "avustralya": {"b": "Canberra", "k": "Okyanusya", "lat": -35.28, "lon": 149.13},
    "guney afrika": {"b": "Pretoria", "k": "Afrika", "lat": -25.74, "lon": 28.18},
    "guney kore": {"b": "Seul", "k": "Asya", "lat": 37.56, "lon": 126.97},
    "suudi arabistan": {"b": "Riyad", "k": "Asya", "lat": 24.71, "lon": 46.67},
    "iran": {"b": "Tahran", "k": "Asya", "lat": 35.68, "lon": 51.38},
    "yunanistan": {"b": "Atina", "k": "Avrupa", "lat": 37.98, "lon": 23.72},
    "meksika": {"b": "Meksiko", "k": "Kuzey Amerika", "lat": 19.43, "lon": -99.13},
    "kolombiya": {"b": "Bogota", "k": "Güney Amerika", "lat": 4.71, "lon": -74.07},
    "peru": {"b": "Lima", "k": "Güney Amerika", "lat": -12.04, "lon": -77.04},
    "sili": {"b": "Santiago", "k": "Güney Amerika", "lat": -33.44, "lon": -70.66},
    "isvec": {"b": "Stokholm", "k": "Avrupa", "lat": 59.32, "lon": 18.06},
    "norvec": {"b": "Oslo", "k": "Avrupa", "lat": 59.91, "lon": 10.75},
    "finlandiya": {"b": "Helsinki", "k": "Avrupa", "lat": 60.16, "lon": 24.93},
    "isvicre": {"b": "Bern", "k": "Avrupa", "lat": 46.94, "lon": 7.44},
    "belcik": {"b": "Brüksel", "k": "Avrupa", "lat": 50.85, "lon": 4.35},
    "avusturya": {"b": "Viyana", "k": "Avrupa", "lat": 48.20, "lon": 16.37},
    "ukrayna": {"b": "Kiev", "k": "Avrupa", "lat": 50.45, "lon": 30.52},
    "polonya": {"b": "Varşova", "k": "Avrupa", "lat": 52.22, "lon": 21.01},
    "cezayir": {"b": "Cezayir", "k": "Afrika", "lat": 36.75, "lon": 3.05},
    "fas": {"b": "Rabat", "k": "Afrika", "lat": 34.02, "lon": -6.83},
    "tunus": {"b": "Tunus", "k": "Afrika", "lat": 36.80, "lon": 10.18},
    "libya": {"b": "Trablus", "k": "Afrika", "lat": 32.88, "lon": 13.17},
    "sudan": {"b": "Hartum", "k": "Afrika", "lat": 15.50, "lon": 32.55},
    "nijerya": {"b": "Abuja", "k": "Afrika", "lat": 9.07, "lon": 7.39},
    "kenya": {"b": "Nairobi", "k": "Afrika", "lat": -1.29, "lon": 36.82},
    "etiyopya": {"b": "Addis Ababa", "k": "Afrika", "lat": 9.02, "lon": 38.74},
    "somali": {"b": "Mogadişu", "k": "Afrika", "lat": 2.04, "lon": 45.33},
    "afganistan": {"b": "Kabil", "k": "Asya", "lat": 34.55, "lon": 69.20},
    "pakistan": {"b": "İslamabad", "k": "Asya", "lat": 33.68, "lon": 73.04},
    "endonezya": {"b": "Cakarta", "k": "Asya", "lat": -6.20, "lon": 106.81},
    "malezya": {"b": "Kuala Lumpur", "k": "Asya", "lat": 3.13, "lon": 101.68},
    "tayland": {"b": "Bangkok", "k": "Asya", "lat": 13.75, "lon": 100.50},
    "vietnam": {"b": "Hanoi", "k": "Asya", "lat": 21.02, "lon": 105.83},
    "filipinler": {"b": "Manila", "k": "Asya", "lat": 14.59, "lon": 120.98},
    "yeni zelanda": {"b": "Wellington", "k": "Okyanusya", "lat": -41.28, "lon": 174.77},
    "irlanda": {"b": "Dublin", "k": "Avrupa", "lat": 53.34, "lon": -6.26},
    "izlanda": {"b": "Reykjavik", "k": "Avrupa", "lat": 64.14, "lon": -21.89},
    "irak": {"b": "Bağdat", "k": "Asya", "lat": 33.31, "lon": 44.36},
    "suriye": {"b": "Şam", "k": "Asya", "lat": 33.51, "lon": 36.29},
    "lubnan": {"b": "Beyrut", "k": "Asya", "lat": 33.89, "lon": 35.50},
    "urdan": {"b": "Amman", "k": "Asya", "lat": 31.95, "lon": 35.91},
    "kuveyt": {"b": "Kuveyt", "k": "Asya", "lat": 29.37, "lon": 47.97},
    "katar": {"b": "Doha", "k": "Asya", "lat": 25.28, "lon": 51.53},
    "uae": {"b": "Abu Dabi", "k": "Asya", "lat": 24.46, "lon": 54.36},
    "birlesik arap emirlikleri": {"b": "Abu Dabi", "k": "Asya", "lat": 24.46, "lon": 54.36},
    "umman": {"b": "Maskat", "k": "Asya", "lat": 23.58, "lon": 58.40},
    "yemen": {"b": "Sana", "k": "Asya", "lat": 15.35, "lon": 44.20},
    "kazakistan": {"b": "Astana", "k": "Asya", "lat": 51.16, "lon": 71.44},
    "ozbekistan": {"b": "Taşkent", "k": "Asya", "lat": 41.29, "lon": 69.24},
    "turkmenistan": {"b": "Aşkabat", "k": "Asya", "lat": 37.95, "lon": 58.38},
    "kirgizistan": {"b": "Bişkek", "k": "Asya", "lat": 42.87, "lon": 74.59},
    "tacikistan": {"b": "Duşanbe", "k": "Asya", "lat": 38.53, "lon": 68.77},
    "gurcistan": {"b": "Tiflis", "k": "Asya", "lat": 41.71, "lon": 44.79},
    "ermenistan": {"b": "Erivan", "k": "Asya", "lat": 40.17, "lon": 44.51},
    "bulgaristan": {"b": "Sofya", "k": "Avrupa", "lat": 42.69, "lon": 23.32},
    "romanya": {"b": "Bükreş", "k": "Avrupa", "lat": 44.43, "lon": 26.10},
    "macaristan": {"b": "Budapeşte", "k": "Avrupa", "lat": 47.49, "lon": 19.04},
    "cekya": {"b": "Prag", "k": "Avrupa", "lat": 50.07, "lon": 14.43},
    "slovakya": {"b": "Bratislava", "k": "Avrupa", "lat": 48.14, "lon": 17.10},
    "sirbistan": {"b": "Belgrad", "k": "Avrupa", "lat": 44.78, "lon": 20.44},
    "hırvatistan": {"b": "Zagreb", "k": "Avrupa", "lat": 45.81, "lon": 15.97},
    "arnavutluk": {"b": "Tiran", "k": "Avrupa", "lat": 41.32, "lon": 19.81},
    "masedonya": {"b": "Üsküp", "k": "Avrupa", "lat": 41.99, "lon": 21.42},
    "israil": {"b": "Kudüs", "k": "Asya", "lat": 31.76, "lon": 35.21},
    "filistin": {"b": "Kudüs", "k": "Asya", "lat": 31.76, "lon": 35.21},
    "isvicre": {"b": "Bern", "k": "Avrupa", "lat": 46.94, "lon": 7.44},
    "ukrayna": {"b": "Kiev", "k": "Avrupa", "lat": 50.45, "lon": 30.52},
    "papua yeni gine": {"b": "Port Moresby", "k": "Okyanusya", "lat": -9.44, "lon": 147.18}
}

# İKİ COĞRAFİ KOORDİNAT ARASINDAKİ MESAFEYİ HESAPLAYAN HA_VERSION FORMÜLÜ
def calculate_haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Dünyanın yarıçapı (km)
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    a = math.sin(d_lat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(d_lon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(R * c)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_message = request.json.get("message", "").lower().strip()
    
    # Harf ve Karakter Normalizasyonu (Hatalı yazımları yumuşatır)
    norm_msg = user_message.replace("ı", "i").replace("ğ", "g").replace("ü", "u").replace("ş", "s").replace("ö", "o").replace("ç", "c")
    norm_msg = norm_msg.replace("'", "").replace("-", "").replace("’", "")

    # Kısaltmalar
    shortcuts = {"knk": "kanka", "slm": "selam", "mrb": "merhaba", "tr": "türkiye", "km": "kilometre"}
    for key, val in shortcuts.items():
        user_message = user_message.replace(f" {key} ", f" {val} ")

    reply = ""
    math_chars = set("0123456789+-*/(). ")
    
    # 👑 YAPIMCI VE KİMLİK KONTROLÜ
    if any(x in norm_msg for x in ["kim yapti", "yapimcin", "kim gelistirdi", "kurucun", "sahibin", "kim yazdi", "sen kimsin"]):
        return jsonify({"reply": '<span class="expert-badge badge-sozel">Sistem Çekirdeği</span><br>Beni tam bir dahi olması için <b>TÜW</b> geliştirdi ve tasarladı! Benim adım <b>ARIES AI</b>, yaratıcım ve tek liderim ise <b>TÜW</b>\'dür. 🚀'})

    # 🔢 DİNAMİK MATEMATİK MOTORU
    if any(char in user_message for char in ['+', '-', '*', '/']) and set(user_message).issubset(math_chars):
        try:
            result = eval(user_message)
            return jsonify({"reply": f'<span class="expert-badge badge-sayisal">Matematik Analizi</span><br><div class="formula-box">{user_message} = {result}</div><b>Sonuç:</b> {result}'})
        except:
            return jsonify({"reply": '<span class="expert-badge badge-sayisal">Hata</span><br>İşlem hesaplanamadı.'})

    # 🌐 DİNAMİK ÇAPRAZ MESAFE VE ÜLKE MOTORU
    matched_countries = []
    for country, data in world_countries.items():
        norm_country = country.replace("ı", "i").replace("ğ", "g").replace("ü", "u").replace("ş", "s").replace("ö", "o").replace("ç", "c")
        if norm_country in norm_msg or country in user_message:
            if country not in [c[0] for c in matched_countries]:
                matched_countries.append((country, data))

    # EĞER İKİ FARKLI ÜLKE BULUNDUYSA CANLI HESAPLA! (Örn: hindistan küba arası)
    if len(matched_countries) >= 2:
        c1_name, c1_data = matched_countries[0]
        c2_name, c2_data = matched_countries[1]
        
        distance = calculate_haversine(c1_data["lat"], c1_data["lon"], c2_data["lat"], c2_data["lon"])
        
        reply = (f'<span class="expert-badge badge-cografya">Canlı Küresel Rota Motoru</span><br>'
                 f'<b>Başlangıç:</b> {c1_name.upper()} ({c1_data["b"]})<br>'
                 f'<b>Varış:</b> {c2_name.upper()} ({c2_data["b"]})<br>'
                 f'📐 <b>Kuş Uçuşu Mesafe:</b> ~{distance} kilometre!<br>'
                 f'🌐 <b>Konumlar:</b> {c1_data["k"]} ➔ {c2_data["k"]}')
        return jsonify({"reply": reply})

    # Eğer sadece tek ülke bulunduysa
    elif len(matched_countries) == 1:
        c_name, c_data = matched_countries[0]
        if "baskent" in norm_msg or "neren" in norm_msg:
            reply = f'<span class="expert-badge badge-cografya">Küresel Coğrafya</span><br><b>Ülke:</b> {c_name.upper()}<br><b>Başkenti:</b> {c_data["b"]}<br><b>Kıta:</b> {c_data["k"]}'
        else:
            # Türkiye ile mesafesini otomatik hesapla
            tr_data = world_countries["turkiye"]
            distance = calculate_haversine(tr_data["lat"], tr_data["lon"], c_data["lat"], c_data["lon"])
            reply = f'<span class="expert-badge badge-cografya">Mesafe Analizi</span><br><b>Rota:</b> TÜRKİYE ➔ {c_name.upper()}<br><b>Mesafe:</b> ~{distance} km<br><b>Başkent:</b> {c_data["b"]}'
        return jsonify({"reply": reply})

    # --- ⏳ ULTRA TARİH ANALİZ MOTORU ---
    if any(x in norm_msg for x in ["tarih", "savas", "osmanli", "kurtulus", "ataturk", "cumhuriyet", "dunya savas", "fetih", "malazgirt"]):
        if "istanbul" in norm_msg and "fet" in norm_msg:
            reply = '<span class="expert-badge badge-sozel">Osmanlı Tarihi</span><br><b>İstanbul\'un Fethi (1453):</b> II. Mehmed Bizans\'ı yıktı, Çağ kapattı.'
        else:
            reply = '<span class="expert-badge badge-sozel">Tarih Arşivi</span><br>1071 Malazgirt, 1453 Fetih, 1923 Cumhuriyet\'in İlanı 🇹🇷'
        return jsonify({"reply": reply})

    # --- 🌍 GENEL COĞRAFYA MODÜLÜ ---
    if any(x in norm_msg for x in ["cografya", "iklim", "dag", "bogaz", "ova"]):
        reply = '<span class="expert-badge badge-cografya">Coğrafya Çekirdeği</span><br>• Harita ölçekleri, paralel-meridyenler ve iklim kuşakları optimize edildi.'
        return jsonify({"reply": reply})

    # Standart Sohbetler
    if "selam" in norm_msg or "slm" in norm_msg:
        reply = "Selam **TÜW**! Canlı harita ve dünya mesafeleri motoruyla emirlerini bekliyorum."
    elif "kanka" in norm_msg or "knk" in norm_msg:
        reply = "Kanka sistem şu an uzay teknolojisine geçti; dünyadaki bütün büyük ülkeleri birbirine bağlayıp mesafeleri canlı hesaplatabiliyorum! **TÜW** farkı işte!"
    else:
        reply = "ARIES Zeka Motoru veriyi süzdü ancak tam eşleşme bulamadı. Bana iki ülkeyi yan yana yazıp aralarındaki mesafeyi veya ders konularını sorabilirsin Kaptan!"

    return jsonify({"reply": reply})

if __name__ == '__main__':
    app.run(debug=True)
