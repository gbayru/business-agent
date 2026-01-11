# Sadece JSON ile İlerleme (Wiki Olmadan)

## Yaklaşım

Wiki'yi hiç kullanmadan, direkt **JSON dosyası** oluşturup onu RAG'a eklemek.

---

## Nasıl Çalışır?

### Akış:

```
1. JSON Dosyası Oluştur (Manuel veya Script ile)
   ↓
2. JSON'u Git'te Tut (Version Control)
   ↓
3. JSON'dan RAG'a Ekle (Otomatik)
   ↓
4. JSON'u Güncelle (Wiki yerine)
   ↓
5. RAG'ı Yeniden Ekle (Güncellenmiş JSON'dan)
```

---

## Avantajlar ✅

### 1. **Tam Kontrol**
- JSON'u istediğin gibi düzenleyebilirsin
- Wiki formatından bağımsızsın
- Structured data garantisi

### 2. **Kolay Güncelleme**
```bash
# JSON'u düzenle
vim brd_knowledge_base.json

# Git'te commit et
git add brd_knowledge_base.json
git commit -m "Update knowledge base"

# RAG'ı güncelle
python update_rag_from_json.py
```

### 3. **Version Control**
- Git ile tüm değişiklikleri track edebilirsin
- Diff görebilirsin
- Rollback yapabilirsin

### 4. **Programatik Erişim**
```python
import json

# JSON'u oku
with open("brd_knowledge_base.json", "r") as f:
    kb = json.load(f)

# Direkt erişim
prepaid_segment = kb["fields"]["Target Customer Group"]["segments"][0]
print(prepaid_segment["statistics"]["total_customers"])
```

### 5. **Schema Validation**
```python
# JSON schema ile validate et
import jsonschema

schema = {
    "type": "object",
    "properties": {
        "fields": {
            "Target Customer Group": {
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
    }
}

jsonschema.validate(kb, schema)
```

### 6. **Hızlı Iterasyon**
- JSON edit → Test → Commit
- Wiki'ye gitmene gerek yok
- Local'de çalışabilirsin

---

## Dezavantajlar ❌

### 1. **Manuel Düzenleme**
- Wiki'deki güzel UI yok
- JSON syntax hatası yapabilirsin
- Formatting manuel

### 2. **Collaboration Zorluğu**
- Wiki'de birden fazla kişi kolayca düzenleyebilir
- JSON'da merge conflict'ler olabilir
- Git bilgisi gerekebilir

### 3. **Wiki Özelliklerini Kaybedersin**
- Wiki'deki rich text editor yok
- Tablo, resim ekleme zor
- Comment, review özellikleri yok

---

## Nasıl Yapılır?

### 1. JSON Dosyası Oluştur

**`brd_knowledge_base.json`** dosyası oluştur:

```json
{
  "version": "1.0",
  "fields": {
    "Background": {
      "examples": [
        {
          "title": "Ödeme Timeout Sorunu",
          "description": "Mevcut ödeme sisteminde timeout sorunları yaşanıyor. Peak saatlerde (18:00-20:00) ödeme işlemlerinin %15'i timeout veriyor.",
          "metrics": {
            "timeout_rate": "%15",
            "peak_hours": "18:00-20:00"
          },
          "tags": ["timeout", "performance", "payment"]
        }
      ],
      "as_is_conditions": [
        {
          "system": "Ödeme Sistemi",
          "status": "Legacy",
          "capacity": "500K transaction/gün",
          "response_time": "3 saniye"
        }
      ]
    },
    "Target Customer Group": {
      "segments": [
        {
          "name": "Prepaid",
          "definition": "Ön ödemeli hat kullanan müşteriler",
          "characteristics": {
            "age_group": "18-35",
            "income_level": "Düşük-Orta",
            "mobile_usage": "%85"
          },
          "statistics": {
            "total_customers": "15M",
            "daily_active": "8M",
            "monthly_transactions": "120M"
          }
        }
      ]
    }
  }
}
```

### 2. JSON'dan RAG'a Ekleme Fonksiyonu

```python
# json_to_rag.py

from src.rag.index import VectorStore
import json

def add_json_to_rag(json_path: str, index_id: str = None):
    """
    JSON dosyasından RAG'a ekle.
    
    Args:
        json_path: JSON dosya yolu
        index_id: Mevcut index ID (varsa), yoksa yeni oluşturur
    """
    # 1. JSON'u oku
    with open(json_path, "r", encoding="utf-8") as f:
        kb = json.load(f)
    
    # 2. Vector store oluştur
    vector_store = VectorStore()
    
    # 3. Index oluştur veya al
    if index_id:
        from src.rag.index import RAGIndex
        index = RAGIndex(index_id=index_id, meta={"collection_name": f"rag_index_{index_id}"})
    else:
        import uuid
        index_id = str(uuid.uuid4())
        index = vector_store.create_index(index_id)
    
    # 4. JSON'dan text'leri extract et
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
                "source": "json",
                "segment_name": segment.get("name", "")
            })
        
        # Examples
        for example in field_data.get("examples", []):
            text = format_example_as_text(example)
            all_texts.append(text)
            all_metadatas.append({
                "field": field_name,
                "type": "example",
                "source": "json",
                "example_title": example.get("title", "")
            })
        
        # As-Is Conditions
        for condition in field_data.get("as_is_conditions", []):
            text = format_condition_as_text(condition)
            all_texts.append(text)
            all_metadatas.append({
                "field": field_name,
                "type": "as_is_condition",
                "source": "json"
            })
        
        # ... diğer veri tipleri
    
    # 5. Vector store'a ekle
    if all_texts:
        vector_store.add_texts(index, all_texts, all_metadatas)
        print(f"✓ Added {len(all_texts)} chunks to RAG index {index_id}")
    
    return index_id


def format_segment_as_text(segment: dict) -> str:
    """Segment'i text formatına çevir"""
    text = f"""
    {segment.get('name', '')} Segmenti
    Tanım: {segment.get('definition', '')}
    
    Özellikler:
    """
    
    for key, value in segment.get("characteristics", {}).items():
        text += f"- {key}: {value}\n"
    
    text += "\nİstatistikler:\n"
    for key, value in segment.get("statistics", {}).items():
        text += f"- {key}: {value}\n"
    
    return text.strip()


def format_example_as_text(example: dict) -> str:
    """Example'ı text formatına çevir"""
    text = f"""
    {example.get('title', '')}
    {example.get('description', '')}
    """
    
    if "metrics" in example:
        text += "\nMetrikler:\n"
        for key, value in example["metrics"].items():
            text += f"- {key}: {value}\n"
    
    return text.strip()


def format_condition_as_text(condition: dict) -> str:
    """As-Is condition'ı text formatına çevir"""
    text = f"""
    {condition.get('system', '')} - Mevcut Durum
    Durum: {condition.get('status', '')}
    Kapasite: {condition.get('capacity', '')}
    Response Time: {condition.get('response_time', '')}
    """
    return text.strip()


if __name__ == "__main__":
    # JSON'dan RAG'a ekle
    index_id = add_json_to_rag("brd_knowledge_base.json")
    print(f"Index ID: {index_id}")
```

