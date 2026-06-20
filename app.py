# 🔐 AKILLI VE GÜVENLİ LOG API ROTASI (KESİN SİLME DESTEKLİ)
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
    
    if password != "F89B2A.ey": 
        return jsonify({"success": False, "message": "Hatalı şifre girdin kanka!"}), 403, response_headers

    # 🗑️ PANELDEKİ SİLME TUŞUNA BASILDIYSA DOSYAYI TAMAMEN SİL VE BOŞ DÖN
    if action == 'clear':
        try:
            if os.path.exists("sorular.txt"):
                os.remove("sorular.txt") # Dosyayı kökten siliyoruz kanka
            return jsonify({"success": True, "logs": [], "cleared": True}), 200, response_headers
        except Exception as e:
            return jsonify({"success": False, "message": str(e)}), 500, response_headers

    # 🔄 NORMAL ŞARTLARDA VERİLERİ ÇEK VE GÖNDER
    if os.path.exists("sorular.txt"):
        try:
            with open("sorular.txt", "r", encoding="utf-8") as file:
                logs = file.readlines()
            
            clean_logs = [line.strip() for line in logs if line.strip()]
            
            if not clean_logs:
                return jsonify({"success": True, "logs": ["Henüz hiç soru sorulmadı kanka."]}), 200, response_headers
                
            return jsonify({"success": True, "logs": list(reversed(clean_logs))}), 200, response_headers
        except:
            return jsonify({"success": True, "logs": ["Henüz hiç soru sorulmadı kanka."]}), 200, response_headers
    else:
        return jsonify({"success": True, "logs": ["Henüz hiç soru sorulmadı kanka."]}), 200, response_headers
