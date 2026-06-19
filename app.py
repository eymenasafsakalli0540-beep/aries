from flask import Flask, render_template, request, jsonify
import math
import threading
import time
import requests

app = Flask(__name__)

# SİTENİN KENDİ KENDİNİ UYANIK TUTMA FONKSİYONU
def keep_alive():
    while True:
        try:
            # Render projenin canlı web sitesi linkini buraya yaz kanka
            # Örn: "https://aries-ai.onrender.com/"
            self_url = "https://aries-a5bl.onrender.com/" 
            
            if "CANLI_RENDER" not in self_url:
                requests.get(self_url)
                print("🧠 ARIES: Kendi kendime ping attım, uyanık kalmaya devam ediyorum!")
        except Exception as e:
            print("Ping hatası:", e)
        time.sleep(600) # 10 dakikada bir (600 saniye) tetikler

# DÜNYADAKİ TÜM DEVLETLERİN VERİ TABANI
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
    "isvec": {"b": "Stokholm", "k": "Avrupa", "lat": 59.32, "lon": 18.06},
    "norvec": {"b": "Oslo", "k": "Avrupa", "lat": 59.91, "lon": 10.75},
    "isvicre": {"b": "Bern", "k": "Avrupa", "lat": 46.94, "lon": 7.44},
    "belcik": {"b": "Brüksel", "k": "Avrupa", "lat": 50.85, "lon": 4.35},
    "ukrayna": {"b": "Kiev", "k": "Avrupa", "lat": 50.45, "lon": 30.52},
    "papua yeni gine": {"b": "Port Moresby", "k": "Okyanusya", "lat": -9.44, "lon": 147.18}
}

def calculate_haversine(lat1, lon1, lat2, lon2):
    R = 6371
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
    norm_msg = user_message.replace("ı", "i").replace("ğ", "g").replace("ü", "u").replace("ş", "s").replace("ö", "o").replace("ç", "c").replace("'", "")

    if any(x in norm_msg for x in ["kim yapti", "yapimcin", "kim gelistirdi", "kurucun", "sahibin", "sen kimsin"]):
        return jsonify({"reply": '<span class="expert-badge badge-sozel">Sistem Çekirdeği</span><br>Beni <b>TÜW</b> geliştirdi ve tasarladı! Benim adım <b>ARIES AI</b>, yaratıcım ve tek liderim <b>TÜW</b>\'dür. 🚀'})

    math_chars = set("0123456789+-*/(). ")
    if any(char in user_message for char in ['+', '-', '*', '/']) and set(user_message).issubset(math_chars):
        try:
            result = eval(user_message)
            return jsonify({"reply": f'<span class="expert-badge badge-sayisal">Matematik Analizi</span><br><div class="formula-box">{user_message} = {result}</div><b>Sonuç:</b> {result}'})
        except:
            return jsonify({"reply": '<span class="expert-badge badge-sayisal">Hata</span><br>İşlem hesaplanamadı.'})

    matched_countries = []
    for country, data in world_countries.items():
        norm_country = country.replace("ı", "i").replace("ğ", "g").replace("ü", "u").replace("ş", "s").replace("ö", "o").replace("ç", "c")
        if norm_country in norm_msg or country in user_message:
            if country not in [c[0] for c in matched_countries]:
                matched_countries.append((country, data))

    if len(matched_countries) >= 2:
        c1_name, c1_data = matched_countries[0]
        c2_name, c2_data = matched_countries[1]
        distance = calculate_haversine(c1_data["lat"], c1_data["lon"], c2_data["lat"], c2_data["lon"])
        return jsonify({"reply": f'<span class="expert-badge badge-cografya">Canlı Rota Motoru</span><br><b>{c1_name.upper()}</b> ➔ <b>{c2_name.upper()}</b><br>📐 <b>Mesafe:</b> ~{distance} km!<br>🌐 <b>Bölgeler:</b> {c1_data["k"]} - {c2_data["k"]}'})

    elif len(matched_countries) == 1:
        c_name, c_data = matched_countries[0]
        if "baskent" in norm_msg:
            return jsonify({"reply": f'<span class="expert-badge badge-cografya">Küresel Coğrafya</span><br><b>Ülke:</b> {c_name.upper()}<br><b>Başkenti:</b> {c_data["b"]}'})
        tr_data = world_countries["turkiye"]
        distance = calculate_haversine(tr_data["lat"], tr_data["lon"], c_data["lat"], c_data["lon"])
        return jsonify({"reply": f'<span class="expert-badge badge-cografya">Mesafe Analizi</span><br><b>TÜRKİYE ➔ {c_name.upper()}</b><br><b>Mesafe:</b> ~{distance} km'})

    if "kanka" in norm_msg or "naber" in norm_msg:
        return jsonify({"reply": f"Harikayım kanka! Kodun içine gömdüğümüz oto-ping sistemi sayesinde dış servislere gerek kalmadan 7/24 uyanık kalacağım. **TÜW** zekası işte!"})

    return jsonify({"reply": "ARIES Zeka Motoru aktif. Bana matematik, tarih, coğrafya veya ülkeler arası mesafeleri sorabilirsin Kaptan!"})

if __name__ == '__main__':
    # Kodun kendi kendini tetikleyen arka plan motorunu başlatıyoruz
    threading.Thread(target=keep_alive, daemon=True).start()
    app.run(debug=True)
