import sys
import os

# --- YOL AYARLARI (Modüllerin bulunması için) ---
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)
# ------------------------------------------------

from models.accounts_module.user import User
from models.accounts_module.channel_base import ChannelModel
from models.content_module.video_base import VideoModel
from models.interaction_module.interaction_base import InteractionModel
from controllers.interaction_controller import InteractionController

print("INTERACTION (ETKİLEŞİM) SİSTEMİ TESTİ BAŞLIYOR (OOP Refactor)")

class InteractionSystemTest:
    """
    Etkileşim sistemi testlerini kapsayan sınıf.
    OOP Özellikleri:
    - @staticmethod (Veri hazırlama)
    - Class yapısı altında test akışı
    """

    @staticmethod
    def setup_database():
        print("1. Veritabanı Tabloları Kontrol Ediliyor...")
        try:
            User.create_table(safe=True)
            ChannelModel.create_table(safe=True)
            VideoModel.create_table(safe=True)
            InteractionModel.create_table(safe=True)
            print("   Tablolar hazır.")
        except Exception as e:
            print(f"   Tablo uyarısı: {e}")

    @staticmethod
    def create_test_data():
        print("2. Test Verileri Oluşturuluyor...")
        
        # Kullanıcı oluştur
        test_user, _ = User.get_or_create(
            username="TestKullanici", 
            defaults={'email': 'test@interaction.com', 'password_hash': '123'}
        )

        # Kanal oluştur
        test_channel, _ = ChannelModel.get_or_create(
            channel_name="TestKanalı",
            defaults={
                'channel_owner': test_user,
                'channel_category': 'Education',
                'channel_type': 'standard',
                'channel_status': 'verified',
                'channel_upload_limit': 100
            }
        )

        # Video oluştur
        test_video, _ = VideoModel.get_or_create(
            title="Python Dersleri #1", 
            defaults={
                'channel': test_channel,
                'description': 'Test videosu',
                'duration_seconds': 600,
                'visibility': 'public',
                'status': 'published',
                'video_type_id': 'standard',
                'video_link': 'http://example.com/test_video'
            }
        )

        print(f"   Kullanıcı: {test_user.username}")
        print(f"   Kanal    : {test_channel.channel_name}")
        print(f"   Video    : {test_video.title}")

        return test_user, test_video

    def run(self):
        # 1. Setup
        InteractionSystemTest.setup_database()

        # 2. Data
        user, video = InteractionSystemTest.create_test_data()

        # Controller
        controller = InteractionController()

        # 3. Yorum Testi
        print("3. Yorum Testi...")
        res = controller.add_comment(user, video, "Harika bir video olmuş!")
        print(f"   -> Ekleme Sonucu: {res}")
        
        comments = controller.get_video_comment(video.id)
        print(f"   -> Videodaki Yorumlar: {comments}")

        if any("Harika" in str(c) for c in comments):
             print("   BAŞARILI: Yorum eklendi.")
        else:
             print("   HATA: Yorum yok.")

        # 4. Like Testi
        print("4. Like Testi (Aç/Kapa)...")
        print(f"   -> 1. Tıklama: {controller.toggle_like(user, video)}")
        print(f"   -> Like Sayısı: {controller.get_like_count(video.id)}")
        print(f"   -> 2. Tıklama: {controller.toggle_like(user, video)}")
        print(f"   -> Like Sayısı: {controller.get_like_count(video.id)}")

        # 5. Dislike Testi
        print("5. Dislike Testi...")
        print(f"   -> Dislike Sonucu: {controller.toggle_dislike(user, video)}")

        # 6. Save Test
        print("6. Kaydetme (Save) Testi...")
        print(f"   -> Kaydetme Sonucu: {controller.toggle_save(user, video)}")

        # 7. Share Test
        print("7. Paylaşma Testi...")
        # Artık property kullanıyor içerde
        print(f"   -> Paylaşım Sonucu: {controller.share_video(user, video, 'Twitter')}")

        # 8. Abonelik Testi
        print("8. Abonelik Testi...")
        print(f"   -> Abonelik Sonucu: {controller.toggle_subscription(user, video)}")

        # 9. Rapor
        print("FİNAL RAPORU (VİDEO İSTATİSTİKLERİ)")
        print(f"Video Başlığı : {video.title}")
        print(f"Like       : {controller.get_like_count(video.id)}")
        print(f"Dislike    : {controller.get_dislike_count(video.id)}")
        print(f"Yorum      : {controller.get_comment_count(video.id)}")
        print(f"Kayıt      : {controller.get_save_count(video.id)}")
        print(f"Paylaşım   : {controller.get_share_count(video.id)}")

if __name__ == "__main__":
    test = InteractionSystemTest()
    test.run()
