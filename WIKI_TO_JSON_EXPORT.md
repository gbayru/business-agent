# Wiki'den JSON'a Export İşlemi

## Ne Demek?

**Wiki'den JSON'a export:** Confluence veya MediaWiki gibi wiki sistemlerindeki sayfaları alıp, yapılandırılmış JSON formatına dönüştürmek.

---

## Örnek: Wiki Sayfası → JSON

### 1. Wiki Sayfası (Confluence'de şöyle görünür):

```markdown
# Müşteri Segmentleri

## Prepaid Segmenti
- Tanım: Ön ödemeli hat kullanan müşteriler
- Özellikler:
  - Yaş grubu: 18-35
  - Gelir seviyesi: Düşük-Orta
  - Mobil uygulama kullanımı: Yüksek (%85)
- İstatistikler:
  - Toplam müşteri: 15M
  - Günlük aktif: 8M
  - Aylık transaction: 120M

## Postpaid Segmenti
- Tanım: Faturalı hat kullanan müşteriler
- Özellikler:
  - Yaş grubu: 25-55
  - Gelir seviyesi: Orta-Üst
  - Web kullanımı: Yüksek (%40)
- İstatistikler:
  - Toplam müşteri: 20M
  - Günlük aktif: 12M
  - Aylık transaction: 200M
```

### 2. JSON'a Dönüştürülmüş Hali:

```json
{
  "field": "Target Customer Group",
  "segments": [
    {
      "name": "Prepaid",
      "definition": "Ön ödemeli hat kullanan müşteriler",
      "characteristics": {
        "age_group": "18-35",
        "income_level": "Düşük-Orta",
        "mobile_usage": "Yüksek (%85)"
      },
      "statistics": {
        "total_customers": "15M",
        "daily_active": "8M",
        "monthly_transactions": "120M"
      }
    },
    {
      "name": "Postpaid",
      "definition": "Faturalı hat kullanan müşteriler",
      "characteristics": {
        "age_group": "25-55",
        "income_level": "Orta-Üst",
        "web_usage": "Yüksek (%40)"
      },
      "statistics": {
        "total_customers": "20M",
        "daily_active": "12M",
        "monthly_transactions": "200M"
      }
    }
  ]
}
```

---

## Nasıl Yapılır?

### Yöntem 1: Manuel Export

1. **Wiki sayfasını aç**
2. **İçeriği kopyala**
3. **Bir parser script ile JSON'a çevir:**
   ```python
   # Wiki content'i parse edip JSON'a çevir
   wiki_content = """
   ## Prepaid Segmenti
   - Tanım: Ön ödemeli hat kullanan müşteriler
   ...
   """
   
   # Parse ve JSON'a çevir
   json_data = parse_wiki_to_json(wiki_content)
   ```

### Yöntem 2: Otomatik Export (API ile)

Confluence veya MediaWiki API'sini kullanarak otomatik export:

```python
from src.rag.wiki_client import ConfluenceClient
import json

# Wiki'ye bağlan
client = ConfluenceClient(
    base_url="https://company.atlassian.net/wiki",
    username="user@company.com",
    api_token="token"
)

# Sayfayı çek
page = client.fetch_page("12345")  # Page ID

# HTML'i parse et
html_content = page["body"]["storage"]["value"]

# Structured data'ya çevir (regex, BeautifulSoup, vb. ile)
structured_data = parse_html_to_structured_data(html_content)

# JSON'a kaydet
with open("wiki_export.json", "w", encoding="utf-8") as f:
    json.dump(structured_data, f, indent=2, ensure_ascii=False)
```

---

## Pratik: Wiki Export Fonksiyonu

### Örnek Implementation:

```python
def export_wiki_to_json(
    wiki_client: WikiClient,
    page_id: str,
    output_path: str
) -> dict:
    """
    Wiki sayfasını alıp JSON'a export et.
    
    Args:
        wiki_client: Wiki client instance
        page_id: Wiki sayfa ID'si
        output_path: JSON dosya yolu
    
    Returns:
        Exported JSON data
    """
    # 1. Wiki sayfasını çek
    page = wiki_client.fetch_page(page_id)
    text = wiki_client.extract_text(page)
    
    # 2. Text'i parse et (regex, BeautifulSoup, vb.)
    structured_data = parse_wiki_text_to_json(text)
    
    # 3. JSON'a kaydet
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(structured_data, f, indent=2, ensure_ascii=False)
    
    return structured_data


def parse_wiki_text_to_json(text: str) -> dict:
    """
    Wiki text'ini parse edip structured JSON'a çevir.
    
    Örnek: Markdown formatındaki wiki content'i parse eder.
    """
    lines = text.split("\n")
    json_data = {
        "field": None,
        "segments": [],
        "examples": [],
        # ... diğer alanlar
    }
    
    current_section = None
    current_item = {}
    
    for line in lines:
        line = line.strip()
        
        # Başlık tespit et
        if line.startswith("##"):
            # Yeni bölüm
            section_name = line.replace("##", "").strip()
            current_section = section_name
            
            if "Segmenti" in section_name:
                # Segment başlıyor
                current_item = {"name": section_name.replace(" Segmenti", "")}
        
        # Liste item'ları
        elif line.startswith("-"):
            key, value = parse_list_item(line)
            if current_item:
                current_item[key] = value
        
        # Alt başlıklar
        elif line.startswith("###"):
            # Alt bölüm başlığı
            pass
    
    return json_data


def parse_list_item(line: str) -> tuple:
    """Liste item'ını parse et: '- Anahtar: Değer' -> (key, value)"""
    line = line.replace("-", "").strip()
    if ":" in line:
        key, value = line.split(":", 1)
        return key.strip(), value.strip()
    return None, line
```

