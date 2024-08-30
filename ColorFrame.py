from PyQt6 import QtCore, QtGui, QtWidgets


class ObscureGraphic(QtWidgets.QLabel):
    def __init__(self, xd, yd, rect: tuple, type, color, *args, **kwargs):
        super(ObscureGraphic, self).__init__(*args, **kwargs)
        self.xd = xd
        self.yd = yd
        self.xv = 5
        self.yv = 5
        self.__type = type
        self.__color = color
        self.setGeometry(QtCore.QRect(*rect))
        blur_effect = QtWidgets.QGraphicsBlurEffect()
        blur_effect.setBlurRadius(200) 
        self.setGraphicsEffect(blur_effect)

    def getX(self):
        return self.pos().x()
    
    def getY(self):
        return self.pos().y()

    def paintEvent(self, event: QtGui.QPaintEvent):
        super().paintEvent(event)
        painter = QtGui.QPainter(self)
        if isinstance(self.__color, tuple):
            painter.setBrush(QtGui.QBrush(QtGui.QColor(*self.__color)))
            painter.setPen(QtGui.QPen(QtGui.QColor(*self.__color)))
        else:
            painter.setBrush(QtGui.QBrush(QtGui.QColor(self.__color)))
            painter.setPen(QtGui.QPen(QtGui.QColor(self.__color)))
        if self.__type == 'rect':
            painter.drawRect(0, 0, self.width(), self.height())
        elif self.__type == 'circle':
            painter.drawEllipse(0, 0, self.width(), self.height())
        elif self.__type == 'triangle':
            painter.drawPolygon(QtGui.QPolygon([
                QtCore.QPoint(0, self.height()),
                QtCore.QPoint(self.width() // 2, 0),
                QtCore.QPoint(self.width(), self.height())
            ]))
        else:
            raise Exception("Invalid Drawing Type")
        
class DynamicColorFrame(QtWidgets.QFrame):
    def __init__(self, pos, size, *args, **kwargs):
        super(DynamicColorFrame, self).__init__(*args, **kwargs)
        self.size = size
        self.setGeometry(QtCore.QRect(*pos, *size))
        self.graphics = (
            ObscureGraphic(0, 0, (0, 0, size[0], size[0]), 'circle', (255, 200, 255), self),
            ObscureGraphic(0, 0, (0, 180, size[0], size[0]), 'circle', (255, 200, 255), self),
            ObscureGraphic(1, 1, (0, 0, size[0], size[1]), 'circle', (175, 160, 255), self),
            ObscureGraphic(1, -1, (size[0] // 4, size[1] // 3, size[0], size[1]), 'circle', 'red', self),
            ObscureGraphic(1, -1, (2 * size[0] // 4, 0, size[0], size[1]), 'circle', 'cyan', self),
            ObscureGraphic(1, 1, (3 * size[0] // 4, 60, 2 * size[1] // 3, size[1]), 'circle', 'blue', self)
        )
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.__update)
        timer.start(20)

    def __update(self):
        for g in self.graphics[2:]:
            g.move(g.getX() + g.xd * g.xv, g.getY() + g.yd * g.yv)

            if g.getX() > self.size[0]:
                g.move(-(g.width() + 40), g.getY())
            if g.getY() < -self.size[1] * 0.1:
                g.yd = 1
            if g.getY() > self.size[1] - self.size[1] * 0.1:
                g.yd = -1
