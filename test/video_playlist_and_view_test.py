import sys
import os
from time import sleep

# Proje ana dizinini Python yoluna ekle
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.database import db
from models.accounts_module.user import User
from models.accounts_module.channel_base import ChannelModel
from models.content_module.video_base import VideoModel
from models.interaction_module.interaction_base import InteractionModel
from controllers.video_controller import VideoController
from models.repositories.interaction_reporsitory import InteractionRepository

# Veritabanını Hazırla
db.connect()
db.drop_tables([User, ChannelModel, VideoModel, InteractionModel])
db.create_tables([User, ChannelModel, VideoModel, InteractionModel])

print("--- VİDEO PLAYLIST VE GÖRÜNTÜLEME TESTİ ---")
print("-" * 50)

# Kullanıcı ve Kanal Oluştur, Controller ve Repository Başlat
print(">> Test kullanıcısı oluşturuluyor.")
user = User.create(
    username="TestKullanici", 
    email="test@example.com",
    password_hash="123",
    role="Standard"
    )
sleep(0.75)
print(">> Test kanalı oluşturuluyor.")
channel = ChannelModel.create(
    channel_owner=user,
    channel_name="Test Kanal",
    channel_category="General",
    channel_type="Standard",
    channel_status="active",
    channel_upload_limit=5,
    channel_link="dek.channel/testkanal"
    )
print(f"✅ Kanal Hazır: {channel.channel_name} (Limit: {channel.channel_upload_limit})")
sleep(0.75)
video_controller = VideoController()
interaction_repo = InteractionRepository()

# Video listesi Oluşturma
print(">> Test videoları oluşturuluyor.")
video_controller.create_video(
    current_user=user,
    channel_id=channel.id,
    video_title="Test Video 1",
    video_description="Açıklama 1",
    video_duration=100,
    video_type_input="Standard",
    video_category_input="General"
    )
video_controller.create_video(
    current_user=user,
    channel_id=channel.id,
    video_title="Test Video 2",
    video_description="Açıklama 2",
    video_duration=200,
    video_type_input="Standard",
    video_category_input="General"
    )
video_controller.create_video(
    current_user=user,
    channel_id=channel.id,
    video_title="Test Video 3",
    video_description="Açıklama 3",
    video_duration=300,
    video_type_input="Standard",
    video_category_input="General"
    )
video_1 = VideoModel.get(VideoModel.title == "Test Video 1")
video_2 = VideoModel.get(VideoModel.title == "Test Video 2")
video_3 = VideoModel.get(VideoModel.title == "Test Video 3")
sleep(0.75)
print(">> Videolar oluşturuldu ve kanala eklendi.")

# Test 1: İzlenme Sayısı Testi
print("\n--- [TEST 1] Video İzlenme Sayısı ---")
video_controller.watch_video(video_1.id)
video_controller.watch_video(video_1.id)
video_controller.watch_video(video_1.id)
video_1_guncel = VideoModel.get_by_id(video_1.id)
if video_1_guncel.view_count == 3:
    print(">> BAŞARILI: İzlenme sayısı doğru!")
else:
    print(">> HATA: İzlenme sayısı yanlış!")
sleep(0.75)

# Test 2: Playlist Testi
print("\n--- [TEST 2] Video Playlist Oluşturma ---")
InteractionModel.create(user=user, video=video_1, interaction_type="like", status="active")
InteractionModel.create(user=user, video=video_3, interaction_type="like", status="active")
user_likes = InteractionModel.select().where(
    (InteractionModel.user == user) &
    (InteractionModel.interaction_type == "like") &
    (InteractionModel.status == "active"))

video_id_list = [interaction.video.id for interaction in user_likes]
print(f">> Kullanıcının beğendiği videoların ID'leri: {video_id_list}")

playlist_output = video_controller.list_playlist_videos(video_id_list)
print(">> Playlist Videoları:")
print (playlist_output)
sleep(0.75)

if "Test Video 1" in str(playlist_output) and "Test Video 3" in str(playlist_output) and "Test Video 2" not in str(playlist_output):
    print(">> BAŞARILI: Playlist doğru oluşturuldu!")
else:
    print(">> HATA: Playlist yanlış oluşturuldu!")
sleep(0.75)