---

## Neden JSON'a Export?

### 1. **Structured Data Korunur**
- Wiki'deki tablolar → JSON object'ler
- Listeler → JSON arrays
- Formatting kaybolmaz

### 2. **Programatik Erişim**
```python
# JSON'dan direkt erişim
import json

with open("wiki_export.json", "r") as f:
    kb = json.load(f)

# Prepaid segment bilgilerini al
prepaid = [s for s in kb["segments"] if s["name"] == "Prepaid"][0]
print(prepaid["statistics"]["total_customers"])  # "15M"
```

### 3. **Güncelleme Kolay**
```python
# JSON'u güncelle
kb["segments"][0]["statistics"]["total_customers"] = "16M"

# Kaydet
with open("wiki_export.json", "w") as f:
    json.dump(kb, f, indent=2)
```

### 4. **Version Control (Git)**
```bash
# JSON dosyasını Git'te track et
git add wiki_export.json
git commit -m "Update knowledge base"
```

### 5. **Schema Validation**
```python
# JSON schema ile validate et
import jsonschema

schema = {
    "type": "object",
    "properties": {
        "segments": {
            "type": "array",
            "items": {
                "properties": {
                    "name": {"type": "string"},
                    "statistics": {"type": "object"}
                }
            }
        }
    }
}

jsonschema.validate(kb, schema)
```

---

## Hybrid Yaklaşım: Wiki → JSON → RAG

### Akış:

```
1. Wiki Sayfası (Confluence)
   ↓
2. Export to JSON (Bir kere yapılır)
   ↓
3. JSON dosyası (Git'te tutulur)
   ↓
4. JSON'dan RAG'a ekleme (Otomatik)
   ↓
5. Vector Store (JSON'dan text extract + embed)
```

### Implementation:

```python
def setup_rag_from_json(json_path: str, vector_store: VectorStore):
    """
    JSON dosyasından RAG kurulumu.
    
    1. JSON'u oku
    2. Text'leri extract et
    3. Embed ve vector store'a ekle
    """
    # 1. JSON'u oku
    with open(json_path, "r", encoding="utf-8") as f:
        kb = json.load(f)
    
    # 2. Her field için text'leri extract et
    all_texts = []
    all_metadatas = []
    
    for field_name, field_data in kb["fields"].items():
        # Segments
        for segment in field_data.get("segments", []):
            text = format_segment_as_text(segment)
            all_texts.append(text)
            all_metadatas.append({
                "field": field_name,
                "type": "segment",
                "source": "json"
            })
        
        # Examples
        for example in field_data.get("examples", []):
            text = format_example_as_text(example)
            all_texts.append(text)
            all_metadatas.append({
                "field": field_name,
                "type": "example",
                "source": "json"
            })
        
        # ... diğer veri tipleri
    
    # 3. Vector store'a ekle
    index = vector_store.create_index("brd_kb")
    vector_store.add_texts(index, all_texts, all_metadatas)
    
    # 4. JSON'u da sakla (structured access için)
    return {
        "json_kb": kb,  # Structured access
        "index_id": index.index_id  # Semantic search için
    }


def format_segment_as_text(segment: dict) -> str:
    """Segment'i text formatına çevir (embedding için)"""
    text = f"""
    {segment['name']} Segmenti
    Tanım: {segment['definition']}
    
    Özellikler:
    - Yaş grubu: {segment['characteristics'].get('age_group', '')}
    - Gelir seviyesi: {segment['characteristics'].get('income_level', '')}
    
    İstatistikler:
    - Toplam müşteri: {segment['statistics'].get('total_customers', '')}
    - Günlük aktif: {segment['statistics'].get('daily_active', '')}
    """
    return text.strip()


def format_example_as_text(example: dict) -> str:
    """Example'ı text formatına çevir"""
    text = f"""
    {example.get('title', '')}
    {example.get('description', '')}
    """
    return text.strip()
```

---

## Wiki → JSON Export Script'i

### Tam Örnek:

