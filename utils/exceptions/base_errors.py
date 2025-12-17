from datetime import datetime

class DekSystemError(Exception):
    def __init__(self,message="Sistemde bilinmeyen bir hata oluştu ... "):
        self.error_code=00
        self.timestamp=datetime.now()
        self.message=message
        super().__init__(self.message)
#Masterkey hatası
class MasterKeyError(DekSystemError):
    def __init__(self):
        self.error_code = 100 
        self.timestamp = datetime.now()
        message = "HATA! Geçersiz Master Key!"
        super().__init__(message)