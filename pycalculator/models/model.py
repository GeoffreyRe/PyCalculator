import os
import sys
from datetime import datetime
from PyQt6.QtSql import QSqlDatabase, QSqlQuery



class Calculator:

	def __init__(self):
		self.databaseHandler = databaseHandler()

	def processSymbol(self, output, symbol):
		if symbol == "=":
			result = self.processExpression(output)
			if result is not None:
				self.databaseHandler.insertRow([output, result])
			return result
		if symbol == "C":
			return ""

		return output + symbol

	def processExpression(self, expr):
		try:
			return str(eval(expr))
		except SyntaxError:
			return None

	def getHistoryRows(self):
		return self.databaseHandler.getRows(limit=10)

	def deleteHistoryRows(self):
		return self.databaseHandler.deleteRows()

	def hasHistoryRows(self):
		return bool(self.databaseHandler.getRows(limit=1))


class databaseHandler:
	def __init__(self):
		self.con = QSqlDatabase.addDatabase("QSQLITE")
		self.con.setDatabaseName(self.getDbFileLocation())
		self.openConnection()
		self.createTables()

	def openConnection(self):
		if not self.con.isOpen():
			self.con.open()

		if not self.con.isOpen():
			sys.exit(1)
	
	def closeConnection(self):
		if self.con.isOpen():
			self.con.close()

	def getDbFileLocation(self):
		root_path = os.path.dirname(os.path.dirname(__file__))

		dbDir = os.path.join(root_path, 'db')
		if not os.path.exists(dbDir):
			os.makedirs(dbDir)

		return os.path.join(dbDir, 'pycalculator.sqlite')

	def createTables(self):
		createTableQuery = QSqlQuery()
		createTableQuery.exec(
		    """
		    CREATE TABLE IF NOT EXISTS calculation_history (
		        id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
		        calculation VARCHAR(120) NOT NULL,
		        result VARCHAR(30) NOT NULL,
		        date_created TIMESTAMP NOT NULL
		    )
		    """
		)

	def insertRow(self, values):
		values.append(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
		insertRow = QSqlQuery()
		r = insertRow.prepare("""
			INSERT INTO calculation_history (calculation, result, date_created)
			VALUES (?, ?, ?)
		""")
		for v in values:
			insertRow.addBindValue(v)
		insertRow.exec()

	def deleteRows(self, ids=None, all=True):
		ids = map(str, ids or [])
		query = "DELETE FROM calculation_history"
		if not all and ids:
			query += f" WHERE id in ({','.join(ids)})"

		deleteRows = QSqlQuery()

		deleteRows.exec(query)

	def getRows(self, all=True, ids=None, limit=None):
		ids = map(str, ids or [])
		query = "SELECT id, calculation, result, date_created FROM calculation_history"
		query += " ORDER BY date_created DESC "
		if not all and ids:
			query += f" WHERE id in ({','.join(ids)}) "

		getRows = QSqlQuery()

		getRows.exec(query)
		return_lst = []
		
		while getRows.next():
			return_lst.append((
				getRows.value('calculation'),
				getRows.value('result'),
				getRows.value('date_created')
			))

		return return_lst[:limit] if limit else return_lst





