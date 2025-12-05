from PyQt6.QtWidgets import QMainWindow,QLabel,QVBoxLayout,QWidget
from core.settings import APP_NAME,WINDOW_WIDTH,WINDOW_HEIGHT

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle(APP_NAME)                       #Pencere İsmi
        self.setGeometry(100,100,WINDOW_WIDTH,WINDOW_HEIGHT)#Pencere Boyutu

        self.setup_ui()
    
    def setup_ui(self):

        #Basit karşılama mesajı
        central_widget=QWidget()
        self.setCentralWidget(central_widget)

        layout=QVBoxLayout()
        label=QLabel("Video Yönetim sistemi")

        #CSS benzeri stil
        label.setStyleSheet("font-size: 20px; font-weight: bold; color: #fffff;")

        layout.addWidget(label)
        central_widget.setLayout(layout)