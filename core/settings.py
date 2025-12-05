import os 

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) #Ana kök dizin konumu

DB_NAME="DEK.db"                        #Veritabanı ismi
DB_PATH=os.path.join(BASE_DIR,DB_NAME)  #Veritabanı yolu

#Çözünürlük
WINDOW_WIDTH=1366
WINDOW_HEIGHT=768

#Uygulama adı
APP_NAME="DEK Video Platformu"

