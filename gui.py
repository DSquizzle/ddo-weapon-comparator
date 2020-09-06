from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QGridLayout, QLineEdit, QPushButton, QLabel, QComboBox, QWidget, QTextEdit
from PyQt5.QtCore import QRegularExpression
from PyQt5.QtGui import QRegularExpressionValidator

class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle("DDO Weapon Comparator")

        self.weaponSelector = QComboBox()
        self.saveButton = QPushButton("Save")
        self.newButton = QPushButton("New")
        weaponSelectorLayout = QHBoxLayout()
        weaponSelectorLayout.addWidget(QLabel("Select a weapon to edit"), 4)
        weaponSelectorLayout.addWidget(self.weaponSelector, 10)
        weaponSelectorLayout.addWidget(self.saveButton, 2)
        weaponSelectorLayout.addWidget(self.newButton, 2)
        weaponSelectorLayout.setContentsMargins(20, 0, 0, 0)

        self.weaponInfoFields = []
        fields = [["Weapon Name", "e.g. Insanity", ".*"],
                 ["Weapon Dice Multiplier", "e.g. 1", ".*"],
                 ["Base Damage Dice", "e.g. 2d6", ".*"],
                 ["Critical Profile", "e.g. 19-20x2", ".*"],
                 ["On-Hit Damage", "e.g. 3d6", ".*"]]

        grid = QGridLayout()
        for row, field in enumerate(fields):
            grid.addWidget(QLabel(field[0]), row, 0)
            grid.addWidget(QLineEdit(placeholderText=field[1]), row, 1)

        grid.setContentsMargins(20, 40, 100, 20)

        self.addPlotButton = QPushButton("Add Plot")
        self.removePlotButton = QPushButton("Remove Plot")
        plotButtonsLayout = QHBoxLayout()
        plotButtonsLayout.addWidget(self.addPlotButton)
        plotButtonsLayout.addWidget(self.removePlotButton)
        plotButtonsLayout.setContentsMargins(300, 0, 0, 0)

        leftColumn = QVBoxLayout()
        leftColumn.addLayout(weaponSelectorLayout)
        leftColumn.addLayout(grid)
        leftColumn.addLayout(plotButtonsLayout)

        rightColumn = QGridLayout()
        rightColumn.addWidget(QTextEdit())

        columns = QHBoxLayout()
        columns.addLayout(leftColumn)
        columns.addLayout(rightColumn)

        widget = QWidget()
        widget.setLayout(columns)
        self.setCentralWidget(widget)


app = QApplication([])
window = MainWindow()
window.show()
app.exec_()
