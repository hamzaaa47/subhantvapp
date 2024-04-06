import sys
from PySide6.QtWidgets import *
from PySide6 import QtCore, QtGui
from PySide6.QtGui import *
from PySide6.QtCore import *
import sys
 
class Clock(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        timer = QTimer(self)
        timer.timeout.connect(self.update)
        timer.start(1000)
 
        self.hPointer = QtGui.QPolygon([QPoint(3, 7),
                                        QPoint(-3, 7),
                                        QPoint(0, -50)])
        self.mPointer = QPolygon([QPoint(3, 7),
                                  QPoint(-3, 7),
                                  QPoint(0, -70)])
        self.sPointer = QPolygon([QPoint(1, 1),
                                  QPoint(-1, 1),
                                  QPoint(0, -90)])
        self.bColor = Qt.black #fcc585
        self.sColor = Qt.gray
        self.setMinimumSize(250, 250)

    def paintEvent(self, event):
        rec = min(self.width(), self.height())
        tik = QTime.currentTime()
        painter = QPainter(self)
 
        def drawPointer(color, rotation, pointer):
            painter.setBrush(QBrush(color))
            painter.save()
            painter.rotate(rotation)
            painter.drawConvexPolygon(pointer)
            painter.restore()
 
        painter.setRenderHint(QPainter.Antialiasing)
        painter.translate(self.width() / 2, self.height() / 2)
        painter.scale(rec / 300, rec / 300)
        painter.setPen(QtCore.Qt.NoPen)
        drawPointer(self.bColor, (30 * (tik.hour() + tik.minute() / 60)), self.hPointer)
        drawPointer(self.bColor, (6 * (tik.minute() + tik.second() / 60)), self.mPointer)
        drawPointer(self.sColor, (6 * tik.second()), self.sPointer)
 
        pen = QPen(self.bColor)
        pen.setWidth(2)
        painter.setPen(pen)
        for i in range(0, 60):
            if (i % 5) == 0:
                painter.drawLine(87, 0, 97, 0)
            painter.rotate(6)
        painter.end()

class SlideShowApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Subhan Moschee TV")
        #self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        #self.showFullScreen()

# Zentrales Widget und Layout
        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)

# Set the VBox layout as main layout
        main_layout = QHBoxLayout(centralWidget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setObjectName("mainLayout")
        centralWidget.setLayout(main_layout)

# Stacked widget
        self.stacked_widget = QStackedWidget()

        # Page 1
        self.createCombinedPage("Page-1")

        main_layout.addWidget(self.stacked_widget)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateTime)
        self.timer.start(1000)

    def updateTime(self):
        currentTime = QTime.currentTime().toString("HH:mm:ss")
        self.digital_clock.setText(currentTime)


    def createCombinedPage(self, pageName):
        combined_widget = QWidget()
        combined_layout = QHBoxLayout(combined_widget)
        combined_layout.setContentsMargins(0, 0, 0, 0)
        if pageName == "Page-1":
            combined_layout.addWidget(self.createPage1())
        elif pageName == "Page-2":
            combined_layout.addWidget(self.createPage1())
        elif pageName == "Page-3":
            combined_layout.addWidget(self.createPage1())
        self.stacked_widget.addWidget(combined_widget)


    def createPage1(self):
        hbox_widget = QWidget()
        hbox_layout = QHBoxLayout()
        hbox_widget.setLayout(hbox_layout)

        main_widget_1 = QWidget()
        main_widget_1.setProperty("class", "layout_widgets")
        main_widget_1_layout = QVBoxLayout()
        main_widget_1_layout.addWidget(QLabel("Hello World 1"))
        main_widget_1_layout.addStretch()
        main_widget_1.setLayout(main_widget_1_layout)
        main_widget_1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        hbox_layout.addWidget(main_widget_1)
 
        main_widget_2 = QWidget()
        main_widget_2.setProperty("class", "layout_widgets")
        main_widget_2_layout = QVBoxLayout()
        main_widget_2_layout.addStretch()


        kalima_label = QLabel()
        kalima_pixmap = QPixmap("media/kalima.png")  # Ersetze mit dem tatsächlichen Pfad zum Bild
        fixed_width = 250 
        kalima_pixmap = kalima_pixmap.scaled(fixed_width, fixed_width, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        kalima_label.setPixmap(kalima_pixmap)
        kalima_label.setAlignment(Qt.AlignCenter)  # Zentriere das Bild, wenn gewünscht

        main_widget_2_layout.addWidget(kalima_label)
        
        analog_clock = Clock()
        main_widget_2_layout.addWidget(analog_clock)

        self.digital_clock = QLabel("00:00:00")
        self.digital_clock.setAlignment(Qt.AlignCenter)
        self.digital_clock.setObjectName("digital_clock")
        main_widget_2_layout.addWidget(self.digital_clock)
        
        fajr_time = "06:00"
        sohr_time = "14:00"
        asr_time = "16:30"
        maghrib_time = "19:45"
        isha_time = "21:30"
        jummah_time = "13:25"

        gebetszeiten = QLabel("Gebetszeiten")
        gebetszeiten.setObjectName("gebetszeiten_heading")
        gebetszeiten.setAlignment(Qt.AlignCenter)
        fajr = QLabel(f"Fajr\t  {fajr_time}")
        fajr.setProperty("class", "salat_timings")
        sohr = QLabel(f"Sohr\t  {sohr_time}")
        sohr.setProperty("class", "salat_timings")      
        asr = QLabel(f"Asr\t  {asr_time}")
        asr.setProperty("class", "salat_timings")
        maghrib = QLabel(f"Maghrib\t  {maghrib_time}")
        maghrib.setProperty("class", "salat_timings")
        isha = QLabel(f"Isha\t  {isha_time}")
        isha.setProperty("class", "salat_timings")
        jummah = QLabel(f"Jummah\t  {jummah_time}")
        jummah.setProperty("class", "salat_timings")

        main_widget_2_layout.addWidget(gebetszeiten)
        main_widget_2_layout.addWidget(fajr)
        main_widget_2_layout.addWidget(sohr)
        main_widget_2_layout.addWidget(asr)
        main_widget_2_layout.addWidget(maghrib)
        main_widget_2_layout.addWidget(isha)
        main_widget_2_layout.addWidget(jummah)
        
        main_widget_2_layout.addStretch()
        main_widget_2.setLayout(main_widget_2_layout)
        #main_widget_2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        hbox_layout.addWidget(main_widget_2)
        
        hbox_layout.addWidget(main_widget_1, 8)  # 30% der verfügbaren Breite
        hbox_layout.addWidget(main_widget_2, 2)
        hbox_layout.setContentsMargins(0, 0, 0, 0)
        hbox_layout.setSpacing(0)

        return hbox_widget


if __name__ == "__main__":
    app = QApplication(sys.argv)
    css_path = "src/style.css"
    try:
        with open(css_path, "r", encoding='utf-8') as file:
            css = file.read()
            app.setStyleSheet(css)
    except Exception as e:
        print(f"Fehler beim Laden des Stylesheets: {e}")

    window = SlideShowApp()
    window.showMaximized()
    #window.show()
    sys.exit(app.exec())
