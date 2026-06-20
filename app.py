from flask import Flask, render_template, request, jsonify
import math
import requests
import os
import re  
from datetime import datetime  

app = Flask(__name__)

# 🌍 MEGA COĞRAFYA VERİ TABANI (TÜM POPÜLER ÜLKELER EKLENDİ)
world_countries = {
    "turkiye": {"b": "Ankara", "k": "Asya/Avrupa", "lat": 39.93, "lon": 32.85, "bilgi": "Asya ve Avrupa'yı birbirine bağlayan, üç tarafı denizlerle çevrili, şanlı bir tarihe sahip stratejik bir köprü ülkedir. En büyük şehri İstanbul'dur."},
    "hindistan": {"b": "Yeni Delhi", "k": "Asya", "lat": 28.61, "lon": 77.20, "bilgi": "Güney Asya'da yer alan, dünyanın en kalabalık nüfusuna sahip, Tac Mahal gibi devasa tarihi eserleri barındıran rengarenk bir kültür ülkesidir."},
    "kuba": {"b": "Havana", "k": "Karayipler", "lat": 23.11, "lon": -82.36, "bilgi": "Karayip Denizi'nde yer alan, kendine has müzikleri, puroları, klasik arabaları ve tarihi mimarisiyle ünlü bir ada devletidir."},
    "abd": {"b": "Washington D.C.", "k": "Kuzey Amerika", "lat": 38.90, "lon": -77.03, "bilgi": "Kuzey Amerika kıtasında bulunan, 50 eyaletten oluşan, ekonomik ve teknolojik açıdan küresel bir süper güçtür."},
    "amerika": {"b": "Washington D.C.", "k": "Kuzey Amerika", "lat": 38.90, "lon": -77.03, "bilgi": "Kuzey Amerika kıtasında bulunan küresel bir federal devlettir."},
    "rusya": {"b": "Moskova", "k": "Asya/Avrupa", "lat": 55.75, "lon": 37.61, "bilgi": "Yüzölçümü bakımından dünyanın en büyük ülkesidir. Devasa doğal gaz ve yer altı kaynaklarına sahip, iki kıtaya yayılmış bir devdir."},
    "almanya": {"b": "Berlin", "k": "Avrupa", "lat": 52.52, "lon": 13.40, "bilgi": "Orta Avrupa'da yer alan; Mercedes, BMW gibi markaları üreten, sanayisi, mühendisliği ve teknolojisi son derece gelişmiş bir Avrupa gücüdür."},
    "fransa": {"b": "Paris", "k": "Avrupa", "lat": 48.85, "lon": 2.35, "bilgi": "Batı Avrupa'da bulunan; sanat, moda, Eyfel Kulesi, gurme mutfağı ve köklü siyasi tarihiyle (Fransız İhtilali) tanınan lider bir ülkedir."},
    "ingiltere": {"b": "Londra", "k": "Avrupa", "lat": 51.50, "lon": -0.12, "bilgi": "Büyük Britanya adasında yer alan, geçmişte 'üzerinde güneş batmayan imparatorluk' olarak bilinen köklü ve güçlü bir denizci ülkesidir."},
    "hollanda": {"b": "Amsterdam", "k": "Avrupa", "lat": 52.36, "lon": 4.90, "bilgi": "Topraklarının büyük kısmı deniz seviyesinin altında olan, bendlerle korunan, yel değirmenleri, kanalları ve laleleriyle ünlü Batı Avrupa ülkesidir."},
    "italya": {"b": "Roma", "k": "Avrupa", "lat": 41.90, "lon": 12.49, "bilgi": "Akdeniz'e uzanan çizme şeklindeki yarımadada kurulmuş; Pisa Kulesi, Kolezyum gibi eserlere sahip Roma İmparatorluğu'nun beşiğidir."},
    "japonya": {"b": "Tokyo", "k": "Asya", "lat": 35.67, "lon": 139.65, "bilgi": "Doğu Asya'da bir ada ülkesidir. Robotik teknolojisi, otomotiv sanayisi, anime kültürü ve köklü samuray gelenekleriyle tanınır."},
    "mısır": {"b": "Kahire", "k": "Afrika", "lat": 30.04, "lon": 31.23, "bilgi": "Kuzey Afrika ile Orta Doğu'yu bağlayan, insanlık tarihinin en eski medeniyetlerinden biri olan, Nil Nehri ve antik Gize Piramitleri'nin ev sahibidir."},
    "brezilya": {"b": "Brasilia", "k": "Güney Amerika", "lat": -15.79, "lon": -47.88, "bilgi": "Güney Amerika'nın en büyük ve en kalabalık ülkesidir. Dünyanın oksijen deposu olan Amazon Ormanları'na ve futbol kültürüne ev sahipliği yapar."},
    "azerbaycan": {"b": "Bakü", "k": "Asya", "lat": 40.40, "lon": 49.86, "bilgi": "Kafkasya'da yer alan, zengin petrol ve doğal gaz yataklarına sahip, Türkiye ile 'Tek millet, iki devlet' bağına sahip can kardeş ülkemizdir."},
    "cin": {"b": "Pekin", "k": "Asya", "lat": 39.90, "lon": 116.40, "bilgi": "Doğu Asya'da devasa bir üretim gücüne ve milyarlık nüfusa sahip, dünyanın en uzun savunma duvarı olan Çin Seddi ile ünlü kadim bir ülkedir."},
    "kanada": {"b": "Ottava", "k": "Kuzey Amerika", "lat": 45.42, "lon": -75.69, "bilgi": "Dünyanın en geniş yüzölçümüne sahip ikinci ülkesidir. Soğuk iklimi, akçaağaç şurubu, gölleri ve yüksek yaşam kalitesiyle bilinir."},
    "ispanya": {"b": "Madrid", "k": "Avrupa", "lat": 40.41, "lon": -3.70, "bilgi": "İber Yarımadası'nda yer alan; boğa güreşleri, flamenko dansı, Endülüs İslam tarihi kalıntıları ve futboluyla ünlü bir Akdeniz ülkesidir."},
    "guney afrika": {"b": "Pretoria", "k": "Afrika", "lat": -25.74, "lon": 28.18, "bilgi": "Afrika kıtasının en güney ucunda yer alan, elmas ve altın madenleri bakımından dünyanın en zengin, doğasıyla büyüleyici ülkesidir."},
    "avustralya": {"b": "Kanberra", "k": "Okyanusya", "lat": -35.28, "lon": 149.13, "bilgi": "Kendi başına bir kıta olan ada ülkesidir. Kangurular, koalalar ve Sidney Opera Binası ile tanınan çok büyük bir coğrafyadır."}
}

