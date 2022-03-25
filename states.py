from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from commands import commands


main_bg_color = 'gray' # Основной задний цвет
main_fg_color = 'white' # Основной передний цвет
main_font = 'Times 20' # Основной шрифт

# Сохраняет/обновляет состояние
def save_state():
	# Добавление
	if (states_list.current() == 0) and (name_state.get() != 'Введите название') and (check_state_in_database()): # Если выбраны параметры для добавления и\или записи нет в БД
		data = {
				'name' : name_state.get(),
				'elbow' : elbow.get(),
				'wrist_x' : wrist_y.get(),
				'wrist_y' : wrist_x.get(),
				'finger_1' : finger_1.get(),
				'finger_2' : finger_2.get(),
				'finger_3' : finger_3.get(),
				'finger_4' : finger_4.get(),
				'finger_5' : finger_5.get()
				}

		commands.AddCommands().execute(data)
		refresh_states()
		messagebox.showinfo('ЗАПИСЬ', f'Запись успешно добавлена!')

	# Обновление
	elif (states_list.current() != 0) and (name_state.get() != 'Введите название') and (not check_state_in_database()): # Если выбраны параметры не для добавления и запись есть в БД 
		data = {
				'name' : name_state.get(),
				'elbow' : elbow.get(),
				'wrist_x' : wrist_y.get(),
				'wrist_y' : wrist_x.get(),
				'finger_1' : finger_1.get(),
				'finger_2' : finger_2.get(),
				'finger_3' : finger_3.get(),
				'finger_4' : finger_4.get(),
				'finger_5' : finger_5.get()
				}

		commands.EditCommand().execute(data)
		refresh_states()	
		messagebox.showinfo('ОБНОВЛЕНИЕ', f'Вы отредактировали настройки.')

	# Исключение
	elif (states_list.current() == 0) and (name_state.get() == 'Введите название'): # Если выбраны параметры для добавления и пользователь не ввёл название
		messagebox.showinfo('ПОДСКАЗКА', f'Чтобы добавить запись, нужно выбрать "Добавить состояние" в выпадающем меню и ввести название этого состояния.')

	# Исключение
	elif not check_state_in_database(): # Если выбраны параметры для добавления и запись есть в БД
		messagebox.showinfo('ОШИБКА', f'Запись с таким именем уже существует.')


# Удаление состояния
def delete_state():
	# Удаление выбранной записи
	if states_list.current() != 0:
		data = name_state.get()
		commands.DeleteCommand().execute(data)
		refresh_states()
		messagebox.showinfo('УДАЛЕНИЕ', f'Запись успешно удалена.')

	# Исключение
	elif (states_list.current() == 0) and (name_state.get() == 'Введите название'): # Если выбраны параметры для добавления и пользователь не ввёл название
		messagebox.showinfo('ПОДСКАЗКА', f'Чтобы удалить запись, нужно выбрать запись в выпадающем списке.')


# Проверка на наличие записи в БД
def check_state_in_database():
	return commands.CheckStateInDatabase().execute(name_state.get())


# Получение значений для выпадающего меню
def get_values():
	values = ['Добавить состояние'] + [f'{i[1]}' for i in commands.ListCommand().execute()]

	return [value for value in values]


# Установка значений для слайдеров и поля для ввода
def set_values(self):
	# Значения по умолчанию
	if states_list.current() == 0:
		name_state['state'] = 'normal'
		name_state.delete(0, END)
		name_state.insert(0, 'Введите название')

		wrist_y.set(0)
		wrist_x.set(0)
		elbow.set(0)
		finger_1.set(0)
		finger_2.set(0)
		finger_3.set(0)
		finger_4.set(0)
		finger_5.set(0)

	# Значения из выбранной записи
	else:
		part = states_list.current() - 1
		values = commands.ListCommand().execute()

		name_state.delete(0, END)
		name_state.insert(0, values[part][1])
		name_state['state'] = 'disabled'

		elbow.set(values[part][2])
		wrist_x.set(values[part][3])
		wrist_y.set(values[part][4])
		finger_1.set(values[part][5])
		finger_2.set(values[part][6])
		finger_3.set(values[part][7])
		finger_4.set(values[part][8])
		finger_5.set(values[part][9])


# Установка значений по умолчанию для выпадающего меню и поля для ввода
def refresh_states():
	states_list.current(0)
	states_list['values'] = get_values()
	set_values('')
	name_state.delete(0, END)
	name_state.insert(0, 'Введите название')



# Создание таблицы
commands.CreateTableCommand().execute()

# Главное окно
root = Tk()
root['bg'] = main_bg_color
# Размеры окна
WIDTH = 800
HEIGHT = 800
# Вычисление середины окна
POS_X = root.winfo_screenwidth() // 2 - WIDTH // 2
POS_Y = root.winfo_screenheight() // 2 - HEIGHT // 2
# Заголовок
root.title('Prosthesis')
#Запрет изменения размера окна
root.resizable(False, False)
#Расположение на экране
root.geometry(f'{WIDTH}x{HEIGHT}+{POS_X}+{POS_Y}')

