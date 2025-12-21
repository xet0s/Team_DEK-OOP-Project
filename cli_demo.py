#Sistemi içe aktarır
import sys
import os
import random
from time import sleep
from peewee import DoesNotExist
#Sistem yolunu tanımlar
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))
#Veritabanını içe aktarır
from models.database import db
#Modulleri içe aktarır
from models.accounts_module.user import User
from models.accounts_module.channel_base import ChannelModel
from models.content_module.video_base import VideoModel
from models.interaction_module.interaction_base import InteractionModel
from models.interaction_module.playlist_base import PlaylistModel
#Playlist sistemini içe aktarır
from models.interaction_module.playlist_item import PlaylistItemModel as PlaylistLinkTable
#Kontrol sistemini içe aktarır
from controllers.video_controller import VideoController
from controllers.channel_controller import ChannelController
from controllers.user_controller import UserControl
from controllers.interaction_controller import InteractionController
from controllers.playlist_controller import PlaylistController
from controllers.admin_controller import AdminController
#Repository sistemini içe atkarır
from models.repositories.channel_repository import ChannelRepository
#Veritabanı bağlantısı yapar
def setup_system():
    print("Sistem başlatılıyor...")
    sleep(0.5)
    print("Veritabanı hazırlanıyor")
    sleep(0.5)
    try:
        db.create_tables([User,ChannelModel,VideoModel,InteractionModel,PlaylistModel,PlaylistLinkTable])
    except:
        pass
    print("Veritabanı hazır")
    sleep(0.2)
#Header kısmını tekrar tekrar elle yazmak yerine fonksiyon olarak alıyoruz
def print_header(text):
    print("\n"+"="*40)
    print(f"{text}")
    print("="*40)
#Girdi alınan yerlerde ayırt edicilik olsun diye ekstra fonksiyon oluşturuyoruz
def get_input(text):
    return input(f">> {text}")
#Giriş menüsü
def auth_menu():
    auth=UserControl()
    while True:
        print_header("Giriş Ekranı")
        print("1. Giriş Yap")
        print("2. Kayıt Ol")
        print("3. Misafir Olarak Giriş Yap")
        print("q. Çıkış yap")
        select=get_input("Seçiminizi giriniz : ")
        #Giriş yapma sistemi
        if select=="1":
            username=get_input("Kullanıcı adı : ")
            password=get_input("Şifre : ")
            try:
                query=auth.login_user(username,password)
                if isinstance(query,tuple) and len(query)==2:
                    user,msg=query
                elif user is not None:
                    user=query
                    msg=f"Hoşgeldiniz {user.username}"
                else:
                    user=None
                    msg="Hatalı giriş"
                if user:
                    print(msg)
                    return user
                else:
                    print(f"{msg}")
                    
            except Exception as e:
                print(f"Beklendemik bir hata oluştu {str(e)}")
                sleep(0.5)
        #Kayıt olma sistemi
        elif select=="2":
            print_header("Kayıt Türü Seçimi")
            print("1. Standart Hesap")
            print("2. Admin hesap")
            r_type= get_input("Hesap Türü : ")
            if r_type in ["1","2"]:
                print("\nÜyelik bilgileri")
                username=get_input("Kullanıcı adı : ")
                email=get_input("E-mail : ")
                while True:
                    password=get_input("Şifre : ")
                    if len(password)<8:
                        print("Şifre en az 8 karakter olmalı!")
                        continue
                    if r_type=="1":
                        succes,msg= auth.create_user(username,password,email)
                        print(msg)
                        sleep(0.5)
                    elif r_type=="2":
                        code=get_input("Master Key : ")
                        succes,msg =auth.create_admin_user(username,password,email,code)
                        print(msg)
                        sleep(0.5)
                    if succes:
                        break
            else:
                print("Hatalı seçim türü!")
                sleep(1)
        #Misafir giriş sistemi
        elif select== "3":
            print("\nMisafir girişi hazırlanıyor...")
            sleep(0.5)
            try:
                guest_user,msg= auth.guest_login()
                print(msg)
                sleep(1)
                return guest_user
            except Exception as e:
                print(f"Hata : {str(e)}")
        elif select.lower()=="q":
            print("Çıkış yapılıyor...")
            sleep(0.75)
            sys.exit()
        else:
            print("Geçersiz seçim")
