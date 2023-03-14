from PyQt6.QtWidgets import (
    QApplication,
)
from pycalculator.views.view import Window
from pycalculator.models.model import Calculator, databaseHandler

class Controller:
    def __init__(self):
        self.app =  QApplication([])
        self.Calculator = Calculator()
        self.window = Window(controller=self)
        self.window.show()

    def startApp(self):
        return self.app.exec()

    def receptSymbol(self, output, symbol):
        return self.Calculator.processSymbol(output, symbol)

    def getHistory(self):
        return self.Calculator.getHistoryRows()

    def hasHistoryRows(self):
        return self.Calculator.hasHistoryRows()

    def deleteHistory(self):
        return self.Calculator.deleteHistoryRows()        

