import sys
import os

# --- PATH AYARI (ÖNEMLİ) ---
# Bu dosya 'tests' klasöründe olduğu için, 'models' klasörünü bulabilmesi adına
# bir üst dizini (proje ana dizinini) Python'un arama yoluna ekliyoruz.
current_dir = os.path.dirname(os.path.abspath(__file__)) # tests klasörünün yolu
root_dir = os.path.dirname(current_dir)                # Bir üst klasör (Proje Root)
sys.path.append(root_dir)
# ---------------------------

# Şimdi importları rahatça yapabiliriz

from models.database import db
from models.accounts_module.user import User
from models.accounts_module.channel_base import ChannelModel 
from models.content_module.video_base import VideoModel
from models.repositories.video_repository import VideoRepository
from models.content_module.video_type import get_video_logic
def create_dummy_data():
    """Test için sahte kullanıcı ve kanal oluşturur"""
    print("--- 1. Hazırlık: Kullanıcı ve Kanal Kontrolü ---")
    
    # Veritabanı bağlantısını garantile
    if db.is_closed():
        db.connect()

    # Kullanıcı Oluştur (Varsa geç)
    try:
        # get_or_create: Varsa getirir, yoksa yaratır (Pratik Peewee metodu)
        user, created = User.get_or_create(
            username="test_user",
            defaults={
                'email': "test@dek.com",
                'password_hash': "1234"
            }
        )
        if created:
            print("-> Yeni 'test_user' oluşturuldu.")
        else:
            print("-> Mevcut 'test_user' kullanılıyor.")
    except Exception as e:
        print(f"-> Kullanıcı hatası: {e}")
        return None

    # Kanal Oluştur (Varsa geç)
    try:
        channel, created = ChannelModel.get_or_create(
            channel_name="DEK Teknoloji",
            defaults={
                'channel_owner': user,
                'channel_category': "Education",
                'channel_type': "brand"
            }
        )
        if created:
            print("-> Yeni 'DEK Teknoloji' kanalı oluşturuldu.")
        else:
            print("-> Mevcut 'DEK Teknoloji' kanalı kullanılıyor.")
            
        return channel
    except Exception as e:
        print(f"-> Kanal hatası: {e}")
        return None

def main():
    # 1. Hazırlık Verilerini Oluştur
    my_channel = create_dummy_data()
    
    if not my_channel:
        print("HATA: Kanal oluşturulamadığı için test iptal edildi.")
        return

    repo = VideoRepository()

    print("\n--- 2. Repository Testi: Video Ekleme (Create) ---")
    
    # Standart Video Ekleme
    v1 = repo.add_video(
        channel_id=my_channel.id,
        title="Python OOP Dersleri 1",
        duration=600,
        video_type_id="standard",
        visibility="public"
    )
    print(f"✔ Eklendi: {v1.title} (Tip: Standard)")

    # Shorts Ekleme
    v2 = repo.add_video(
        channel_id=my_channel.id,
        title="Komik Yazılımcı Anları",
        duration=45,
        video_type_id="short",
        visibility="public"
    )
    print(f"✔ Eklendi: {v2.title} (Tip: Short)")

    # Canlı Yayın Ekleme
    v3 = repo.add_video(
        channel_id=my_channel.id,
        title="Büyük Proje Final Sunumu",
        duration=0,
        video_type_id="live",
        visibility="unlisted"
    )
    print(f"✔ Eklendi: {v3.title} (Tip: Live)")


    print("\n--- 3. Polimorfizm Testi: Mantık Katmanı ---")
    # Kanala ait videoları çek
    videos = repo.get_videos_by_channel(my_channel.id)

    if not videos:
        print("Uyarı: Video listesi boş geldi!")
    
    for video in videos:
        # FACTORY DESIGN PATTERN: Veriyi mantığa giydiriyoruz
        logic = get_video_logic(video)
        
        # Her video türü için hesaplamalar farklı çalışmalı
        print(f"\n📺 Video: {video.title}")
        print(f"   Tip: {video.video_type_id}")
        print(f"   Tahmini İşleme: {logic.get_processing_time_estimate()} sn")
        print(f"   Anasayfa Puanı: {logic.calculate_listing_score()}")


    print("\n--- 4. Update Testi: Durum Güncelleme ---")
    # Canlı yayını 'published' (yayınlanmış/bitmiş) yapalım
    print(f"Güncelleniyor: {v3.title} (Eski Durum: {v3.status})")
    
    updated_video = repo.update_video_status(v3.id, "published")
    
    if updated_video:
        print(f"✔ Yeni Durum: {updated_video.status}")
        
        # Durum değişince puanın değiştiğini (Live mantığı) kontrol edelim
        logic_new = get_video_logic(updated_video)
        print(f"   (Yayın Bittiği İçin) Yeni Puan: {logic_new.calculate_listing_score()}")
    else:
        print("❌ Güncelleme başarısız oldu!")

if __name__ == "__main__":
    main()