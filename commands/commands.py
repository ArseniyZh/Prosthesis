import sys
from database.database import DatabaseManager

db = DatabaseManager('states.db')

# Создание таблицы
class CreateTableCommand:
	def execute(self):
		db.create_table('states', {
			'id': 'integer primary key autoincrement',
			'name' : 'text not null',
			'elbow' : 'integer',
			'wrist_y' : 'integer',
			'wrist_x' : 'integer',
			'finger_1' : 'integer',
			'finger_2' : 'integer',
			'finger_3' : 'integer',
			'finger_4' : 'integer',
			'finger_5' : 'integer'
			})


# Добавление состояние
class AddCommands:
	def execute(self, data):
		db.add('states', data)


# Удаление состояние
class DeleteCommand:
	def execute(self, data):
		db.delete('states', {'name' : data})


# Вывод состояний (сортировка по имени)
class ListCommand:
	def __init__(self, order_by = 'name'):
		self.order_by = order_by

	def execute(self):
		return db.select('states', order_by = self.order_by).fetchall()


# Проверка: есть ли состояние в базе
class CheckStateInDatabase:
	def execute(self, data):
		return db.check('states', {'name' : data})


# Обновляет состояние в базе
class EditCommand:
	def execute(self, data):
		db.update(
			'states',
			{'name' : data['name']},
			data
			)