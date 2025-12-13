from peewee import *
from models.base_model import BaseModel 
import datetime


class LikeInteractionBase(BaseModel): 
    user = ForeignKeyField('models.user_model.User', backref='likes') #kimin beğendiği
    video = ForeignKeyField('models.video_model.Video', backref='likes') #hangi videoyu beğendi
    interaction_type = CharField(default='like') 
    status = CharField(default='active') #beğeni geçerli mi
    timestamp = DateTimeField(default=datetime.datetime.now)

    class Meta:
        table_name = 'like_interactions'   
        # veritabanına her kullanıcı için bir beğeni düşsün fazlası düşmesin 
        
        indexes = (
            (('user', 'video'), True),
                  )

from models.interactions import LikeInteraction  
from peewee import fn

class LikeController:

    @staticmethod
    def Toggle_like(user_id,video_id):
        """Bu metod eğer beğeni varsa bir kez daha basıldığında beğeniyi silecek beğeni yoksa da beğenecek """

        mevcut_durum=  LikeInteraction.get_or_none(
                   (LikeInteraction.user == user_id) & 
                   (LikeInteraction.video == video_id))
    
        son_durum=False

        if mevcut_durum:
            #Önceden beğenilmişse
            if mevcut_durum.status=="active":
                #Daha önceden beğenilmiş->Beğeniyi sil
                mevcut_durum.status="deleted" 
                son_durum=False

            else:
             #daha önce beğenilmemiş ilk defa basılıyor ->Beğenilmiş olacak
                mevcut_durum.status="active"
                son_durum=True

            mevcut_durum.save() #son durum kaydedilecek

        else:
            #Eğer beğeni tuşuna ilk kez basılıyorsa
            LikeInteraction.create(user=user_id,
                               video=video_id,
                               status='active',
                               interaction_type='like' )
            
        mevcut_durum=True
        
        #yukardaki işlemlerde ne yapıldıysa yapılsın sadece active olanları say diğerlerini sil
        total_durum = LikeInteraction.select().where(
            (LikeInteraction.video == video_id) & 
            (LikeInteraction.status == 'active')  ).count()

        return mevcut_durum,total_durum     
    

    