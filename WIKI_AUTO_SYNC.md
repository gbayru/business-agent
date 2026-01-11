# Wiki Otomatik Senkronizasyon

## Mevcut Durum ❌

**Şu anda otomatik değil!** Wiki'de yaptığın değişiklikler otomatik olarak RAG'a yansımaz.

### Nasıl Çalışıyor Şu Anda?

```python
# Manuel olarak çağırman gerekiyor
from src.core.service import add_wiki_documents

result = add_wiki_documents(
    session_id=session_id,
    wiki_type="confluence",
    base_url="...",
    username="...",
    api_token="...",
    space_key="ENG"
)
```

**Sorun:** Her wiki güncellemesinde bu fonksiyonu tekrar çağırman gerekiyor.

---

## Otomatik Senkronizasyon Seçenekleri

### 1. Webhook (En İyi Çözüm) ✅

Confluence'de sayfa güncellendiğinde webhook tetiklenir, RAG otomatik güncellenir.

#### Nasıl Çalışır?

```
Wiki'de Sayfa Güncellendi
    ↓
Confluence Webhook Tetiklenir
    ↓
Webhook → API Endpoint'e POST Request
    ↓
RAG Sistemi Otomatik Güncellenir
```

#### Implementation:

**1. Webhook Endpoint Oluştur:**

```python
# backend/app.py veya service.py'ye ekle

from fastapi import FastAPI, Request
from src.core.service import add_wiki_documents
import json

app = FastAPI()

@app.post("/webhook/confluence-updated")
async def confluence_webhook(request: Request):
    """
    Confluence webhook handler.
    Wiki sayfası güncellendiğinde çağrılır.
    """
    payload = await request.json()
    
    # Confluence webhook payload'ı
    event_type = payload.get("event")
    page_id = payload.get("page", {}).get("id")
    space_key = payload.get("space", {}).get("key")
    
    if event_type == "page_updated" or event_type == "page_created":
        # Tüm session'ları bul (veya belirli bir index'i güncelle)
        # Bu örnekte tüm session'ları güncellemek yerine,
        # belirli bir index'i güncellemek daha mantıklı
        
        # Index'i güncelle
        update_rag_index_from_wiki(
            page_id=page_id,
            space_key=space_key
        )
        
        return {"status": "success", "message": "RAG updated"}
    
    return {"status": "ignored"}


def update_rag_index_from_wiki(page_id: str, space_key: str):
    """
    Belirli bir wiki sayfasından RAG index'i güncelle.
    """
    from src.rag.wiki_client import ConfluenceClient
    from src.rag.index import VectorStore
    from src.rag.wiki_ingest import ingest_wiki_pages
    import os
    
    # Wiki client
    client = ConfluenceClient(
        base_url=os.getenv("CONFLUENCE_BASE_URL"),
        username=os.getenv("CONFLUENCE_USERNAME"),
        api_token=os.getenv("CONFLUENCE_API_TOKEN")
    )
    
    # Vector store
    vector_store = VectorStore()
    
    # Mevcut index'i bul (space_key'den)
    index_id = get_index_id_for_space(space_key)
    
    # Sadece güncellenen sayfayı ekle/güncelle
    ingest_wiki_pages(
        wiki_client=client,
        vector_store=vector_store,
        page_ids=[page_id],  # Sadece bu sayfa
        index_id=index_id,   # Mevcut index'e ekle
        max_chunk_chars=3500
    )
```

**2. Confluence'de Webhook Ayarla:**

Confluence Admin Panel'de:
1. Settings → Webhooks
2. "Create webhook" butonuna tıkla
3. URL: `https://your-api.com/webhook/confluence-updated`
4. Events: "Page created", "Page updated"
5. Save

**3. Webhook Güvenliği:**

```python
import hmac
import hashlib

@app.post("/webhook/confluence-updated")
async def confluence_webhook(request: Request):
    # Webhook secret ile doğrula
    webhook_secret = os.getenv("CONFLUENCE_WEBHOOK_SECRET")
    signature = request.headers.get("X-Confluence-Signature")
    
    body = await request.body()
    expected_signature = hmac.new(
        webhook_secret.encode(),
        body,
        hashlib.sha256
    ).hexdigest()
    
    if signature != expected_signature:
        return {"status": "unauthorized"}, 401
    
    # ... webhook işlemi
```

---

### 2. Scheduled Job (Polling) ⏰

Belirli aralıklarla wiki'yi kontrol et, değişiklik varsa güncelle.

#### Nasıl Çalışır?

```
Her 1 saatte bir (veya belirlediğin sürede)
    ↓
Wiki'deki sayfaları kontrol et
    ↓
Değişiklik var mı? (last_modified kontrolü)
    ↓
Varsa → RAG'ı güncelle
```

#### Implementation:

