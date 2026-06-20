from flask import Flask, request, jsonify
import math
import requests
import os
import re  
from datetime import datetime  
from bs4 import BeautifulSoup  

app = Flask(__name__)

# Sunucu taraflı düz metin şifre (ARIES'in eski dostu)
GERCEK_SIFRE = 'F89B2A.ey'

# 🌍 MEGA COĞRAFYA VERİ TABANI
world_countries = {
    "turkiye": {"b": "Ankara", "k": "Asya/Avrupa", "lat": 39.93, "lon": 32.85, "bilgi": "Asya ve Avrupa'yı birbirine bağlayan stratejik bir köprü ülkedir."},
    "hindistan": {"b": "Yeni Delhi", "k": "Asya", "lat": 28.61, "lon": 77.20, "bilgi": "Güney Asya'da yer alan, dünyanın en kalabalık nüfusuna sahip ülkesidir."},
    "kuba": {"b": "Havana", "k": "Karayipler", "lat": 23.11, "lon": -82.36, "bilgi": "Karayip Denizi'nde yer alan bir ada devletidir."},
    "abd": {"b": "Washington D.C.", "k": "Kuzey Amerika", "lat": 38.90, "lon": -77.03, "bilgi": "Kuzey Amerika kıtasında bulunan, 50 eyaletten oluşan küresel bir güçtür."},
    "rusya": {"b": "Moskova", "k": "Asya/Avrupa", "lat": 55.75, "lon": 37.61, "bilgi": "Yüzölçümü bakımından dünyanın en büyük ülkesidir."},
    "almanya": {"b": "Berlin", "k": "Avrupa", "lat": 52.52, "lon": 13.40, "bilgi": "Orta Avrupa'da yer alan, sanayisi gelişmiş bir Avrupa gücüdür."},
    "fransa": {"b": "Paris", "k": "Avrupa", "lat": 48.85, "lon": 2.35, "bilgi": "Batı Avrupa'da bulunan; sanat ve moda merkezidir."},
    "ingiltere": {"b": "Londra", "k": "Avrupa", "lat": 51.50, "lon": -0.12, "bilgi": "Büyük Britanya adasında yer alan köklü bir ülkedir."},
    "azerbaycan": {"b": "Bakü", "k": "Asya", "lat": 40.40, "lon": 49.86, "bilgi": "Kafkasya'da yer alan kardeş canı ülkedir."},
    "cin": {"b": "Pekin", "k": "Asya", "lat": 39.90, "lon": 116.40, "bilgi": "Doğu Asya'da milyarlık nüfusa sahip kadim bir ülkedir."},
    "brezilya": {"b": "Brasilia", "k": "Güney Amerika", "lat": -15.79, "lon": -47.88, "bilgi": "Güney Amerika'nın en büyük ülkesidir."},
}

# 📜 TARİH VERİ TABANI
historical_events = {
    "istanbulun fethi": "<b>1453 - İstanbul'un Fethi:</b> Fatih Sultan Mehmed liderliğindeki Osmanlı ordusu Bizans'ı yıktı. Orta Çağ kapandı, Yeni Çağ başladı.",
    "cumhuriyetin ilani": "<b>29 Ekim 1923 - Cumhuriyetin İlanı:</b> Gazi Mustafa Kemal Atatürk önderliğinde Türkiye Cumhuriyet Cumhuriyeti resmen kuruldu. 🇹🇷",
    "malazgirt": "<b>1071 - Malazgirt Meydan Muharebesi:</b> Sultan Alparslan komutasındaki Büyük Selçuklu ordusu, Anadolu'nun kapılarını Türklere açtı.",
    "buyuk taarruz": "<b>1922 - Büyük Taarruz:</b> Türk Kurtuluş Savaşı'nın son evresi. Anadolu düşman işgalinden tamamen temizlendi."
}

# 🕋 DİNİ TERİMLER VERİ TABANI
religious_database = {
    "hicret": "<b>Hicret (622):</b> Hz. Muhammed (s.a.v.) ve Müslümanların Mekke'den Medine'ye göç etmesidir. Hicri takvimin başlangıcıdır.",
    "bedir savasi": "<b>Bedir Savaşı (624):</b> Müslümanlar ile Mekkeli müşrikler arasındaki ilk büyük savaştır.",
    "uhud savasi": "<b>Uhud Savaşı (625):</b> Hz. Hamza'nın şehit düştüğü, Müslümanlar için zor anların yaşandığı savaştır.",
    "mekkenin fethi": "<b>Mekke'nin Fethi (630):</b> Hz. Muhammed liderliğindeki İslam ordusu kan dökmeden Mekke'ye girdi.",
    "fikih": "<b>Fıkıh:</b> İslam'ın ibadet, evlilik, ticaret gibi günlük hayatla ilgili hukuksal ve ameli kurallarını inceleyen bilim dalıdır.",
    "siyer": "<b>Siyer:</b> Peygamber Efendimiz Hz. Muhammed'in (s.a.v.) hayatını inceleyen bilim dalıdır."
}

# 🧬 ANATOMİ VE FEN VERİ TABANI
science_database = {
    "kalp": "<b>Anatomi - Kalp:</b> Göğüs boşluğunda yer alan, kaslı bir pompadır. Vücuda kan pompalar.",
    "akciyer": "<b>Anatomi - Akciğer:</b> Solunum sisteminin ana organıdır. Kana oksijen sağlar, karbondioksiti dışarı atar.",
    "hucre": "<b>Fen Bilgisi - Hücre:</b> Canlıların canlılık özelliği gösteren en küçük yapı taşıdır.",
    "fotosentez": "<b>Fen Bilgisi - Fotosentez:</b> Bitkilerin güneş ışığı yardımıyla besin ve oksijen üretmesi olayıdır.",
    "mitokondri": "<b>Fen Bilgisi - Mitokondri:</b> Hücrenin enerji santralidir. ATP (enerji) üretir."
}

