from flask import Flask, render_template, request, jsonify

import ast
import operator
import math
import requests
import os
import re
from difflib import get_close_matches
from datetime import datetime


app = Flask(__name__)

# 🌍 COĞRAFYA VERİ TABANI

world_countries = {
    "turkiye": {"b": "Ankara", "k": "Asya/Avrupa", "lat": 39.93, "lon": 32.85, "bilgi": "Asya ve Avrupa'yı birbirine bağlayan stratejik bir köprü ülkedir."},
    "hindistan": {"b": "Yeni Delhi", "k": "Asya", "lat": 28.61, "lon": 77.20, "bilgi": "Güney Asya'da yer alan, dünyanın en kalabalık nüfusuna sahip ülkesidir."},
    "kuba": {"b": "Havana", "k": "Karayipler", "lat": 23.11, "lon": -82.36, "bilgi": "Karayip Denizi'nde yer alan bir ada devletidir."},
    "abd": {"b": "Washington D.C.", "k": "Kuzey Amerika", "lat": 38.90, "lon": -77.03, "bilgi": "50 eyaletten oluşan küresel bir güçtür."},
    "rusya": {"b": "Moskova", "k": "Asya/Avrupa", "lat": 55.75, "lon": 37.61, "bilgi": "Yüzölçümü bakımından dünyanın en büyük ülkesidir."},
    "almanya": {"b": "Berlin", "k": "Avrupa", "lat": 52.52, "lon": 13.40, "bilgi": "Orta Avrupa'da yer alan sanayi devidir."},
    "fransa": {"b": "Paris", "k": "Avrupa", "lat": 48.85, "lon": 2.35, "bilgi": "Batı Avrupa'da bulunan; sanat ve moda merkezidir."},
    "ingiltere": {"b": "Londra", "k": "Avrupa", "lat": 51.50, "lon": -0.12, "bilgi": "Büyük Britanya adasında yer alan köklü bir ülkedir."},
    "azerbaycan": {"b": "Bakü", "k": "Asya", "lat": 40.40, "lon": 49.86, "bilgi": "Kafkasya'da yer alan kardeş canı ülkedir."},

    # Avrupa
    "italya": {"b": "Roma", "k": "Avrupa", "lat": 41.90, "lon": 12.49, "bilgi": "Akdeniz'de çizme şeklindeki yarımadada yer alan, tarih ve sanatıyla ünlü bir ülkedir."},
    "ispanya": {"b": "Madrid", "k": "Avrupa", "lat": 40.42, "lon": -3.70, "bilgi": "İber Yarımadası'nda yer alan, flamenko ve boğa güreşiyle bilinen bir ülkedir."},
    "portekiz": {"b": "Lizbon", "k": "Avrupa", "lat": 38.72, "lon": -9.14, "bilgi": "İber Yarımadası'nın batısında, Atlas Okyanusu kıyısında yer alan bir ülkedir."},
    "yunanistan": {"b": "Atina", "k": "Avrupa", "lat": 37.98, "lon": 23.73, "bilgi": "Antik uygarlığın beşiklerinden biri olan, Ege'de yer alan bir ülkedir."},
    "hollanda": {"b": "Amsterdam", "k": "Avrupa", "lat": 52.37, "lon": 4.90, "bilgi": "Deniz seviyesinin altındaki topraklarıyla ve lale tarlalarıyla bilinen bir ülkedir."},
    "belcika": {"b": "Brüksel", "k": "Avrupa", "lat": 50.85, "lon": 4.35, "bilgi": "Avrupa Birliği'nin merkezi kabul edilen, Batı Avrupa'da yer alan bir ülkedir."},
    "isvicre": {"b": "Bern", "k": "Avrupa", "lat": 46.95, "lon": 7.45, "bilgi": "Alp Dağları'nda yer alan, tarafsızlığı ve bankacılığıyla bilinen bir ülkedir."},
    "avusturya": {"b": "Viyana", "k": "Avrupa", "lat": 48.21, "lon": 16.37, "bilgi": "Orta Avrupa'da yer alan, klasik müzik geleneğiyle bilinen bir ülkedir."},
    "polonya": {"b": "Varşova", "k": "Avrupa", "lat": 52.23, "lon": 21.01, "bilgi": "Orta Avrupa'da yer alan, Baltık Denizi'ne kıyısı olan bir ülkedir."},
    "ukrayna": {"b": "Kiev", "k": "Avrupa", "lat": 50.45, "lon": 30.52, "bilgi": "Doğu Avrupa'da yer alan, yüzölçümü bakımından Avrupa'nın en büyük ikinci ülkesidir."},
    "isvec": {"b": "Stockholm", "k": "Avrupa", "lat": 59.33, "lon": 18.07, "bilgi": "İskandinav Yarımadası'nda yer alan bir Kuzey Avrupa ülkesidir."},
    "norvec": {"b": "Oslo", "k": "Avrupa", "lat": 59.91, "lon": 10.75, "bilgi": "Fiyortlarıyla ünlü, İskandinav Yarımadası'nda yer alan bir ülkedir."},
    "finlandiya": {"b": "Helsinki", "k": "Avrupa", "lat": 60.17, "lon": 24.94, "bilgi": "Binlerce gölüyle bilinen, Kuzey Avrupa'da yer alan bir ülkedir."},
    "danimarka": {"b": "Kopenhag", "k": "Avrupa", "lat": 55.68, "lon": 12.57, "bilgi": "İskandinavya'nın güneyinde yer alan bir Kuzey Avrupa ülkesidir."},
    "irlanda": {"b": "Dublin", "k": "Avrupa", "lat": 53.35, "lon": -6.26, "bilgi": "Yeşil manzaralarıyla bilinen, Büyük Britanya'nın batısındaki bir ada ülkesidir."},
    "cekya": {"b": "Prag", "k": "Avrupa", "lat": 50.08, "lon": 14.44, "bilgi": "Orta Avrupa'da yer alan, tarihi mimarisiyle bilinen bir ülkedir."},
    "macaristan": {"b": "Budapeşte", "k": "Avrupa", "lat": 47.50, "lon": 19.04, "bilgi": "Orta Avrupa'da, Tuna Nehri kıyısında yer alan bir ülkedir."},
    "romanya": {"b": "Bükreş", "k": "Avrupa", "lat": 44.43, "lon": 26.10, "bilgi": "Balkanlar'ın kuzeyinde, Karadeniz'e kıyısı olan bir ülkedir."},
    "bulgaristan": {"b": "Sofya", "k": "Avrupa", "lat": 42.70, "lon": 23.32, "bilgi": "Balkanlar'da yer alan, Türkiye'nin komşusu olan bir ülkedir."},
    "sirbistan": {"b": "Belgrad", "k": "Avrupa", "lat": 44.79, "lon": 20.45, "bilgi": "Balkanlar'ın merkezinde yer alan, denize kıyısı olmayan bir ülkedir."},
    "kibris": {"b": "Lefkoşa", "k": "Asya/Avrupa", "lat": 35.19, "lon": 33.38, "bilgi": "Akdeniz'in doğusunda yer alan bir ada ülkesidir."},

    # Asya
    "japonya": {"b": "Tokyo", "k": "Asya", "lat": 35.68, "lon": 139.69, "bilgi": "Pasifik Okyanusu'nda yer alan, teknolojisiyle bilinen bir ada ülkesidir."},
    "cin": {"b": "Pekin", "k": "Asya", "lat": 39.90, "lon": 116.41, "bilgi": "Nüfus bakımından dünyanın en kalabalık ülkelerinden biridir."},
    "guney kore": {"b": "Seul", "k": "Asya", "lat": 37.57, "lon": 126.98, "bilgi": "Kore Yarımadası'nın güneyinde yer alan, teknoloji ve pop kültürüyle bilinen bir ülkedir."},
    "kuzey kore": {"b": "Pyongyang", "k": "Asya", "lat": 39.03, "lon": 125.75, "bilgi": "Kore Yarımadası'nın kuzeyinde yer alan bir ülkedir."},
    "endonezya": {"b": "Cakarta", "k": "Asya", "lat": -6.21, "lon": 106.85, "bilgi": "Binlerce adadan oluşan, Güneydoğu Asya'da yer alan bir ülkedir."},
    "pakistan": {"b": "İslamabad", "k": "Asya", "lat": 33.68, "lon": 73.05, "bilgi": "Güney Asya'da, Hindistan'ın komşusu olan bir ülkedir."},
    "banglades": {"b": "Dakka", "k": "Asya", "lat": 23.81, "lon": 90.41, "bilgi": "Güney Asya'da, nüfus yoğunluğu en yüksek ülkelerden biridir."},
    "iran": {"b": "Tahran", "k": "Asya", "lat": 35.69, "lon": 51.39, "bilgi": "Orta Doğu'da yer alan, köklü bir uygarlık tarihine sahip ülkedir."},
    "irak": {"b": "Bağdat", "k": "Asya", "lat": 33.31, "lon": 44.36, "bilgi": "Orta Doğu'da, Dicle ve Fırat nehirleri arasında yer alan bir ülkedir."},
    "suudi arabistan": {"b": "Riyad", "k": "Asya", "lat": 24.71, "lon": 46.68, "bilgi": "Arap Yarımadası'nın büyük bölümünü kaplayan, petrol rezervleriyle bilinen bir ülkedir."},
    "arap emirlikleri": {"b": "Abu Dabi", "k": "Asya", "lat": 24.47, "lon": 54.37, "bilgi": "Arap Yarımadası'nda yedi emirlikten oluşan bir ülkedir."},
    "katar": {"b": "Doha", "k": "Asya", "lat": 25.29, "lon": 51.53, "bilgi": "Arap Yarımadası'nda, Basra Körfezi'ne kıyısı olan küçük ama zengin bir ülkedir."},
    "misir": {"b": "Kahire", "k": "Afrika", "lat": 30.04, "lon": 31.24, "bilgi": "Nil Nehri kıyısında yer alan, antik piramitleriyle ünlü bir ülkedir."},
    "gurcistan": {"b": "Tiflis", "k": "Asya", "lat": 41.72, "lon": 44.79, "bilgi": "Kafkasya'da, Karadeniz'e kıyısı olan bir ülkedir."},
    "ermenistan": {"b": "Erivan", "k": "Asya", "lat": 40.18, "lon": 44.51, "bilgi": "Güney Kafkasya'da yer alan, denize kıyısı olmayan bir ülkedir."},
    "kazakistan": {"b": "Astana", "k": "Asya", "lat": 51.18, "lon": 71.45, "bilgi": "Orta Asya'da yer alan, yüzölçümü bakımından dünyanın en büyük dokuzuncu ülkesidir."},
    "ozbekistan": {"b": "Taşkent", "k": "Asya", "lat": 41.30, "lon": 69.24, "bilgi": "Orta Asya'da yer alan bir ülkedir."},
    "suriye": {"b": "Şam", "k": "Asya", "lat": 33.51, "lon": 36.28, "bilgi": "Orta Doğu'da, Türkiye'nin güney komşusu olan bir ülkedir."},
    "urdun": {"b": "Amman", "k": "Asya", "lat": 31.95, "lon": 35.93, "bilgi": "Orta Doğu'da yer alan, Petra antik kentiyle bilinen bir ülkedir."},
    "lubnan": {"b": "Beyrut", "k": "Asya", "lat": 33.89, "lon": 35.50, "bilgi": "Doğu Akdeniz kıyısında yer alan küçük bir Orta Doğu ülkesidir."},
    "israil": {"b": "Kudüs / Tel Aviv", "k": "Asya", "lat": 31.77, "lon": 35.21, "bilgi": "Orta Doğu'da yer alan bir ülkedir; başkent statüsü uluslararası düzeyde tartışmalıdır, birçok ülke büyükelçiliğini Tel Aviv'de bulundurur."},

    # Afrika
    "fas": {"b": "Rabat", "k": "Afrika", "lat": 34.02, "lon": -6.84, "bilgi": "Kuzey Afrika'da, Cebelitarık Boğazı'na yakın konumda yer alan bir ülkedir."},
    "cezayir": {"b": "Cezayir", "k": "Afrika", "lat": 36.75, "lon": 3.06, "bilgi": "Kuzey Afrika'da, Akdeniz kıyısında yer alan, yüzölçümü açısından Afrika'nın en büyük ülkesidir."},
    "tunus": {"b": "Tunus", "k": "Afrika", "lat": 36.81, "lon": 10.18, "bilgi": "Kuzey Afrika'da, Akdeniz kıyısında yer alan küçük bir ülkedir."},
    "nijerya": {"b": "Abuja", "k": "Afrika", "lat": 9.08, "lon": 7.40, "bilgi": "Batı Afrika'da yer alan, nüfusu en kalabalık Afrika ülkesidir."},
    "guney afrika": {"b": "Pretoria", "k": "Afrika", "lat": -25.75, "lon": 28.19, "bilgi": "Afrika kıtasının en güneyinde yer alan, üç başkenti olan bir ülkedir."},
    "kenya": {"b": "Nairobi", "k": "Afrika", "lat": -1.29, "lon": 36.82, "bilgi": "Doğu Afrika'da yer alan, safari turizmiyle bilinen bir ülkedir."},
    "etiyopya": {"b": "Addis Ababa", "k": "Afrika", "lat": 9.03, "lon": 38.74, "bilgi": "Doğu Afrika'da yer alan, hiç sömürge olmamış nadir Afrika ülkelerinden biridir."},

    # Amerika
    "brezilya": {"b": "Brasilia", "k": "Güney Amerika", "lat": -15.79, "lon": -47.88, "bilgi": "Güney Amerika'da yer alan, Amazon Ormanları'nın büyük kısmını barındıran ülkedir."},
    "arjantin": {"b": "Buenos Aires", "k": "Güney Amerika", "lat": -34.60, "lon": -58.38, "bilgi": "Güney Amerika'da yer alan, tango ve futbolla özdeşleşmiş bir ülkedir."},
    "sili": {"b": "Santiago", "k": "Güney Amerika", "lat": -33.45, "lon": -70.65, "bilgi": "And Dağları boyunca uzanan, ince ve uzun şekliyle bilinen bir Güney Amerika ülkesidir."},
    "meksika": {"b": "Meksiko", "k": "Kuzey Amerika", "lat": 19.43, "lon": -99.13, "bilgi": "Kuzey Amerika'nın güneyinde yer alan, Aztek ve Maya mirasına sahip bir ülkedir."},
    "kanada": {"b": "Ottava", "k": "Kuzey Amerika", "lat": 45.42, "lon": -75.70, "bilgi": "Yüzölçümü bakımından dünyanın en büyük ikinci ülkesidir."},

    # Okyanusya
    "avustralya": {"b": "Kanberra", "k": "Okyanusya", "lat": -35.28, "lon": 149.13, "bilgi": "Hem kıta hem ülke olan, kendine özgü hayvan türleriyle bilinen bir ülkedir."},
    "yeni zelanda": {"b": "Wellington", "k": "Okyanusya", "lat": -41.29, "lon": 174.78, "bilgi": "Pasifik Okyanusu'nda yer alan, doğal manzaralarıyla ünlü bir ada ülkesidir."}
}

