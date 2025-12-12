from models.base_model import BaseModel
import datetime
from peewee import CharField,DateTimeField
class User(BaseModel):
    #unique=True -->Benzersiz değişken
    #null=False  -->Boş bırakılamz değişken

    username=CharField(unique=True,null=False)  
    email=CharField(unique=True,null=False)     
    password_hash=CharField(null=False)                   
    
    joined_at=DateTimeField(default=datetime.datetime.now)
    class Meta:  #SQL için Tablo ismi oluşturur
        table_name="users"