#Kanal işlemleri menüsü
def channel_menu(current_user):
    controller=ChannelController()
    repo=ChannelRepository()
    user_model=current_user.data
    while True:
        print_header(f"KANAL İŞLEMLERİ | Kullanıcı: {current_user.data.username}")
        #Varolan kanalı çeker
        my_channel = repo.get_channel_by_owner(user_model.id)
        #Kanal varlığını sorgular
        has_channel = (my_channel is not None)
        #Menü
        if not has_channel:
            print("1. Yeni Kanal Oluştur")
        else:
            print("1. [KİLİTLİ] Yeni Kanal Oluştur (Zaten kanalınız var)")
            print("2. Kanalımı Görüntüle")
            print("3. Kanal Bilgilerini Güncelle")
            print("4. Kanalımı Sil")
        print("q. Geri Dön")
        choice=get_input("Seçiminizi giriniz : ")
        #Kanal oluşumu
        if choice=="1":
            if has_channel:
                print("Zaten kanalınız var! Yeni kanal açmak için mevcut olanı silmelisiniz!")
                sleep(1.5)
                continue
            print("\n---Kanal Oluşturma Sihirbazı---")
            c_name=get_input("Kanal adı (En az 3 harf) giriniz: ")
            c_cat=get_input("Kategori (Eğitim,oyun,vlog...) giriniz : ")
            print("\nKanal Türleri [Personal,Brand,Kid,Music,Education,Advertising]")
            c_type=get_input("Kanal türü giriniz : ").capitalize()
            c_info=get_input("Kanal Hakkında (Opsiyonel) : ")
            print("İşlem Yapılıyor ...")
            sleep(0.5)
            success,msg= controller.create_channel(user_model,c_name,c_cat,c_type,c_info)
            print(msg)
            sleep(1)
        #Kanal detay
        elif choice=="2":
            if not has_channel:
                print("\n HATA! Bir kanalınız yok")
            else:
                print_header(f"KANAL DETAYLARI: {my_channel.channel_name}")
                print(f"ID       : {my_channel.id}")
                print(f"Kategori : {my_channel.channel_category}")
                print(f"Tür      : {my_channel.channel_type}")
                print(f"Durum    : {my_channel.status}")
                print(f"Limit    : {my_channel.channel_upload_limit} Video")
                print(f"Link     : {my_channel.channel_link}")
                print(f"Hakkında : {my_channel.channel_info}")
                print("-" * 40)
                input("Devam etmek için Enter'a basınız...")
        #Kanal güncelleme
        elif choice=="3":
            if not has_channel:
                print("\n HATA! Bir kanalınız yok")
            else:
                print("---Güncelleme Seçenekleri---")
                print(f"Mevcut isim : {my_channel.channel_name}")
                #güncellenecek isim ve hakkında kısmı
                new_name=get_input("Yeni isim giriniz (Değişmeyecekseniz Enter'a basınız) : ")
                new_info=get_input("Yeni hakkımda yazısı giriniz (Değişmeyecekseniz Enter'a basınız) : ")
                #Girdi sorgusu
                name_to_send=new_name if new_name.strip() != "" else None
                info_to_send=new_info if new_info.strip() != "" else None
                #Veri güncelleme
                if name_to_send or info_to_send:
                    success,msg = controller.update_existing_channel(
                        channel_id=my_channel.id,
                        current_user=user_model,
                        updated_channel_name=name_to_send,
                        updated_info=info_to_send
                    )
                    print(msg)
                    sleep(0.5)
                else:
                    print("Değişiklik yapılmadı.")
                    sleep(0.5)
        #Kanal silme
        elif choice=="4":
            if not has_channel:
                print("\n HATA! Bir kanalınız yok")
            else:
                #Onay
                confirm=get_input(f"'{my_channel.channel_name}' kanalını silmek istediğinize emin misiniz ?(e/h) : ")
                if confirm.lower()=="e":
                    success,msg=controller.delete_existing_channel(my_channel.id,user_model)
                    print(msg)
                    sleep(0.5)
                else:
                    print("İşlem iptal edildi")
                    sleep(0.5)
        #Çıkış
        elif choice=="q":
            print("Çıkış yapılıyor . . . ")
            break
        #Hatalı giriş sorgusu
        else:
            print("Geçersiz işlem")
            sleep(0.3)