# 📜 TARİH VERİ TABANI

historical_events = {
    "istanbulun fethi": "<b>1453 - İstanbul'un Fethi:</b> Fatih Sultan Mehmed liderliğindeki Osmanlı ordusu Bizans'ı yıktı. Orta Çağ kapandı, Yeni Çağ başladı.",
    "cumhuriyetin ilani": "<b>29 Ekim 1923 - Cumhuriyetin İlanı:</b> Gazi Mustafa Kemal Atatürk önderliğinde Türkiye Cumhuriyeti resmen kuruldu. 🇹🇷",
    "malazgirt": "<b>1071 - Malazgirt Meydan Muharebesi:</b> Sultan Alparslan komutasındaki Büyük Selçuklu ordusu, Anadolu'nun kapılarını Türklere açtı.",
    "buyuk taarruz": "<b>1922 - Büyük Taarruz:</b> Türk Kurtuluş Savaşı'nın son evresi. Anadolu düşman işgalinden tamamen temizlendi."
}

# 🕋 DİNİ TERİMLER VERİ TABANI

religious_database = {
    "hicret": "<b>Hicret (622):</b> Hz. Muhammed (s.a.v.) ve Müslümanların Mekke'den Medine'ye göç etmesidir. Hicri takvimin başlangıcıdır.",
    "bedir savasi": "<b>Bedir Savaşı (624):</b> Müslümanlar ile Mekkeli müşrikler arasındaki ilk büyük savaştır. Müslümanlar zafer kazanmıştır.",
    "mekkenin fethi": "<b>Mekke'nin Fethi (630):</b> Hz. Muhammed liderliğindeki İslam ordusu kan dökmeden Mekke'ye girdi.",
    "siyer": "<b>Siyer:</b> Peygamber Efendimiz Hz. Muhammed'in (s.a.v.) hayatını inceleyen bilim dalıdır."
}

