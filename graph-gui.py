#!/usr/bin/python3

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QFrame
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt, QPoint


class Grapher(QWidget):

    def __init__(self):
        super().__init__()

        self.desktop_width = QDesktopWidget().availableGeometry().size().\
            width()
        self.desktop_height = QDesktopWidget().availableGeometry().size().\
            height()
        """
        Dimensions of a window should be about 2/3 of a screen's dimension
        rounded to the nearest 100 to make sure it fits properly.
        """
        self.window_width = (round(self.desktop_width * 2 / 300) * 100)
        self.window_height = (round(self.desktop_height * 2 / 300) * 100)

        if self.window_height > self.window_width:
            self.grid_size = self.window_width
        else:
            self.grid_size = self.window_height

        self.initUI()

    def initUI(self):
        self.grid = Grid(self, self.grid_size)
        self.grid.setGeometry(0, 0, self.grid_size, self.grid_size)
        self.grid.setStyleSheet('QWidget { background-color: #e8e8e8;'
                                'border-right: 1px solid #d5d5d5; }')
        self.resize(self.window_width, self.window_height)
        # Move window to the center of the screen
        window_rec = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        window_rec.moveCenter(center_point)
        self.move(window_rec.topLeft())

        self.setWindowTitle('Graph Points')
        self.show()


class Grid(QFrame):
    def __init__(self, parent=None, grid_size=0):
        super().__init__(parent)

        self.grid_size = grid_size
        self.grid_scale = grid_size // 20
        self.axis_midpoint = QPoint(10 * self.grid_scale, 10 * self.grid_scale)
        self.axis_ticks = 0

        self.translate_val = QPoint(0, 0)
        self.cursor_lastpos = 0.0

        self.PointsList = []
        self.PointsList.append(QPoint(-9, 1))
        self.PointsList.append(QPoint(-4, -4))
        self.PointsList.append(QPoint(6, -8))
        self.PointsList.append(QPoint(0, 7))

    def mousePressEvent(self, event):
        self.cursor_lastpos = event.screenPos()

    def mouseMoveEvent(self, event):
        position_diff = event.screenPos() - self.cursor_lastpos

        if event.buttons() & Qt.MidButton:
            self.translate_val += position_diff
            self.cursor_lastpos = event.screenPos()
            self.axis_midpoint += position_diff
            self.update()

    def wheelEvent(self, event):
        # if event.angleDelta().y() > 0 and self.grid_scale < 50:
        #    self.grid_scale += 10
        # if event.angleDelta().y() < 0 and self.grid_scale > 10:
        #    self.grid_scale -= 10

        self.update()

    def paintEvent(self, event):
        grid_color = QColor(0, 0, 0)
        grid_color.setNamedColor('#d5d5d5')

        axis_color = QColor(0, 0, 0)
        axis_color.setNamedColor('#727272')

        painter = QPainter()
        painter.begin(self)
        painter.setRenderHints(QPainter.Antialiasing, True)

        pen = QPen(grid_color, 1, Qt.SolidLine)
        painter.setPen(pen)

        # Draw grid acording to the scale
        t = self.translate_val
        s_point = QPoint(t.x(), t.y())
        e_point = QPoint(self.grid_size + t.x(),
                         self.grid_size + t.y())

        print(t.x() // 40)

        while s_point.x() <= e_point.x():
            painter.drawLine(s_point.x(), t.y(), s_point.x(),
                             (self.grid_size + t.y()))
            s_point += QPoint(self.grid_scale, 0)

        while s_point.y() <= e_point.y():
            painter.drawLine(t.x(), s_point.y(), (self.grid_size + t.x()),
                             s_point.y())
            s_point += QPoint(0, self.grid_scale)

        pen.setColor(axis_color)
        pen.setWidth(1)
        painter.setPen(pen)

        # Snap axis to the grid
        if t.x() < 0:
            painter.drawLine(0, self.axis_midpoint.y(),
                             (self.grid_size - t.x()),
                             self.axis_midpoint.y())
        else:
            painter.drawLine(0, self.axis_midpoint.y(),
                             (self.grid_size),
                             self.axis_midpoint.y())

        if t.y() < 0:
            painter.drawLine(self.axis_midpoint.x(), 0,
                             self.axis_midpoint.x(),
                             (self.grid_size - t.y()))
        else:
            painter.drawLine(self.axis_midpoint.x(), 0,
                             self.axis_midpoint.x(),
                             self.grid_size)

        for point in self.PointsList:
            self.plotPoint(point.x(), point.y())

        painter.end()

    def plotPoint(self, x, y):
        x = self.axis_midpoint.x() + self.grid_scale * x
        y = self.axis_midpoint.y() - self.grid_scale * y

        painter = QPainter()
        painter.begin(self)
        painter.setRenderHints(QPainter.Antialiasing, True)

        point_color = QColor(0, 0, 0)
        point_color.setNamedColor('#7c2136')
        painter.setPen(point_color)
        painter.setBrush(point_color)
        painter.drawEllipse(QPoint(x, y), 5, 5)

        painter.end()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    grapher = Grapher()
    sys.exit(app.exec_())
