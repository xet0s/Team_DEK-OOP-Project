from peewee import *
from models.base_model import BaseModel # Veya InteractionBase'in olduğu yer
import datetime

# Eğer InteractionBase zaten tanımlıysa ondan miras al
class LikeInteraction(BaseModel): 
    user = ForeignKeyField('models.user_model.User', backref='likes') # User modelinin yolunu string verdim (Circular Import önlemi)
    video = ForeignKeyField('models.video_model.Video', backref='likes')
    interaction_type = CharField(default='like') # [cite: 130]
    status = CharField(default='active') # active, deleted (Soft Delete için)
    timestamp = DateTimeField(default=datetime.datetime.now)

    class Meta:
        table_name = 'like_interactions'
        # AYNI KULLANICI AYNI VİDEOYU SADECE 1 KEZ BEĞENEBİLİR 
        indexes = (
            (('user', 'video'), True),
                  )