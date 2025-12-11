import datetime
from peewee import Model,DateTimeField
from models.database import db

class BaseModel(Model): #tÜM MODELLERİN MİRAS ALACAĞI ANA SINIF YAPISI
    
    created_at=DateTimeField(default=datetime.datetime.now)
    update_at=DateTimeField(default=datetime.datetime.now)
    
    def save(self,*args,**kwargs):
        self.update_at=datetime.datetime.now()
        return super(BaseModel,self).save(*args,**kwargs)
    
    class Meta:
        database=db

        