```python
#!/usr/bin/env python3
"""
Wiki'den JSON'a export script'i.
Confluence sayfasını alıp structured JSON'a çevirir.
"""

from src.rag.wiki_client import ConfluenceClient
import json
import re
from typing import Dict, List, Any


def export_confluence_page_to_json(
    base_url: str,
    username: str,
    api_token: str,
    page_id: str,
    output_path: str
) -> dict:
    """
    Confluence sayfasını JSON'a export et.
    
    Args:
        base_url: Confluence base URL
        username: Confluence username
        api_token: Confluence API token
        page_id: Confluence page ID
        output_path: Output JSON file path
    
    Returns:
        Exported JSON data
    """
    # 1. Wiki client oluştur
    client = ConfluenceClient(
        base_url=base_url,
        username=username,
        api_token=api_token
    )
    
    # 2. Sayfayı çek
    print(f"Fetching page {page_id}...")
    page = client.fetch_page(page_id)
    
    # 3. Text'i extract et
    text = client.extract_text(page)
    
    # 4. Parse et ve JSON'a çevir
    print("Parsing content...")
    json_data = parse_wiki_content_to_json(text, page.get("title", ""))
    
    # 5. Metadata ekle
    json_data["metadata"] = {
        "source": "confluence",
        "page_id": page_id,
        "page_title": page.get("title", ""),
        "page_url": page.get("_links", {}).get("webui", ""),
        "exported_at": datetime.now().isoformat()
    }
    
    # 6. JSON'a kaydet
    print(f"Saving to {output_path}...")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Exported to {output_path}")
    return json_data


def parse_wiki_content_to_json(text: str, page_title: str) -> dict:
    """
    Wiki content'ini parse edip JSON'a çevir.
    
    Bu basit bir örnek. Gerçek implementasyonda daha sofistike parsing gerekebilir.
    """
    lines = text.split("\n")
    
    # Field'ı sayfa başlığından veya içerikten tespit et
    field_name = detect_field_from_title(page_title)
    
    json_data = {
        "field": field_name,
        "segments": [],
        "examples": [],
        "channels": [],
        "journeys": [],
        # ... diğer alanlar
    }
    
    current_section = None
    current_item = {}
    
    for line in lines:
        line = line.strip()
        
        # Başlıklar
        if line.startswith("##"):
            section = line.replace("##", "").strip()
            current_section = section.lower()
            
            # Segment tespit et
            if "segment" in section.lower():
                segment_name = section.replace("Segmenti", "").strip()
                current_item = {"name": segment_name}
                json_data["segments"].append(current_item)
            
            # Channel tespit et
            elif "kanal" in section.lower() or "channel" in section.lower():
                # Channel parsing...
                pass
        
        # Liste item'ları
        elif line.startswith("-") and current_item:
            parse_list_item_to_dict(line, current_item)
    
    return json_data


def detect_field_from_title(title: str) -> str:
    """Sayfa başlığından field adını tespit et"""
    title_lower = title.lower()
    
    if "segment" in title_lower or "müşteri" in title_lower:
        return "Target Customer Group"
    elif "kanal" in title_lower or "channel" in title_lower:
        return "Impacted Channels"
    elif "journey" in title_lower:
        return "Impacted Journey"
    elif "background" in title_lower or "problem" in title_lower:
        return "Background"
    elif "kpi" in title_lower or "metric" in title_lower or "hedef" in title_lower:
        return "Expected Results"
    # ... diğer alanlar
    
    return "Unknown"


def parse_list_item_to_dict(line: str, item: dict):
    """Liste item'ını parse edip dict'e ekle"""
    line = line.replace("-", "").strip()
    
    if ":" in line:
        key, value = line.split(":", 1)
        key = key.strip().lower()
        value = value.strip()
        
        # Nested keys (örn: "Özellikler: Yaş grubu: 18-35")
        if ":" in value:
            # İç içe yapı
            nested_key, nested_value = value.split(":", 1)
            if "characteristics" not in item:
                item["characteristics"] = {}
            item["characteristics"][nested_key.strip()] = nested_value.strip()
        else:
            # Normal key-value
            item[key] = value


if __name__ == "__main__":
    # Kullanım örneği
    export_confluence_page_to_json(
        base_url="https://company.atlassian.net/wiki",
        username="user@company.com",
        api_token="your-token",
        page_id="12345",  # Confluence page ID
        output_path="wiki_export.json"
    )
```

---

## Sonuç

**Wiki'den JSON'a export** işlemi:
1. ✅ Wiki içeriğini **structured JSON**'a çevirir
2. ✅ **Programatik erişim** sağlar
3. ✅ **Güncelleme** kolaylaşır
4. ✅ **Version control** (Git) ile takip edilebilir
5. ✅ **Schema validation** yapılabilir
6. ✅ **Hem structured hem semantic** search kullanılabilir

**Akış:**
```
Wiki → Export (Bir kere) → JSON (Ana kaynak) → RAG (JSON'dan text extract + embed)
```

Böylece hem wiki'de düzenleyebilirsin, hem de JSON'u structured olarak kullanabilirsin! 🚀
