import sys
from PyQt6.QtWidgets import QApplication
from models.database import db
from models import create_tables
from views.main_window import MainWindow

def main():

    print("Sistem başlatılıyor ...")
    db.connect()                    #database bağlantısı
    create_tables()                 #tablo oluşumu

    app=QApplication(sys.argv)      #uygulama ataması

    window=MainWindow()             #pencere ataması
    window.show()                   #çalıştırma

    sys.exit(app.exec())            

if __name__=="__main__":
    main()