import sys
import os
from time import sleep

# Proje ana dizinini Python yoluna ekle
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.database import db
from models.accounts_module.user import User
from models.accounts_module.channel_base import ChannelModel
from models.content_module.video_base import VideoModel
from controllers.video_controller import VideoController
from models.repositories.video_repository import VideoRepository

# Veritabanını Hazırla
db.connect()
db.drop_tables([User, ChannelModel, VideoModel])
db.create_tables([User, ChannelModel, VideoModel])

print("--- VİDEO LİSTELEME VE FİLTRELEME TESTİ ---")
print("-"*50)

# Kullanıcı, Kanal ve Controller Oluştur
user = User.create(username="Lister",
                    email="list@test.com",
                    password_hash="123",
                    role="Standard")
channel = ChannelModel.create(channel_owner=user,
                                channel_name="Liste Kanalı",
                                channel_category="General",
                                channel_type="Personal",
                                channel_status="active",
                                channel_upload_limit=50,
                                channel_link="dek.channel/list")

controller = VideoController()
repo = VideoRepository()

# Listelnecek Videoları Ekle
print(">> Veriler hazırlanıyor...")
sleep(0.75)

# Video 1: Public, Published
repo.add_video({
    "channel": channel, "title": "Public Video", "description": "...", "duration_seconds": 60,
    "video_type_id": "standard", "status": "published", "visibility": "public", "video_link": "v/1"
})
# Video 2: Private, Uploaded
repo.add_video({
    "channel": channel, "title": "Private Video", "description": "...", "duration_seconds": 60,
    "video_type_id": "short", "status": "uploaded", "visibility": "private", "video_link": "v/2"
})

# Test 1: Tüm Videolar
print("\n--- [TEST 1] Tüm Videoları Listele ---")
print(controller.list_all_videos())
sleep(0.75)

# Test 2: Status Filtresi Testi
print("\n--- [TEST 2] Sadece 'published' Olanlar ---")
res_status = controller.list_videos_by_status("published")
print(res_status)
sleep(0.75)

if "Public Video" in res_status and "Private Video" not in res_status:
    print("BAŞARILI: Status filtresi doğru çalışıyor.")
else:
    print("HATA: Yanlış filtreleme.")
sleep(0.75)

# Test 3: Visibility Filtresi Testi
print("\n--- [TEST 3] Sadece 'private' Olanlar ---")
res_vis = controller.list_videos_by_visibility("private")
print(res_vis)
sleep(0.75)

if "Private Video" in res_vis and "Public Video" not in res_vis:
    print("BAŞARILI: Visibility filtresi doğru çalışıyor.")
else:
    print("HATA: Yanlış filtreleme.")
sleep(0.75)

print("\n--- TEST BİTTİ ---")