# 🧬 ANATOMİ VE FEN VERİ TABANI

science_database = {
    "kalp": "<b>Anatomi - Kalp:</b> Göğüs boşluğunda yer alan, kaslı bir pompadır. Vücuda kan pompalar. Üstte iki kulakçık, altta iki karıncık olmak üzere 4 odacıktan oluşur.",
    "akciyer": "<b>Anatomi - Akciğerler:</b> Solunum sisteminin ana organıdır. Göğüs kafesinde sağ ve sol olmak üzere iki adettir. Kana oksijen sağlar, karbondioksiti dışarı atar.",
    "karaciyer": "<b>Anatomi - Karaciğer:</b> Vücudun en büyük iç organıdır ve adeta bir kimya fabrikası gibi çalışır. Safra üretir, toksinleri temizler ve glikoz depolar.",
    "hucre": "<b>Fen Bilgisi - Hücre:</b> Canlıların canlılık özelliği gösteren en küçük yapı taşıdır. Hücre zarı, sitoplazma ve çekirdek olmak üzere üç temel kısımdan oluşur.",
    "fotosentez": "<b>Fen Bilgisi - Fotosentez:</b> Bitkilerin kloroplast organelinde, güneş ışığı yardımıyla su ve karbondioksiti birleştirerek besin (glikoz) ve oksijen üretmesi olayıdır.",
    "mitokondri": "<b>Fen Bilgisi - Mitokondri:</b> Hücrenin enerji santralidir. Oksijenli solunum yaparak hücre için gerekli olan ATP (enerji) molekülünü üretir."
}