# 📜 UPUPUZUN TARİH VERİ TABANI
historical_events = {
    "istanbulun fethi": "<b>1453 - İstanbul'un Fethi:</b> Fatih Sultan Mehmed liderliğindeki Osmanlı ordusu Bizans'ı (Doğu Roma) yıktı. Gemiler karadan yürütüldü, surlar dev toplarla yıkıldı. Orta Çağ kapandı, Yeni Çağ başladı.",
    "cumhuriyetin ilani": "<b>29 Ekim 1923 - Cumhuriyetin İlanı:</b> Gazi Mustafa Kemal Atatürk önderliğinde kazanılan Kurtuluş Savaşı'nın ardından Türkiye Cumhuriyeti resmen kuruldu ve egemenlik kayıtsız şartsız millete geçti. 🇹🇷",
    "malazgirt": "<b>1071 - Malazgirt Meydan Muharebesi:</b> Büyük Selçuklu Sultanı Alparslan komutasındaki Türk ordusu, kendinden kat kat kalabalık Bizans ordusunu hilal taktiğiyle yenerek Anadolu'nun kapılarını Türklere sonsuza dek açtı.",
    "buyuk taarruz": "<b>30 Ağustos 1922 - Büyük Taarruz (Başkomutanlık Meydan Muharebesi):</b> Atatürk'ün 'Ordular, ilk hedefiniz Akdeniz'dir, ileri!' emriyle başlayan büyük harekat. Yunan ordusu bozguna uğratıldı ve Anadolu işgalden tamamen temizlendi.",
    "1 dunya savasi": "<b>1914 - 1918 (I. Dünya Savaşı):</b> İtilaf (İngiltere, Fransa, Rusya) ve İttifak (Almanya, Osmanlı, Avusturya-Macaristan) devletleri arasında çıkan, Osmanlı'nın Çanakkale'de destan yazdığı küresel büyük savaştır.",
    "2 dunya savasi": "<b>1939 - 1945 (II. Dünya Savaşı):</b> Adolf Hitler liderliğindeki Almanya'nın Polonya'yı işgaliyle başlayan; Mihver ve Müttefik devletler arasında geçen, atom bombasının kullanıldığı insanlık tarihinin en kanlı savaşıdır.",
    "fransiz ihtilali": "<b>1789 - Fransız İhtilali:</b> Halkın krala isyan etmesiyle Fransa'da başlayan olaylardır. Dünyada milliyetçilik, hürriyet, adalet ve eşitlik akımlarının yayılmasına sebep olmuş, imparatorlukları sarsmış ve Yakın Çağ'ı başlatmıştır.",
    "ronesans": "<b>14. - 17. Yüzyıl (Rönesans):</b> İtalya'da başlayan; bilim, sanat, edebiyat ve felsefede 'yeniden doğuşu' simgeleyen dönemdir. Leonardo da Vinci, Michelangelo gibi dâhiler bu dönemde yetişmiştir.",
    "cografi kesifler": "<b>15. ve 16. Yüzyıl - Coğrafi Keşifler:</b> Avrupalıların pusulanın gelişmesiyle yeni ticaret yolları ve kıtalar (Amerika gibi) bulmak amacıyla başlattığı, ipek ve baharat yollarına alternatif arayan büyük deniz aşırı keşif dönemidir.",
    "reform": "<b>16. Yüzyıl - Reform Dönemi:</b> Almanya'da Martin Luther öncülüğünde başlayan, Katolik Kilisesi'nin baskılarına ve yozlaşmasına karşı yapılan dini yenilik hareketidir. Eğitimin kiliseden alınmasını sağlamıştır."
}

