import os # Kodun en üstüne ekle

# ... (diğer kodların aynen kalıyor) ...

if __name__ == '__main__':
    # Render'ın portunu dinamik olarak alır, bulamazsa yerelde 5000 portunda çalışır.
    port = int(os.environ.get("PORT", 5000))
    # Render üzerinde debug=True güvenlik riski yaratacağı için canlıda kapatılması önerilir.
    app.run(host='0.0.0.0', port=port)