def video_menu(current_user):
    video_controller=VideoController()
    interaction_controller=InteractionController()
    channel_repo=ChannelRepository()
    playlist_controller=PlaylistController()
    user_model=current_user.data
    user_role=user_model.role
    while True:
        total_views = VideoModel.get_total_view_count()
        print_header(f"DEK VİDEO PLATFORMU | Kullanıcı : {user_model.username}")
        print(f"Platform Geneli Toplam Görüntülenme Sayısı : {total_views}")
        print("-"*40)
        sleep(0.3)
        print("1. Videoları Listele")
        print("2. Video İzle (ID ile)")

        if user_role !="Guest":
            my_channel=channel_repo.get_channel_by_owner(user_model.id)
            if my_channel:
                print("3. Video Yükle")
                print("4. Videoları Yönet")
                print("5. Playlist İşlemleri")
            else:
                print("Vide yükleme ve yönetme işlemleri için kanal açmalısınız . ")
                sleep(0.5)
        print("q. Geri Dön")

        choice=get_input("Seçiminizi giriniz : ")

        if choice=="1":
            print("\n--- 📜 LİSTELEME SEÇENEKLERİ ---")
            print("1. Tüm Videoları Listele")
            print("2. Son Yüklenenler (Tarihe Göre)")
            print("3. Duruma Göre Filtrele (Published/Deleted)")
            print("4. Görünürlüğe Göre Filtrele (Public/Private)")
            print("0. İptal")

            sub_choice=get_input("Seçiminizi giriniz : ")
            sleep(0.3)

            if sub_choice=="1":
                print("\n"+video_controller.list_all_videos())
            elif sub_choice=="2":
                print("\n"+ video_controller.list_recent_videos())
            elif sub_choice=="3":
                status_input= get_input("Aranacak Durumu giriniz (published, deleted) : ")
                print("\n"+ video_controller.list_videos_by_status(status_input))
            elif sub_choice=="4":
                visibility_input=get_input("Görünürülük durumu giriniz (Public,Private) : ")
                print("\n"+video_controller.list_videos_by_visibility(visibility_input))
            elif sub_choice=="0":
                pass
            else:
                print("Geçersiz işlem.")
        
        elif choice=="2":
            vid_id=get_input("İzlemek istediğiniz videonun ID'sini giriniz : ")
            sleep(0.5)
            if  vid_id.isdigit():
                vid_id=int(vid_id)
                try:
                    video_obj=video_controller.repo.get_video_by_id(vid_id)
                    if not video_obj:
                        print("Video Bulunamadı")
                        sleep(0.5)
                        continue
                    msg=video_controller.watch_video(vid_id, user_role, user_model.id)
                    print(msg)
                    while True:
                        print("\n--- ETKİLEŞİM MENÜSÜ ---")
                        print("1. Beğen / Beğeni Geri Çek")
                        print("2. Yorum Yap")
                        print("3. Yorumları Oku")
                        print("4. Videoyu Paylaş")
                        print("q. Videodan Çık")
                        action=get_input("İşlem Seçiniz : ")
                        
                        if action=="1":
                            if user_role=="Guest":
                                print("Misafir girişteyken etkileşimde bulunamazsınız.")
                            else:
                                l_msg=interaction_controller.toggle_like(current_user.data,video_obj)
                                print(f"\n>> {l_msg}")
                        elif action=="2":
                            if user_role=="Guest":
                                print("Misafir girişteyken etkileşimde bulunamazsınız.")
                            else:
                                comment_text=get_input("Yorumunuzu yazınız : ")
                                c_msg=interaction_controller.add_comment(current_user.data,video_obj,comment_text)
                                print(f"\n>> {c_msg}")
                        elif action=="3":
                            comments=interaction_controller.get_video_comment(vid_id)
                            if comments:
                                print("--- Video Yorumları ---")
                                for c in comments:
                                    print(c)
                                    print("-" * 30)
                            else:
                                print("Yorum bulunamadı")
                        elif action=="4":
                            share_msg = interaction_controller.share_video(current_user.data, video_obj)
                            print(f"\n>> {share_msg}")
                        elif action=="q":
                            print("Videodan çıkılıyor . . . ")
                            sleep(1)
                            break
                        else:
                            print("Geçersiz seçim")
                    
                except Exception as e:
                    print(f"HATA! Modül arızası : {e}")
                sleep(1)
                input("Devam . . .")
            else:
                print("Geçersiz ID ")
                sleep(1)
        
        elif choice=="3":
            if user_role=="Guest" or not my_channel:
                print("Yetkisiz erişim")
            else:
                print("\n--- Video Yükleme ---")
                title =get_input("Başlık    : ")
                desc = get_input("Açıklama  : ")
                tags = get_input("Etiketler : ")
                print("Kategoriler: [Gaming, Education, Music, Technology, Sports]")
                
                cat_input = get_input("Kategori: ")
                if not cat_input: cat_input = "General"

                print("Türler: [Standard, Short, LiveStream]")
                type_input = get_input("Video Türü: ").capitalize()
                if not type_input: type_input = "Standard"

                print("Görünürlük Durumu: [Public, Private]")
                visibility_input = get_input("Görünürlük: ").capitalize()

                duration_sim = random.randint(60, 600)

                print("Video işleniyor...")
                sleep(0.5)
                # Rastgele içerik simülasyonu
                content=f"vid_{random.randint(100,999)}.mp4"
                msg = video_controller.create_video(
                    current_user=user_model,
                    channel_id=my_channel.id,
                    video_title=title,
                    video_description=desc,
                    video_duration=duration_sim,
                    video_type_input=type_input,
                    video_category_input=cat_input,
                    video_visibility_input=visibility_input
                    )
                print(msg)
                sleep(1)

        elif choice=="4":
            if not my_channel:
                print("Yetkisiz.")
            else:
                success,videos=video_controller.get_channel_videos(my_channel.id)
                if videos:
                    print(f"\n{my_channel.channel_name} Videoları:")
                    for v in videos: 
                        # Modelindeki alan adı 'title' mı 'video_title' mı kontrol et
                        t = getattr(v, 'title', getattr(v, 'video_title', 'Başlıksız'))
                        print(f"ID: {v.id} | {t}")
                    d_id = get_input("Silinecek ID (İptal: q): ")
                    if d_id.isdigit():
                        st, mg = video_controller.delete_existing_video(int(d_id), user_model)
                        print(mg)
                    else:
                        print("Videonuz yok.")
                sleep(1.5)
        elif choice=="5":
            if user_role=="Guest":
                print("Misafir kullanıcı erişimine kapalı")
                sleep(1)
                continue
            while True:
                print("\n--- PLAYLIST MENÜSÜ ---")
                print("1. Yeni Playlist Oluştur")
                print("2. Playlistlerimi Listele")
                print("3. Playlist İçeriğini Gör (Detay)")
                print("4. Playlist Sil")
                print("5. Videolarımı Playliste Ekle")
                print("0. Video Menüsüne Dön")
                playlist_c=get_input("İşlem seçiniz : ")

                if playlist_c=="1":
                    p_title=get_input("Playlist ismi giriniz : ")
                    p_public=get_input("Herkese açık olarak listelensin mi? (e/h): ")
                    msg = playlist_controller.create_playlist(user_model,p_title,p_public)
                    print(msg)
                elif playlist_c == "2":
                    print(playlist_controller.list_my_playlist(user_model.id))
                elif playlist_c=="3":
                    pid=get_input("Liste ID'si giriniz : ")
                    if pid.isdigit():
                        print(playlist_controller.get_playlist_details(int(pid)))
                        print("-"*30)
                        print(playlist_controller.show_playlist_content(int(pid)))
                        sub_act = get_input("Video silmek ister misiniz? (ID girin veya Enter basıp geçin): ")
                        if sub_act.isdigit():
                            res = playlist_controller.remove_video(user_model, int(pid), int(sub_act))
                            print(res)
                    else:
                        print("Geçersiz ID.")
                elif playlist_c=="4":
                    pid = get_input("Silinecek Playlist ID: ")
                    if pid.isdigit():
                        res = playlist_controller.delete_playlist(user_model, int(pid))
                        print(res)
                    else:
                        print("Geçersiz ID.")
                elif playlist_c=="5":
                    if not my_channel:
                        print("Kanalınız olmadığı için liste oluşturamazsınız!")
                    else:
                        print("\n---1. Adım---\n---Playlist Seçme---")
                        print(playlist_controller.list_my_playlist(user_model.id))
                        target_pid= get_input("Video ekleyeceğiniz playlisti seçiniz : ")

                        if not target_pid.isdigit():
                            print("Geçersiz ID!")
                            continue

                        print("\n---2. Adım---\n---Video Seçme---")
                        s, my_videos = video_controller.get_channel_videos(my_channel.id)
                        if not s or not my_videos:
                            print("Kanalınızda video yok!")
                        else:
                            for v in my_videos:
                                t=getattr(v,"title",getattr(v,"video_title","Başlıksız"))
                                print(f"ID: {v.id} | {t}")
                            target_vid = get_input("Hangi Video ID?: ")
                            if target_vid.isdigit():
                                print("Ekleniyor . . .")
                                sleep(0.3)
                                result = playlist_controller.add_video(user_model, int(target_pid), int(target_vid))
                                print(f"\n>> {result}")
                            else:
                                print("Geçersiz ID")
                elif playlist_c=="0":
                    break
                else:
                    print("Geçersiz seçim")
        elif choice.lower() == "q":
            print("Sistem kapatılıyor . . .")
            sleep(1)
            break
        else:
            print("Geçersiz seçim.")
