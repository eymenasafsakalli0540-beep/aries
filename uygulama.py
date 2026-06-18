from flask import Flask, render_template, request, jsonify, session
from google import genai
import base64
import os

app = Flask(__name__, template_folder='templates')
app.secret_key = 'aries_eymen_ozel_anahtar_2026'

# --- GOOGLE GEMINI API KEYİNİ BURAYA YAPIŞTIR KANKA ---
# Google AI Studio'dan aldığın AIzaSy... diye başlayan şifreni buraya koy
API_KEY = "BURAYA_ALDIĞIN_API_KEYİ_YAPIŞTIR"
client = genai.Client(api_key=API_KEY)

@app.route('/')
def ana_sayfa():
    # Giriş sistemi falan uğraşmadan direkt sade arayüze bağladık
    return render_template('index.html', kullanici="Eymen")

@app.route('/sor', methods=['POST'])
def sor():
    try:
        veri = request.get_json()
        soru = veri.get('soru', '').strip()
        
        if not soru:
            return jsonify({'cevap': 'Bir şey yazmadın kanka?', 'tip': 'metin'})

        soru_alt = soru.lower()
        # Eğer kullanıcı resim/çizim istiyorsa Imagen modelini tetikliyoruz
        if "çiz" in soru_alt or "resim" in soru_alt or "görsel" in soru_alt or "fotoğraf" in soru_alt:
            try:
                gorsel_response = client.models.generate_images(
                    model='imagen-3.0-generate-002',
                    prompt=soru,
                    config=dict(number_of_images=1, output_mime_type="image/jpeg")
                )
                for resim in gorsel_response.generated_images:
                    resim_base64 = resim.image.image_bytes
                    encoded = base64.b64encode(resim_base64).decode('utf-8')
                    return jsonify({'cevap': f"data:image/jpeg;base64,{encoded}", 'tip': 'resim'})
            except Exception as img_err:
                return jsonify({'cevap': f"Resim çizemedim kanka, hata: {str(img_err)}", 'tip': 'metin'})

        # Normal sohbet soruları için Gemini devrede
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=f"Senin adın Aries. Eymen Safa Sakallı tarafından geliştirilmiş çok zeki bir yapay zekasın. Karşındaki kişiye samimi, havalı ama net cevaplar ver. Soru: {soru}"
        )
        return jsonify({'cevap': response.text, 'tip': 'metin'})
        
    except Exception as e:
        return jsonify({'cevap': f"Bağlantı hatası kanka: {str(e)}", 'tip': 'metin'})

if __name__ == '__main__':
    app.run(debug=True)