# 🕋 UPUPUZUN DİNİ TERİMLER VERİ TABANI
religious_database = {
    "hicret": "<b>Hicret (622):</b> Hz. Muhammed (s.a.v.) ve Mekkeli Müslümanların, müşriklerin baskıları yüzünden Mekke'den Medine'ye göç etmesidir. Bu olay İslam devletinin temelini atmış ve Hicri takvimin başlangıcı olmuştur.",
    "bedir savasi": "<b>Bedir Savaşı (624):</b> Müslümanlar ile Mekkeli müşrikler arasındaki ilk büyük savaştır. Sayıca az olan Müslüman ordusu, Allah'ın yardımıyla büyük bir zafer kazanmış ve İslam'ın gücünü kanıtlamıştır.",
    "uhud savasi": "<b>Uhud Savaşı (625):</b> Mekkeli müşriklerle yapıldı. Efendimizin görevlendirdiği okçuların yerlerini erkenden terk etmesi sonucu Müslümanlar iki ateş arasında kalmış, zor anlar yaşanmış ve Peygamberimizin amcası Hz. Hamza şehit düşmüştür.",
    "hendek savasi": "<b>Hendek Savaşı (627):</b> Medine'yi kuşatmaya gelen dev müşrik ordusuna karşı, Selman-ı Farisi'nin önerisiyle şehrin etrafına derin hendekler kazılarak yapılan efsanevi, sabır ve strateji dolu bir savunma savaşıdır.",
    "mekkenin fethi": "<b>Mekke'nin Fethi (630):</b> Hz. Muhammed (s.a.v.) liderliğindeki muazzam İslam ordusu, hiçbir kan dökmeden, büyük bir merhamet ve barışla Mekke'ye girdi. Kabe'deki tüm putlar yıkılarak tevhid inancı hakim kılındı.",
    "dort halife": "<b>Dört Halife Dönemi:</b> Peygamber Efendimizden sonra İslam toplumunu adaletle yöneten sırasıyla şu mübarek isimlerdir:<br>1. Hz. Ebubekir (Sadakat)<br>2. Hz. Ömer (Adalet)<br>3. Hz. Osman (Haya ve Kur'an'ın toplanması)<br>4. Hz. Ali (İlim ve Cesaret)",
    "fikih": "<b>Fıkıh İlmi:</b> İslam'ın ibadet, evlilik, ticaret gibi günlük hayatla ilgili hukuksal ve ameli kurallarını, detaylarını derinlemesine inceleyen ve yorumlayan İslam hukuku bilim dalıdır.",
    "tefsir": "<b>Tefsir İlmi:</b> Kur'an-ı Kerim'in ayetlerini iniş sebeplerine, dil özelliklerine ve peygamberimizin açıklamalarına dayanarak en doğru ve detaylı şekilde açıklayan, yorumlayan kutsal bilim dalıdır.",
    "hadis": "<b>Hadis-i Şerif:</b> Sevgili Peygamberimiz Hz. Muhammed'in (s.a.v.) söylediği mübarek sözler, yaptığı davranışlar ve ashabının yaptığı işleri onaylamasının (takrir) yazılı ve sözlü bütün bütünüdür.",
    "kelam": "<b>Kelam İlmi:</b> İslam dininin inanç esaslarını (imanın şartlarını) akli mantık yürütmelerle ve ayet-hadis delilleriyle savunan, felsefi eleştirilere karşı inancı koruyan bilim dalıdır.",
    "akait": "<b>Akait:</b> İslam dininde gönülden inanılması, şüphe duyulmaması zorunlu olan temel inanç esaslarının (Allah'a, meleklere, kitaplara, peygamberlere, ahirete, kadere iman) oluşturduğu kurallar bütünüdür.",
    "siyer": "<b>Siyer Bilimi:</b> Peygamber Efendimiz Hz. Muhammed'in (s.a.v.) kutlu doğumu, mucizeleri, çocukluğu, gençliği, evliliği ve peygamberlik dönemindeki tüm savaş ve mücadelelerini, yani tüm hayatını kronolojik inceleyen bilim dalıdır."
}

