from flask import Flask, render_template, request, jsonify

app = Flask(__name__, template_folder='templates')
app.secret_key = 'aries_eymen_dev_hafiza_2026'

# --- ARIES'IN API OLMADAN HER ŞEYİ BİLDİĞİ DEV ANSİKLOPEDİK HAFIZASI ---
DEV_HAFIZA = {
    # --- OKUL DERSLERİ ---
    "matematik": (
        "📊 **MATEMATİK KÜTÜPHANESİ**\n\n"
        "• **Alan Formülleri:** Kare = $a^2$ | Dikdörtgen = $a \cdot b$ | Üçgen = $\\frac{\\text{Taban} \\cdot \\text{Yükseklik}}{2}$\n"
        "• **Çevre Formülleri:** Kare = $4a$ | Dikdörtgen = $2(a+b)$ | Çember = $2\\pi r$\n"
        "• **İşlem Önceliği:** 1. Parantez, 2. Üslü Sayılar, 3. Çarpma/Bölme, 4. Toplama/Çıkarma\n"
        "• **Sayı Kümeleri:** Doğal Sayılar (N) 0'dan başlar, Sayma Sayıları 1'den başlar. Tam Sayılar (Z) eksileri de kapsar."
    ),
    "fen": (
        "🔬 **FEN VE TEKNOLOJİ LABORATUVARI**\n\n"
        "• **Hücre:** Zar (korur), Sitoplazma (yaşam döner), Çekirdek (yönetir).\n"
        "• **Organeller:** Mitokondri (Enerji ⚡), Kloroplast (Bitkide fotosentez 🌱), Ribozom (Protein), Lizozom (Sindirim).\n"
        "• **Elementler:** Hidrojen (H), Helyum (He), Lityum (Li), Karbon (C), Azot (N), Oksijen (O), Flor (F), Neon (Ne).\n"
        "• **Güneş Sistemi:** Güneşe yakınlık sırası: Merkür, Venüs, Dünya, Mars, Jüpiter, Satürn, Uranüs, Neptün."
    ),
    "türkçe": (
        "📚 **TÜRKÇE VE DİL BİLGİSİ**\n\n"
        "• **Sözcükte Anlam:** Gerçek (ilk akla gelen), Mecaz (gerçek dışı yeni anlam), Terim (bilim/sanat/spor kelimesi).\n"
        "• **Ses Olayları:** Ünsüz Yumuşaması (p-ç-t-k -> b-c-d-g/ğ), Ünsüz Benzeşmesi (Fıstıkçı Şahap yanına p-ç-t-k alır).\n"
        "• **Cümle Bilgisi:** Yüklemi sonda olan cümle Kurallı, sonda olmayan cümle Devriktir. İş, oluş, hareket bildiren kelimeler fiildir."
    ),
    "tarih": (
        "📜 **TARİH VE KÜLTÜR HAFIZASI**\n\n"
        "• **Malazgirt Savaşı (1071):** Anadolu'nun kapıları Türklere açıldı.\n"
        "• **İstanbul'un Fethi (1453):** Fatih Sultan Mehmet Bizans'ı yıktı, Orta Çağ kapandı, Yeni Çağ başladı.\n"
        "• **Kurtuluş Savaşı:** 19 Mayıs 1919'da Atatürk'ün Samsun'a çıkışıyla başladı. 29 Ekim 1923'te Cumhuriyet ilan edildi.\n"
        "• **İlk Türk Devletleri:** Göktürkler (İlk Türk adı), Uygurlar (Yerleşik hayata geçen ilk Türk devleti)."
    ),
    "coğrafya": (
        "🌍 **COĞRAFYA VE DÜNYA ATLASI**\n\n"
        "• **Yeryüzü Şekilleri:** Dağ (yüksek), Ova (alçak düzlük), Plato (yüksek düzlük), Akarsu, Göl, Körfez.\n"
        "• **Türkiye'nin Bölgeleri:** Marmara, Ege, Akdeniz, Karadeniz, İç Anadolu, Doğu Anadolu, Güneydoğu Anadolu.\n"
        "• **İklimler:** Karadeniz (Her mevsim yağışlı), Akdeniz (Yazlar sıcak-kurak, kışlar ılık-yağışlı), Karasal (Kışlar soğuk-karlı)."
    ),
    "ingilizce": (
        "🇬🇧 **İNGİLİZCE KILAVUZU (ENGLISH)**\n\n"
        "• **To Be:** I am | He/She/It is | You/We/They are\n"
        "• **Geniş Zaman:** He/She/It öznelerinde fiile '-s' takısı gelir (Örn: He likes coding).\n"
        "• **Soru Kelimeleri:** What (Ne), Where (Nerede), Who (Kim), When (Ne zaman), Why (Neden), How (Nasıl).\n"
        "• **Günler:** Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday."
    ),

    # --- GENEL KÜLTÜR VE DÜNYA BİLGİLERİ ---
    "türkiye": (
        "🇹🇷 **TÜRKİYE CUMHURİYETİ BİLGİ KARTI**\n\n"
        "• **Başkent:** Ankara | **En Büyük Şehir:** İstanbul\n"
        "• **Para Birimi:** Türk Lirası (₺) | **Resmi Dil:** Türkçe\n"
        "• **Komşular:** Yunanistan, Bulgaristan, Gürcistan, Ermenistan, Azerbaycan (Nahçıvan), İran, Irak, Suriye.\n"
        "• **Denizler:** Kuzeyde Karadeniz, Batıda Ege Denizi, Güneyde Akdeniz, İç deniz olarak Marmara Denizi."
    ),
    "dünya": (
        "🗺️ **DÜNYA VE KITALAR BİLGİSİ**\n\n"
        "• **Kıtalar:** Asya (En büyük), Afrika, Kuzey Amerika, Güney Amerika, Antarktika, Avrupa, Okyanusya (Avustralya).\n"
        "• **Okyanuslar:** Büyük Okyanus (Pasifik), Atlas Okyanusu (Atlantik), Hint Okyanusu.\n"
        "• **Enler:** En yüksek dağ Everest, En uzun nehir Nil Nehri, En büyük çöl Sahra Çölü, En derin yer Mariana Çukuru."
    ),
    "bilim": (
        "⚡ **GENEL BİLİM VE TEKNOLOJİ TOZLARI**\n\n"
        "• **Suyun Formülü:** $H_2O$ (2 Hidrojen, 1 Oksijen)\n"
        "• **Yerçekimi:** Isaac Newton tarafından elmanın kafasına düşmesiyle formülize edilmiştir.\n"
        "• **Işık Hızı:** Saniyede yaklaşık $300.000\\text{ km}$ hızla hareket eder. Evrendeki en yüksek hız sınırıdır.\n"
        "• **Yapay Zeka:** Bilgisayarların insan gibi düşünmesini, analiz yapmasını ve öğrenmesini sağlayan yazılım teknolojisidir."
    )
}

