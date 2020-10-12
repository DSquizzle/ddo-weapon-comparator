import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout,
                             QHBoxLayout, QGridLayout, QLineEdit, QPushButton,
                             QLabel, QComboBox, QWidget)

from PyQt5.QtCore import QRegularExpression
from PyQt5.QtGui import QRegularExpressionValidator

import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from ddoweapons.weapon_comparator import Weapon
matplotlib.use("Qt5Agg")


class MplCanvas(FigureCanvasQTAgg):
    """
    A class that will be used to create the widget that contains the
    graphs
    """

    def __init__(self):
        fig = Figure()
        self.axes = fig.add_subplot(111)
        super().__init__(fig)


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        """
        Create widgets, define layouts, and connect signals to slots
        """
        super().__init__(*args, **kwargs)
        self.setWindowTitle("DDO Weapon Comparator")

        # Create a list to hold user input fields
        self.weaponInfoFields = []
        # Create a dict to hold inputted weapons
        self.weapons = {}
        # Create a dict to hold weapon plots
        self.plottedWeapons = {}

        self.weaponSelector = QComboBox()
        self.weaponSelector.addItem("New Weapon")
        self.weaponSelector.currentTextChanged.connect(self.loadWeapon)
        self.deleteButton = QPushButton("Delete")
        self.deleteButton.clicked.connect(self.onDeleteButtonClicked)
        self.newButton = QPushButton("New")
        self.newButton.clicked.connect(self.onNewButtonClicked)
        weaponSelectorLayout = QHBoxLayout()
        weaponSelectorLayout.addWidget(QLabel("Select a weapon to edit"), 4)
        weaponSelectorLayout.addWidget(self.weaponSelector, 10)
        weaponSelectorLayout.addWidget(self.deleteButton, 2)
        weaponSelectorLayout.addWidget(self.newButton, 2)
        weaponSelectorLayout.setContentsMargins(20, 0, 0, 0)

        self.fields = [["Weapon Name", "e.g. Insanity", ".*"],
                       ["Weapon Enhancement Bonus", "e.g. 5", "\\d+"],
                       ["Weapon Dice Multiplier", "e.g. 1", "\\d*(\\.\\d+)?"],
                       ["Base Damage Dice", "e.g. 2d6", "(?:(?:(?:\\d*d\\d+)|(?:\\d+(\\.\\d+)?|\\.\\d+))\\s*\\+\\s*)*(?:(?:\\d*d\\d+)|(?:\\d+(\\.\\d+)?|\\.\\d+))"],
                       ["Critical Profile", "e.g. 19-20x2", "[12]?\\d-20x\\d+"],
                       ["On-Hit Damage", "e.g. 3d6", "(?:(?:(?:\\d*d\\d+)|(?:\\d+(\\.\\d+)?|\\.\\d+))\\s*\\+\\s*)*(?:(?:\\d*d\\d+)|(?:\\d+(\\.\\d+)?|\\.\\d+))"]]

        # Add a label, input field, and input validator for each item in
        # each list in self.fields
        grid = QGridLayout()
        for row, field in enumerate(self.fields):
            widget = QLineEdit(placeholderText=field[1])
            widget.textChanged.connect(self.onInputFieldChanged)
            widget.setValidator(QRegularExpressionValidator(
                                QRegularExpression(field[2])))
            self.weaponInfoFields.append(widget)
            grid.addWidget(QLabel(field[0]), row, 0)
            grid.addWidget(widget, row, 1)

        grid.setContentsMargins(20, 40, 100, 20)

        self.addPlotButton = QPushButton("Add Plot")
        self.addPlotButton.setDisabled(True)
        self.addPlotButton.clicked.connect(self.plotWeapon)
        self.removePlotButton = QPushButton("Remove Plot")
        self.removePlotButton.setDisabled(True)
        self.removePlotButton.clicked.connect(self.removePlot)
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

    def onInputFieldChanged(self):
        """
        When user inputs change, set the "Add Plot" and "Remove Plot"
        buttons to be enabled or disabled, as appropriate, and update
        the plot if the plot for the current weapon is toggled on
        """
        self.addPlotButton.setEnabled(self.plotIsAddable())
        self.removePlotButton.setEnabled(self.plotIsRemovable())

        if self.inputsAreAcceptable():
            # Auto-save the weapon any time all inputs pass the regex
            self.saveWeapon()
            if graph := self.plottedWeapons.get(  # noqa: E203, E701, E231
               self.weaponSelector.currentText(), None):  # noqa: E203, E701, E231, E501
                # Don't do anything unless the plot has been added but not
                # removed
                if not graph.get_figure():
                    # If the plot for the weapon has been hidden, unhide it!
                    self.chart.axes.add_artist(graph)
                # Update the plot for this weapon based on the new inputs
                graph.set_ydata([self.weapons[self.weaponSelector
                                .currentText()].averageDamage(deadly)
                                for deadly in range(50)])
                self.drawPlot()
        else:
            if graph := self.plottedWeapons.get(self.weaponSelector  # noqa: E203, E701, E231, E501
                                                .currentText(), None):  # noqa: E203, E701, E231, E501
                # Hide the current weapon's plot if inputs are not acceptable
                # and the plot has been added but not removed
                self.fig = graph.get_figure()
                # Need a better way to save self.fig
                if graph.get_figure():
                    graph.remove()
                    self.drawPlot()

    def onNewButtonClicked(self):
        """
        Loads a new weapon for editing
        """
        self.weaponSelector.setCurrentText("New Weapon")
        for field in self.weaponInfoFields:
            field.clear()

    def onDeleteButtonClicked(self):
        """
        Deletes the current weapon and removes its graph if applicable
        """
        if self.weaponSelector.currentText() != "New Weapon":
            del(self.weapons[self.weaponSelector.currentText()])
            self.removePlot()
            self.weaponSelector.removeItem(self.weaponSelector.currentIndex())

    def saveWeapon(self):
        """
        Saves the current weapon in self.weapons and adds the current
        weapon to the self.weaponSelector options if it is not already
        there
        """
        weaponInfo = [field.text() for field in self.weaponInfoFields]
        wName = weaponInfo[0]
        self.weapons[weaponInfo[0]] = Weapon(*weaponInfo)

        if self.weaponSelector.findText(wName) == -1:
            # Make sure the weapon's name is in self.weaponSelector
            self.weaponSelector.addItem(wName)
        if not self.weaponSelector.currentText() in [wName, "New Weapon"]:
            # If the name of the weapon has changed, remove references
            # to the old name from self.weapons and self.weaponSelector
            del(self.weapons[self.weaponSelector.currentText()])
            self.weaponSelector.removeItem(self.weaponSelector.currentIndex())
        self.weaponSelector.setCurrentText(wName)

    def loadWeapon(self, name):
        """
        Loads the properties of a weapon into the input fields
        """
        if name == "New Weapon":
            # Clear all input fields
            return self.onNewButtonClicked()

        for field, value in enumerate(self.weapons[name].__dict__.values()):
            # Populate each user input field with the appropriate value
            # for the selected weapon UNLESS that input field is active
            if self.weaponInfoFields[field].hasFocus():
                pass
            else:
                self.weaponInfoFields[field].setText(str(value))

    def plotWeapon(self):
        """
        Saves the current weapon and adds the plot to the graph
        """
        self.saveWeapon()
        weapon = self.weapons[self.weaponSelector.currentText()]
        data = [range(50), [weapon.averageDamage(deadly)
                            for deadly in range(50)]]
        self.plottedWeapons[weapon.name] = self.chart.axes.plot(
                                           *data, label=weapon.name)[0]
        self.drawPlot()
        self.removePlotButton.setEnabled(True)
        self.addPlotButton.setDisabled(True)

    def removePlot(self):
        """
        Removes the plot for the current weapon to the graph
        """
        if plot := self.plottedWeapons.get(self.weaponSelector.currentText(),  # noqa: E203, E701, E231, E501
                                           None):  # noqa: E203, E701, E231
            plot.remove()
            del(self.plottedWeapons[self.weaponSelector.currentText()])
            self.drawPlot()
            self.removePlotButton.setDisabled(True)
            self.addPlotButton.setEnabled(self.plotIsAddable())

    def plotIsRemovable(self):
        """
        Returns true if and only if the plot for the current weapon is
        toggled on
        """
        return bool(self.plottedWeapons.get(self.weaponSelector.currentText(),
                                            None))

    def plotIsAddable(self):
        """
        Returns true if and only if the plot for the current weapon is
        toggled off AND all user inputs are acceptable
        """
        if self.inputsAreAcceptable():
            return False if self.plotIsRemovable() else True

        return False

    def inputsAreAcceptable(self):
        """
        Returns true if and only if ALL user input fields have
        acceptable inputs
        """
        for field in self.weaponInfoFields:
            if not (field.hasAcceptableInput() and field.text()):
                return False

        return True

    def drawPlot(self):
        """
        Updates the graph and legendwith the most recent user inputs
        """
        # Grab all weapon names and their plots IF the plots should be
        # visible so they can be added to the legend. If no plots
        # should be visible, set labels and handles to be empty lists
        labels, handles = (list(zip(*filter(lambda x: x[1].get_figure(),
                                            self.plottedWeapons.items())))
                           or [[], []])
        self.chart.axes.legend(handles, labels)
        self.chart.draw()


def main(*args):
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main(*sys.argv[1:])
