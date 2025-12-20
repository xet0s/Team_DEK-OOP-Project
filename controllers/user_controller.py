import bcrypt
from models.accounts_module.user import User
from models.accounts_module.user_type import UserBase
from models.repositories.user_repository import UserRepository
from utils.exceptions.base_errors import MasterKeyError #Master key hatası
from utils.exceptions.user_error import (
    UsernameLengthError,        #Kullancı adı uzunluk hatası
    WeakPasswordError,          #Zayıf şifre hatası
    InvalidEmailError,          #Geçersiz mail hatası
    UserNotFoundError,          #Kullanıcı bulunamadı hatası
    IncorrectPasswordError,     #Yanlış şifre hatası
)
class UserControl:
    #repository bağlantısı
    def __init__(self):
        self.repo=UserRepository()  
    def create_user(self,username,password,email):
        #Kayıt olan kullanıcının standart rolü
        role="Standard"
        #Girdi kontrolü
        if len(username)<3:
            raise UsernameLengthError(username,3)
        if len(password)<8:
            raise WeakPasswordError()
        if '@' not in email:
            raise InvalidEmailError(email)
        #Kaydedilecek kullanıcı verielri
        try:
            #Kullanıcı oluşturu
            created_user=User(username=username,email=email,role=role)
            #setter ile şifrelenmiş bir password getirir
            created_user.password=password
            created_user.save()
        except Exception as e:
            return False,f"Veritabanı hatası : {str(e)}"
        return (True,
f""" 
--------------------------------
    [✓]KULLANICI OLUŞTURULDU
--------------------------------
    Kullanıcı Adı     : {created_user.username}
    Kullanıcı ID      : {created_user.id}
    Kullanıcı e-maili : {created_user.email}
    Kullanıcı rolü    : {created_user.role}
--------------------------------
""")
    def create_admin_user(self,username,password,email,security_code):
        #Sabit Güvenlik anahtarı
        MASTER_KEY= "DekMasterKey2025"
        #Yetki sorgusu
        if security_code != MASTER_KEY:
            raise MasterKeyError()
        #Kayıt olan kullanıcının standart rolü
        role="Admin"
        #Girdi kontrolü
        if len(username)<3:
            raise UsernameLengthError(username)
        if len(password)<8:
            raise WeakPasswordError()
        if '@' not in email:
            raise InvalidEmailError(email)
        try:
            created_user.User(username=username,email=email,role=role)
            created_user.password=password
            created_user.save()
        except Exception as e:
            return (False,f"Veritabanı hatası : {str(e)}")
        #Kaydedilecek kullanıcı verielri
        user_information={
            "username":username,
            "password_hash":password,
            "email":email,
            "role":role
        }
        try:#Kontrol 2
            created_user=self.repo.add_user(user_information)
        except Exception as e:
            return (False,f"Veritabani Hatası : {str(e)}")
        return (True,
f""" 
--------------------------------------
    [✓]ADMİN KULLANICI OLUŞTURULDU
--------------------------------------
    Kullanıcı Adı     : {created_user.username}
    Kullanıcı ID      : {created_user.id}
    Kullanıcı e-maili : {created_user.email}
    Kullanıcı rolü    : {created_user.role}
------------------------------------
""")
    def login_user(self,username,password):
        query=self.repo.get_user_by_name(username)
        if query==None:
            raise UserNotFoundError(username)
        if query.check_password:
            active_user=UserBase.get_user_policy(query.role,query)
            return (active_user ,f""" 
*****************************
##########HOŞGELDİN##########
*****************************
    Kullanıcı  {active_user.data.username.upper()}! 
    Yetki    : {active_user.data.role.upper()}
*****************************
""")
        else:
            raise IncorrectPasswordError()