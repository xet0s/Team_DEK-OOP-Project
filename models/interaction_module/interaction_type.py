from .interaction_base import InteractionModel
from abc import ABC, abstractmethod

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
            self.model.status = 'deleted'
            self.model.content = "Unliked"
            self.model.save()
            return "Beğenme Durumu: Beğeni Geri Alındı "
        
        else:
            # Beğenme (Like)
            self.model.status = "active"
            self.model.content = "Liked"
            self.model.save()
            return "Beğenme Durumu: Video Beğenildi "

class SubscriptionInteraction(InteractionBase):
    def __init__(self, model):
        super().__init__(model)

    def interaction_status(self):
        # Zaten abone ise (active), çıkış yap (deleted).
        # Değilse, abone ol (active).
        
        if self.model.status == 'active':
            # Abonelikten Çıkma
            self.model.status = 'deleted'
            self.model.content = "Unsubscribed"
            self.model.save()
            return "Abonelik Durumu: Abonelikten Çıkıldı "
            
        else:
            # Abone Olma
            self.model.status = 'active'
            self.model.content = "Subscribed"
            self.model.save()
            return "Abonelik Durumu: Kanala Abone Olundu "


def get_interaction_logic(model):
    """
    Veritabanından gelen modelin türüne (interaction_type) bakar
    ve uygun sınıfı (Comment, Like veya Subscription) başlatıp geri döndürecek.
    """
    if model.interaction_type == 'like':
        return LikeInteraction(model)
    elif model.interaction_type == 'subscription':
        return SubscriptionInteraction(model)
    else:
        # Varsayılan olarak Yorum gibi davran
        return CommentInteraction(model)

