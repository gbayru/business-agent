#!/usr/bin/env python3
"""
Wiki RAG Entegrasyonu Örnek Kullanımı

Bu script, wiki'den doküman çekip RAG sistemine ekleme işlemini gösterir.
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
    
    # 2. Wiki dokümanlarını ekle
    print("2. Wiki dokümanları ekleniyor...")
    print("   (Confluence bağlantı bilgilerini güncelleyin!)")
    
    try:
        result = add_wiki_documents(
            session_id=session_id,
            wiki_type="confluence",
            base_url=os.getenv("CONFLUENCE_BASE_URL", "https://your-company.atlassian.net/wiki"),
            username=os.getenv("CONFLUENCE_USERNAME", "your-email@company.com"),
            api_token=os.getenv("CONFLUENCE_API_TOKEN", "your-api-token"),
            space_key=os.getenv("CONFLUENCE_SPACE_KEY", "ENG"),  # İsteğe bağlı
            limit=10  # Test için küçük sayı
        )
        print(f"   ✓ Başarılı! Index ID: {result['index_id']}\n")
    except Exception as e:
        print(f"   ✗ Hata: {e}\n")
        print("   Not: Confluence bağlantı bilgilerini .env dosyasına veya environment variable olarak ayarlayın.\n")
        return
    
    # 3. Test mesajı gönder
    print("3. Test mesajı gönderiliyor (RAG aktif)...")
    response = message(
        session_id=session_id,
        current_field="Background",
        user_text="Mevcut sistemde performans sorunları var"
    )
    print(f"   ✓ Mesaj işlendi. Sonraki soru: {response.get('next_questions', [])}\n")




def example_specific_pages():
    """Belirli sayfaları ekleme örneği"""
    print("=== Belirli Sayfaları Ekleme ===\n")
    
    session = create_session()
    session_id = session["session_id"]
    print(f"Session ID: {session_id}\n")
    
    # Belirli sayfa ID'lerini belirt
    page_ids = ["12345", "67890"]  # Gerçek sayfa ID'lerini kullanın
    
    try:
        result = add_wiki_documents(
            session_id=session_id,
            wiki_type="confluence",
            base_url=os.getenv("CONFLUENCE_BASE_URL", "https://your-company.atlassian.net/wiki"),
            username=os.getenv("CONFLUENCE_USERNAME", "your-email@company.com"),
            api_token=os.getenv("CONFLUENCE_API_TOKEN", "your-api-token"),
            page_ids=page_ids
        )
        print(f"✓ {len(page_ids)} sayfa başarıyla eklendi. Index ID: {result['index_id']}\n")
    except Exception as e:
        print(f"✗ Hata: {e}\n")


if __name__ == "__main__":
    print("Wiki RAG Entegrasyonu Örnekleri\n")
    print("=" * 50 + "\n")
    
    # Environment variables kontrolü
    print("Not: Bağlantı bilgilerini environment variable olarak ayarlayabilirsiniz:")
    print("  - CONFLUENCE_BASE_URL")
    print("  - CONFLUENCE_USERNAME")
    print("  - CONFLUENCE_API_TOKEN")
    print("  - CONFLUENCE_SPACE_KEY")
    print("  - MEDIAWIKI_API_URL\n")
    print("=" * 50 + "\n")
    
    # Hangi örneği çalıştırmak istediğinizi seçin
    choice = input("Hangi örneği çalıştırmak istersiniz?\n1. Confluence\n2. Belirli Sayfalar\nSeçim (1-2): ")
    
    if choice == "1":
        example_confluence()
    elif choice == "2":
        example_specific_pages()
    else:
        print("Geçersiz seçim. Confluence örneği çalıştırılıyor...\n")
        example_confluence()