```python
# scheduled_sync.py

import schedule
import time
from datetime import datetime
from src.rag.wiki_client import ConfluenceClient
from src.rag.index import VectorStore
from src.rag.wiki_ingest import ingest_wiki_pages
import os
import json

def sync_wiki_to_rag():
    """
    Wiki'yi kontrol et ve değişiklik varsa RAG'ı güncelle.
    """
    # Son sync zamanını oku
    last_sync_file = "data/last_sync.json"
    
    try:
        with open(last_sync_file, "r") as f:
            last_sync = json.load(f)
    except:
        last_sync = {}
    
    # Wiki client
    client = ConfluenceClient(
        base_url=os.getenv("CONFLUENCE_BASE_URL"),
        username=os.getenv("CONFLUENCE_USERNAME"),
        api_token=os.getenv("CONFLUENCE_API_TOKEN")
    )
    
    # Space'deki sayfaları kontrol et
    space_key = os.getenv("CONFLUENCE_SPACE_KEY", "ENG")
    pages = client.fetch_pages(space_key=space_key, limit=100)
    
    updated_pages = []
    for page in pages:
        page_id = page.get("id")
        last_modified = page.get("version", {}).get("when", "")
        
        # Son sync'ten sonra güncellenmiş mi?
        if page_id not in last_sync or last_sync[page_id] < last_modified:
            updated_pages.append(page_id)
            last_sync[page_id] = last_modified
    
    # Güncellenen sayfalar varsa RAG'ı güncelle
    if updated_pages:
        print(f"Found {len(updated_pages)} updated pages, updating RAG...")
        
        vector_store = VectorStore()
        index_id = get_index_id_for_space(space_key)
        
        ingest_wiki_pages(
            wiki_client=client,
            vector_store=vector_store,
            page_ids=updated_pages,
            index_id=index_id
        )
        
        # Son sync zamanını kaydet
        last_sync["last_sync_time"] = datetime.now().isoformat()
        with open(last_sync_file, "w") as f:
            json.dump(last_sync, f, indent=2)
        
        print(f"✓ RAG updated with {len(updated_pages)} pages")
    else:
        print("No updates found")


# Her 1 saatte bir çalıştır
schedule.every(1).hours.do(sync_wiki_to_rag)

# Veya her 30 dakikada bir
# schedule.every(30).minutes.do(sync_wiki_to_rag)

# Veya her gün saat 02:00'de
# schedule.every().day.at("02:00").do(sync_wiki_to_rag)

if __name__ == "__main__":
    print("Starting scheduled wiki sync...")
    while True:
        schedule.run_pending()
        time.sleep(60)  # Her 1 dakikada bir kontrol et
```

**Çalıştırma:**

```bash
# Background'da çalıştır
python scheduled_sync.py &

# Veya systemd service olarak
# /etc/systemd/system/wiki-sync.service
```

---

### 3. Manual Trigger (Mevcut) 🔧

Her değişiklikte manuel olarak çağır.

**Avantajlar:**
- Basit
- Kontrol sende
- Hemen güncellenir

**Dezavantajlar:**
- Unutulabilir
- Manuel işlem

---

### 4. Hybrid: Webhook + Scheduled Backup 🔄

En güvenilir çözüm: Webhook + yedek polling.

```python
# Hem webhook hem scheduled job

# 1. Webhook (anlık güncelleme)
@app.post("/webhook/confluence-updated")
async def webhook_handler(...):
    # Anlık güncelleme
    update_rag_from_wiki(...)

# 2. Scheduled job (yedek, günde bir)
schedule.every().day.at("03:00").do(full_sync_wiki)
```

---

## Karşılaştırma

| Yöntem | Hız | Güvenilirlik | Karmaşıklık | Önerilen |
|--------|-----|--------------|-------------|-----------|
| **Webhook** | ⚡ Anlık | ⭐⭐⭐ Yüksek | ⚙️ Orta | ✅ **Evet** |
| **Scheduled Job** | 🐌 Gecikmeli | ⭐⭐ Orta | ⚙️ Düşük | ⚠️ Yedek olarak |
| **Manual** | ⚡ Anlık | ⭐ Düşük | ✅ Çok Basit | ❌ Geliştirme için |

---

## Önerilen Çözüm: Webhook

### Neden Webhook?

1. ✅ **Anlık güncelleme** - Wiki'de değişiklik olur olmaz RAG güncellenir
2. ✅ **Güvenilir** - Confluence tarafından tetiklenir
3. ✅ **Efficient** - Sadece değişen sayfalar güncellenir
4. ✅ **Scalable** - Çok sayıda sayfa için de çalışır

### Kurulum Adımları:

1. **Webhook endpoint oluştur** (yukarıdaki kod)
2. **Confluence'de webhook ayarla:**
   - Admin → Webhooks → Create
   - URL: `https://your-api.com/webhook/confluence-updated`
   - Events: Page created, Page updated
3. **Test et:**
   - Wiki'de bir sayfa güncelle
   - Webhook'un tetiklendiğini kontrol et
   - RAG'ın güncellendiğini doğrula

---

## Sonuç

**Mevcut durum:** ❌ Otomatik değil, manuel çağırman gerekiyor

**Önerilen çözüm:** ✅ **Webhook** ile otomatik senkronizasyon

**Alternatif:** ⏰ Scheduled job (webhook yoksa)

Webhook kurulumu için yukarıdaki kodu kullanabilirsin. İstersen tam implementation'ı hazırlayabilirim! 🚀
