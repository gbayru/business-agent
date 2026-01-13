#!/usr/bin/env python3
"""
Wiki RAG Entegrasyonu Örnek Kullanımı

Bu script, Confluence wiki'den BRD Knowledge Base dokümanını çekip 
RAG sistemine ekleme işlemini gösterir.
"""

import os
import sys

# PYTHONPATH ayarı
sys.path.insert(0, os.path.dirname(__file__))

from src.core.service import create_session, add_wiki_documents, message


def example_confluence():
    """Confluence wiki örneği"""
    print("=== Confluence Wiki Entegrasyonu ===\n")
    
    # 1. Session oluştur
    print("1. Session oluşturuluyor...")
    session = create_session()
    session_id = session["session_id"]
    print(f"   Session ID: {session_id}\n")
    
    # 2. Confluence'den BRD Knowledge Base sayfasını ekle
    print("2. BRD Knowledge Base sayfası ekleniyor...")
    print("   (Confluence bağlantı bilgilerini güncelleyin!)")
    
    try:
        result = add_wiki_documents(
            session_id=session_id,
            wiki_type="confluence",
            base_url=os.getenv("CONFLUENCE_BASE_URL", "https://your-company.atlassian.net/wiki"),
            username=os.getenv("CONFLUENCE_USERNAME", "your-email@company.com"),
            api_token=os.getenv("CONFLUENCE_API_TOKEN", "your-api-token"),
            space_key=os.getenv("CONFLUENCE_SPACE_KEY", "ENG"),
            limit=10  # Test için küçük sayı
        )
        print(f"   ✓ Başarılı! Index ID: {result['index_id']}\n")
        print(f"   BRD Knowledge Base RAG sistemine eklendi.\n")
    except Exception as e:
        print(f"   ✗ Hata: {e}\n")
        print("   Not: Confluence bağlantı bilgilerini .env dosyasına veya environment variable olarak ayarlayın.\n")
        return
    
    # 3. Test mesajları gönder
    print("3. Test mesajları gönderiliyor (RAG aktif)...\n")
    
    # Test 1: Background field
    print("   Test 1: Background field")
    response = message(
        session_id=session_id,
        current_field="Background",
        user_text="Mevcut sistemde performans sorunları var"
    )
    print(f"   ✓ RAG'dan ilgili sistem bilgileri çekildi")
    print(f"   Sonraki soru: {response.get('next_questions', [])[:1]}\n")
    
    # Test 2: Target Customer Group field
    print("   Test 2: Target Customer Group field")
    response = message(
        session_id=session_id,
        current_field="Target Customer Group",
        user_text="Postpaid müşterileri"
    )
    print(f"   ✓ RAG'dan segment bilgileri çekildi")
    print(f"   Normalize edilen cevap snippet: {response.get('normalized', {}).get('value', '')[:100]}...\n")
    
    # Test 3: Impacted Channels field
    print("   Test 3: Impacted Channels field")
    response = message(
        session_id=session_id,
        current_field="Impacted Channels",
        user_text="Mobil app ve web"
    )
    print(f"   ✓ RAG'dan kanal bilgileri çekildi\n")




def example_specific_page():
    """Belirli BRD sayfasını ekleme"""
    print("=== BRD Knowledge Base Sayfası (Specific Page) ===\n")
    
    session = create_session()
    session_id = session["session_id"]
    print(f"Session ID: {session_id}\n")
    
    # BRD Knowledge Base page ID (Confluence'den alınacak)
    # Confluence'de sağ üst menüden "..." -> "Page Information" -> URL'den page ID
    brd_page_id = os.getenv("BRD_PAGE_ID", "123456789")
    
    print(f"BRD Page ID: {brd_page_id}")
    print("(Gerçek page ID'yi BRD_PAGE_ID env variable olarak set edin)\n")
    
    try:
        result = add_wiki_documents(
            session_id=session_id,
            wiki_type="confluence",
            base_url=os.getenv("CONFLUENCE_BASE_URL", "https://your-company.atlassian.net/wiki"),
            username=os.getenv("CONFLUENCE_USERNAME", "your-email@company.com"),
            api_token=os.getenv("CONFLUENCE_API_TOKEN", "your-api-token"),
            page_ids=[brd_page_id]
        )
        print(f"✓ BRD Knowledge Base başarıyla eklendi!")
        print(f"  Index ID: {result['index_id']}")
        print(f"  Doküman sayısı: {result['documents_count']}")
        print(f"  Chunk sayısı: {result.get('chunks_count', 'N/A')}\n")
        
        # RAG içeriği özeti
        print("RAG'a eklenen içerik:")
        print("  - Background: Problem tanımları ve mevcut durum")
        print("  - Expected Results: KPI'lar ve hedefler")
        print("  - Target Customer Group: Müşteri segmentleri")
        print("  - Impacted Channels: Kanallar ve entegrasyonlar")
        print("  - Impacted Journey: Journey tanımları")
        print("  - Journeys Description: As-Is/To-Be akışlar, edge case'ler")
        print("  - Reports Needed: Rapor gereksinimleri")
        print("  - Traffic Forecast: Trafik tahminleri\n")
    except Exception as e:
        print(f"✗ Hata: {e}\n")


if __name__ == "__main__":
    print("Wiki RAG Entegrasyonu Örnekleri\n")
    print("=" * 60 + "\n")
    
    # Environment variables kontrolü
    print("Environment Variables:")
    print("  - CONFLUENCE_BASE_URL: https://your-company.atlassian.net/wiki")
    print("  - CONFLUENCE_USERNAME: your-email@company.com")
    print("  - CONFLUENCE_API_TOKEN: your-api-token")
    print("  - CONFLUENCE_SPACE_KEY: ENG (Space key)")
    print("  - BRD_PAGE_ID: Confluence page ID (optional)\n")
    print("=" * 60 + "\n")
    
    # Hangi örneği çalıştırmak istediğinizi seçin
    choice = input("Hangi örneği çalıştırmak istersiniz?\n1. Confluence Wiki (Önerilen)\n2. Specific BRD Page\nSeçim (1-2): ")
    
    if choice == "1":
        example_confluence()
    elif choice == "2":
        example_specific_page()
    else:
        print("Geçersiz seçim. Confluence örneği çalıştırılıyor...\n")
        example_confluence()