def admin_menu(current_user):
    """Admin kullanıcılar için yönetim menüsü"""
    admin_controller = AdminController()
    
    # Güvenlik Kontrolü (Çift dikiş)
    if not admin_controller.check_admin_access(current_user):
        print("!!! GÜVENLİK İHLALİ: BURAYA ERİŞİM YETKİNİZ YOK !!!")
        return

    while True:
        print_header(f"ADMİN PANELİ | Yönetici: {current_user.data.username}")
        print("1. Sistem İstatistikleri (Dashboard)")
        print("2. Kullanıcı Listesi ve Yasaklama")
        print("3. Tüm Videoları Yönet (Zorla Silme)")
        print("q. Ana Menüye Dön")
        
        choice = get_input("Yönetim İşlemi: ")
        
        # --- [1] DASHBOARD ---
        if choice == "1":
            stats = admin_controller.get_system_stats()
            print("\n--- SİSTEM RAPORU ---")
            if "error" in stats:
                print(f"Veri alınamadı: {stats['error']}")
            else:
                print(f"Toplam Üye   : {stats.get('users', 0)}")
                print(f"Toplam Video : {stats.get('videos', 0)}")
                print(f"Sistem Durumu: {stats.get('status', 'OK')}")
            input("\nDevam etmek için Enter...")

        elif choice == "2":
            print("\n--- KAYITLI KULLANICILAR ---")
            users = admin_controller.list_all_users()
            for u in users:
                print(f"ID: {u.id} | {u.username} | Rol: {u.role} | Email: {u.email}")
            
            act = get_input("Yasaklamak (Silmek) istediğiniz ID (İptal: Enter): ")
            if act.isdigit():
                if int(act) == current_user.data.id:
                    print("Kendinizi silemezsiniz!")
                else:
                    confirm = get_input(f"{act} ID'li kullanıcı silinecek. Emin misin? (evet/hayır): ")
                    if confirm.lower() == "evet":
                        success, msg = admin_controller.ban_user(int(act))
                        print(f">> {msg}")
            sleep(1)
        elif choice == "3":
            vc = VideoController()
            
            print("\n--- PLATFORMDAKİ TÜM VİDEOLAR ---")
            print(vc.list_all_videos())
            
            v_id = get_input("Kaldırılacak (Sansürlenecek) Video ID (İptal: Enter): ")
            if v_id.isdigit():
                reason = get_input("Silme Sebebi (Log için): ")
                success, msg = admin_controller.delete_harmful_video(int(v_id))
                print(f">> {msg} (Sebep: {reason})")
            sleep(1.5)

        elif choice.lower() == "q":
            break
        else:
            print("Geçersiz işlem.")
