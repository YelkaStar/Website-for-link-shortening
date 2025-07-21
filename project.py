import sys

from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QTabWidget, QLabel, QFrame, QTableWidgetItem, QLabel
from PyQt6.QtCore import Qt

newTab = []

def NewWindow():
    newTab = QTabWidget()
    newTab.resize(1750, 1000)
    MainTab.addTab(newTab, f"Новое Окно")
    MainTab.setTabsClosable(True)

def CloseWindow(index):
    if index != 0:
        MainTab.removeTab(index)

MyProgram = QApplication([])

Globalwindow = QWidget()
Globalwindow.setWindowTitle("Smilto")
Globalwindow.resize(1750, 1000)

# Кнопка
# CreateWindow = QPushButton("Создание Окна")
# layout = QVBoxLayout(Globalwindow)
# layout.addWidget(CreateWindow, alignment=Qt.AlignmentFlag.AlignVCenter)
CreateWindow = QPushButton("Создание Окна", Globalwindow)
CreateWindow.setFixedSize(125, 50)
CreateWindow.move(1775, 305)
CreateWindow.clicked.connect(NewWindow)

# Tab
MainTab = QTabWidget()
MainTab.addTab(Globalwindow, "Главная")
MainTab.resize(1920, 1080)
MainTab.show()

MainTab.tabCloseRequested.connect(CloseWindow)

#интерфейс
palka = QFrame(Globalwindow)
palka.setGeometry(300, 0, 12, 20000)
palka.setStyleSheet("background-color: gray;")
palka.show()
palka1 = QFrame(Globalwindow)
palka1.setGeometry(300,300, 20000,10)
palka1.setStyleSheet("background-color: gray;")
palka1.show()
palka2 = QFrame(Globalwindow)
palka2.setGeometry(300,350,20000,10)
palka2.setStyleSheet("background-color: gray;")
palka2.show()

Text = QLabel("Name", Globalwindow)
Text.setFont(QFont("Arial",14))
Text.move(345,320)
Text.show()

Globalwindow.show()
sys.exit(MyProgram.exec())