# 🧬 UPUPUZUN ANATOMİ VE FEN VERİ TABANI
science_database = {
    "kalp": "<b>Anatomi - Kalp:</b> Göğüs boşluğunda, iki akciğer arasında yer alan, güçlü kaslardan oluşan hayati bir pompadır. Kirli kanı akciğere temizlenmesi için gönderir, temiz kanı ise tüm vücuda pompalar. Üstte iki kulakçık, altta iki karıncık olmak üzere toplam 4 odacıktan oluşur.",
    "akciyer": "<b>Anatomi - Akciğerler:</b> Solunum sistemimizin merkez organıdır. Göğüs kafesinin içinde, sağ ve sol olmak üzere iki adettir. Havadan alınan oksijeni kana geçirir, kandaki zararlı karbondioksiti ise soluk verme yoluyla dışarı atarak vücudu temizler.",
    "karaciyer": "<b>Anatomi - Karaciğer:</b> Vücudumuzun en büyük iç organıdır ve adeta muazzam bir kimya fabrikasıdır. Yağların sindirimi için safra üretir, vücuda giren zehirli maddeleri (toksinleri) etkisiz hale getirir, glikozu depolar ve kanın pıhtılaşmasını sağlayan proteinleri üretir.",
    "mide": "<b>Anatomi - Mide:</b> Sindirim sisteminin kaslı ve j şeklinde genişlemiş organıdır. İçindeki güçlü mide asidi (Hidroklorik asit) ve enzimler sayesinde besinleri mekanik ve kimyasal olarak parçalayarak 'bulamaç' (kimus) haline getirir ve ince bağırsağa gönderir.",
    "beyin": "<b>Anatomi - Beyin:</b> Merkezi sinir sisteminin kontrol kulesidir. Kafatası içinde yer alır; düşünme, hafıza, öğrenme, duygular, beş duyu organının yönetimi ve vücuttaki tüm hormonal dengelerin, organların birbiriyle uyum içinde çalışmasını sağlayan ana bilgisayardır.",
    "hucre": "<b>Fen Bilgisi - Hücre:</b> Canlıların canlılık özelliği gösteren, büyüme, bölünme ve beslenme yeteneğine sahip en küçük yapı taşıdır. Dıştan içe doğru: Hücre zarı (seçici geçirgen koruyucu), Sitoplazma (organellerin bulunduğu sıvı kısım) ve Çekirdek (yönetim merkezi, DNA) olmak üzere 3 temel kısımdır.",
    "fotosentez": "<b>Fen Bilgisi - Fotosentez:</b> Bitkilerin, alglerin ve bazı bakterilerin kloroplast organelinde bulunan klorofil pigmenti sayesinde; güneş ışığını kullanarak, topraktan aldıkları su ($H_2O$) ve havadan aldıkları karbondioksiti ($CO_2$) birleştirerek kendi besinlerini (glikoz) ve dışarıya hayat veren Oksijeni ($O_2$) üretmesi olayıdır.",
    "mitokondri": "<b>Fen Bilgisi - Mitokondri Organeli:</b> Hücrenin yüksek verimli enerji santralidir. Hücre içerisine gelen besin maddelerini oksijen kullanarak parçalar (oksijenli solunum) ve hücrenin hayati faaliyetlerinde (büyüme, hareket, bölünme) kullanacağı ATP (Adenozin Trifosfat) yani enerji molekülünü sentezler."
}