@app.route('/')
def ana_sayfa():
    return render_template('index.html', kullanici="Eymen")

@app.route('/sor', methods=['POST'])
def sor():
    try:
        veri = request.get_json()
        soru = veri.get('soru', '').strip().lower()
        
        if not soru:
            return jsonify({'cevap': 'Bir şey yazmadın kanka?'})

        # Tek tek kelimeleri tarayarak hafızadaki en doğru yere yönlendiriyoruz
        if "matematik" in soru or "mat" in soru or "formül" in soru or "hesap" in soru:
            cevap = DEV_HAFIZA["matematik"]
        elif "fen" in soru or "hücre" in soru or "organel" in soru or "element" in soru or "kimya" in soru:
            cevap = DEV_HAFIZA["fen"]
        elif "türkçe" in soru or "anlam" in soru or "yazım" in soru or "dil bilgisi" in soru:
            cevap = DEV_HAFIZA["türkçe"]
        elif "tarih" in soru or "savaş" in soru or "feth" in soru or "atatürk" in soru:
            cevap = DEV_HAFIZA["tarih"]
        elif "coğrafya" in soru or "bölge" in soru or "iklim" in soru or "dağ" in soru or "ova" in soru:
            cevap = DEV_HAFIZA["coğrafya"]
        elif "ingilizce" in soru or "english" in soru or "kelime" in soru or "translation" in soru:
            cevap = DEV_HAFIZA["ingilizce"]
        elif "türkiye" in soru or "ankara" in soru or "deniz" in soru or "şehir" in soru:
            cevap = DEV_HAFIZA["türkiye"]
        elif "dünya" in soru or "kıta" in soru or "okyanus" in soru or "ülke" in soru:
            cevap = DEV_HAFIZA["dünya"]
        elif "bilim" in soru or "fizik" in soru or "ışık" in soru or "formül" in soru:
            cevap = DEV_HAFIZA["bilim"]
        else:
            # Kullanıcı başka bir kelime yazarsa ona rehberlik eden genel mesaj
            cevap = (
                "Selam Eymen kanka! Şu an tamamen API'siz, internet gerektirmeyen yerel dev hafızamla çalışıyorum. "
                "Kota veya bağlantı derdimiz sıfır! 🚀\n\n"
                "Hafızamdan anında çekip getirmemi istediğin konuyu yazman yeterli:\n"
                "👉 **Matematik, Fen, Türkçe, Tarih, Coğrafya, İngilizce, Türkiye, Dünya, Bilim**\n\n"
                "Hangi konuyu inceleyelim?"
            )

        return jsonify({'cevap': cevap})
        
    except Exception as e:
        return jsonify({'cevap': f"Hafıza hatası kanka: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True)
