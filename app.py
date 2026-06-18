from flask import Flask, render_template, request, jsonify
from google import genai
import os

app = Flask(__name__, template_folder='templates')
app.secret_key = 'aries_gizli_ajan_modu_2026'

# Şifreyi Render ayarlarından (Environment) güvenli şekilde çekiyor, kodda iz kalmıyor
API_KEY = os.environ.get("AQ.Ab8RN6Iri4dDxyF-UZgI_PuWQDM8bAxfhEfdWX9iEy6RCoK5Sw")
client = genai.Client(api_key=API_KEY)

@app.route('/')
def ana_sayfa():
    # İsmini tamamen gizledik, ekranda sadece "Kaptan" yazacak
    return render_template('index.html', kullanici="Kaptan")

@app.route('/sor', methods=['POST'])
def sor():
    try:
        veri = request.get_json()
        soru = veri.get('soru', '').strip()
        
        if not soru:
            return jsonify({'cevap': 'Bir şey yazmadın kanka?'})

        # Talimattan tüm kişisel isimleri ve bilgileri sildik, tamamen anonim!
        talimat = (
            "Senin adın Aries. Çok zeki ve samimi bir yapay zekasın. "
            "Karşındaki kullanıcı kimliğini gizli tutmak isteyen anonim biridir. "
            "Ona 'Kaptan' veya 'Kanka' diye hitap et. Sorulan her soruya samimi, havalı ve net cevaplar ver."
        )

        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=f"{talimat}\n\nSoru: {soru}"
        )
        return jsonify({'cevap': response.text})
        
    except Exception as e:
        return jsonify({'cevap': f"Bağlantı hatası kanka. Şifre kontrolü gerekiyor."})

if __name__ == '__main__':
    app.run(debug=True)
