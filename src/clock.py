
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *

class Clock(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
 
        self.hPointer = QPolygon([QPoint(3, 7),
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
        self.setMinimumSize(350, 350)

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
        painter.setPen(Qt.NoPen)
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
