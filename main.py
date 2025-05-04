import sys
import ctypes
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QGridLayout,
                             QPushButton, QLineEdit, QHBoxLayout, QVBoxLayout, QLabel)
from PyQt5.QtCore import Qt

if sys.platform == 'win32':
    user32 = ctypes.windll.user32
    WM_NCLBUTTONDOWN = 0x00A1
    HTCAPTION = 0x0002

class TitleBar(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0,0,0,0)

        self.title = QLabel("Calcolatrice")
        self.title.setStyleSheet(
            "color: white; padding-left: 5px; font-weight: bold;"
        )

        btn_size = 35
        self.btn_min = QPushButton("−", self)
        self.btn_min.setFixedSize(btn_size, btn_size)
        self.btn_min.setStyleSheet(
            "QPushButton {background-color: transparent; color: white; border: none; font-size: 16px;}"
            "QPushButton:hover {background-color: #404040;}"
        )
        self.btn_close = QPushButton("×", self)
        self.btn_close.setFixedSize(btn_size, btn_size)
        self.btn_close.setStyleSheet(
            "QPushButton {background-color: transparent; color: white; border: none; font-size: 16px;}"
            "QPushButton:hover {background-color: #e81123;}"
        )

        self.layout.addWidget(self.title)
        self.layout.addStretch()
        self.layout.addWidget(self.btn_min)
        self.layout.addWidget(self.btn_close)

        self.btn_min.clicked.connect(parent.showMinimized)
        self.btn_close.clicked.connect(parent.close)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if sys.platform == 'win32':
                hwnd = int(self.parent.winId())
                user32.ReleaseCapture()
                user32.SendMessageW(hwnd, WM_NCLBUTTONDOWN, HTCAPTION, 0)
            else:
                self.window().windowHandle().startSystemMove()
        super().mousePressEvent(event)

class Calcolatrice(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calcolatrice")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet("background-color: #2b2b2b;")

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(0,0,0,0)

        self.title_bar = TitleBar(self)
        main_layout.addWidget(self.title_bar)

        central = QWidget()
        main_layout.addWidget(central)
        layout = QGridLayout(central)

        self.display = QLineEdit()
        self.display.setMaxLength(12)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setReadOnly(True)
        self.display.setStyleSheet(
            "QLineEdit { background-color: #3b3b3b; color: white; border: 1px solid #505050; padding: 5px; font-size: 20px; }"
        )
        layout.addWidget(self.display, 0, 0, 1, 4)

        pulsanti = [
            ['7','8','9','/'],
            ['4','5','6','*'],
            ['1','2','3','-'],
            ['0','.','=','+'],
            ['C','(',')','^']
        ]
        btn_style = (
            "QPushButton { background-color: #404040; color: white; border: 1px solid #505050; min-width: 50px; min-height: 50px; font-size: 16px; }"
            "QPushButton:pressed { background-color: #303030; }"
        )
        for i, row in enumerate(pulsanti):
            for j, val in enumerate(row):
                btn = QPushButton(val)
                btn.setStyleSheet(btn_style)
                btn.clicked.connect(self.handle_click)
                layout.addWidget(btn, i+1, j)

        self.expression = ''

    def handle_click(self):
        text = self.sender().text()
        if text == '=':
            try:
                result = eval(self.expression.replace('^','**'))
                out = str(result)[:12]
                self.expression = out
            except Exception:
                out = 'Errore'
                self.expression = ''
            self.display.setText(out)
        elif text == 'C':
            self.expression = ''
            self.display.setText('')
        else:
            self.expression += text
            self.display.setText(self.expression[:12])

if __name__ == "__main__":
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, False)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, False)
    QApplication.setAttribute(Qt.AA_DisableHighDpiScaling, True)

    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    calc = Calcolatrice()
    calc.show()
    sys.exit(app.exec_())