# ⚡ FİZİK VE GEOMETRİ VERİ TABANI

physics_geometry_database = {
    "yercekimi": "<b>Fizik - Yerçekimi Kuvveti:</b> Kütlesi olan cisimlerin birbirini çekmesidir. Dünyadaki yerçekimi ivmesi yaklaşık olarak $g = 9.81 m/s^2$ kabul edilir. Keşfeden bilim insanı Isaac Newton'dır.",
    "surtunme": "<b>Fizik - Sürtünme Kuvveti:</b> Harekete karşı koyan zorlayıcı kuvvettir. Temas eden yüzeyler arasında oluşur ve kinetik enerjiyi ısı enerjisine dönüştürür.",
    "ohm kanunu": "<b>Fizik - Ohm Kanunu:</b> Bir elektrik devresinde gerilim (V), akım (I) ve direnç (R) arasındaki ilişkiyi açıklar. Formülü: $V = I \\cdot R$ şeklindedir.",
    "ucgen": "<b>Geometri - Üçgen:</b> Üç doğrunun kesişmesiyle oluşan kapalı şekildir. İç açılarının toplamı her zaman **180°**, dış açılarının toplamı ise **360°**'dir.",
    "kare": "<b>Geometri - Kare:</b> Tüm kenarları birbirine eşit ve tüm iç açıları **90°** olan düzgün bir dörtgendir. Alanı bir kenarının karesidir ($A = a^2$).",
    "dikdortgen": "<b>Geometri - Dikdörtgen:</b> Karşılıklı kenarları eşit ve paralel, tüm iç açıları **90°** olan dörtgendir. Çevresi: $2(a+b)$, Alanı: $a \\cdot b$ formülüyle bulunur."
}