def main_menu(active_user):
    """Kullanıcı rolüne göre menüleri yönlendiren ana fonksiyon"""
    user_role = active_user.data.role

    while True:
        print_header(f"ANA MENÜ | Hoşgeldin {active_user.data.username} ({user_role})")
        
        # --- GUEST MENÜSÜ ---
        if user_role == "Guest":
            print("1. Video Dünyası (İzle/Keşfet)")
            print("q. Çıkış Yap")
            
            choice = get_input("Seçim: ")
            if choice == "1":
                video_menu(active_user)
            elif choice.lower() == "q":
                break
        
        # --- STANDARD & ADMIN MENÜSÜ ---
        else:
            print("1. Kanal İşlemleri")
            print("2. Video İşlemleri")
            if user_role == "Admin":
                print("3. Admin Paneli")
            print("q. Oturumu Kapat")
            
            choice = get_input("Seçim: ")
            
            if choice == "1":
                channel_menu(active_user)
            elif choice == "2":
                video_menu(active_user)
            elif choice == "3":
                if user_role == "Admin":
                    admin_menu(active_user)
                else:
                    print("Yetkisiz alan!")
            elif choice.lower() == "q":
                break
            else:
                print("Geçersiz seçim.")

# --- PROGRAM BAŞLANGICI ---
if __name__ == "__main__":
    setup_system()
    
    # 1. Giriş Yap
    active_session_user = auth_menu()
    
    # 2. Giriş başarılıysa Ana Menüye git
    if active_session_user:
        main_menu(active_session_user)
    print("Sistem kapatılıyor . . .")
    sleep(1.5)
    print("Program sonlandı. Güle güle!")