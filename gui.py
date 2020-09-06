from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QGridLayout, QLineEdit, QPushButton, QLabel, QComboBox, QWidget, QTextEdit
from PyQt5.QtCore import QRegularExpression
from PyQt5.QtGui import QRegularExpressionValidator

import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from weapon_comparator import Weapon

class MplCanvas(FigureCanvasQTAgg):

    def __init__(self):
        fig = Figure()
        self.axes = fig.add_subplot(111)
        super().__init__(fig)

class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle("DDO Weapon Comparator")

        self.weaponInfoFields = []
        self.weapons = {}

        self.weaponSelector = QComboBox()
        self.weaponSelector.addItem("New Weapon")
        self.weaponSelector.currentTextChanged.connect(self.loadWeapon)
        self.saveButton = QPushButton("Save")
        self.saveButton.setDisabled(True)
        self.saveButton.clicked.connect(self.onSaveButtonClicked)
        self.newButton = QPushButton("New")
        self.newButton.clicked.connect(self.onNewButtonClicked)
        weaponSelectorLayout = QHBoxLayout()
        weaponSelectorLayout.addWidget(QLabel("Select a weapon to edit"), 4)
        weaponSelectorLayout.addWidget(self.weaponSelector, 10)
        weaponSelectorLayout.addWidget(self.saveButton, 2)
        weaponSelectorLayout.addWidget(self.newButton, 2)
        weaponSelectorLayout.setContentsMargins(20, 0, 0, 0)

        self.fields = [["Weapon Name", "e.g. Insanity", ".*"],
                       ["Weapon Dice Multiplier", "e.g. 1", "\\d*(\\.\\d+)?"],
                       ["Base Damage Dice", "e.g. 2d6", "\\d*d\\d+"],
                       ["Critical Profile", "e.g. 19-20x2", "[01]?\\d-20x\\d+"],
                       ["On-Hit Damage", "e.g. 3d6", "\\d*d\\d+"]]

        grid = QGridLayout()
        for row, field in enumerate(self.fields):
            widget = QLineEdit(placeholderText=field[1])
            widget.textChanged.connect(self.onInputFieldChanged)
            widget.setValidator(QRegularExpressionValidator(QRegularExpression(field[2])))
            self.weaponInfoFields.append(widget)
            grid.addWidget(QLabel(field[0]), row, 0)
            grid.addWidget(widget, row, 1)

        grid.setContentsMargins(20, 40, 100, 20)

        self.addPlotButton = QPushButton("Add Plot")
        self.addPlotButton.clicked.connect(self.plotWeapon)
        self.removePlotButton = QPushButton("Remove Plot")
        plotButtonsLayout = QHBoxLayout()
        plotButtonsLayout.addWidget(self.addPlotButton)
        plotButtonsLayout.addWidget(self.removePlotButton)
        plotButtonsLayout.setContentsMargins(300, 0, 0, 0)

        leftColumn = QVBoxLayout()
        leftColumn.addLayout(weaponSelectorLayout)
        leftColumn.addLayout(grid)
        leftColumn.addLayout(plotButtonsLayout)

        self.chart = MplCanvas()
        rightColumn = QGridLayout()
        rightColumn.addWidget(self.chart)

        columns = QHBoxLayout()
        columns.addLayout(leftColumn)
        columns.addLayout(rightColumn)

        widget = QWidget()
        widget.setLayout(columns)
        self.setCentralWidget(widget)

    def onNewButtonClicked(self):
        self.weaponSelector.setCurrentText("New Weapon")
        for field in self.weaponInfoFields:
            field.clear()

    def onSaveButtonClicked(self):
        weaponInfo = [self.weaponInfoFields[i].text() for i in range(5)]
        wName = weaponInfo[0]
        self.weapons[weaponInfo[0]] = Weapon(*weaponInfo)

        if self.weaponSelector.findText(wName) == -1:
            self.weaponSelector.addItem(wName)
        if not self.weaponSelector.currentText() in [wName, "New Weapon"]:
            del(self.weapons[self.weaponSelector.currentText()])
            self.weaponSelector.removeItem(self.weaponSelector.currentIndex())
        self.weaponSelector.setCurrentText(wName)

    def onInputFieldChanged(self):
        for field in self.weaponInfoFields:
            if not (field.hasAcceptableInput() and field.text()):
                return self.saveButton.setDisabled(True)

        return self.saveButton.setEnabled(True)

    def loadWeapon(self, name):
        if name == "New Weapon":
            return self.onNewButtonClicked()

        for field, value in enumerate(self.weapons[name].__dict__.values()):
            self.weaponInfoFields[field].setText(str(value))

    def plotWeapon(self):
        self.onSaveButtonClicked()
        weapon = self.weapons[self.weaponSelector.currentText()]
        data = [range(100), [weapon.averageDamage(deadly) for deadly in range(100)]]
        self.chart.axes.plot(*data, label=weapon.name)
        self.chart.axes.legend()
        self.chart.draw()


app = QApplication([])
window = MainWindow()
window.show()
app.exec_()
