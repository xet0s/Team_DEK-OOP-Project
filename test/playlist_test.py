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
from models.interaction_module.playlist_base import PlaylistModel
from models.interaction_module.playlist_item import PlaylistItemModel
from controllers.playlist_controller import PlaylistController

# Test başlangıcı
print("PLAYLIST SİSTEMİ TESTİ BAŞLIYOR")

# 1. TABLOLARI OLUŞTUR 
# 1. Veritabanı tablolarını oluşturuyoruz.  tablolar yoksa hata almamamızı sağlar.
print("1. Veritabanı Tabloları Kontrol Ediliyor...")
try:
    User.create_table(safe=True)
    ChannelModel.create_table(safe=True)
    VideoModel.create_table(safe=True)
    PlaylistModel.create_table(safe=True)
    PlaylistItemModel.create_table(safe=True)
    print("   Tablolar hazır.")
except Exception as e:
    print(f"   Tablo uyarısı: {e}")

# 2. SAHTE VERİ OLUŞTUR
# 2. Test verilerini (kullanıcı, kanal, video) oluşturuyoruz.
print("2. Test Verileri Oluşturuluyor...")

# Kullanıcı oluştur
test_user, created = User.get_or_create(
    username="MuzikSever", 
    defaults={'email': 'muzik@test.com', 'password_hash': '1234'}
)

# Kanal oluştur (Video için)
test_channel, created = ChannelModel.get_or_create(
    channel_name="MuzikKanalim",
    defaults={
        'channel_owner': test_user,
        'channel_category': 'Music',
        'channel_type': 'standard',
        'channel_status': 'verified'
    }
)

# Videolar oluştur
video1, created1 = VideoModel.get_or_create(
    title="Pop Şarkılar 2024", 
    defaults={
        'channel': test_channel,
        'description': 'En yeni pop şarkılar',
        'duration_seconds': 180,
        'status': 'published',
        'video_type_id': 'standard'
    }
)

video2, created2 = VideoModel.get_or_create(
    title="Rock Klasikleri", 
    defaults={
        'channel': test_channel,
        'description': 'Efsane rock parçalar',
        'duration_seconds': 240,
        'status': 'published',
        'video_type_id': 'standard'
    }
)

print(f"   Kullanıcı: {test_user.username}")
print(f"   Video 1  : {video1.title}")
print(f"   Video 2  : {video2.title}")

# Controller'ı Başlat
controller = PlaylistController()

# 3. PLAYLIST OLUŞTURMA TESTİ
# 3. Playlist oluşturma işlemini test ediyoruz.
print("3. Playlist Oluşturma Testi...")

# Yeni bir liste oluştur
olusturma_sonuc = controller.create_playlist(test_user, "Favori Şarkılarım", "E") # E -> Public
print(f"   -> Oluşturma Sonucu: {olusturma_sonuc}")

# Oluşan playlisti bulmak için kullanıcının listelerini çekelim
kullanici_listeleri = controller.repo.get_playlists_by_user(test_user.id)
secilen_playlist = kullanici_listeleri[-1] if kullanici_listeleri else None

if secilen_playlist:
    print(f"   BAŞARILI: Playlist oluşturuldu. (ID: {secilen_playlist.id})")
else:
    print("   HATA: Playlist oluşturulamadı.")
    sys.exit() # Playlist yoksa devam etme


# 4. VIDEO EKLEME TESTİ
# 4. Oluşturulan playliste video ekleme işlemini test ediyoruz.
print("4. Video Ekleme Testi...")

# 1. Videoyu Ekle
ekleme1 = controller.add_video(test_user, secilen_playlist.id, video1.id)
print(f"   -> Video 1 Ekleme: {ekleme1}")

# 2. Videoyu Ekle
ekleme2 = controller.add_video(test_user, secilen_playlist.id, video2.id)
print(f"   -> Video 2 Ekleme: {ekleme2}")

# İçeriği Kontrol Et
icerik = controller.show_playlist_countent(secilen_playlist.id)
print(f"   -> Liste İçeriği: {icerik}")

if "Pop Şarkılar" in icerik and "Rock Klasikleri" in icerik:
    print("   BAŞARILI: Videolar listeye eklendi.")
else:
    print("   HATA: Videolar listede görünmüyor.")


# 5. AYNI VİDEOYU TEKRAR EKLEME (DUPLICATE) TESTİ
# 5. Aynı videonun tekrar eklenmesini (duplicate) engelleme testini yapıyoruz.
print("5. Duplicate (Tekrar Ekleme) Testi...")
tekrar_ekle = controller.add_video(test_user, secilen_playlist.id, video1.id)
print(f"   -> Tekrar Ekleme Denemesi: {tekrar_ekle}")

if "zaten listede var" in tekrar_ekle:
    print("   BAŞARILI: Aynı video tekrar eklenmedi.")
else:
    print("   UYARI: Duplicate kontrolü çalışmıyor olabilir.")


# 6. VIDEO ÇIKARMA TESTİ
# 6. Listeden video çıkarma (silme) işlemini test ediyoruz.
print("6. Video Çıkarma (Silme) Testi...")
silme_sonuc = controller.remove_video(test_user, secilen_playlist.id, video1.id)
print(f"   -> Çıkarma Sonucu: {silme_sonuc}")

# Son durumu kontrol et
guncel_icerik = controller.show_playlist_countent(secilen_playlist.id)
print(f"   -> Güncel İçerik: {guncel_icerik}")

if "Pop Şarkılar" not in guncel_icerik and "Rock Klasikleri" in guncel_icerik:
    print("   BAŞARILI: Video başarıyla listeden çıkarıldı.")
else:
    print("   HATA: Video silinemedi.")


# 7. LİSTELERİMİ GÖSTER TESTİ
# 7. Kullanıcının tüm listelerini gösterme işlemini test ediyoruz.
print("7. 'Listelerim' Testi...")
listeler = controller.list_my_playlist(test_user.id)
print(f"   -> Listeler Çıktısı:\n{listeler}")


# 8. PLAYLIST SİLME TESTİ
# 8. Playlisti tamamen silme işlemini test ediyoruz.
print("8. Playlist Silme Testi...")
playlist_sil = controller.delete_playlist(test_user, secilen_playlist.id)
print(f"   -> Playlist Silme Sonucu: {playlist_sil}")

# Silindi mi kontrol et
kontrol = controller.repo.get_playlist_by_id(secilen_playlist.id)
if kontrol is None:
    print("   BAŞARILI: Playlist ve içindeki öğeler veritabanından silindi.")
else:
    print("   HATA: Playlist hala duruyor.")

print("TEST TAMAMLANDI")