### 3. JSON Güncelleme Workflow

```bash
# 1. JSON'u düzenle
vim brd_knowledge_base.json

# 2. Validate et (opsiyonel)
python validate_json.py brd_knowledge_base.json

# 3. RAG'ı güncelle
python json_to_rag.py

# 4. Git'te commit et
git add brd_knowledge_base.json
git commit -m "Update knowledge base: Added new segment"
```

### 4. Otomatik Güncelleme (Git Hook ile)

```bash
# .git/hooks/post-commit

#!/bin/bash
# JSON değiştiyse RAG'ı otomatik güncelle

if git diff-tree --name-only HEAD HEAD~1 | grep -q "brd_knowledge_base.json"; then
    echo "JSON updated, updating RAG..."
    python json_to_rag.py
fi
```

---

## JSON Yapısı Örneği

### Tam Yapı:

```json
{
  "version": "1.0",
  "last_updated": "2024-01-15T10:30:00Z",
  "fields": {
    "Background": {
      "examples": [...],
      "as_is_conditions": [...],
      "pain_points": [...]
    },
    "Expected Results": {
      "kpis": [...],
      "metrics": [...],
      "success_criteria_template": {...}
    },
    "Target Customer Group": {
      "segments": [...],
      "channel_preferences": {...}
    },
    "Impacted Channels": {
      "channels": [...],
      "impact_scenarios": [...]
    },
    "Impacted Journey": {
      "journeys": [...],
      "journey_states": {...}
    },
    "Journeys Description": {
      "as_is_template": {...},
      "to_be_template": {...},
      "edge_cases": [...],
      "before_after_examples": [...]
    },
    "Reports Needed": {
      "existing_reports": [...],
      "report_templates": {...}
    },
    "Traffic Forecast": {
      "methodology": {...},
      "benchmarks": {...},
      "forecast_template": {...}
    }
  },
  "metadata": {
    "tags": {
      "rag_search_terms": {
        "Background": ["problem", "pain point", "current situation"],
        "Expected Results": ["KPI", "metrics", "measurable"],
        ...
      }
    }
  }
}
```

---

## Workflow Karşılaştırması

### Wiki Yaklaşımı:
```
1. Wiki'de sayfa aç
2. Edit butonuna tıkla
3. İçeriği düzenle (rich text editor)
4. Save
5. RAG'ı manuel güncelle (add_wiki_documents çağır)
```

### JSON Yaklaşımı:
```
1. JSON dosyasını aç (editor'de)
2. İçeriği düzenle
3. Save
4. RAG'ı güncelle (json_to_rag.py çalıştır)
5. Git commit (opsiyonel)
```

---

## Ne Zaman JSON Kullanmalı?

### ✅ JSON Kullan:
- Tek kişi veya küçük ekip
- Git kullanıyorsun
- Programatik erişim istiyorsun
- Structured data önemli
- Hızlı iterasyon istiyorsun

### ❌ Wiki Kullan:
- Büyük ekip (collaboration önemli)
- Non-technical kullanıcılar var
- Rich text, tablo, resim gerekli
- Review/approval süreci var
- Wiki zaten kullanılıyor

---

## Hybrid Yaklaşım (En İyisi)

**Wiki → JSON → RAG**

```
1. Wiki'de düzenle (insan için kolay)
   ↓
2. Wiki'den JSON'a export (otomatik veya manuel)
   ↓
3. JSON'u Git'te tut (version control)
   ↓
4. JSON'dan RAG'a ekle (otomatik)
```

**Avantajlar:**
- ✅ Wiki'de düzenleme kolay (insan için)
- ✅ JSON structured (kod için)
- ✅ Git ile version control
- ✅ Hem wiki hem JSON avantajları

---

## Sonuç

**Sadece JSON ile ilerlemek:**

✅ **Avantajlar:**
- Tam kontrol
- Kolay güncelleme
- Version control (Git)
- Programatik erişim
- Schema validation

❌ **Dezavantajlar:**
- Manuel düzenleme
- Collaboration zor
- Wiki özelliklerini kaybedersin

**Öneri:** Eğer tek başına çalışıyorsan ve Git kullanıyorsan, JSON yaklaşımı iyi çalışır. Eğer ekip çalışması varsa, Wiki + JSON hybrid yaklaşımı daha iyi olur.
