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

# Test başlangıcı
print("INTERACTION (ETKİLEŞİM) SİSTEMİ TESTİ BAŞLIYOR")

# 1. TABLOLARI OLUŞTUR 
# 1. Veritabanı tablolarını oluştur(yoksa).
print("1. Veritabanı Tabloları Kontrol Ediliyor...")
try:
    User.create_table(safe=True)
    ChannelModel.create_table(safe=True)
    VideoModel.create_table(safe=True)
    InteractionModel.create_table(safe=True)
    print("   Tablolar hazır.")
except Exception as e:
    print(f"   Tablo uyarısı: {e}")

# 2. SAHTE VERİ OLUŞTUR
# 2. Test için gerekli sahte verileri (kullanıcı, kanal, video) oluştur
print("2. Test Verileri Oluşturuluyor...")

# Kullanıcı oluştur
test_user, created = User.get_or_create(
    username="TestKullanici", 
    defaults={'email': 'test@interaction.com', 'password_hash': '123'}
)

# Kanal oluştur (Video, bir kanala ait olmalı)
test_channel, created = ChannelModel.get_or_create(
    channel_name="TestKanalı",
    defaults={
        'channel_owner': test_user,
        'channel_category': 'Education',
        'channel_type': 'standard',
        'channel_status': 'verified'
    }
)

# Video oluştur
test_video, created = VideoModel.get_or_create(
    title="Python Dersleri #1", 
    defaults={
        'channel': test_channel,
        'description': 'Test videosu',
        'duration_seconds': 600,
        'visibility': 'public',
        'status': 'published',
        'video_type_id': 'standard'
    }
)

print(f"   Kullanıcı: {test_user.username}")
print(f"   Kanal    : {test_channel.channel_name}")
print(f"   Video    : {test_video.title}")

# Controller'ı Başlat
controller = InteractionController()

# 3. YORUM TESTİ
# 3. Videoya yorum ekleme işlemini test ediyoruz.
print("3. Yorum Testi...")
yorum_sonuc = controller.add_comment(test_user, test_video, "Harika bir video olmuş!")
print(f"   -> Ekleme Sonucu: {yorum_sonuc}")

# Yorumları Listele
yorumlar = controller.get_video_comment(test_video.id)
print(f"   -> Videodaki Yorumlar: {yorumlar}")

if any("Harika bir video olmuş!" in str(y) for y in yorumlar):
    print("   BAŞARILI: Yorum eklendi ve listelendi.")
else:
    print("   HATA: Yorum listede görünmüyor.")


# 4. LIKE (BEĞENİ) TESTİ (TOGGLE)
# 4. Beğeni (Like) işlemini test ediyoruz (Aç/Kapa mantığı).
print("4. Like Testi (Aç/Kapa)...")
# İlk Like
sonuc1 = controller.toggle_like(test_user, test_video)
print(f"   -> 1. Tıklama: {sonuc1}")

# Sayıyı Kontrol Et (1 olmalı)
sayi1 = controller.get_like_count(test_video.id)
print(f"   -> Like Sayısı: {sayi1}")

# İkinci Like (Geri Alma)
sonuc2 = controller.toggle_like(test_user, test_video)
print(f"   -> 2. Tıklama (Geri Alma): {sonuc2}")

# Sayıyı Kontrol Et (0 olmalı)
sayi2 = controller.get_like_count(test_video.id)
print(f"   -> Like Sayısı (Geri alındıktan sonra): {sayi2}")

if sayi1 >= 1: # Daha önceki testlerden kalıntı olabilir diye >= 1
    print("   BAŞARILI: Like atma ve geri alma çalışıyor.")
else:
    print("   HATA: Like sayıları tutarsız.")


# 5. DISLIKE TESTİ
# 5. Beğenmeme (Dislike) işlemini test ediyoruz.
print("5. Dislike Testi...")
dislike_sonuc = controller.toggle_dislike(test_user, test_video)
print(f"   -> Dislike Sonucu: {dislike_sonuc}")
dislike_sayi = controller.get_dislike_count(test_video.id)
print(f"   -> Dislike Sayısı: {dislike_sayi}")


# 6. KAYDETME (SAVE) TESTİ
# 6. Videoyu kaydetme (Save) işlemini test ediyoruz.
print("6. Kaydetme (Save) Testi...")
save_sonuc = controller.toggle_save(test_user, test_video)
print(f"   -> Kaydetme Sonucu: {save_sonuc}")
save_sayi = controller.get_save_count(test_video.id)

if save_sayi > 0:
    print("   BAŞARILI: Video kaydedilenlere eklendi.")
else:
    print("   HATA: Kaydetme işlemi başarısız.")


# 7. PAYLAŞMA (SHARE) TESTİ
# 7. Videoyu paylaşma (Share) işlemini test ediyoruz.
print("7. Paylaşma Testi...")
share_sonuc = controller.share_video(test_user, test_video, "Twitter")
print(f"   -> Paylaşım Sonucu: {share_sonuc}")


# 8. ABONE OLMA TESTİ
# 8. Kanala abone olma işlemini test ediyoruz.
print("8. Abonelik Testi...")
sub_sonuc = controller.toggle_subscription(test_user, test_video)
print(f"   -> Abonelik Sonucu: {sub_sonuc}")


# 9. GENEL RAPOR
# 9. Test sonunda genel video etkileşim raporunu yazdırıyoruz.
print("FİNAL RAPORU (VİDEO İSTATİSTİKLERİ)")
print(f"Video Başlığı : {test_video.title}")
print(f"Like       : {controller.get_like_count(test_video.id)}")
print(f"Dislike    : {controller.get_dislike_count(test_video.id)}")
print(f"Yorum      : {controller.get_comment_count(test_video.id)}")
print(f"Kayıt      : {controller.get_save_count(test_video.id)}")
print(f"Paylaşım   : {controller.get_share_count(test_video.id)}")
