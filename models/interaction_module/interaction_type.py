from .interaction_base import InteractionModel
from abc import ABC, abstractmethod
import random

class InteractionBase(ABC):
    def __init__(self,model):
        self.model=model

    @abstractmethod    
    def interaction_status(self):    
        pass

class CommentInteraction(InteractionBase): #yorum kısmını veri tabanına kaydeder
    def __init__(self, model):
        super().__init__(model)

    def interaction_status(self):
        #1. durum güncelle
        self.model.status="active"

        #2. içerik kontrolü(boşsa hata vermesin)
        if not self.model.content:
            self.model.content=""

        #3. kaydet
        self.model.save()       

        #4.durum mesajı döndür
        #Yorumun başını alıp önizleme yapıyor
        preview = self.model.content[:20] + "..." if len(self.model.content) > 20 else self.model.content
        return f"Yorum Durumu: Paylaşıldı ({preview})"
        
class LikeInteraction(InteractionBase): #beğenme kısmı
    def __init__(self, model):
        super().__init__(model)

    def interaction_status(self):
        #  Eğer zaten beğenmişse (active), beğeniyi geri al (deleted).
        # Değilse, beğen (active).
        
        if self.model.status == 'active':
            # Beğeniyi Geri Alma (Unlike)
            self.model.status = 'deactive'
            self.model.content = "Unliked"
            self.model.save()
            return "Beğenme Durumu: Beğeni Geri Alındı "
        
        else:
            # Beğenme (Like)
            self.model.status = "active"
            self.model.content = "Liked"
            self.model.save()
            return "Beğenme Durumu: Video Beğenildi "
        
#DİSLİKE 
class DislikeInteraction(InteractionBase):
    def __init__(self, model):
        super().__init__(model)      

    def interaction_status(self):
        #Eğer dislike atıldıysa(active),dislike geri al.
        # Değilse,dislike(active).

        if self.model.status=="active":
            #dislike geri alma
            self.model.status="deactive"
            self.model.content="Undislike"
            self.model.save()
            return "Beğenmeme Durumu:Dislike geri alındı"   

        else:
            #Dislike
            self.model.status="active"
            self.model.content="disliked"
            self.model.save()
            return "Beğenmeme Durumu:Video beğenilmedi"       
        

#ABONE OLMA
class SubscriptionInteraction(InteractionBase):
    def __init__(self, model):
        super().__init__(model)

    def interaction_status(self):
        # Zaten abone ise (active), çıkış yap (deleted).
        # Değilse, abone ol (active).
        
        if self.model.status == 'active':
            # Abonelikten Çıkma
            self.model.status = 'deactive'
            self.model.content = "Unsubscribed"
            self.model.save()
            return "Abonelik Durumu: Abonelikten Çıkıldı "
            
        else:
            # Abone Olma
            self.model.status = 'active'
            self.model.content = "Subscribed"
            self.model.save()
            return "Abonelik Durumu: Kanala Abone Olundu "
        
#PAYLAŞMA (share)
class ShareInteraction(InteractionBase):
    """Video paylaşımı yapar"""  

    def __init__(self, model):
        super().__init__(model)

    def interaction_status(self):
        #Paylaşma işlemi kaydedilir kullanıcıya link verir

        self.model.status="active" #paylaşma geri alınama ondan dolayı hep aktif.
        video_id=self.model.video.id
        fake_link=f"https://dek.video/v/{video_id}?s={random.randint(1000,9999)}"
        self.model.content = f"Shared Link: {fake_link}"

        self.model.save()
        return f"Paylaşım başarılı: Link panoya kopyalandı ({fake_link})"

#KAYDETME(SAVE)
class SaveInteraction(InteractionBase):
    """Videoyu daha sonra izle işlemini yapar"""  

    def __init__(self, model):
        super().__init__(model)

    def interaction_status(self):
        #Zaten kayededilyse (active), kaydetmeyi sil(deleted).
        # Daha önce kaydedilmediyse kaydet

        if self.model.status=="active":
            #Kaydı sil
           self.model.status="deactive"
           self.model.content=""     
           self.model.save()
           return "Kaydetme Durumu: Video kaydedilenlerden kaldırıldı"

        else:
            #Kaydetme
            self.model.status="active"
            self.model.content=""
            self.model.save()      
            return "Kaydetme Durumu:Video daha sonra izle listesine kaydedildi"


def get_interaction_logic(model):
    """
    Veritabanından gelen modelin türüne (interaction_type) bakar
    ve uygun sınıfı (Comment, Like veya Subscription,Dislike,Share) başlatıp geri döndürecek.
    """

    interaction_type=model.interaction_type
    if model.interaction_type == 'like':
        return LikeInteraction(model)
    elif model.interaction_type == 'subscription':
        return SubscriptionInteraction(model)
    elif interaction_type == 'dislike':     
        return DislikeInteraction(model)
    elif interaction_type == 'share':       
        return ShareInteraction(model)
    elif interaction_type == 'save':        
        return SaveInteraction(model)
    else:
        # Varsayılan olarak Yorum gibi davran
        return CommentInteraction(model)

