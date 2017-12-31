import random
import sqlite3
from generate_sheets import MAX_GRID_VALUE

def get_drawn_numbers_list(db_name):
	drawn_numbers_list = []
	with sqlite3.connect(db_name) as connection:
		c = connection.cursor()
		#c.execute("""DROP TABLE drawn_numbers""")
		#c.excute("""CREATE TABLE drawn_numbers (NUMBER INTEGER)""")

		result_set = c.execute('SELECT * from drawn_numbers') # results set is tuples

		for row in result_set:
			drawn_numbers_list.append(row[0])

	return drawn_numbers_list

def get_last_drawn_number(db_name):
	drawn_list = get_drawn_numbers_list(db_name)
	list_len = len(drawn_list)
	if list_len == 0:
		return " "
	else:
		return drawn_list[list_len-1]

def add_drawn_number(db_name, drawn_number):
    with sqlite3.connect(db_name) as connection:
        c = connection.cursor()
        query = "INSERT INTO drawn_numbers values (" + str(drawn_number) + ")" 
        result_set = c.execute(query)

def delete_drawn_numbers(db_name):
    with sqlite3.connect(db_name) as connection:
        c = connection.cursor()
        query = "DELETE FROM drawn_numbers" 
        result_set = c.execute(query)

def draw_a_number():
	drawn_list = get_drawn_numbers_list('tambola.db')
	x = 0
	drawn_number = 0
	while x <= MAX_GRID_VALUE:
		drawn_number = random.randint(1, MAX_GRID_VALUE)
		x += 1
		if drawn_number in drawn_list:
			continue
		else:
			drawn_list.append(drawn_number)
			add_drawn_number('tambola.db', drawn_number)
			break
	return drawn_number

#print(get_last_drawn_number('tambola.db'))
#add_drawn_number('tambola.db', 11)
#print(get_last_drawn_number('tambola.db'))
#delete_drawn_numbers('tambola.db')

#print (draw_a_number())
#print (get_drawn_numbers_list('tambola.db'))
