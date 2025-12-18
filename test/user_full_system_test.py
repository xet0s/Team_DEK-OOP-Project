import sys
import os

# Mevcut dosyanın yolunu al, bir üst klasöre (parent directory) çık ve onu Python yoluna ekle
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import random
import string
import time
from controllers.user_controller import UserControl
from models.accounts_module.user_base import UserModel

# --- YARDIMCI ARAÇLAR ---
def get_random_string(length=6):
    """Rastgele harf ve rakam üretir."""
    chars = string.ascii_lowercase + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def run_comprehensive_test(number_of_users=5):
    print("==================================================")
    print(f"🚀 OTOMATİK SİSTEM TESTİ BAŞLIYOR ({number_of_users} Kullanıcı)")
    print("==================================================\n")

    # 1. Veritabanı Hazırlığı
    UserModel.create_table(safe=True)
    controller = UserControl()
    
    success_count = 0
    fail_count = 0

    for i in range(1, number_of_users + 1):
        print(f"\n--- [SENARYO {i}] ---")
        
        # A) RASTGELE KİMLİK OLUŞTURMA
        base_name = get_random_string(5)
        username = f"user_{base_name}"
        password = get_random_string(10)
        email = f"{base_name}@test.com"
        
        # %30 İhtimalle Admin, %70 İhtimalle Standart Üye olsun
        is_admin_scenario = random.random() < 0.3
        
        # B) KAYIT AŞAMASI (CREATE)
        print(f"1. Kayıt Deneniyor... ({'Admin' if is_admin_scenario else 'Standart'})")
        
        if is_admin_scenario:
            create_result = controller.create_admin_user(
                username, password, email, "DekMasterKey2025"
            )
        else:
            create_result = controller.create_user(
                username, password, email
            )

        # Tuple Çözümleme (Success, Message)
        is_created, create_msg = create_result
        
        if not is_created:
            print(f"❌ KAYIT HATASI: {create_msg}")
            fail_count += 1
            continue # Sonraki tura geç
        
        print(f"   ✅ Kayıt Başarılı: {username}")

        # C) GİRİŞ AŞAMASI (LOGIN)
        print("2. Giriş Yapılıyor...")
        login_result = controller.login_user(username, password)
        
        # Tuple Çözümleme (UserObject, Message)
        active_user, login_msg = login_result

        if active_user is None:
            print(f"❌ GİRİŞ HATASI: Kullanıcı oluşturuldu ama giriş yapılamadı!")
            print(f"   Detay: {login_msg}")
            fail_count += 1
            continue

        print(f"   ✅ Giriş Başarılı. Algılanan Sınıf: {type(active_user).__name__}")

        # D) DOĞRULAMA AŞAMASI (VERIFICATION)
        print("3. Yetki Kontrolü (Polimorfizm)...")
        
        has_access = active_user.has_admin_access()
        can_upload = active_user.upload_video()

        # Mantık Testi
        logic_error = False
        
        if is_admin_scenario:
            # Senaryo Admindi, yetki True olmalı
            if has_access and can_upload:
                print("   ✅ DOĞRULANDI: Admin yetkileri tam.")
            else:
                print("   ❌ MANTIK HATASI: Admin ama yetkileri eksik!")
                logic_error = True
        else:
            # Senaryo Standarttı, admin yetkisi False olmalı
            if not has_access and can_upload:
                print("   ✅ DOĞRULANDI: Standart üye kısıtlamaları doğru.")
            elif has_access:
                print("   ❌ MANTIK HATASI: Standart üye Admin paneline girebiliyor!")
                logic_error = True

        if logic_error:
            fail_count += 1
        else:
            success_count += 1
            print("   ✨ BU SENARYO KUSURSUZ TAMAMLANDI.")

        # Hızlı akmasın, gözle takip edelim
        time.sleep(0.5)

    # --- RAPOR ---
    print("\n" + "="*50)
    print(f"📊 TEST SONUCU RAPORU")
    print("="*50)
    print(f"Toplam Senaryo : {number_of_users}")
    print(f"✅ Başarılı    : {success_count}")
    print(f"❌ Başarısız   : {fail_count}")
    print("="*50)

if __name__ == "__main__":
    # Kaç kullanıcı ile test etmek istersen parantez içine yaz
    run_comprehensive_test(5)