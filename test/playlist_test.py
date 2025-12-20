import sys
import os

# --- YOL AYARLARI ---
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)
# --------------------

from models.accounts_module.user import User
from models.accounts_module.channel_base import ChannelModel
from models.content_module.video_base import VideoModel
from models.interaction_module.playlist_base import PlaylistModel
from models.interaction_module.playlist_item import PlaylistItemModel
from controllers.playlist_controller import PlaylistController

print("PLAYLIST SİSTEMİ TESTİ BAŞLIYOR (OOP Refactor)")

class PlaylistSystemTest:
    """
    Playlist sistemi testlerini kapsayan sınıf.
    İstenen OOP özellikleri:
    - @staticmethod (Veri oluşturma)
    - @property (En son işlem gören veriye erişim)
    """

    def __init__(self):
        self.controller = PlaylistController()
        self._last_playlist = None
        self._last_user = None

    @property
    def last_created_playlist(self):
        """Test sırasında oluşturulan son playlisti döndürür."""
        if not self._last_playlist:
            # Eğer henüz atanmadıysa, kullanıcının son playlistini bulmaya çalış
            if self._last_user:
                 playlists = self.controller.repo.get_playlists_by_user(self._last_user.id)
                 if playlists:
                     self._last_playlist = playlists[-1]
        return self._last_playlist

    @staticmethod
    def setup_database():
        print("1. Veritabanı Tabloları Kontrol Ediliyor...")
        try:
            # Tabloları temizle (Şema değişikliği varsa yansıması için)
            try: PlaylistItemModel.drop_table(safe=True)
            except: pass
            try: PlaylistModel.drop_table(safe=True)
            except: pass
            try: VideoModel.drop_table(safe=True)
            except: pass
            try: ChannelModel.drop_table(safe=True)
            except: pass
            try: User.drop_table(safe=True)
            except: pass
            
            # Tabloları yeniden oluştur
            User.create_table(safe=True)
            ChannelModel.create_table(safe=True)
            VideoModel.create_table(safe=True)
            PlaylistModel.create_table(safe=True)
            PlaylistItemModel.create_table(safe=True)
            print("   Tablolar hazır.")
        except Exception as e:
            print(f"   Tablo uyarısı: {e}")

    @staticmethod
    def create_test_data():
        print("2. Test Verileri Oluşturuluyor...")
        # Kullanıcı
        test_user, _ = User.get_or_create(
            username="MuzikSever", 
            defaults={'email': 'muzik@test.com', 'password_hash': '1234'}
        )
        
        # Kanal
        test_channel, _ = ChannelModel.get_or_create(
            channel_name="MuzikKanalim",
            defaults={
                'channel_owner': test_user,
                'channel_category': 'Music',
                'channel_type': 'standard',
                'channel_status': 'verified',
                'channel_upload_limit': 10
            }
        )

        # Videolar
        v1, _ = VideoModel.get_or_create(
            title="Pop Şarkılar 2024", 
            defaults={
                'channel': test_channel,
                'description': 'En yeni pop şarkılar',
                'duration_seconds': 180,
                'status': 'published',
                'video_type_id': 'standard',
                'video_link': 'http://example.com/video1'
            }
        )

        v2, _ = VideoModel.get_or_create(
            title="Rock Klasikleri", 
            defaults={
                'channel': test_channel,
                'description': 'Efsane rock parçalar',
                'duration_seconds': 240,
                'status': 'published',
                'video_type_id': 'standard',
                'video_link': 'http://example.com/video2'
            }
        )

        print(f"   Kullanıcı: {test_user.username}")
        print(f"   Video 1  : {v1.title}")
        print(f"   Video 2  : {v2.title}")

        return test_user, v1, v2

    def run_tests(self):
        # 1. Setup
        PlaylistSystemTest.setup_database()

        # 2. Data Creation
        user, video1, video2 = PlaylistSystemTest.create_test_data()
        self._last_user = user

        # 3. Playlist Creation
        print("3. Playlist Oluşturma Testi...")
        self.controller.create_playlist(user, "Favori Şarkılarım", "E")
        
        # Property kullanımı
        playlist = self.last_created_playlist
        
        if playlist:
            print(f"   BAŞARILI: Playlist oluşturuldu. ID: {playlist.id}")
            # Yeni eklenen property testi
            print(f"   Durum Metni (Property): {playlist.status_text}")
        else:
            print("   HATA: Playlist oluşturulamadı.")
            return

        # 4. Add Video
        print("4. Video Ekleme Testi...")
        print(f"   -> Video 1 Ekleme: {self.controller.add_video(user, playlist.id, video1.id)}")
        print(f"   -> Video 2 Ekleme: {self.controller.add_video(user, playlist.id, video2.id)}")

        content = self.controller.show_playlist_countent(playlist.id)
        print(f"   -> Liste İçeriği: {content}")

        if "Pop Şarkılar" in content and "Rock Klasikleri" in content:
            print("   BAŞARILI: Videolar listeye eklendi.")
        else:
            print("   HATA: Videolar eksik.")

        # 5. Duplicate Test
        print("5. Duplicate (Tekrar Ekleme) Testi...")
        res = self.controller.add_video(user, playlist.id, video1.id)
        print(f"   -> Tekrar Ekleme: {res}")

        # 6. Remove Video
        print("6. Video Çıkarma Testi...")
        print(f"   -> Çıkarma Sonucu: {self.controller.remove_video(user, playlist.id, video1.id)}")
        current_content = self.controller.show_playlist_countent(playlist.id)
        print(f"   -> Güncel İçerik: {current_content}")

        # 7. List My Playlists
        print("7. 'Listelerim' Testi...")
        print(self.controller.list_my_playlist(user.id))

        # 8. Delete Playlist
        print("8. Playlist Silme Testi...")
        print(f"   -> Silme Sonucu: {self.controller.delete_playlist(user, playlist.id)}")

        if self.controller.repo.get_playlist_by_id(playlist.id) is None:
             print("   BAŞARILI: Playlist silindi.")
