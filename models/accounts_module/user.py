from models.base_model import BaseModel
import datetime
from peewee import CharField,DateTimeField
try:
    import bcrypt
except ImportError:
    bcrypt=None
class User(BaseModel):
    #unique=True -->Benzersiz değişken
    #null=False  -->Boş bırakılamz değişken

    username=CharField(unique=True,null=False)  
    email=CharField(unique=True,null=False)     
    password_hash=CharField(null=False)                   
    role= CharField(default="standard",null=False)
    joined_at=DateTimeField(default=datetime.datetime.now)
    class Meta:  #SQL için Tablo ismi oluşturur
        table_name="users"

    @property
    def password(self):
        return "..."
    
    @password.setter
    def password(self,plain_password):
        if not plain_password:
            raise ValueError("Şifre boş olamaz!")
        
        if bcrypt:
            hashed=bcrypt.hashpw(plain_password.encode("utf-8"), bcrypt.gensalt())
            self.password_hash=hashed.decode("utf-8                                                         ")
        else:
            self.password_hash= f"hashed_{plain_password}"

    
    def check_password(self,plain_password):
        if bcrypt:
            try:
                return bcrypt.checkpw(plain_password.encode("utf-8"),self.password_hash.encode("utf-8"))
            except:
                return False
        else:
            return self.password_hash==f"hashed_{plain_password}"
        
    @classmethod
    def find_by_email(cls,email_address):
        return cls.get_or_none(cls.email == email_address)
    @classmethod
    def get_admins(cls):
        return cls.select().where(cls.role=="admin")
        