# 👋 SELAMLAŞMA KELİMELERİ (fuzzy eşleşme için)
GREETING_WORDS = ["selam", "merhaba", "naber", "selamlar", "merhabalar", "hey", "hi"]

# 🙏 TEŞEKKÜR / NEZAKET KELİMELERİ (fuzzy eşleşme için)
THANKS_WORDS = ["tesekkurler", "tesekkur", "sagol", "sagolasin", "eyvallah", "sagolun", "minnettarim", "ellerinesaglik"]

# 😊 "RİCA EDERİM" TÜRÜ KARŞILIK KALIPLARI (kullanıcı bota teşekkür ettiğinde bot cevap veriyor;
# ama kullanıcı "rica ederim" derse bota bir onay/nezaket cevabı gerekiyor)
YOURE_WELCOME_WORDS = ["ricaederim", "ricaederiz", "birseydegil", "nedemek", "onemlidegil"]

# 🏗️ "KİM YAPTI" SORU KALIPLARI (boşluksuz/bitişik hâliyle de kontrol edilecek)
CREATOR_PHRASES = ["kim yapti", "yapimcin", "kim gelistirdi", "kurucun", "sahibin", "sen kimsin", "adini kim verdi"]


def calculate_haversine(lat1, lon1, lat2, lon2):
    R = 6371
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    a = math.sin(d_lat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(d_lon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(R * c)


def fetch_country_from_api(country_name):
    try:
        url = f"https://restcountries.com/v3.1/name/{country_name}"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()[0]
            name_tr = data.get("translations", {}).get("tur", {}).get("common", country_name).upper()
            capital = data.get("capital", ["Bilinmiyor"])[0]
            region = data.get("continents", ["Bilinmiyor"])[0]
            population = data.get("population", 0)
            flag = data.get("flag", "🌐")
            latlng = data.get("latlng", [0, 0])
            return {
                "name": name_tr, "b": capital, "k": region, "lat": latlng[0], "lon": latlng[1],
                "bilgi": f"{flag} {name_tr}, {region} kıtasında yer alan bir ülkedir."
            }
    except Exception:
        pass
    return None


# --------------------------------------------------------------------------
# 🔒 GÜVENLİ MATEMATİK MOTORU (eval() yerine)
# eval() kullanıcı girdisini doğrudan çalıştırdığı için güvenlik riski
# taşır. Bunun yerine sadece +,-,*,/ ve parantezlere izin veren bir
# ast tabanlı hesaplayıcı kullanıyoruz. Ayrıca çok uzun / çok büyük
# işlemleri (DoS riski) baştan engelliyoruz.
# --------------------------------------------------------------------------

_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}

MAX_EXPRESSION_LENGTH = 60          # aşırı uzun ifadeleri reddet
MAX_NUMBER_LENGTH = 15               # tek bir sayı en fazla 15 haneli olabilir


def _safe_eval_node(node):
    if isinstance(node, ast.Expression):
        return _safe_eval_node(node.body)
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            if len(str(node.value).replace(".", "").replace("-", "")) > MAX_NUMBER_LENGTH:
                raise ValueError("Sayı çok büyük.")
            return node.value
        raise ValueError("Geçersiz değer.")
    if isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED_OPERATORS:
        left = _safe_eval_node(node.left)
        right = _safe_eval_node(node.right)
        return _ALLOWED_OPERATORS[type(node.op)](left, right)
    if isinstance(node, ast.UnaryOp) and type(node.op) in _ALLOWED_OPERATORS:
        return _ALLOWED_OPERATORS[type(node.op)](_safe_eval_node(node.operand))
    raise ValueError("Desteklenmeyen işlem.")


def safe_math_eval(expression):
    if len(expression) > MAX_EXPRESSION_LENGTH:
        raise ValueError("İfade çok uzun.")
    tree = ast.parse(expression, mode="eval")
    return _safe_eval_node(tree.body)


def fuzzy_word_in(word, candidates, cutoff=0.8):
    """Kelimeyi ve adaylarını difflib ile karşılaştırıp yazım hatalarını tolere eder."""
    if word in candidates:
        return True
    return bool(get_close_matches(word, candidates, n=1, cutoff=cutoff))


@app.route('/')
def home():
    return render_template('index.html')


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

    if password != "4235":
        return jsonify({"success": False, "message": "Hatalı şifre!"}), 403, response_headers

    if action == 'clear':
        if os.path.exists("sorular.txt"):
            os.remove("sorular.txt")
        return jsonify({"success": True, "logs": []}), 200, response_headers

    if os.path.exists("sorular.txt"):
        with open("sorular.txt", "r", encoding="utf-8") as file:
            logs = file.readlines()
        clean_logs = [line.strip() for line in logs if line.strip()]
        return jsonify({"success": True, "logs": list(reversed(clean_logs)) if clean_logs else ["Henüz hiç soru sorulmadı."]}), 200, response_headers
    return jsonify({"success": True, "logs": ["Henüz hiç soru sorulmadı."]}), 200, response_headers


@app.route('/ask', methods=['POST'])
def ask():
    user_message = request.json.get("message", "").lower().strip()
    raw_message = request.json.get("message", "").strip()
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    user_ip = request.remote_addr

    def save_log(status_msg):
        with open("sorular.txt", "a", encoding="utf-8") as file:
            file.write(f"[{current_time}] IP: {user_ip} | DURUM: {status_msg} -> Soru: {raw_message}\n")

    # Noktalama temizliği
    user_message = re.sub(r'[.,\?!;\(\)"\'’\-]', '', user_message)
    norm_msg = user_message.replace("ı", "i").replace("ğ", "g").replace("ü", "u").replace("ş", "s").replace("ö", "o").replace("ç", "c")

    # 🛠️ YANLIŞ YAZIM VE KISALTMA TOLERANS MOTORU (nber, slm, naber, marhaba...)
    typo_rules = {
        "nber": "naber", "nbr": "naber", "slm": "selam", "mrb": "merhaba",
        "mrhb": "merhaba", "knk": "kanka", "kgo": "coğrafya", "mat": "matematik",
        "fzk": "fizik", "gmt": "geometri", "antm": "anatomi", "akciger": "akciyer",
        "marhaba": "merhaba", "mehraba": "merhaba", "selm": "selam",
    }
    words = norm_msg.split()
    fixed_words = [typo_rules.get(w, w) for w in words]
    norm_msg = " ".join(fixed_words)
    norm_msg_nospace = norm_msg.replace(" ", "")  # bitişik yazımları yakalamak için (örn. "kimyapti")

    # Kanka modu SADECE kullanıcı gerçekten "kanka" derse aktif olur.
    # ("naber" artık kanka modunu tetiklemiyor; varsayılan ton ciddi/nazik kalır.)
    is_buddy_mode = "kanka" in norm_msg

    # 🏗️ Yapımcı Kontrolü (bitişik yazımı da destekler: "seni kimyaptı")
    if any(p in norm_msg for p in CREATOR_PHRASES) or any(p.replace(" ", "") in norm_msg_nospace for p in CREATOR_PHRASES):
        save_log("CEVAPLANDI")
        if is_buddy_mode:
            return jsonify({"reply": '<span class="expert-badge badge-sozel">Sistem Çekirdeği</span><br>Beni tam bir dahi olmam için <b>MİC</b> geliştirdi kanka! Adım <b>ARIES AI</b>. 🚀'})
        return jsonify({"reply": '<span class="expert-badge badge-sozel">Sistem Çekirdeği</span><br>Beni <b>MİC</b> geliştirdi. Adım <b>ARIES AI</b>.'})

    # 👋 Selamlaşma Kontrolü (fuzzy: "naber", "marhaba dostum" gibi yazım hatalarını da yakalar)
    if any(fuzzy_word_in(w, GREETING_WORDS) for w in fixed_words):
        save_log("CEVAPLANDI")
        if is_buddy_mode:
            return jsonify({"reply": "Naber kanka! ARIES AI hazır, ne soruyoruz? 😎"})
        return jsonify({"reply": "Merhaba, ben ARIES AI. Size nasıl yardımcı olabilirim?"})

    # 🙏 Teşekkür Kontrolü ("teşekkürler", "sağol", "eyvallah" vb. — fuzzy eşleşme ile yazım hatalarını da tolere eder)
    if any(fuzzy_word_in(w, THANKS_WORDS, cutoff=0.75) for w in fixed_words):
        save_log("CEVAPLANDI")
        if is_buddy_mode:
            return jsonify({"reply": "Rica ederim kanka, başka bir sorun olursa buradayım! 🙌"})
        return jsonify({"reply": "Rica ederim, başka bir konuda yardımcı olabilirim."})

    # 😊 "Rica ederim / bir şey değil" Kontrolü (kullanıcı bota bu şekilde karşılık verdiğinde)
    if any(p in norm_msg_nospace for p in YOURE_WELCOME_WORDS):
        save_log("CEVAPLANDI")
        return jsonify({"reply": "Ne demek, her zaman yardımcı olmaktan memnuniyet duyarım. 😊"})

    # 🔢 Matematik Motoru (güvenli hesaplayıcı ile)
    math_message = user_message.replace(",", ".")
    math_chars = set("0123456789+-*/(). ")
    if any(char in math_message for char in ['+', '-', '*', '/']) and set(math_message).issubset(math_chars):
        try:
            result = safe_math_eval(math_message)
            save_log("CEVAPLANDI")
            return jsonify({"reply": f'<span class="expert-badge badge-sayisal">Matematiksel Analiz</span><br><div class="formula-box">{user_message} = {result}</div>'})
        except Exception:
            save_log("HATA")
            if is_buddy_mode:
                return jsonify({"reply": "İşlem hesaplanamadı kanka, sayılar çok büyük olabilir ya da ifade geçersiz. Kontrol et."})
            return jsonify({"reply": "İşlem hesaplanamadı. Sayılar çok büyük olabilir ya da ifade geçersiz görünüyor, lütfen kontrol edin."})

    # 🧬 Anatomi ve Fen Bilgisi Kontrolü
    for key, response in science_database.items():
        if key in norm_msg:
            save_log("CEVAPLANDI")
            return jsonify({"reply": f'<span class="expert-badge badge-sayisal" style="background-color:#00e676; color:black;">Fen Bilimleri & Anatomi</span><br>{response}'})

    # ⚡ Fizik ve Geometri Kontrolü
    for key, response in physics_geometry_database.items():
        if key in norm_msg:
            save_log("CEVAPLANDI")
            return jsonify({"reply": f'<span class="expert-badge badge-sayisal" style="background-color:#ff9100; color:black;">Fizik & Geometri</span><br>{response}'})

    # 🕋 Dini Terimler Kontrolü
    for key, response in religious_database.items():
        if key in norm_msg:
            save_log("CEVAPLANDI")
            return jsonify({"reply": f'<span class="expert-badge badge-sozel" style="background-color:#9c27b0;">İslami Tarih</span><br>{response}'})

    # 📜 Tarih Kontrolü
    for key, response in historical_events.items():
        if key.replace("ı", "i").replace("ğ", "g") in norm_msg:
            save_log("CEVAPLANDI")
            return jsonify({"reply": f'<span class="expert-badge badge-sozel">Tarih Bilgisi</span><br>{response}'})

    # 🌍 Coğrafya Kontrolü
    matched_countries = []
    for country, data in world_countries.items():
        if country in norm_msg:
            matched_countries.append({"name": country.upper(), "b": data["b"], "k": data["k"], "lat": data["lat"], "lon": data["lon"], "bilgi": data["bilgi"]})

    if len(matched_countries) >= 2:
        distance = calculate_haversine(matched_countries[0]["lat"], matched_countries[0]["lon"], matched_countries[1]["lat"], matched_countries[1]["lon"])
        save_log("CEVAPLANDI")
        return jsonify({"reply": f'<span class="expert-badge badge-cografya">Rota Analizi</span><br>📐 <b>Mesafe:</b> ~{distance} Kilometre'})
    elif len(matched_countries) == 1:
        save_log("CEVAPLANDI")
        return jsonify({"reply": f'<span class="expert-badge badge-cografya">Coğrafya</span><br><b>Ülke:</b> {matched_countries[0]["name"]}<br><b>Başkent:</b> {matched_countries[0]["b"]}'})

    save_log("CEVAPLANAMADI")
    if is_buddy_mode:
        return jsonify({"reply": "ARIES bu soruyu analiz etti ama tam bir eşleşme bulamadı kanka. Matematik, fen, fizik, geometri, anatomi, tarih veya coğrafya sormayı dene!"})
    return jsonify({"reply": "ARIES bu soruyu analiz etti ancak tam bir eşleşme bulamadı. Matematik, fen bilimleri, fizik, geometri, anatomi, tarih veya coğrafya ile ilgili bir soru sormayı deneyebilirsiniz."})


if __name__ == '__main__':
    app.run(debug=True)
