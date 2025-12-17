from datetime import datetime
from utils.exceptions.base_errors import DekSystemError
"""
Kanal oluşum hataları
"""
#Kullanıcı kanal limit kontrolü hatası
class ChannelLimitExceededError(DekSystemError):
    def __init__(self,username):
        self.error_code = 1001 
        self.timestamp = datetime.now() 
        message=f"HATA! '{username}' adlı kullanıcıya ait bir kanal zaten var!"
        super().__init__(message)
#Geçersiz isim hatası
class InvalidNameError(DekSystemError):
    def __init__(self, channel_name, min_length):
        self.error_code = 1002 
        self.timestamp = datetime.now() 
        message=f"HATA! '{channel_name}' ismi geçersiz. En az {min_length} uzunluğunda bir isim giriniz!"
        super().__init__(message)
#Geçersiz kanal türü hatası
class InvalidChannelTypeError(DekSystemError):
    def __init__(self,channel_type):
        self.error_code = 1003 
        self.timestamp = datetime.now() 
        message=f"HATA! '{channel_type}' geçersiz! Lütfen geçerli bir kanal türü giriniz!"
        super().__init__(message)
"""
Varlık ve arama hataları
"""
#Kanal bulunamadı hatası
class ChannelNotFoundError(DekSystemError):
    def __init__(self, channel_id=None, channel_name=None):
        self.error_code = 2001 
        self.timestamp = datetime.now()
        # Varsayılan mesaj
        message = "HATA! Aranan kriterlere uygun bir kanal bulunamadı!"
        #ID ye göre yapılan aramada çıkacak olan hata
        if channel_id is not None:
            message = f"HATA! '{channel_id}' ID'sine sahip bir kanal bulunamadı!"
        #İsme göre yapılacak aramada çıkacak olan hata
        elif channel_name is not None:
            message = f"HATA! '{channel_name}' isminde bir kanal bulunamadı!"
        super().__init__(message)
#Kanal zaten var hatası
class ChannelAlreadyExistError(DekSystemError):
    def __init__(self, channel_name):
        self.error_code = 2002 
        self.timestamp = datetime.now() 
        message=f"HATA! '{channel_name}' adında bir kanal zaten var!"
        super().__init__(message)
"""
Sahiplik ve limit hataları
"""
#Kanal sahibi kontrolü hatası
class NotChannelOwnerError(DekSystemError):
    def __init__(self, username,channel_name):
        self.error_code = 3001 
        self.timestamp = datetime.now() 
        message=f"HATA! Sayın '{username}', {channel_name} isimli kanala erişim hakkınız yok!"
        super().__init__(message)
#Kanal yükleme limiti hatası
class ChannelUploadLimitError(DekSystemError):
    def __init__(self,channel_name,upload_limit):
        self.error_code = 3002 
        self.timestamp = datetime.now() 
        message=f"HATA! '{channel_name}' adlı kanal yükleme limitine ulaşmıştır! Yükleme Limiti={upload_limit}"
        super().__init__(message)