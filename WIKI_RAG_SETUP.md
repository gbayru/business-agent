# Wiki RAG Entegrasyonu Kılavuzu

Bu kılavuz, wiki sayfalarından doküman çekip RAG sistemine ekleme işlemini açıklar.

> 💡 **Önemli:** Wiki'ye ne koymanız gerektiğini öğrenmek için [WIKI_CONTENT_GUIDE.md](./WIKI_CONTENT_GUIDE.md) dosyasına bakın!

## Kurulum

1. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

## Wiki Türleri

Sistem üç farklı wiki türünü destekler:

### 1. Confluence (Atlassian)

En yaygın kurumsal wiki çözümü.

**Gereksinimler:**
- Confluence base URL
- Kullanıcı adı (email)
- API Token veya şifre

**Kullanım:**

```python
from src.core.service import add_wiki_documents

result = add_wiki_documents(
    session_id="your-session-id",
    wiki_type="confluence",
    base_url="https://your-company.atlassian.net/wiki",
    username="your-email@company.com",
    api_token="your-api-token",  # veya password="your-password"
    space_key="ENG",  # İsteğe bağlı: belirli bir space'den sayfalar
    limit=100  # Maksimum sayfa sayısı
)
```

**API Token Oluşturma:**
1. Atlassian hesabınıza giriş yapın
2. https://id.atlassian.com/manage-profile/security/api-tokens
3. "Create API token" butonuna tıklayın
4. Token'ı kopyalayın

### 2. MediaWiki

Wikipedia ve birçok özel wiki MediaWiki kullanır.

**Kullanım:**

```python
result = add_wiki_documents(
    session_id="your-session-id",
    wiki_type="mediawiki",
    base_url="https://wiki.example.com/w/api.php",
    limit=100
)
```

**Opsiyonel Parametreler:**
- `namespace`: Namespace ID (0 = ana sayfalar, 2 = kullanıcı sayfaları)
- `category`: Belirli bir kategoriden sayfalar

### 3. Generic REST API

Özel wiki veya REST API kullanan sistemler için.

**Kullanım:**

```python
result = add_wiki_documents(
    session_id="your-session-id",
    wiki_type="generic",
    base_url="https://wiki.example.com/api",
    headers={"Authorization": "Bearer your-token"},
    page_endpoint="/pages",  # İsteğe bağlı
    text_field="content"  # İsteğe bağlı
)
```

## Adım Adım Kullanım

### 1. Session Oluşturma

```python
from src.core.service import create_session

session = create_session()
session_id = session["session_id"]
```

### 2. Wiki Dokümanlarını Ekleme

```python
from src.core.service import add_wiki_documents

# Confluence örneği
result = add_wiki_documents(
    session_id=session_id,
    wiki_type="confluence",
    base_url="https://company.atlassian.net/wiki",
    username="user@company.com",
    api_token="your-token",
    space_key="ENG",  # Sadece ENG space'indeki sayfalar
    limit=50
)

print(f"Index ID: {result['index_id']}")
```

### 3. Belirli Sayfaları Ekleme

Eğer sadece belirli sayfaları eklemek istiyorsanız:

```python
result = add_wiki_documents(
    session_id=session_id,
    wiki_type="confluence",
    base_url="https://company.atlassian.net/wiki",
    username="user@company.com",
    api_token="your-token",
    page_ids=["12345", "67890", "11111"]  # Belirli sayfa ID'leri
)
```

### 4. Normal Kullanım

Wiki dokümanları eklendikten sonra, sistem otomatik olarak RAG'ı kullanır:

```python
from src.core.service import message

response = message(
    session_id=session_id,
    current_field="Background",
    user_text="Mevcut sistemde performans sorunları var"
)
```

RAG sistemi, kullanıcının cevabını normalize ederken wiki'den ilgili bilgileri çeker.

## Environment Variables

Wiki bağlantı bilgilerini environment variable olarak da ayarlayabilirsiniz:

```bash
# .env dosyası
CONFLUENCE_USERNAME=user@company.com
CONFLUENCE_API_TOKEN=your-token
```

Sonra kodda sadece base_url belirtmeniz yeterli:

```python
result = add_wiki_documents(
    session_id=session_id,
    wiki_type="confluence",
    base_url="https://company.atlassian.net/wiki",
    space_key="ENG"
)
```

## Sorun Giderme

### 1. Authentication Hatası

- API token'ın doğru olduğundan emin olun
- Kullanıcı adının email formatında olduğundan emin olun
- Confluence'de API erişiminin açık olduğundan emin olun

### 2. Sayfa Bulunamadı

- `space_key` parametresinin doğru olduğundan emin olun
- `page_ids` kullanıyorsanız, ID'lerin doğru olduğundan emin olun
- Wiki URL'inin doğru olduğundan emin olun

### 3. Embedding Model Yüklenemiyor

İlk kullanımda `sentence-transformers` modeli indirilir. İnternet bağlantınızı kontrol edin.

### 4. RAG Sonuçları Boş

- Vector store'un düzgün oluşturulduğundan emin olun
- `data/indexes` klasörüne yazma izniniz olduğundan emin olun
- Wiki sayfalarının içeriğinin yeterli olduğundan emin olun (çok kısa sayfalar atlanır)

## Gelişmiş Kullanım

### CQL Query ile Filtreleme (Confluence)

```python
# wiki_ingest.py'yi doğrudan kullanarak
from src.rag.wiki_ingest import ingest_wiki_pages
from src.rag.wiki_client import ConfluenceClient
from src.rag.index import VectorStore

client = ConfluenceClient(
    base_url="https://company.atlassian.net/wiki",
    username="user@company.com",
    api_token="token"
)

# CQL query ile özel filtreleme
pages = client.fetch_pages(
    cql="type=page AND space=ENG AND label=brd-template",
    limit=100
)

vector_store = VectorStore()
index_id = ingest_wiki_pages(
    wiki_client=client,
    vector_store=vector_store,
    page_ids=[p["id"] for p in pages]
)
```

### Mevcut Index'e Ekleme

Aynı session için yeni sayfalar eklemek:

```python
# Session state'den mevcut index_id'yi al
from src.core.state import load_session

state = load_session(session_id)
existing_index_id = state.rag_index_id

# Yeni sayfalar ekle (aynı index'e)
result = add_wiki_documents(
    session_id=session_id,
    wiki_type="confluence",
    base_url="...",
    username="...",
    api_token="...",
    # index_id otomatik olarak mevcut index'i kullanır
)
```

## Notlar

- Wiki sayfaları otomatik olarak chunk'lara bölünür (maksimum 3500 karakter)
- Her chunk metadata ile saklanır (sayfa başlığı, URL, vb.)
- RAG sorguları field-specific query'ler kullanır (field_queries.py'de tanımlı)
- Sistem demo-safe: RAG başarısız olursa normal çalışmaya devam eder
