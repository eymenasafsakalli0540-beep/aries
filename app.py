from flask import Flask, render_template, request, jsonify
from google import genai
import os

app = Flask(__name__, template_folder='templates')
app.secret_key = 'aries_eymen_saf_ders_canavari_2026'

# --- GOOGLE GEMINI API KEYİNİ BURAYA YAPIŞTIR KANKA ---
API_KEY = "AQ.Ab8RN6Iri4dDxyF-UZgI_PuWQDM8bAxfhEfdWX9iEy6RCoK5Sw"
client = genai.Client(api_key=API_KEY)

@app.route('/')
def ana_sayfa():
    return render_template('index.html', kullanici="Eymen")

@app.route('/sor', methods=['POST'])
def sor():
    try:
        veri = request.get_json()
        soru = veri.get('soru', '').strip()
        
        if not soru:
            return jsonify({'cevap': 'Bir şey yazmadın kanka?'})

        # Aries'e tüm derslerde (Matematik, Tarih, Coğrafya, Fen, Türkçe, İngilizce) uzmanlık yüklüyoruz
        ders_talimati = (
            "Senin adın Aries. Eymen Safa Sakallı tarafından geliştirilmiş dahi bir yapay zekasın. "
            "Matematik, Fen Bilimleri, Türkçe, İngilizce, Sosyal Bilgiler, Tarih ve Coğrafya başta olmak üzere tüm okul derslerinde tam bir uzmansın. "
            "Sorulan sorulara bir öğretmen kadar doğru, net ve anlaşılır cevaplar vermelisin. "
            "Aynı zamanda Eymen'e karşı her zaman çok samimi, motive edici ve havalı bir dost gibi davranmalısın."
        )

        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=f"{ders_talimati}\n\nKullanıcıdan gelen soru: {soru}"
        )
        return jsonify({'cevap': response.text})
        
    except Exception as e:
        return jsonify({'cevap': f"Bağlantı hatası kanka: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True)
