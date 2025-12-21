
from models.repositories.interaction_repository import InteractionRepository
from models.interaction_module.interaction_type import get_interaction_logic
from models.interaction_module.interaction_base import InteractionModel

from models.repositories.interaction_repository import InteractionRepository     # Veritabanı işlerini yapan 'Depocu' 
from models.interaction_module.interaction_type import get_interaction_logic     #etkileşim modulunü getirir
from models.interaction_module.interaction_base import InteractionModel          #etkileşim türleri


class InteractionController:
    """Kullanıcı etkileşimlerini (beğeni,yorum,kaydetme,abonelik,vb) töntemlerin kontrolünü sağlar"""

    def __init__(self):
        #Veritabanı için repository başlatılıyor
        self.repo=InteractionRepository()

    @staticmethod
    def validate_comment(comment_text):
        """Yorum içeriğini kontrol eder."""
        #eğer yorum yoksa veya sadece boşluksa False döndürür
        if not comment_text or comment_text.strip() == "":
            return False
        return True

    #YORUM EKLEME

    def add_comment(self,user,video,comment_text):  #Videoya yeni yorum ekler

        #Yorum içeriği boş olup olmadığına bak
        if not InteractionController.validate_comment(comment_text):
            return "Hata:Yorum içeriği boş olamaz"
    
        #Veritabanına kaydedilecek yorum
        data={
            "user":user,                                          #yorumu yapan kişi
            "video":video,                                        #yorum yapılan video
            "interaction_type":InteractionModel.TYPE_COMMENT,     #türü
            "content": comment_text,                              #yorumun kendisi
            "status": "active",                                   #durum
            }

        #Repositorye kaydediyor    
        saved_interaction = self.repo.add_interaction(data)  

        #Kayıt başarılıysa kullanıcıya bilgi mesajı ver
        if saved_interaction:
            # Refactor: Property kullanımı
            return saved_interaction.status_text
        else:
            return "Hata:Yorum kaydedilemedi"

    #Yorumları getirme
    def get_video_comment(self,video_id):
        """Videonun yorumlarını liste halinde getrecek"""

        interactions = self.repo.get_comments_by_video(video_id)
        results = []     
        #eğer yorum yoksa bilgi ver
        if not interactions:
            return ["Henüz yorum yapılmamış."] 
    
        for interaction in interactions:
                try:
                    
                    username=interaction.user.username
                    
                    content=interaction.content
                    formatted_comment = f"👤 {username}: {content}"
                    results.append(formatted_comment)
                except AttributeError:
                # Eğer bir veri eksikse programı durdurma, atla
                    results.append("⚠️ (Hatalı yorum verisi)")
                    continue
        return results

    #Beğenme 
    def toggle_like(self,user,video):
        """Beğeni butonuna basıldığında çalışacak 
        beğeni varsa siler yoksa beğenecek  """
        #Kullanıcı daha önce beğenmiş mi diye bakıcak
        existing_interaction = self.repo.find_interaction(
                        user.id, 
                        video.id, 
                        InteractionModel.TYPE_LIKE  # Sadece 'like' olanlara bak
                        )    
        #Daha önce beğenildiyse
        if existing_interaction:
            logic=get_interaction_logic(existing_interaction)   #Kaydı getir
            return logic.interaction_status()                   #active->deleted mesajını döndür
     
        #eğer kayıt yoksa(ilk defa beğeniliyorsa)
        else:
            data={
                "user":user,
                "video":video,
                "interaction_type":InteractionModel.TYPE_LIKE,
                "content":"Liked"
                }
            #Veritabanına kaydet
            new_interaction=self.repo.add_interaction(data)
            #Beğendi mesajını döndür
            logic = get_interaction_logic(new_interaction)
            return logic.interaction_status()
     
    #Dislike
    def toggle_dislike(self,user,video):
        #Dislike butonuna basınca çalışır
        #Kullanıcı daha önce dislike atmış mı
        existing_interaction = self.repo.find_interaction(
                user.id, 
                video.id, 
                InteractionModel.TYPE_DISLIKE # Tür: Dislike
                )    
        #Dislike varsa geri al.
        if existing_interaction:
            logic=get_interaction_logic(existing_interaction)
            return logic.interaction_status() #dislike geri alındı 
        #Yoksa dislike at
        else:
                data = {
                    "user": user,
                    "video": video,
                    "interaction_type": InteractionModel.TYPE_DISLIKE,
                    "content": "Disliked"
                }
                new_interaction = self.repo.add_interaction(data)
            
                logic = get_interaction_logic(new_interaction)
                return logic.interaction_status() # Dislike döner.
     
    #Abone olma 
    def toggle_subscription(self, user, video):
        #Abone ol butonuna basınca çalışır
        #Daha önce abone olmuş mu
        existing_interaction = self.repo.find_interaction(
                user.id, 
                video.id, 
                InteractionModel.TYPE_SUBSCRIPTION
            )
        #Zaten aboneyse,abonelikten çık
        if existing_interaction:
            logic = get_interaction_logic(existing_interaction)
            return logic.interaction_status() # Abonelikten çıkıldı
        #Abone değilse abone olur
        else:
                data = {
                    "user": user,
                    "video": video,
                    "interaction_type": InteractionModel.TYPE_SUBSCRIPTION,
                    "content": "Subscribed"
                }
                new_interaction = self.repo.add_interaction(data)
            
                logic = get_interaction_logic(new_interaction)
                return logic.interaction_status() # Abone olundu yazar

    #Kaydetme işlemi
    def toggle_save(self,user,video):
        #Daha sonra izle butonuna basınca çalışır
        #video daha önce kaydedilmiş mi?
        existing_interaction = self.repo.find_interaction(
                user.id, 
                video.id, 
                InteractionModel.TYPE_SAVE
            )
        #Kayıtlı ise listeden çıkar
        if existing_interaction:
                logic = get_interaction_logic(existing_interaction)
                return logic.interaction_status()
        #Kayıtlı değilse kaydet
        else:
                data = {
                    "user": user,
                    "video": video,
                    "interaction_type": InteractionModel.TYPE_SAVE,
                    "content": "Saved"
                }
                new_interaction = self.repo.add_interaction(data)
            
                logic = get_interaction_logic(new_interaction)
                return logic.interaction_status()

    #Paylaşma işlemi
    def share_video(self,user,video,platform_name="Social Media"):
        #Paylaşma butonuna basınca çalışır
        data = {
                "user": user,
                "video": video,
                "interaction_type": InteractionModel.TYPE_SHARE,
                "content": platform_name # Örn: "Twitter", "WhatsApp"
            }
        #yeni kayıt oluşturcak
        saved = self.repo.add_interaction(data)
        if saved:
            # Refactor: Property kullanımı
            return saved.status_text # Link kopyalandı mesajı 
        else:
                return "Hata: Paylaşım gerçekleştirilemedi."  

    #istatislikler
    def get_like_count(self, video_id):
            #Videonun toplam beğeni sayısını Repository'e saydırır
            return self.repo.count_interactions(video_id, InteractionModel.TYPE_LIKE)
    
    def get_dislike_count(self, video_id):
            #Videonun toplam dislike sayısını Repository'e saydırır
            return self.repo.count_interactions(video_id, InteractionModel.TYPE_DISLIKE)  

    def get_comment_count(self, video_id):
            #Videonun altına yapılan toplam yorum sayısını getirir.
            return self.repo.count_interactions(video_id, InteractionModel.TYPE_COMMENT)  

    def get_share_count(self, video_id):
            #Videonun kaç kez paylaşıldığını gösterir
            return self.repo.count_interactions(video_id, InteractionModel.TYPE_SHARE)

    def get_save_count(self, video_id):
            #Videonun kaç kişinin daha sonra izle listesinde olduğunu gösterir
            return self.repo.count_interactions(video_id, InteractionModel.TYPE_SAVE) 