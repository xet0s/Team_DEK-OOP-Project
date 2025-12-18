import os
import sys
import unittest

current_dir= os.path.dirname(os.path.abspath(__file__))
root_dir=os.path.dirname(current_dir)
sys.path.append(root_dir)

import random
from time import sleep
from peewee import SqliteDatabase, IntegrityError
from models.accounts_module.user import User
from models.accounts_module.channel_base import ChannelModel
from controllers.channel_controller import ChannelController

test_db=SqliteDatabase(":memory:")

class AccountModuleMasterTest:
    """
    Hesap modulleri kapsamlı entegrasyon testi
    """
    #Gerekli veriler
    #Başlangıç değeri olarak boş bırakıldı (None)
    def __init__(self):
        self.controller=None
        self.owner_user=None
        self.hacker_user=None
        self.test_channel_id=None
    #Test için ayrı bir veritabanı kurar
    def setup_database(self):
        """
        Geçici test veritabanı oluşumu
        """
        print()
        print("="*50+"\n---[KURULUM]--- \n---Veritabanı Hazırlanıyo---\n"+"="*50)
        sleep(0.5)
        test_db.bind([User,ChannelModel],bind_refs=False,bind_backrefs= False)
        test_db.connect()
        test_db.create_tables([User,ChannelModel])
        #ChannelController modulünü çeker
        self.controller=ChannelController()
        #Kullanıcı oluşum
        try:
            self.owner_user=User.create(
                username="MasterAdmin",
                email="admin@dek.com",
                password_hash="secret123",
                role="admin"
            )
            self.hacker_user=User.create(
                username="HackerUser",
                email="hacker@dek.com",
                password_hash="123secret",
                role="Standard"
            )
        except Exception as e:
            print(f"Veritabanı kurulum hatası: {str(e)}")
    #TEST1
    def test_user_scenario(self):
        """
        Kullanıcı oluşumu ve benzersizlik testleri yapan kısım
        """
        print()
        print("="*50+"\n---[TEST-1] Kullanıcı Senaryoları---\n"+"="*50)
        sleep(0.5)
        print("Senaryo: Aynı kullanıcı adıyla kayıt testi (Duplicate)")
        sleep(0.3)
        try:
            User.create(username="MasterAdmin",email="123456@dek.com",password_hash="000")
            print("SİSTEM HATASI")
        except IntegrityError:
            print("Senanryo başarılı, 'unique constrain' hatası fırlattı. Koruma çalışıyor.\n")
        except Exception as e:
            print(f"Beklenmedik hata : {e}")
        sleep(1)
    #TEST2
    def test_channel_polymorphism(self):
        """ Farklı kanal türlerinin limitlerini test eder """
        print()
        print("="*50+"\n---[TEST-2] Kanal Oluşturma ve Polimorfizm testi---\n"+"="*50)
        sleep(0.5)
        #Test edilecek kanal türleri
        type_to_test=[
            ("Personal",5),
            ("Brand",1000),
            ("Kid",2),
            ("Music",10),
            ("Education",50),
            ("Advertising",100)
        ]
        for ch_type,expected_limit in type_to_test:
            random_id=random.randint(1000,9999)
            temp_username= f"User_{ch_type}_{random_id}"
            temp_email= f"{ch_type}_{random_id}@dek.com"
            try:
                temp_owner = User.create(
                    username=temp_username,
                    email=temp_email,
                    password_hash="temp123",
                    role="standard"
                )
                print(f"\n👤 Geçici Kullanıcı Oluşturuldu: {temp_username}\n")
                
            except Exception as e:
                print(f"❌ Kullanıcı oluşturma hatası: {e}\n")
                continue 
            
            ch_name= f"Kanal_{ch_type}_{random_id}"
            print(f"Senaryo: '{ch_type}' türünde kanal açılıyor...\n")
            sleep(0.3)
            #Kanal oluşumu
            self.controller.create_channel(
                channel_owner=temp_owner,
                channel_name=ch_name,
                channel_category="Test",
                channel_type=ch_type
            )
            #Limit kontrol testi
            try:
                saved_channel=ChannelModel.get(ChannelModel.channel_name==ch_name)
                if ch_type=="Personal":
                    self.test_channel_id=saved_channel.id
                if saved_channel.channel_upload_limit==expected_limit:
                    print(f"BAŞARILI! {ch_type} yükleme limiti doğru atandı. Yükleme limiti : {expected_limit}\n")
                    sleep(0.3)
                else:
                    print(f"HATA! {ch_type} yükleme limiti doğru atanamadı . Yükleme limiti\n Beklenen: {expected_limit}\n Gelen : {saved_channel.channel_upload_limit}\n\n")
                    sleep(0.3)
            except Exception as e :
                print(f"Veritabanı hatası : {e}\n")
            sleep(0.5)
    #TEST3
    def test_update_security(self):
        """ Kanal güncelleme işlemlerinde yetki limiti testi (Güvenlik Kontrolü)"""
        print()
        print("="*50+"\n---[TEST-3] Kanal Güncelleme Güvenlik testi---\n"+"="*50)
        sleep(0.5)
        #Kanal varlık sorgusu
        if not self.test_channel_id:
            print("\nÖnceki test başarısız olduğu için bu test atlanıyor.\n")
            return
        print("\nSenaryo: Yetkisiz kullanıcı (Hacker) isim değiştirmeye çalışıyor...\n")
        try:
            self.controller.update_existing_channel(
                channel_id=self.test_channel_id,
                current_user=self.hacker_user,
                updated_channel_name="Hacked Channel"
            )
            print("\nHATA: Hacker güncellemeyi başardı! (Sistem hata fırlatmadı)\n")
        except Exception as e:
            print(f"✅ BAŞARILI: Sistem yetkisiz işlemi engelledi. Yakalanan Mesaj: '{e}'\n")
        print("\nSenaryo: Yetkili kullanıcı (Sahip) isim değiştirmeye çalışıyor...\n")
        try:
            new_name = "Resmi Güncel Kanal"
            self.controller.update_existing_channel(
                channel_id=self.test_channel_id,
                current_user=self.owner_user,
                updated_channel_name=new_name
            )
            
            # Veritabanından teyit et
            channel = ChannelModel.get_by_id(self.test_channel_id)
            if channel.channel_name == new_name:
                print(f"\nBAŞARILI: İsim veritabanında başarıyla değişti.\n")
            else:
                print("\nHATA: İşlem hatasız bitti ama veritabanında isim değişmedi!\n")
        except Exception as e:
            print(f"\nHATA: Sahip işlem yaparken hata aldı! Detay: {e}\n")
    #Test4
    def test_delete_and_search(self):
        """Arama, Silme ve Silinmiş veriye erişim testleri."""
        print()
        print("="*50+"\n---[TEST 4] Arama ve Silme---\n"+"="*50)
        sleep(0.5)
        print("\nSenaryo: Kategoriye göre arama yapılıyor...\n")
        #Kanal arama testi
        try:   
            if hasattr(self.controller, 'search_channels'):
                found, msg = self.controller.search_channels("category", "Test")
                if found:
                    print("\nArama Sonucu: {len(msg)} karakter veri döndü.\n")
                else:
                    print("\nController'da 'search_channels' metodu yok, geçiliyor.\n")
            else:
                print("\nUYARI: 'search_channels' metodu Controller'da bulunamadı. Bu adım atlanıyor.\n")
        except Exception as e:
            print(f"\nArama testi sırasında hata: {e}\n")
        #Yetkisiz silme testi
        print("\nSenaryo: Hacker kanalı silmeye çalışıyor...\n")
        res = self.controller.delete_existing_channel(self.test_channel_id, self.hacker_user)
        if "yetki" in res.lower() or "değilsiniz" in res.lower():
            print("\nBAŞARILI: Silme engellendi.")
        else:
            print(f"\nHATA: Hacker silmeyi başardı! Mesaj: {res}")
        #Yetkili silme testi
        print("\nSenaryo: Sahibi kanalı siliyor...\n")
        res = self.controller.delete_existing_channel(self.test_channel_id, self.owner_user)
        #Varlık kontrolü
        try:
            ChannelModel.get_by_id(self.test_channel_id)
            print("\nHATA: 'Silindi' denmesine rağmen kanal hala veritabanında!\n")
        except:
            print(f"\nBAŞARILI: Kanal veritabanından uçuruldu. Mesaj: {res}")
    #Sistemi çalıştıran komut
    def run_all(self):
        """Tüm testleri birbirinden bağımsız çalıştırır."""
        # 1. Veritabanı Kurulumu (Bu patlarsa diğerleri çalışamaz, o yüzden try dışında kalabilir veya en başta kontrol edilir)
        try:
            self.setup_database()
        except Exception as e:
            print(f"KURULUM HATASI: Veritabanı oluşturulamadı. Test iptal. Detay: {e}")
            return
        # --- TEST 1 ---
        try:
            self.test_user_scenario()
        except Exception as e:
            print(f"TEST 1 PATLADI: {e}")
        # --- TEST 2 ---
        try:
            self.test_channel_polymorphism()
        except Exception as e:
            print(f"TEST 2 PATLADI: {e}")
        # --- TEST 3 ---
        try:
            self.test_update_security()
        except Exception as e:
            print(f"TEST 3 PATLADI: {e}")
        # --- TEST 4 ---
        try:
            self.test_delete_and_search()
        except Exception as e:
            print(f"TEST 4 PATLADI: {e}")
        print("\n--- TEST SÜRECİ TAMAMLANDI ---")
        # Temizlik
        test_db.close()
# --- ÇALIŞTIRMA BLOĞU ---
if __name__ == "__main__":
    tester = AccountModuleMasterTest()
    tester.run_all()