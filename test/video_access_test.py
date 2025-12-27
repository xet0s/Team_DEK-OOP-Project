import sys
import os
from time import sleep

# Proje ana dizinini Python yoluna ekle
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.database import db
from models.accounts_module.user import User
from models.accounts_module.channel_base import ChannelModel
from models.interaction_module.interaction_base import InteractionModel
from models.content_module.video_base import VideoModel
from controllers.video_controller import VideoController

# Veritabanını Hazırla
db.connect()
try:
    from models.interaction_module.playlist_item import PlaylistItemModel
    from models.interaction_module.playlist_base import PlaylistModel
    db.drop_tables([PlaylistItemModel, PlaylistModel, InteractionModel, VideoModel, ChannelModel, User], safe=True)
except Exception:
    pass
db.create_tables([User, ChannelModel, VideoModel, InteractionModel])

print("--- VİDEO MODÜLÜ GÜVENLİK VE ROL TESTİ ---")
print("-"*50)

# Kullanıcıları ve Controller'ı Oluştur
print("\n>> Aktörler Oluşturuluyor...")      # 1. Standart (Video Sahibi)
owner = User.create(username="GaribanKoylu",
                    email="owner@test.com",
                    password_hash="123",
                    role="Standard")

guest = User.create(username="MerakliMisafir",  # 2. Guest (Yetkisiz Misafir)
                    email="guest@test.com",
                    password_hash="123",
                    role="Guest")

admin = User.create(username="YoneticiBey",     # 3. Admin (Süper Yetkili)
                    email="admin@test.com",
                    password_hash="123",
                    role="Admin")
controller = VideoController()

channel = ChannelModel.create(
    channel_owner=owner, channel_name="Koy Meydani", channel_category="Vlog", 
    channel_type="Personal", channel_status="active", channel_upload_limit=10, channel_link="vlog/koy"
)
sleep(0.75)

# Video Oluştur (Test Edilecek Olan)
print("\n>> Test için bir video oluşturuluyor...")
controller.create_video(
    current_user=owner, 
    channel_id=channel.id, 
    video_title="Hasat Zamani", 
    video_description="Bugdaylar toplandi", 
    video_duration=300, 
    video_type_input="Standard",
    video_category_input="Vlog",
    video_visibility_input="Public"
)
target_video = VideoModel.select().first()
print(f"✅ Hazırlık Tamam: Video ID {target_video.id} (Sahibi: {owner.username}) oluşturuldu.")
sleep(0.75)

# Test 1: Guest Video Yüklemeye Çalışıyor
print("\n--- [SENARYO 1] Guest Kullanıcı Video Yüklemeye Çalışıyor ---")
res_guest_upload = controller.create_video(
    current_user=guest,
    channel_id=channel.id,
    video_title="Hacker Video",
    video_description="...",
    video_duration=10,
    video_type_input="Short",
    video_category_input="Education",
    video_visibility_input="Private"
)
sleep(0.75)

if "yetkiniz bulunmamaktadır" in str(res_guest_upload):
    print("BAŞARILI: Guest engellendi.")
else:
    print(f"GÜVENLİK AÇIĞI: Guest video yükledi! -> {res_guest_upload}")
sleep(0.75)


# Test 2: Guest Başkasının Videosunu Silmeye Çalışıyor
print("\n--- [SENARYO 2] Guest Kullanıcı Videoyu Silmeye Çalışıyor ---")
res_guest_del = controller.delete_existing_video(target_video.id, guest)

if "yetkiniz yoktur" in str(res_guest_del):
    print("BAŞARILI: Guest silme işlemi engellendi.")
else:
    print(f"GÜVENLİK AÇIĞI: Guest videoyu sildi! -> {res_guest_del}")
sleep(0.75)


# Test 3: Guest Başkasının Videosunu Güncellemeye Çalışıyor
print("\n--- [SENARYO 3] Guest Kullanıcı Videoyu Güncellemeye Çalışıyor ---")
res_guest_upd = controller.update_existing_video(target_video.id, guest, new_title="HACKED")

if "yetkiniz yoktur" in str(res_guest_upd):
    print("BAŞARILI: Guest güncelleme işlemi engellendi.")
else:
    print(f"GÜVENLİK AÇIĞI: Guest videoyu güncelledi! -> {res_guest_upd}")
sleep(0.75)


# Test 4: Admin Başkasının Videosunu Silmeye Çalışıyor
print("\n--- [SENARYO 4] Admin Kullanıcı (Sahibi Değil) Videoyu Silmeye Çalışıyor ---")
res_admin_del = controller.delete_existing_video(target_video.id, admin)
check_video = VideoModel.get_or_none(VideoModel.id == target_video.id)

if check_video is None:
    print(f"BAŞARILI: Admin yetkisini kullandı ve videoyu sildi. (Mesaj: {res_admin_del})")
else:
    print(f"HATA: Admin videoyu silemedi! Yetki kontrolünü kontrol et. (Mesaj: {res_admin_del})")
sleep(0.75)

print("\n--- TEST BİTTİ ---")