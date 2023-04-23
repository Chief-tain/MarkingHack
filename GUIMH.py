import sys
import pymorphy2
from datetime import datetime
from PyQt5.QtCore import QUrl
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QFont, QPalette, QBrush, QPixmap, QIntValidator
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout,  QLineEdit, QMessageBox
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import QSize
from pyqt5_plugins.examplebuttonplugin import QtGui
import pyqtgraph as pg
import fon_rc
from map import Map
from database import DbAdvanced


class Example(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(Example, self).__init__(*args, **kwargs)

        self.setMinimumSize(QSize(1900, 1000))
        self.setWindowTitle("MarkingHack")
        self.setGeometry(0, 0, 1900, 1000)

        self.layout = QGridLayout()

        self.browser = QWebEngineView()
        self.browser.setGeometry(0, 0, 1300, 810)
        self.browser.setUrl(QUrl("https://hack.markirovka.ru/task2"))
        self.setCentralWidget(self.browser)

        self.layout.addWidget(self.browser)

        self.graphWidget = pg.PlotWidget()
        hour = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        temperature = [30, 32, 34, 32, 33, 31, 29, 32, 35, 45]
        self.graphWidget.plot(hour, temperature)
        self.graphWidget.setGeometry(1310, 0, 610, 400)
        self.graphWidget.setBackground('y')
        self.setCentralWidget(self.graphWidget)

        self.layout.addWidget(self.graphWidget)

        self.graphWidget2 = pg.PlotWidget()
        hour = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        temperature = [30, 32, 34, 32, 33, 31, 29, 32, 35, 45]
        self.graphWidget2.plot(hour, temperature)
        self.graphWidget2.setGeometry(1310, 410, 610, 400)
        self.graphWidget2.setBackground('y')
        self.setCentralWidget(self.graphWidget2)

        self.layout.addWidget(self.graphWidget2)

        self.setLayout(self.layout)

        self.textbox1 = QLineEdit(self)
        self.textbox1.move(220, 820)
        self.textbox1.resize(340, 50)
        self.textbox1.setFont(QFont('San Francisco', 10))
        self.textbox1.setStyleSheet("""QLineEdit {
                                                color: rgb(80,85,88);
                                                background-color: yellow;
                                                border-radius: 10px;} """)

        self.label1 = QLabel('<b>Все города</b>', self)
        self.label1.setGeometry(1500, 880, 300, 50)
        self.label1.setFont(QFont('San Francisco', 12))
        self.label1.setStyleSheet(styletext)

        self.label2 = QLabel('<b>GTIN</b>', self)
        self.label2.setGeometry(40, 820, 300, 50)
        self.label2.setFont(QFont('San Francisco', 12))
        self.label2.setStyleSheet(styletext)

        self.label3 = QLabel('<b>Построить графики</b>', self)
        self.label3.setGeometry(1500, 820, 300, 50)
        self.label3.setFont(QFont('San Francisco', 12))
        self.label3.setStyleSheet(styletext)

        self.label4 = QLabel('<b>Карта ввода товара</b>', self)
        self.label4.setGeometry(40, 880, 300, 50)
        self.label4.setFont(QFont('San Francisco', 12))
        self.label4.setStyleSheet(styletext)

        self.label5 = QLabel('<b>Карта вывода товара</b>', self)
        self.label5.setGeometry(40, 940, 300, 50)
        self.label5.setFont(QFont('San Francisco', 12))
        self.label5.setStyleSheet(styletext)

        self.label6 = QLabel('<b>Создать БД из CSV</b>', self)
        self.label6.setGeometry(1500, 940, 300, 50)
        self.label6.setFont(QFont('San Francisco', 12))
        self.label6.setStyleSheet(styletext)

        self.label7 = QLabel('<b>Маршрутная карта</b>', self)
        self.label7.setGeometry(800, 820, 300, 50)
        self.label7.setFont(QFont('San Francisco', 12))
        self.label7.setStyleSheet(styletext)

        self.label8 = QLabel('<b>Предиктивная модель</b>', self)
        self.label8.setGeometry(800, 880, 300, 50)
        self.label8.setFont(QFont('San Francisco', 12))
        self.label8.setStyleSheet(styletext)

        self.bt1 = QPushButton("Выполнить", self)
        self.bt1.move(1740, 820)
        self.bt1.setFont(QFont('Arial', 12))
        self.bt1.setFixedSize(140, 50)
        self.bt1.setObjectName("pushButton")

        self.bt1.setStyleSheet(stylesheet)
        self.bt1.clicked.connect(self.Button1)

        self.bt2 = QPushButton("Отобразить", self)
        self.bt2.move(1740, 880)
        self.bt2.setFont(QFont('Arial', 12))
        self.bt2.setFixedSize(140, 50)
        self.bt2.setObjectName("pushButton")
        self.bt2.setStyleSheet(stylesheet)
        self.bt2.clicked.connect(self.Button2)

        self.bt3 = QPushButton("Отобразить", self)
        self.bt3.move(270, 880)
        self.bt3.setFont(QFont('Arial', 12))
        self.bt3.setFixedSize(140, 50)
        self.bt3.setObjectName("pushButton")
        self.bt3.setStyleSheet(stylesheet)
        self.bt3.clicked.connect(self.Button3)

        self.bt4 = QPushButton("Отобразить", self)
        self.bt4.move(270, 940)
        self.bt4.setFont(QFont('Arial', 12))
        self.bt4.setFixedSize(140, 50)
        self.bt4.setObjectName("pushButton")
        self.bt4.setStyleSheet(stylesheet)
        self.bt4.clicked.connect(self.Button4)

        self.bt5 = QPushButton("Карта\nввода/вывода\nтовара", self)
        self.bt5.move(420, 880)
        self.bt5.setFont(QFont('Arial', 12))
        self.bt5.setFixedSize(140, 110)
        self.bt5.setObjectName("pushButton")
        self.bt5.setStyleSheet(stylesheet)
        self.bt5.clicked.connect(self.Button5)

        self.bt6 = QPushButton("Выполнить", self)
        self.bt6.move(1740, 940)
        self.bt6.setFont(QFont('Arial', 12))
        self.bt6.setFixedSize(140, 50)
        self.bt6.setObjectName("pushButton")
        self.bt6.setStyleSheet(stylesheet)
        self.bt6.clicked.connect(self.Button6)

        self.bt7 = QPushButton("Отобразить", self)
        self.bt7.move(1150, 820)
        self.bt7.setFont(QFont('Arial', 12))
        self.bt7.setFixedSize(140, 50)
        self.bt7.setObjectName("pushButton")
        self.bt7.setStyleSheet(stylesheet)
        self.bt7.clicked.connect(self.Button7)

        self.bt8 = QPushButton("Отобразить", self)
        self.bt8.move(1150, 880)
        self.bt8.setFont(QFont('Arial', 12))
        self.bt8.setFixedSize(140, 50)
        self.bt8.setObjectName("pushButton")
        self.bt8.setStyleSheet(stylesheet)
        self.bt8.clicked.connect(self.Button8)

        self.showMaximized()

        self.database = DbAdvanced()

    def Button1(self):
        self.graphWidget.clear()
        vvod_data = self.database.create_plot_vvod(self.textbox1.text())
        vivod_data = self.database.create_plot_vivod(self.textbox1.text())
        vvod_mas = []
        vivod_mas = []

        for key, value in vvod_data.items():
            if key in vivod_data:
                vvod_mas.append(value)
                vivod_mas.append(vivod_data[key])

        self.graphWidget.plot(range(len(vvod_mas)), vvod_mas, pen=pg.mkPen(color=(255, 0, 0)))
        self.graphWidget.plot(range(len(vivod_mas)), vivod_mas, pen=pg.mkPen(color=(0, 0, 255)))
        self.graphWidget.setTitle("<span style=\"color:red;font-size:20px\">Ввод/</span><span style=\"color:blue;font-size:20px\">вывод</span><span style=\"color:black;font-size:20px\"> товаров </span>")
        styles = {'color': 'r', 'font-size': '20px'}
        self.graphWidget.setLabel('left', 'Количество', **styles)
        self.graphWidget.setLabel('bottom', 'Дата', **styles)
        self.graphWidget.showGrid(x=True, y=True)
        self.graphWidget.addLegend()

    def Button2(self):
        self.new_map = Map()
        self.new_map.add_points()
        url = QtCore.QUrl.fromLocalFile(r"C:\Users\Chubu\PycharmProjects\MarkingHack\marking_hack.html")
        self.browser.load(url)

    def Button3(self):
        self.gtin_new_map = Map()
        self.gtin_new_map.add_gtin_points(self.textbox1.text())
        url = QtCore.QUrl.fromLocalFile(r"C:\Users\Chubu\PycharmProjects\MarkingHack\gtin_marking_hack.html")
        self.browser.load(url)

    def Button4(self):
        self.gtin_new_map_vivod = Map()
        self.gtin_new_map_vivod.add_gtin_points_vivod(self.textbox1.text())
        url = QtCore.QUrl.fromLocalFile(r"C:\Users\Chubu\PycharmProjects\MarkingHack\gtin_marking_hack_vivod.html")
        self.browser.load(url)

    def Button5(self):
        self.gtin_new_map_total = Map()
        self.gtin_new_map_total.add_gtin_points_total(self.textbox1.text())
        url = QtCore.QUrl.fromLocalFile(r"C:\Users\Chubu\PycharmProjects\MarkingHack\marking_hack_total.html")
        self.browser.load(url)

    def Button6(self):
        self.new_db = DbAdvanced()
        self.new_db.insert_into_db()

    def Button7(self):
        self.route_map = Map()
        self.route_map.routes(self.textbox1.text())
        url = QtCore.QUrl.fromLocalFile(r"C:\Users\Chubu\PycharmProjects\MarkingHack\marking_hack_route.html")
        self.browser.load(url)

    def Button8(self):
        self.graphWidget2.clear()
        self.prediction_db = DbAdvanced()
        self.prediction_db.prediction(self.textbox1.text())

        self.graphWidget2.plot(range(len(self.prediction_db.current1)), self.prediction_db.current2, pen=pg.mkPen(color=(255, 0, 0)))
        self.graphWidget2.plot(range(len(self.prediction_db.current1), (len(self.prediction_db.current1)+len(self.prediction_db.predicted1))), self.prediction_db.predicted2, pen=pg.mkPen(color=(0, 0, 255)))
        self.graphWidget2.setTitle(('Продажи продукта "{}"'.format(self.textbox1.text())))
        styles = {'color': 'r', 'font-size': '20px'}
        self.graphWidget2.setLabel('left', 'Количество', **styles)
        self.graphWidget2.setLabel('bottom', 'Дата', **styles)
        self.graphWidget2.showGrid(x=True, y=True)
        self.graphWidget2.addLegend()


styletext = ("""QLabel {color: rgb(80,85,88)}""")

stylesheet = ("""QPushButton#pushButton {
                                    color: rgb(80,85,88);
                                    border-style: outset; 
                                    border-radius: 10px;
                                    font: bold 16px; 
                                    padding: 6px;
                                    border-bottom-width: 4px;
                                    border-right-width: 4px;
                                    border-color: rgb(217, 217, 20) ;     
                                    background-color: yellow;
                                    }
                                    QPushButton#pushButton:pressed {
                                    border-top-width: 4px;
                                    border-left-width: 4px; 
                                    border-bottom-width: 0px;
                                    border-right-width: 0px;
                                    background-color: yellow;
                                    border-style: inset;}""")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = Example()
    mainWin.setStyleSheet("""Example {
                              background-image: url(:/main_window/Fon.png);
                              background-repeat: no-repeat;
                              background-position: center;

    }""")
    mainWin.show()
    sys.exit(app.exec_())