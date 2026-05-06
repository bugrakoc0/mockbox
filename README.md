<div align="center">

# 📦 MockBox

**Instant REST API from JSON — No config, no database setup, no hassle.**

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.128-green?logo=fastapi)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

[English](#english) · [Türkçe](#türkçe)

</div>

---

## English

### What is MockBox?

MockBox turns any JSON data into a fully working REST API in seconds.  
No configuration files, no database setup — just upload your JSON and start making requests.

Perfect for:
- Frontend developers who need a backend before it's ready
- Rapid prototyping and demos
- API integration testing

---

### 🚀 Quick Start

**1. Install dependencies**
```bash
pip install fastapi uvicorn
```

**2. Run the server**
```bash
python mockbox.py
```

**3. Load your JSON**
```bash
curl -X POST http://localhost:8000/mockbox/load \
  -H "Content-Type: application/json" \
  -d '{
    "users": [
      {"name": "Alice", "email": "alice@example.com", "city": "New York", "age": 28},
      {"name": "Bob",   "email": "bob@example.com",   "city": "London",   "age": 34}
    ],
    "products": [
      {"name": "Laptop", "price": 1499, "stock": 10},
      {"name": "Mouse",  "price": 29,   "stock": 50}
    ]
  }'
```

**Done.** Your API is live. 🎉

---

### 📡 Endpoints

Once data is loaded, these endpoints are automatically available for every resource:

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/{resource}` | Get all records |
| `GET` | `/{resource}/{id}` | Get a single record |
| `GET` | `/{resource}/search` | Filter by fields |
| `POST` | `/{resource}` | Create a new record |
| `PUT` | `/{resource}/{id}` | Update a record |
| `DELETE` | `/{resource}/{id}` | Delete a record |

---

### 🔍 Filtering & Search

**General search** — searches across all fields:
```bash
GET /users?search=london
```

**Field filter** — filter by specific fields (AND logic):
```bash
GET /users/search?city=London
GET /users/search?city=London&age=34
```

**Pagination** — works on all endpoints:
```bash
GET /users?page=1&limit=5
GET /users/search?city=London&page=1&limit=10
```

**Example response:**
```json
{
  "data": [
    { "id": 2, "name": "Bob", "email": "bob@example.com", "city": "London", "age": 34 }
  ],
  "pagination": {
    "page": 1,
    "limit": 10,
    "total": 1,
    "total_pages": 1,
    "has_next": false,
    "has_prev": false
  },
  "filters": { "city": "London" }
}
```

---

### 📄 Interactive Docs

MockBox comes with automatic Swagger UI documentation:

```
http://localhost:8000/docs
```

---

### 🛠 Tech Stack

- **[FastAPI](https://fastapi.tiangolo.com)** — Modern async web framework
- **SQLite** — Lightweight local database (built into Python)
- **Uvicorn** — Lightning-fast ASGI server

---

### 📁 Project Structure

```
mockbox/
├── mockbox.py      # Main application
├── mockbox.db      # Auto-generated database (SQLite)
└── README.md
```

---

### 🗺 Roadmap

- [ ] `PATCH` support (partial updates)
- [ ] Sorting (`?sort=age&order=asc`)
- [ ] Multiple JSON file import
- [ ] Docker support
- [ ] Deploy to cloud (Railway / Render)

---

## Türkçe

### MockBox Nedir?

MockBox, herhangi bir JSON verisini saniyeler içinde tam çalışan bir REST API'ye dönüştürür.  
Hiçbir konfigürasyon dosyası yok, veritabanı kurulumu yok — sadece JSON'ını yükle ve isteklerini yapmaya başla.

Şunlar için idealdir:
- Backend hazır olmadan çalışması gereken frontend geliştiriciler
- Hızlı prototipleme ve demolar
- API entegrasyon testleri

---

### 🚀 Hızlı Başlangıç

**1. Bağımlılıkları kur**
```bash
pip install fastapi uvicorn
```

**2. Sunucuyu başlat**
```bash
python mockbox.py
```

**3. JSON'ını yükle**
```bash
curl -X POST http://localhost:8000/mockbox/load \
  -H "Content-Type: application/json" \
  -d '{
    "kullanicilar": [
      {"ad": "Ali",  "email": "ali@ornek.com",  "sehir": "Istanbul", "yas": 25},
      {"ad": "Veli", "email": "veli@ornek.com", "sehir": "Ankara",   "yas": 30}
    ]
  }'
```

**Bitti.** API'n hazır. 🎉

---

### 📡 Endpoint'ler

Veri yüklendikten sonra her kaynak için şu endpoint'ler otomatik olarak oluşur:

| Method | Endpoint | Açıklama |
|--------|----------|----------|
| `GET` | `/{kaynak}` | Tüm kayıtları getir |
| `GET` | `/{kaynak}/{id}` | Tek kayıt getir |
| `GET` | `/{kaynak}/search` | Alanlara göre filtrele |
| `POST` | `/{kaynak}` | Yeni kayıt ekle |
| `PUT` | `/{kaynak}/{id}` | Kayıt güncelle |
| `DELETE` | `/{kaynak}/{id}` | Kayıt sil |

---

### 🔍 Filtreleme ve Arama

**Genel arama** — tüm alanlarda arar:
```bash
GET /kullanicilar?search=ankara
```

**Alan filtresi** — belirli alanlara göre filtrele (AND mantığı):
```bash
GET /kullanicilar/search?sehir=Istanbul
GET /kullanicilar/search?sehir=Istanbul&yas=25
```

**Sayfalama** — tüm endpoint'lerde çalışır:
```bash
GET /kullanicilar?page=1&limit=5
GET /kullanicilar/search?sehir=Istanbul&page=1&limit=10
```

---

### 📄 Interaktif Dokümantasyon

MockBox, otomatik Swagger UI dokümantasyonu ile gelir:

```
http://localhost:8000/docs
```

---

### 🛠 Teknoloji

- **[FastAPI](https://fastapi.tiangolo.com)** — Modern async web framework
- **SQLite** — Python'a gömülü hafif veritabanı
- **Uvicorn** — Yüksek performanslı ASGI sunucu

---

### 🗺 Yol Haritası

- [ ] `PATCH` desteği (kısmi güncelleme)
- [ ] Sıralama (`?sort=yas&order=asc`)
- [ ] Birden fazla JSON dosyası import
- [ ] Docker desteği
- [ ] Cloud deploy (Railway / Render)

---

<div align="center">

Made with by [Buğra](https://github.com/bugrakoc0)

</div>

