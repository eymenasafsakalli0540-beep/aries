import streamlit as st
import google.generativeai as genai
import os

# --- VERİ TABANLARI ---
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

historical_events = {
    "istanbulun fethi": "1453 - İstanbul'un Fethi: Fatih Sultan Mehmed liderliğindeki Osmanlı ordusu Bizans'ı yıktı. Orta Çağ kapandı, Yeni Çağ başladı.",
    "cumhuriyetin ilani": "29 Ekim 1923 - Cumhuriyetin İlanı: Gazi Mustafa Kemal Atatürk önderliğinde Türkiye Cumhuriyeti resmen kuruldu.",
    "malazgirt": "1071 - Malazgirt Meydan Muharebesi: Sultan Alparslan komutasındaki Büyük Selçuklu ordusu, Anadolu'nun kapılarını Türklere açtı.",
    "buyuk taarruz": "1922 - Büyük Taarruz: Türk Kurtuluş Savaşı'nın son evresi. Anadolu düşman işgalinden tamamen temizlendi."
}

religious_database = {
    "hicret": "Hicret (622): Hz. Muhammed (s.a.v.) ve Müslümanların Mekke'den Medine'ye göç etmesidir.",
    "bedir savasi": "Bedir Savaşı (624): Müslümanlar ile Mekkeli müşrikler arasındaki ilk büyük savaştır.",
    "mekkenin fethi": "Mekke'nin Fethi (630): Hz. Muhammed liderliğindeki İslam ordusu kan dökmeden Mekke'ye girdi.",
    "siyer": "Siyer: Peygamber Efendimiz Hz. Muhammed'in (s.a.v.) hayatını inceleyen bilim dalıdır."
}

science_database = {
    "kalp": "Kalp: Göğüs boşluğunda yer alan, kaslı bir pompadır. Vücuda kan pompalar.",
    "akciyer": "Akciğerler: Solunum sisteminin ana organıdır. Kana oksijen sağlar.",
    "karaciyer": "Karaciğer: Vücudun en büyük iç organıdır, toksinleri temizler.",
    "hucre": "Hücre: Canlıların canlılık özelliği gösteren en küçük yapı taşıdır.",
    "fotosentez": "Fotosentez: Bitkilerin güneş ışığı yardımıyla besin üretmesi olayıdır.",
    "mitokondri": "Mitokondri: Hücrenin enerji santralidir, ATP üretir."
}

physics_geometry_database = {
    "yercekimi": "Yerçekimi: Kütlesi olan cisimlerin birbirini çekmesidir. ivme g=9.81 m/s^2.",
    "ohm kanunu": "Ohm Kanunu: V = I * R formülü ile elektriksel direnci açıklar.",
    "ucgen": "Üçgen: İç açıları toplamı 180°, dış açıları toplamı 360°'dir.",
    "kare": "Kare: Alanı a^2 olan, tüm kenarları eşit 90 derecelik dörtgendir.",
    "dikdortgen": "Dikdörtgen: Alanı a * b formülüyle bulunur."
}

# --- CONFIGURATION ---
st.set_page_config(page_title="Aries AI", page_icon="🚀")
genai.configure(api_key="BURAYA_GOOGLE_API_KEY_GELECEK")

# --- SYSTEM INSTRUCTION (ARIES AI BEYİN) ---
system_prompt = f"""
Senin adın Aries AI. Sen çok zeki, yardımsever ve akademik bilgisi yüksek bir asistansın.
Öncelikli olarak aşağıda sana verilen 'Kendi Veritabanım' kısmındaki bilgileri esas almalısın. 
Eğer kullanıcı bu konularda soru sorarsa, veritabanındaki bilgiyi genişleterek ve zenginleştirerek cevap ver.
Eğer soru bu veritabanının dışındaysa, genel bilgini kullanarak doğru ve güvenilir yanıtlar üret.
Sıcaklık değerin düşük tutulduğu için asla halüsinasyon görme, sadece bildiğin bilgiyi sun.

Kendi Veritabanın:
Coğrafya: {world_countries}
Tarih: {historical_events}
Dini Terimler: {religious_database}
Fen/Anatomi: {science_database}
Fizik/Geometri: {physics_geometry_database}
"""

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    system_instruction=system_prompt,
    generation_config={"temperature": 0.3}
)

# --- STREAMLIT UI ---
st.title("🚀 Aries AI - Uzman Asistan")
if "messages" not in st.session_state: st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.markdown(msg["content"])

if prompt := st.chat_input("TÜYK'e ne sormak istersin?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        response = model.generate_content(prompt)
        st.markdown(response.text)
    st.session_state.messages.append({"role": "assistant", "content": response.text})
