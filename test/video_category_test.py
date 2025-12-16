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

# Veritabanını Hazırla
db.connect()
db.drop_tables([User, ChannelModel, VideoModel])
db.create_tables([User, ChannelModel, VideoModel])

print("--- KATEGORİ, ETİKET VE AÇIKLAMA TESTİ ---")
print("-" * 50)
sleep(0.75)

#Kullanıcıları ve Kanalı Oluştur, Controlleri Başlat
user = User.create(username="TestKullanıcı",
                    email="gamer@test.com",
                    password_hash="123",
                    role="Standard")

channel = ChannelModel.create(channel_owner=user,
                            channel_name="Test Kanalı",
                            channel_category="Gaming",
                            channel_type="Personal",
                            channel_status="active",
                            channel_upload_limit=10,
                            channel_link="dek.channel/test")
controller = VideoController()

# Test 1: Gaming Kategorisi Testi
print("\n--- [TEST 1] Gaming Kategorisi ---")
video1 = controller.create_video(
        current_user=user,
        channel_id=channel.id,
        video_title="Oyun İncelemesi",
        video_description="Bu bir oyun incelemesi videosudur.",
        video_duration=600,
        video_type_input="Standard",
        video_category_input="Gaming"
        )
print(video1)
sleep(0.75)

v1 = VideoModel.get_or_none(VideoModel.title == "Oyun İncelemesi")
is_tag_ok = "#game" in v1.tags
is_desc_ok = "Oyun videoları" in v1.description

if is_tag_ok and is_desc_ok:
    print("BAŞARILI: Gaming kategorisi için etiket ve açıklama doğru.")
    print(f"Açıklama: {v1.description}")
else:
    print("HATA: Gaming kategorisi için etiket veya açıklama yanlış.")
sleep(0.75)

#Test 2: Education Kategorisi Testi
print("\n--- [TEST 2] Education Kategorisi ---")
video2 = controller.create_video(
        current_user=user,
        channel_id=channel.id,
        video_title="Eğitim Videom",
        video_description="Bu bir eğitim videosudur.",
        video_duration=800,
        video_type_input="Standard",
        video_category_input="Education"
        )
print(video2)
sleep(0.75)

v2 = VideoModel.get_or_none(VideoModel.title == "Eğitim Videom")

if "#learn" in v2.tags and "Eğitim videoları" in v2.description:
    print("BAŞARILI: Education kategorisi için etiket ve açıklama doğru.")
    print(f"Açıklama: {v2.description}")
else:
    print("HATA: Education kategorisi için etiket veya açıklama yanlış.")
sleep(0.75)

print("\n--- TEST BİTTİ ---")