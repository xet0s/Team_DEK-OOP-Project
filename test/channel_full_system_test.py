import sys
import os

# Mevcut dosyanın yolunu al, bir üst klasöre (parent directory) çık ve onu Python yoluna ekle
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import random
import string
import time

# --- MODÜL IMPORTLARI ---
# Dosya yollarının projene uygun olduğundan emin ol
try:
    from models.accounts_module.user_base import UserModel
    from models.accounts_module.channel_base import ChannelModel # Model adın farklıysa düzelt
    from controllers.user_controller import UserControl
    from controllers.channel_controller import ChannelController # Sınıf adını kontrol et
except ImportError as e:
    print(f"❌ IMPORT HATASI: {e}")
    print("Lütfen dosya yollarını ve sınıf isimlerini kontrol et.")
    exit()

# --- YARDIMCI ARAÇLAR ---
def get_random_string(length=6):
    chars = string.ascii_lowercase + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def get_random_channel_type():
    # Projendeki geçerli kanal tipleri
    types = ["Personal", "Brand", "Kid", "Game", "Vlog"] 
    # Senin projende sadece 'Free' ve 'Paid' varsa burayı ona göre güncelle:
    # return random.choice(["Free", "Paid"])
    return random.choice(types)

def run_full_simulation(user_count=5):
    print("==================================================")
    print(f"🌍 GENEL SİSTEM SİMÜLASYONU ({user_count} Kişi)")
    print("==================================================\n")

    # 1. TEMİZLİK VE HAZIRLIK
    UserModel.create_table(safe=True)
    ChannelModel.create_table(safe=True)
    
    user_ctrl = UserControl()
    channel_ctrl = ChannelController()

    success_ops = 0
    fail_ops = 0

    for i in range(1, user_count + 1):
        print(f"\n--- [SENARYO {i}] ---")
        
        # -------------------------------------------------
        # ADIM 1: RASTGELE KULLANICI OLUŞTURMA
        # -------------------------------------------------
        base_name = get_random_string(5)
        username = f"user_{base_name}"
        password = get_random_string(9)
        email = f"{base_name}@test.com"

        print(f"1. Kullanıcı Kaydı: {username}")
        # Tuple döndüğünü varsayıyoruz: (True, "Mesaj")
        u_res, u_msg = user_ctrl.create_user(username, password, email)

        if not u_res:
            print(f"   ❌ KAYIT BAŞARISIZ: {u_msg}")
            fail_ops += 1
            continue # Kullanıcı yoksa kanal da açamaz, sonraki tura geç

        # -------------------------------------------------
        # ADIM 2: GİRİŞ YAPMA (Nesneyi Almak İçin)
        # -------------------------------------------------
        # Login fonksiyonun (UserWrapper, Mesaj) veya (User, Mesaj) dönüyor
        login_obj, l_msg = user_ctrl.login_user(username, password)
        
        if not login_obj:
            print(f"   ❌ GİRİŞ BAŞARISIZ: {l_msg}")
            fail_ops += 1
            continue

        # Controller'ın yapısına göre User nesnesini ayıkla
        # Eğer wrapper kullanıyorsan .data, yoksa kendisi
        active_user = login_obj.data if hasattr(login_obj, 'data') else login_obj
        print(f"   ✅ Giriş Yapıldı (ID: {active_user.id})")

        # -------------------------------------------------
        # ADIM 3: RASTGELE KANAL OLUŞTURMA
        # -------------------------------------------------
        ch_name = f"Kanal {get_random_string(4)}"
        ch_cat = random.choice(["Eğlence", "Eğitim", "Müzik", "Oyun"])
        ch_type = get_random_channel_type()
        
        print(f"2. Kanal Açılıyor: '{ch_name}' ({ch_type})")
        
        # Controller parametrelerine dikkat! (owner, name, category, type)
        ch_res_tuple = channel_ctrl.create_channel(
            channel_owner=active_user, # Nesneyi gönderiyoruz
            channel_name=ch_name,
            channel_category=ch_cat,
            channel_type=ch_type
        )
        
        is_ch_created, ch_msg = ch_res_tuple

        if is_ch_created:
            print(f"   ✅ KANAL OLUŞTURULDU!")
            
            # -------------------------------------------------
            # ADIM 4: VERİTABANI SAĞLAMASI (Verification)
            # -------------------------------------------------
            db_channel = ChannelModel.get_or_none(ChannelModel.channel_name == ch_name)
            
            if db_channel:
                if db_channel.channel_owner.id == active_user.id:
                    print("   🔗 DB KONTROL: Kanal ve Sahibi başarıyla eşleşti.")
                    success_ops += 1
                else:
                    print("   ❌ KRİTİK HATA: Kanal sahibinde karışıklık var!")
                    fail_ops += 1
            else:
                print("   ❌ HATA: Kanal oluşturuldu dendi ama DB'de yok!")
                fail_ops += 1
        else:
            print(f"   ❌ KANAL HATASI: {ch_msg}")
            fail_ops += 1

        time.sleep(0.2) # Terminal akışını görmek için minik bekleme

    # --- RAPOR ---
    print("\n" + "="*50)
    print(f"📊 SİMÜLASYON RAPORU")
    print("="*50)
    print(f"Toplam İşlem : {user_count}")
    print(f"✅ Başarılı  : {success_ops}")
    print(f"❌ Hatalı    : {fail_ops}")
    print("="*50)

if __name__ == "__main__":
    run_full_simulation(5)