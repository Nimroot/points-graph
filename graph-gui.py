#!/usr/bin/python3

import sys
from collections     import namedtuple
from PyQt5.QtWidgets import (QApplication, QWidget, QDesktopWidget,
    QFrame, QPushButton)
from PyQt5.QtGui     import QPainter, QColor, QPen
from PyQt5.QtCore    import Qt, QPoint

class Grapher(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.grid = Grid(self)
        self.grid.setGeometry(0, 0, 800, 800)
        self.grid.setStyleSheet('QWidget { background-color: #e8e8e8;'
            'border-right: 1px solid #d5d5d5; }')

        self.resize(1200, 800)
        # Move window to the center of the screen
        window_rec   = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        window_rec.moveCenter(center_point)
        self.move(window_rec.topLeft())

        self.setWindowTitle('Graph Points')
        self.show()

class Grid(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent);

        self.grid_scale  = 25
        self.axis_midpoint = 0
        self.GPoint = namedtuple('GPoint', ['x', 'y'])
        self.GPointList = []

        self.GPointList.append(self.GPoint(-9, 1))
        self.GPointList.append(self.GPoint(-4, -4))
        self.GPointList.append(self.GPoint(6, -8))
        self.GPointList.append(self.GPoint(0, 7))


    def wheelEvent(self, event):
        if event.angleDelta().y() > 0 and self.grid_scale < 50:
            self.grid_scale += 1
        if event.angleDelta().y() < 0 and self.grid_scale > 10:
            self.grid_scale -= 1

        self.update()

    def plotPoint(self, x, y):
        x = self.axis_midpoint + self.grid_scale * x
        y = self.axis_midpoint + self.grid_scale * y

        painter = QPainter()
        painter.begin(self)
        painter.setRenderHints(QPainter.Antialiasing, True)

        point_color = QColor(0, 0, 0)
        point_color.setNamedColor('#7c2136')
        painter.setPen(point_color)
        painter.setBrush(point_color)
        painter.drawEllipse(QPoint(x,y), 5, 5)

        painter.end()


    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHints(QPainter.Antialiasing, True)

        grid_color = QColor(0, 0, 0)
        grid_color.setNamedColor('#d5d5d5')

        axis_color = QColor(0, 0, 0)
        axis_color.setNamedColor('#727272')

        pen = QPen(grid_color, 1, Qt.SolidLine)
        painter.setPen(pen)

        # Draw grid acording to the scale
        i = 0
        while i <= 800:
            painter.drawLine(0, i, 800, i)
            painter.drawLine(i, 0, i, 800)
            i += self.grid_scale

        pen.setColor(axis_color)
        pen.setWidth(1)
        painter.setPen(pen)

        # Calculate midpoint and snap axis to the grid
        self.axis_midpoint = ((800 // self.grid_scale) // 2) * self.grid_scale
        painter.drawLine(0, self.axis_midpoint, 800, self.axis_midpoint)
        painter.drawLine(self.axis_midpoint, 0, self.axis_midpoint, 800)

        for point in self.GPointList:
            self.plotPoint(point.x, point.y)

        painter.end()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    grapher = Grapher()
    sys.exit(app.exec_())
