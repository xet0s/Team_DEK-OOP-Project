from datetime import datetime
from utils.exceptions.base_errors import DekSystemError
"""
Kullanıcı yazım hataları
"""
#Kullanıcı adı uzunluk hatası
class UsernameLengthError(DekSystemError):
    def __init__(self, input_username,min_length):
        self.error_code = 101 
        self.timestamp = datetime.now() 
        message=f"HATA! {input_username} çok kısa. En az {min_length} uzunluğunda olmalı!"
        super().__init__(message)
#Kullanıcı adı Geçersiz Karakter hatası
class InvalidUsernameError(DekSystemError):
    def __init__(self, input_username):
        self.error_code = 102  
        self.timestamp = datetime.now() 
        message=f"HATA! Kullanıcı adı geçersiz karakter içeriyor!"
        super().__init__(message)
"""
Şifre yazım hataları
"""
#Zayıf şifre hatası
class WeakPasswordError(DekSystemError):
    def __init__(self):
        self.error_code = 201  
        self.timestamp = datetime.now() 
        message="HATA! Şifre güvenliği yetersiz! En az 8 karakter olmalı!"
        super().__init__(message)
"""
E-posta hataları
"""
#Geçersiz e-posta hatası
class InvalidEmailError(DekSystemError):
    def __init__(self, input_email):
        self.error_code = 202  
        self.timestamp = datetime.now() 
        message= f"HATA! {input_email} geçerli değil. Geçerli bir e-posta formatı giriniz"
        super().__init__(message)
"""
Veritabanı çakışma hataları
"""
#Varolan kullanıcı hatası
class UserAlreadyExistError(DekSystemError):
    def __init__(self, input_username):
        self.error_code = 301  
        self.timestamp = datetime.now() 
        message= f"HATA! '{input_username}' adlı bir kullanıcı bulunmakta!"
        super().__init__(message)
#Varolan e-posta hatası
class EmailAlreadyExistError(DekSystemError):
    def __init__(self,input_email):
        self.error_code = 302  
        self.timestamp = datetime.now() 
        message= f"HATA! '{input_email}' halihazırda sisteme kayıtlı! Lütfen farklı bir e-posta giriniz!"
        super().__init__(message)
"""
Giriş ve Kimlik hatası
"""
#Geçersiz kullanıcı hatası
class UserNotFoundError(DekSystemError):
    def __init__(self, input_username):
        self.error_code = 401  
        self.timestamp = datetime.now() 
        message=f"HATA! '{input_username}' adında bir kullanıcı bulunamadı!"
        super().__init__(message)
#Geçersiz şifre hatası
class IncorrectPasswordError(DekSystemError):
    def __init__(self):
        self.error_code = 402  
        self.timestamp = datetime.now() 
        message="HATA! Girilen şifre hatalı! Tekrar deneyin!"
        super().__init__(message)
"""
Yetki ve rol hatası
"""
#Yetkisiz giriş hatası
class AdminPrivilegeRequiredError(DekSystemError):
    def __init__(self, username):
        self.error_code = 501  
        self.timestamp = datetime.now() 
        message=f"HATA! Sayın {username} Bu alan sadece Admin kullanıcılar erişim sağlayabilir"
        super().__init__(message)
#Yetkisiz modul kullanım hatası
class UnauthorizedActionError(DekSystemError):
    def __init__(self):
        self.error_code = 502  
        self.timestamp = datetime.now() 
        message="HATA! Bu işlemi yapmak için gerekli erişime sahip değilsin"
        super().__init__(message)