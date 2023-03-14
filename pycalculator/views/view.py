from PyQt6.QtCore import Qt, QAbstractTableModel
from PyQt6 import QtGui
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QGridLayout,
    QPushButton,
    QWidget,
    QLineEdit,
    QDialog,
    QLabel,
    QToolBar,
    QStyle,
    QTableView,
    QHeaderView,
    QMenu
)

class Window(QMainWindow):
    def __init__(self, controller):
        super().__init__(parent=None)
        self.setWindowTitle("PyCalculator")
        self._createCentralWidgetCalculator()
        self._createToolBar()
        self.setFixedSize(450, 450)
        self.controller = controller
        self.clearNextSymbol = False

    def _createCentralWidgetCalculator(self):
        centralWidget = QWidget(self)
        centralWidget.externalId = 'Calculator'
        centralWidget.setLayout(self.createLayoutCalculator())
        self.setCentralWidget(centralWidget)
        centralWidget.show()

    def _createCentralWidgetHistory(self):
        data = self.controller.getHistory()
        headers = ['Calculation', 'Result', 'Date']
        centralWidget = QTableView()
        centralWidget.externalId = 'History'
        model = TableModel(data, headers)
        centralWidget.setModel(model)
        centralWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        centralWidget.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        centralWidget.verticalHeader().setVisible(False)
        self.setCentralWidget(centralWidget)
        centralWidget.show()

    def SetOutputDisplay(self, text):
        self.outputDisplay.setText(text)

    def clearOutputDisplay(self):
        self.outputDisplay.setText("")

    def _createToolBar(self):
        toolbar = QToolBar("My main toolbar")
        self.addToolBar(toolbar)

        buttonShowCalculator = QtGui.QAction("Calculator", self)
        buttonShowCalculator.setStatusTip("Show calculator")
        buttonShowCalculator.triggered.connect(self.showCalculator)
        toolbar.addAction(buttonShowCalculator)

        buttonShowHistory = QtGui.QAction("History", self)
        buttonShowHistory.setStatusTip("Show history")
        buttonShowHistory.triggered.connect(self.showHistory)
        toolbar.addAction(buttonShowHistory)

        buttonDelHistory = QtGui.QAction("Delete history", self)
        buttonDelHistory.setStatusTip("Delete history")
        buttonDelHistory.triggered.connect(self.deleteHistory)
        toolbar.addAction(buttonDelHistory)

    def showCalculator(self):
        current = self.centralWidget()
        if current.externalId != 'Calculator':
            self.takeCentralWidget()
            self._createCentralWidgetCalculator()

    def showHistory(self):
        current = self.centralWidget()
        if not self.controller.hasHistoryRows():
            self.showErrorPopup(text="No history data !")
            return None
        if current.externalId != 'History':
            self.takeCentralWidget()
            self._createCentralWidgetHistory()

    def deleteHistory(self):
        self.controller.deleteHistory()
        self.showCalculator()


    def sendSymbol(self, symbol):
        def processResult():
            if self.clearNextSymbol:
                self.clearNextSymbol = False
                self.clearOutputDisplay()
            output = self.controller.receptSymbol(self.outputDisplay.text(), symbol)
            if symbol == '=':
                self.clearNextSymbol = True
            if output is not None:
                self.SetOutputDisplay(output)
            else:
                self.clearOutputDisplay()
                self.showErrorPopup()

        return processResult

    def showErrorPopup(self, text="Invalid syntax"):
        dlg = QDialog(self)
        dlg.setWindowTitle("Error")
        errorMsg = QLabel(f"<h1 style='color:red;'>{text}</h1>", parent=dlg)
        errorMsg.move(40, 15)
        dlg.setFixedSize(300, 80)
        dlg.exec()

    def createLayoutCalculator(self):
        layout = QGridLayout()

        self._createOutputDisplay()
        layout.addWidget(self.outputDisplay, 0,0,1,5)

        self._createButtons(layout)

        return layout

    def _createOutputDisplay(self):
        outputDisplay = QLineEdit()
        self.outputDisplay = outputDisplay
        self.outputDisplay.setReadOnly(True)
        self.outputDisplay.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.outputDisplay.setFixedHeight(75)
        self.outputDisplay.setStyleSheet("QLineEdit { border-radius:7px; }")
        outputFont = self.outputDisplay.font()
        outputFont.setPointSize(25)
        self.outputDisplay.setFont(outputFont)

    def _createButtons(self, layout):
        widgetsToAdd = [
            [('7'), ('8'), ('9'), ('/'), ('C')],
            [('4'), ('5'), ('6'), ('*'), ('(')],
            [('1'), ('2'), ('3'), ('-'), (')')],
            [('0'), ('00'), ('.'), ('+'), ('=')]
        ]
        for i, line in enumerate(widgetsToAdd):
            for j, widget in enumerate(line):
                newWidget = QPushButton(widget)
                newWidget.setFixedSize(75, 75)
                newWidget.clicked.connect(self.sendSymbol(widget))
                layout.addWidget(newWidget, i + 1, j)


class TableModel(QAbstractTableModel):
    def __init__(self, data, colHeaders):
        super(TableModel, self).__init__()
        self._data = data
        self._colHeaders = colHeaders


    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            #import pdb; pdb.set_trace()
            return self._data[index.row()][index.column()]

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return self._colHeaders[section]
        return super().headerData(section, orientation, role)

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._data[0])


