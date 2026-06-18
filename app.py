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
    "hindistan": {"b": "Yeni Delhi", "m": "4.500 km", "k": "Asya"}
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_message = request.json.get("message", "").lower().strip()
    
    # Kısaltma Çözücü
    shortcuts = {
        "knk": "kanka", "slm": "selam", "mrb": "merhaba", "tr": "türkiye",
        "km": "kilometre", "baskent": "başkenti", "baskenti": "başkenti",
        "arasında": "arası", "mesafe": "arası", "dg": "dağı", "gl": "gölü"
    }
    for key, val in shortcuts.items():
        user_message = user_message.replace(f" {key} ", f" {val} ")
        if user_message.startswith(key): user_message = user_message.replace(key, val, 1)
        if user_message.endswith(key): user_message = user_message[:-len(key)] + val

    reply = ""
    math_chars = set("0123456789+-*/(). ")
    
    # Dinamik Matematik Motoru
    if any(char in user_message for char in ['+', '-', '*', '/']) and set(user_message).issubset(math_chars):
        try:
            result = eval(user_message)
            reply = f'<span class="expert-badge badge-sayisal">Matematik Hesaplama</span><br><div class="formula-box">{user_message} = {result}</div><b>Sonuç:</b> {result}'
        except:
            reply = '<span class="expert-badge badge-sayisal">Hata</span><br>İşlem hesaplanamadı.'
            
    # Coğrafya & Sözel Motoru
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
        
        # Hazır Şablonlar
        elif "hız" in user_message or "hiz" in user_message:
            reply = '<span class="expert-badge badge-sayisal">Fizik Analizi</span><br><div class="formula-box">V = x / t</div><b>V:</b> Hız, <b>x:</b> Yol, <b>t:</b> Zaman.'
        elif "istanbul" in user_message and "fetih" in user_message:
            reply = '<span class="expert-badge badge-sozel">Tarih Analizi</span><br><b>İstanbul\'un Fethi (1453):</b> Yeni Çağ\'ı açan askeri başarıdır.'
        elif "selam" in user_message or "merhaba" in user_message:
            reply = "Selam **TÜW**! **Aries** Python web sunucusu üzerinden aktif, seni dinliyorum."
        elif "kanka" in user_message or "naber" in user_message:
            reply = "İyidir kanka, sistemi Python ile canavara dönüştürdük! Nereyi merak ediyorsun?"
        else:
            reply = "Aries Zeka Motoru veriyi Python arka planında taradı ancak eşleşme bulamadı."

    return jsonify({"reply": reply})

if __name__ == '__main__':
    app.run(debug=True)