# ⚡ FİZİK VE GEOMETRİ VERİ TABANI
physics_geometry_database = {
    "yercekimi": "<b>Fizik - Yerçekimi Kuvveti:</b> Kütlesi olan cisimlerin birbirini çekmesidir. Dünyadaki yerçekimi ivmesi yaklaşık $g = 9.81 m/s^2$ kabul edilir.",
    "ohm kanunu": "<b>Fizik - Ohm Kanunu:</b> Elektrik devresinde gerilim (V), akım (I) ve direnç (R) arasındaki ilişkidir. Formülü: $V = I \\cdot R$.",
    "ucgen": "<b>Geometri - Üçgen:</b> İç açılarının toplamı her zaman **180°**, dış açılarının toplamı ise **360°**'dir.",
    "kare": "<b>Geometri - Kare:</b> Tüm kenarları eşit, tüm iç açıları **90°** olan düzgün dörtgendir. Alanı: $A = a^2$.",
    "daire": "<b>Geometri - Daire:</b> Merkezden kenara olan mesafeye yarıçap (r) denir. Alanı: $A = \\pi \\cdot r^2$."
}

def google_gibi_ara(sorgu):
    try:
        url = f"https://html.duckduckgo.com/html/?q={sorgu}"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            result = soup.find('a', class_='result__snippet')
            if result: return result.text.strip()
    except: pass
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
    except: pass
    return None

@app.route('/')
def home():
    return "ARIES AI API Server Active."

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
    action = data.get('action', 'get')
    
    if password != GERCEK_SIFRE: 
        return jsonify({"success": False, "message": "Hatalı şifre!"}), 403, response_headers

    if action == 'clear':
        if os.path.exists("sorular.txt"): 
            os.remove("sorular.txt")
        return jsonify({"success": True, "logs": []}), 200, response_headers

    if os.path.exists("sorular.txt"):
        with open("sorular.txt", "r", encoding="utf-8") as file: 
            logs = file.readlines()
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

    user_message = re.sub(r'[.,\?!;\(\)"\'’\-]', '', user_message)
    norm_msg = user_message.replace("ı", "i").replace("ğ", "g").replace("ü", "u").replace("ş", "s").replace("ö", "o").replace("ç", "c")

    typo_rules = {
        "nber": "naber", "nbr": "naber", "slm": "selam", "mrb": "merhaba", 
        "mrhb": "merhaba", "knk": "kanka"
    }
    words = norm_msg.split()
    fixed_words = [typo_rules.get(w, w) for w in words]
    norm_msg = " ".join(fixed_words)

    if any(x in norm_msg for x in ["kim yapti", "yapimcin", "kim gelistirdi", "kurucun", "sahibin", "sen kimsin", "adini kim verdi"]):
        save_log("CEVAPLANDI")
        return jsonify({"reply": 'Beni tam bir dahi olmam için <b>TÜW</b> geliştirdi kanka! Adım <b>ARIES AI</b>. 🚀'})

    math_message = user_message.replace(",", ".")
    math_chars = set("0123456789+-*/(). ")
    if any(char in math_message for char in ['+', '-', '*', '/']) and set(math_message).issubset(math_chars):
        try:
            result = eval(math_message)
            save_log("CEVAPLANDI")
            return jsonify({"reply": f'{user_message} = {result}'})
        except:
            save_log("HATA")
            return jsonify({"reply": "İşlem hesaplanamadı kanka, kontrol et."})

    for key, response in science_database.items():
        if key in norm_msg: save_log("CEVAPLANDI"); return jsonify({"reply": response})

    for key, response in physics_geometry_database.items():
        if key in norm_msg: save_log("CEVAPLANDI"); return jsonify({"reply": response})

    for key, response in religious_database.items():
        if key in norm_msg: save_log("CEVAPLANDI"); return jsonify({"reply": response})

    for key, response in historical_events.items():
        if key.replace("ı", "i").replace("ğ", "g") in norm_msg: save_log("CEVAPLANDI"); return jsonify({"reply": response})

    matched_countries = []
    for country, data in world_countries.items():
        if country in norm_msg:
            matched_countries.append({"name": country.upper(), "b": data["b"], "k": data["k"], "bilgi": data["bilgi"]})

    if len(matched_countries) == 0:
        for word in words:
            if len(word) > 3:
                api_data = fetch_country_from_api(word)
                if api_data: matched_countries.append(api_data); break

    if len(matched_countries) == 1:
        save_log("CEVAPLANDI")
        return jsonify({"reply": f'<b>Ülke:</b> {matched_countries[0]["name"]}<br><b>Başkent:</b> {matched_countries[0]["b"]}<br><br>ℹ️ {matched_countries[0]["bilgi"]}'})

    if any(x in norm_msg for x in ["selam", "merhaba"]):
        save_log("CEVAPLANDI")
        return jsonify({"reply": "Selam kanka! ARIES AI hazır, ne soruyoruz?"})

    canli_sonuc = google_gibi_ara(raw_message)
    if canli_sonuc:
        save_log("CEVAPLANDI (CANLI)")
        return jsonify({"reply": canli_sonuc})

    save_log("CEVAPLANAMADI")
    return jsonify({"reply": "ARIES bu soruyu analiz etti ama tam bir eşleşme bulamadı kanka. Matematik, fen, fizik, geometri, anatomi, tarih veya coğrafya sormayı dene!"})

if __name__ == '__main__':
    app.run(debug=True)
