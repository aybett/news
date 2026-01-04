# Haber Sitesi

**Açıklama**

Basit, öğretici amaçlı bir Flask tabanlı haber uygulaması. Kullanıcılar kayıt olabilir, giriş yapabilir, haberleri listeleyebilir ve içeriklerle etkileşime geçebilir. Statik yüklemeler (ör. logo ve görseller) proje içinde `static/uploads/` altında tutulur.

---

## ⚙️ Özellikler

- Kullanıcı kayıt/giriş (Flask-Login)
- Haber listeleme, detay görünümü ve kategori desteği
- Basit admin paneli (editör rolleri)
- Yüklenen medya dosyalarını `static/uploads/` altında saklama
- Basit DB yardımı ve geliştirme araçları (helper scriptler)

---

## 🧩 Gereksinimler

- Python 3.11+ önerilir
- Gerekli paketler `requirements.txt` içinde listelenmiştir

---

## 🚀 Hızlı Başlangıç

1. Sanal ortam oluşturun ve aktifleştirin:

Windows (PowerShell):

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

Linux / macOS:

```bash
python -m venv venv
source venv/bin/activate
```

2. Bağımlılıkları yükleyin:

```bash
pip install -r requirements.txt
```

3. Uygulamayı çalıştırın (geliştirme modu):

```bash
python app.py
# ya da
flask run
```

Tarayıcıda http://127.0.0.1:5000 adresine gidin.

Not: İlk çalıştırmada veritabanı (`database.db`) otomatik oluşturulur.

# Kullanıcı Bilgileri 
Kullanım ve deneme için birkaç kullanıcı oluşturulmuştur.
1. Editör mail: editor@example.com şifre: editorpass
2. Üye mail: uye1@example.com şifre: uye1pass
3. Üye mail: uye2@exampleçcom şifre: uye2pass

---

## 📁 Önemli Dosya/Dizin Yapısı

- `app.py` — Uygulamanın başlatma ve konfigürasyon kodu
- `auth.py` — Kimlik doğrulama rotaları
- `news.py` — Haberlerle ilgili rotalar
- `admin.py` — Admin / editör özellikleri
- `models.py` — SQLAlchemy modelleri
- `static/uploads/` — Kullanıcı tarafından yüklenen medya dosyaları (logo, görseller)
- `templates/` — Jinja2 şablon dosyaları

---

## ✨ Katkıda Bulunma

- Değişiklik yapmak isterseniz bir dal (branch) oluşturup pull request (veya patch) gönderin.
- Küçük değişiklikler için doğrudan issue açabilirsiniz.

---

## 📄 Lisans

Bu depo için varsayılan ve hafif bir lisans önerisi: **MIT**. 