# Выбор состояния
states_list = ttk.Combobox(root, width = 50)
states_list['values'] = get_values()
states_list['state'] = 'readonly'
states_list.bind("<<ComboboxSelected>>", set_values)

states_list.place(x = 225, y = 50)
states_lbl = Label(text = 'ВЫБОР СОСТОЯНИЯ', font = main_font, bg = main_bg_color, fg = main_fg_color, relief = 'flat')
states_lbl.place(x = 250, y = 10)

# Настройки руки
# Пальцы
finger_lbl = Label(text = 'ПАЛЬЦЫ', font = main_font, bg = main_bg_color, fg = main_fg_color, relief = 'flat')
finger_lbl.place(x = 200, y = 110)
# Большой палец
finger_1_lbl = Label(text = 'БОЛЬШОЙ', font = main_font, bg = main_bg_color, fg = main_fg_color, relief = 'flat')
finger_1_lbl.place(x = 45, y = 170)
finger_1 = Scale(root, orient = HORIZONTAL, length = 300, from_ = -60, to = 60, tickinterval = 10, resolution = 1)
finger_1.place(x = 45, y = 200)
# Указательный палец
finger_2_lbl = Label(text = 'УКАЗАТЕЛЬНЫЙ', font = main_font, bg = main_bg_color, fg = main_fg_color, relief = 'flat')
finger_2_lbl.place(x = 45, y = 270)
finger_2 = Scale(root, orient = HORIZONTAL, length = 300, from_ = -60, to = 60, tickinterval = 10, resolution = 1)
finger_2.place(x = 45, y = 300)
# Средний палец
finger_3_lbl = Label(text = 'СРЕДНИЙ', font = main_font, bg = main_bg_color, fg = main_fg_color, relief = 'flat')
finger_3_lbl.place(x = 45, y = 370)
finger_3 = Scale(root, orient = HORIZONTAL, length = 300, from_ = -60, to = 60, tickinterval = 10, resolution = 1)
finger_3.place(x = 45, y = 400)
# Безымянный палец
finger_4_lbl = Label(text = 'БЕЗЫМЯННЫЙ', font = main_font, bg = main_bg_color, fg = main_fg_color, relief = 'flat')
finger_4_lbl.place(x = 45, y = 470)
finger_4 = Scale(root, orient = HORIZONTAL, length = 300, from_ = -60, to = 60, tickinterval = 10, resolution = 1)
finger_4.place(x = 45, y = 500)
# Мезинец палец
finger_5_lbl = Label(text = 'МИЗИНЕЦ', font = main_font, bg = main_bg_color, fg = main_fg_color, relief = 'flat')
finger_5_lbl.place(x = 45, y = 570)
finger_5 = Scale(root, orient = HORIZONTAL, length = 300, from_ = -60, to = 60, tickinterval = 10, resolution = 1)
finger_5.place(x = 45, y = 600)

# Поворот руки
arm_lbl = Label(text = 'ПОВОРОТ РУКИ', font = main_font, bg = main_bg_color, fg = main_fg_color, relief = 'flat')
arm_lbl.place(x = 450, y = 110)
# Локоть
elbow_lbl = Label(text = 'ЛОКОТЬ', font = main_font, bg = main_bg_color, fg = main_fg_color, relief = 'flat')
elbow_lbl.place(x = 450, y = 170)
elbow = Scale(root, orient = HORIZONTAL, length = 300, from_ = -60, to = 60, tickinterval = 10, resolution = 1)
elbow.place(x = 450, y = 200)
# Запястье
wrist_lbl = Label(text = 'ЗАПЯСТЬЕ', font = main_font, bg = main_bg_color, fg = main_fg_color, relief = 'flat')
wrist_lbl.place(x = 450, y = 270)
wrist_x = Scale(root, orient = HORIZONTAL, length = 300, from_ = -60, to = 60, tickinterval = 10, resolution = 1)
wrist_x.place(x = 450, y = 300)
wrist_y = Scale(root, orient = VERTICAL, length = 300, from_ = -60, to = 60, tickinterval = 10, resolution = 1)
wrist_y.place(x = 575, y = 360)

# Кнопки
# Кнопка сохранения/обновления
save_btn = startButton = Button(text = 'СОХРАНИТЬ', font = main_font, width = 50, background = main_bg_color, fg = main_fg_color, command = lambda: save_state())
save_btn.place(x = 20, y = 740)
# Кнопка удаления
delete_btn = startButton = Button(text = 'УДАЛИТЬ', font = main_font, width = 25, background = main_bg_color, fg = main_fg_color, command = lambda: delete_state())
delete_btn.place(x = 20, y = 680)

# Поле для ввода
default_text = StringVar()
default_text.set('Введите название')
name_state = Entry(font = 'Times 31', bg = 'white', fg = 'black', relief = 'flat', textvariable = default_text, width = 17)
name_state.place(x = 410,y = 682)

refresh_states()

root.mainloop()