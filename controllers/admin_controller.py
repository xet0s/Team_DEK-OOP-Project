# controllers/admin_controller.py

from models.repositories.user_repository import UserRepository
from models.repositories.video_repository import VideoRepository
from models.repositories.channel_repository import ChannelRepository
from models.content_module.video_base import VideoModel
from models.accounts_module.user import User
from models.accounts_module.user import User
from models.content_module.video_base import VideoModel
from models.accounts_module.channel_base import ChannelModel

class AdminController:
    def __init__(self):
        # Admin her yere erişebilir, o yüzden tüm repoları başlatıyoruz
        self.user_repo = UserRepository()
        self.video_repo = VideoRepository()
        self.channel_repo = ChannelRepository()

    def check_admin_access(self, current_user):
        """Güvenlik Kontrolü: İşlem yapan gerçekten admin mi?"""
        if current_user.data.role != "Admin":
            return False
        return True

    def get_system_stats(self):
        """Sistemin genel durumunu özetler."""
        try:
            # Peewee'de count() metodu ile sayıları alıyoruz
            total_users = User.select().count()
            total_videos = VideoModel.select().count()
            total_channel= ChannelModel.select().count()
            # ChannelModel import edilmediyse repo üzerinden de sayabiliriz ama model daha hızlıdır
            users = self.user_repo.get_all_users() # Repo'da bu metod varsa
            return {
                "users": total_users,
                "videos": total_videos,
                "channels":total_channel,
                "status": "Active"
            }
        except Exception as e:
            return {"error": str(e)}

    # --- 2. KULLANICI YÖNETİMİ ---
    def list_all_users(self):
        try:
            # User modelinden hepsini çekiyoruz
            return User.select()
        except:
            return []

    def ban_user(self, target_user_id):
        """Kullanıcıyı sistemden siler (Banlar)."""
        # Admin kendisini silememeli
        # (Bu kontrolü CLI tarafında veya burada yapabiliriz)
        try:
            user = self.user_repo.get_user_by_id(target_user_id)
            if not user:
                return False, "Kullanıcı bulunamadı."
            
            if user.role == "Admin":
                return False, "HATA: Başka bir admini silemezsiniz!"

            # Kullanıcıyı sil (Peewee delete_instance)
            user.delete_instance()
            return True, f"{user.username} sistemden uzaklaştırıldı (Banlandı)."
        except Exception as e:
            return False, f"Hata: {str(e)}"

    # --- 3. İÇERİK YÖNETİMİ ---
    def delete_harmful_video(self, video_id):
        """Zararlı videoyu sahibinden bağımsız olarak siler."""
        try:
            video = self.video_repo.get_video_by_id(video_id)
            if not video:
                return False, "Video bulunamadı."
            
            title = video.video_title
            # Repo'daki delete fonksiyonunu kullanıyoruz
            self.video_repo.delete_video(video_id)
            
            return True, f"'{title}' videosu yayından kaldırıldı (Admin Kararı)."
        except Exception as e:
            return False, f"Hata: {str(e)}" 