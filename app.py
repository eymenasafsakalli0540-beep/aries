from flask import Flask, render_template, request, jsonify
import os
import re
import difflib
from sympy import sympify

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
    "hindistan": {"b": "Yeni Delhi", "m": "4.500 km", "k": "Asya"}
}

shortcuts = {
    "knk": "kanka", "slm": "selam", "mrb": "merhaba", "tr": "türkiye",
    "km": "kilometre", "baskent": "başkenti", "baskenti": "başkenti",
    "arasında": "arası", "mesafe": "arası", "dg": "dağı", "gl": "gölü"
}

def preprocess_text(text):
    text = text.lower().strip()
    words = text.split()
    resolved_words = [shortcuts.get(w, w) for w in words]
    return " ".join(resolved_words)

def find_best_country(user_msg):
    for country in global_geography.keys():
        if country in user_msg:
            return country
    for word in user_msg.split():
        matches = difflib.get_close_matches(word, global_geography.keys(), n=1, cutoff=0.8)
        if matches:
            return matches[0]
    return None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    raw_message = request.json.get("message", "")
    user_message = preprocess_text(raw_message)
    reply = ""

    if re.match(r'^[\d+\-*/(). x=]+$', user_message) and any(c in user_message for c in '+-*/='):
        try:
            if '=' in user_message:
                parts = user_message.split('=')
                equation = sympify(f"{parts[0]} - ({parts[1]})")
                result = float(sympify(f"solve({equation})")[0])
            else:
                result = float(sympify(user_message))
            
            if result.is_integer(): result = int(result)
            reply = f'<span class="expert-badge badge-sayisal">Matematik Hesaplama</span><br><div class="formula-box">{raw_message} = {result}</div><b>Sonuç:</b> {result}'
        except Exception:
            reply = '<span class="expert-badge badge-sayisal">Hata</span><br>İşlem veya denklem hesaplanamadı.'

    else:
        found_country = find_best_country(user_message)
        
        if found_country:
            data = global_geography[found_country]
            if any(k in user_message for k in ["başkenti", "nerenin", "merkezi"]):
                reply = f'<span class="expert-badge badge-cografya">Küresel Coğrafya</span><br><b>Bölge:</b> {found_country.upper()}<br><b>Başkenti:</b> {data["b"]}<br><b>Bulunduğu Kıta:</b> {data["k"]}'
            elif any(k in user_message for k in ["arası", "km", "uzak", "mesafe"]):
                reply = f'<span class="expert-badge badge-cografya">Mesafe Analizi</span><br><b>Rota:</b> Türkiye ➔ {found_country.upper()}<br><b>Uzaklık:</b> {data["m"]}<br><b>Konum:</b> {data["k"]}'
            else:
                reply = f'<span class="expert-badge badge-cografya">Genel Bilgi</span><br><b>Bölge:</b> {found_country.upper()}<br><b>Başkent:</b> {data["b"]}<br><b>Mesafe:</b> {data["m"]}'
        
        elif "hız" in user_message or "hiz" in user_message:
            reply = '<span class="expert-badge badge-sayisal">Fizik Analizi</span><br><div class="formula-box">V = x / t</div><b>V:</b> Hız, <b>x:</b> Yol, <b>t:</b> Zaman.'
        elif "istanbul" in user_message and "fetih" in user_message:
            reply = '<span class="expert-badge badge-sozel">Tarih Analizi</span><br><b>İstanbul\'un Fethi (1453):</b> Yeni Çağ\'ı açan askeri başarıdır.'
        elif any(k in user_message for k in ["selam", "merhaba"]):
            reply = f"Selam Eymen! **TÜYK** (Aries Motoru) Python web sunucusu üzerinden aktif, seni dinliyorum."
        elif any(k in user_message for k in ["kanka", "naber", "nasılsın"]):
            reply = "İyidir kanka, sistemi Python ile canavara dönüştürdük! Nereyi merak ediyorsun?"
        else:
            reply = "TÜYK Zeka Motoru veriyi Python arka planında taradı ancak eşleşme bulamadı."

    return jsonify({"reply": reply})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