# ⚡ UPUPUZUN FIZIK VE GEOMETRI VERI TABANI
physics_geometry_database = {
    "yercekimi": "<b>Fizik - Yerçekimi Kuvveti:</b> Kütlesi olan tüm büyük gök cisimlerinin (Dünya, Ay, Güneş) üzerindeki nesnelere uyguladığı çekim kuvvetidir. Dünyadaki yerçekimi ivmesi yaklaşık $g = 9.81 m/s^2$ kabul edilir. Formülü $F = m \cdot g$'dir. Kafasına elma düşen Sir Isaac Newton tarafından sistemleştirilmiştir.",
    "surtunme": "<b>Fizik - Sürtünme Kuvveti:</b> Birbirine temas eden iki yüzey arasında, cismin hareket yönüne her zaman zıt yönde oluşan, hareketi zorlaştıran veya engelleyen kuvvettir. Yüzeyin pürüzlülüğüne bağlıdır. Hareket enerjisini (kinetik) doğrudan ısı enerjisine dönüştürür. Formülü: $F_s = k \cdot N$ şeklindedir.",
    "ohm kanunu": "<b>Fizik - Ohm Kanunu:</b> Bir elektrik devresindeki iletkenin iki ucu arasındaki gerilim (V - Volt), üzerinden geçen elektrik akımı (I - Amper) ve iletkenin gösterdiği direnç (R - Ohm) arasındaki altın ilişkiyi açıklar. Müthiş formülü şudur: $V = I \cdot R$ (yani Vır formülü).",
    "ucgen": "<b>Geometri - Üçgen:</b> Aynı doğru üzerinde olmayan üç noktanın düz çizgilerle birleşmesinden oluşan en temel kapalı geometrik şekildir. Çeşit kenar, ikizkenar ve eşkenar çeşitleri vardır. Bir üçgenin iç açılarının toplamı her zaman **180°**, dış açılarının toplamı ise **360°**'dir. Alanı: $\\frac{\\text{Taban} \\cdot \\text{Yükseklik}}{2}$ formülüyle hesaplanır.",
    "kare": "<b>Geometri - Kare:</b> Dört kenar uzunluğu da birbirine tamamen eşit olan ve tüm iç açıları tam **90°** (dik açı) olan düzgün bir dörtgendir. Köşegenleri birbirini dik keser ve ortalar. Bir kenarına 'a' dersek; Çevresi: $4a$, Alanı ise bir kenarının kendisiyle çarpımı olan $A = a^2$ formülüyle bulunur.",
    "dikdortgen": "<b>Geometri - Dikdörtgen:</b> Karşılıklı kenarları birbirine eşit ve paralel olan, dört iç açısının her biri **90°** olan bir dörtgendir. Komşu kenarları birbirine diktir. Uzun kenarına 'a', kısa kenarına 'b' dersek; Çevresi: $2(a+b)$, Alanı ise uzun ve kısa kenarın çarpımı olan $A = a \cdot b$ formülüyle hesaplanır.",
    "daire": "<b>Geometri - Daire ve Çember:</b> Düzlemde sabit bir noktaya (merkez) eşit uzaklıktaki noktalar kümesine çember, iç bölgesinin de dahil olduğu şekle daire denir. Merkezden kenara olan mesafeye yarıçap (r) denir. Çemberin Çevresi: $2 \\cdot \\pi \\cdot r$, Dairenin Alanı ise ünlü $\\text{Alan} = \\pi \\cdot r^2$ formülüyle tıkır tıkır hesaplanır."
}

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
                "bilgi": f"{flag} {name_tr}, {region} kıtasında yer alan, yaklaşık {population:,} nüfuslu harika bir ülkedir."
            }
    except:
        pass
    return None

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
    if request.method == 'OPTIONS': return jsonify({"success": True}), 200, response_headers

    data = request.json or {}
    password = data.get('password', '')
    action = data.get('action', 'get')
    
    if password != "F89B2A.ey": 
        return jsonify({"success": False, "message": "Hatalı şifre!"}), 403, response_headers

    if action == 'clear':
        if os.path.exists("sorular.txt"): os.remove("sorular.txt")
        return jsonify({"success": True, "logs": []}), 200, response_headers

    if os.path.exists("sorular.txt"):
        with open("sorular.txt", "r", encoding="utf-8") as file: logs = file.readlines()
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

    # Noktalama temizliği
    user_message = re.sub(r'[.,\?!;\(\)"\'’\-]', '', user_message)
    norm_msg = user_message.replace("ı", "i").replace("ğ", "g").replace("ü", "u").replace("ş", "s").replace("ö", "o").replace("ç", "c")

    # GELİŞTİRİLMİŞ YANLIŞ YAZIM TOLERANS MOTORU (nber, nbr, mrb vb.)
    typo_rules = {
        "nber": "naber", "nbr": "naber", "slm": "selam", "mrb": "merhaba", 
        "mrhb": "merhaba", "knk": "kanka", "kgo": "coğrafya", "mat": "matematik",
        "fzk": "fizik", "gmt": "geometri", "antm": "anatomi", "akciger": "akciyer"
    }
    words = norm_msg.split()
    fixed_words = [typo_rules.get(w, w) for w in words]
    norm_msg = " ".join(fixed_words)

    is_buddy_mode = "kanka" in norm_msg or "naber" in norm_msg

    # Yapımcı Kontrolü
    if any(x in norm_msg for x in ["kim yapti", "yapimcin", "kim gelistirdi", "kurucun", "sahibin", "sen kimsin", "adini kim verdi"]):
        save_log("CEVAPLANDI")
        return jsonify({"reply": '<span class="expert-badge badge-sozel">Sistem Çekirdeği</span><br>Beni tam bir dahi olmam için <b>TÜW</b> geliştirdi kanka! Adım <b>ARIES AI</b>. Mekaniğin sahibi odur. 🚀'})

    # Matematik Motoru
    math_message = user_message.replace(",", ".")
    math_chars = set("0123456789+-*/(). ")
    if any(char in math_message for char in ['+', '-', '*', '/']) and set(math_message).issubset(math_chars):
        try:
            result = eval(math_message)
            save_log("CEVAPLANDI")
            return jsonify({"reply": f'<span class="expert-badge badge-sayisal">Matematiksel Analiz</span><br><div class="formula-box">{user_message} = {result}</div>'})
        except:
            save_log("HATA")
            return jsonify({"reply": "İşlem hesaplanamadı kanka, formülü kontrol et."})

    # Anatomi ve Fen Bilgisi Kontrolü
    for key, response in science_database.items():
        if key in norm_msg:
            save_log("CEVAPLANDI")
            return jsonify({"reply": f'<span class="expert-badge badge-sayisal" style="background-color:#00e676; color:black;">Fen Bilimleri & Anatomi</span><br>{response}'})

    # Fizik ve Geometri Kontrolü
    for key, response in physics_geometry_database.items():
        if key in norm_msg:
            save_log("CEVAPLANDI")
            return jsonify({"reply": f'<span class="expert-badge badge-sayisal" style="background-color:#ff9100; color:black;">Fizik & Geometri</span><br>{response}'})

    # Dini Terimler Kontrolü
    for key, response in religious_database.items():
        if key in norm_msg:
            save_log("CEVAPLANDI")
            return jsonify({"reply": f'<span class="expert-badge badge-sozel" style="background-color:#9c27b0;">İslami Tarih & İlim</span><br>{response}'})

    # Tarih Kontrolü
    for key, response in historical_events.items():
        if key.replace("ı", "i").replace("ğ", "g") in norm_msg:
            save_log("CEVAPLANDI")
            return jsonify({"reply": f'<span class="expert-badge badge-sozel">Tarih Bilgisi</span><br>{response}'})

    # Coğrafya Kontrolü (Yerel Devasa Liste)
    matched_countries = []
    for country, data in world_countries.items():
        if country in norm_msg:
            matched_countries.append({"name": country.upper(), "b": data["b"], "k": data["k"], "lat": data["lat"], "lon": data["lon"], "bilgi": data["bilgi"]})

    # Eğer yerel listede yoksa canlı API'ye başvur (Dünyadaki tüm ülkeler için koruma kalkanı)
    if len(matched_countries) == 0:
        for word in words:
            if len(word) > 3:
                api_data = fetch_country_from_api(word)
                if api_data:
                    matched_countries.append(api_data)
                    break

    if len(matched_countries) >= 2:
        distance = calculate_haversine(matched_countries[0]["lat"], matched_countries[0]["lon"], matched_countries[1]["lat"], matched_countries[1]["lon"])
        save_log("CEVAPLANDI")
        return jsonify({"reply": f'<span class="expert-badge badge-cografya">Rota Analizi</span><br>📐 <b>Mesafe:</b> {matched_countries[0]["name"]} ile {matched_countries[1]["name"]} arası yaklaşık ~{distance} Kilometre kanka!'})
    elif len(matched_countries) == 1:
        save_log("CEVAPLANDI")
        return jsonify({"reply": f'<span class="expert-badge badge-cografya">Coğrafya Analizi</span><br><b>Ülke:</b> {matched_countries[0]["name"]}<br><b>Kıta:</b> {matched_countries[0]["k"]}<br><b>Başkent:</b> {matched_countries[0]["b"]}<br><br>ℹ️ {matched_countries[0]["bilgi"]}'})

    if any(x in norm_msg for x in ["selam", "merhaba"]):
        save_log("CEVAPLANDI")
        return jsonify({"reply": "Selam kanka! ARIES AI emrinde. Ne soruyoruz, fen mi tarih mi?"})

    save_log("CEVAPLANAMADI")
    return jsonify({"reply": "ARIES bu soruyu analiz etti ama veri tabanında tam bir eşleşme bulamadı kanka. Matematik, fen, fizik, geometri, anatomi, tarih, dini ilimler veya coğrafya sormayı dene!"})

if __name__ == '__main__':
    app.run(debug=True)
