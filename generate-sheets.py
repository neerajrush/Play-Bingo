import sqlite3
import random
from flask_table import Table, Col

RANDOM_FACTOR = 5
gridSize = 5

MAX_GRID_VALUE = gridSize * gridSize * RANDOM_FACTOR

def createTambolaSheet():
    tambola_grid = []
    column = 0
    while column < gridSize:
        tambola_grid.append([])
        row = 0
        while row < gridSize:
            row_start_value = (column * gridSize * RANDOM_FACTOR) + 1
            row_end_value = row_start_value + (row * RANDOM_FACTOR)
            while True:
                val = random.randint(row_start_value, row_end_value)
                if val in tambola_grid[column]:
                    continue
                else:
                    tambola_grid[column].append(val)
                break
            row += 1
        tambola_grid[column].sort()
        column += 1
    return tambola_grid

def generate_sheets(nPlayers):
	tambola_sheets_count = nPlayers * 3
	tambola_sheets = []
	tambola_sheets_id = []
	idx = 0
	while idx < tambola_sheets_count:
		tambola_sheets.append(createTambolaSheet())
		sheet_id = '{0}'.format("SHEET-" + str(idx+1))
		tambola_sheets_id.append(sheet_id)
		idx += 1

	tambola_sheets_list = {}
	tambola_sheets_list = tambola_sheets_list.fromkeys(tambola_sheets_id)
	idx = 0
	for sheet in tambola_sheets_list:
		tambola_sheets_list[sheet] = tambola_sheets[idx]
		idx += 1
	return tambola_sheets_list

def sheets_list_html_table(sheets_list):
	class ItemTable(Table):
    		c1 = Col('*** PRINTED SHEETS ARE ***')

	class Item(object):
    		def __init__(self, c1):
        		self.c1 = c1

	items = []
	for sheet in sheets_list:
		items.append(Item(sheet))
	return ItemTable(items)

def a_sheet_html_table(a_sheet):
	class ItemTable(Table):
	    	c1 = Col('H')
	    	c2 = Col('O')
	    	c3 = Col('U')
	    	c4 = Col('S')
	    	c5 = Col('E')

	class Item(object):
		def __init__(self, col_arr):
			self.c1 = col_arr[0]
			self.c2 = col_arr[1]
			self.c3 = col_arr[2]
			self.c4 = col_arr[3]
			self.c5 = col_arr[4]
	items = []
	for column in a_sheet:
		items.append(Item(column))
	return ItemTable(items)

def get_generated_sheets(db_name, nplayers):
	tambola_sheets_list = {}
	sheet_names_list = []
	sheet_value_list = []
	with sqlite3.connect(db_name) as connection:
		c = connection.cursor()
		#c.execute("""DROP TABLE sheet_details""")
		#c.excute("""CREATE TABLE sheet_details (NAME TEXT, VALUE TEXT)""")

		result_set = c.execute('SELECT * from sheet_details;')

		for row in result_set:
			sheet_names_list.append('{0}'.format(row[0]))
			sheet_value_list.append('{0}'.format(row[1]))

	if len(sheet_names_list) == 0:
		print("MSG: No previously generated sheets found in DB. So generating new ones.")
		tambola_sheets_list = generate_sheets(nplayers)
		persist_generated_sheets('tambola.db', tambola_sheets_list)
		return tambola_sheets_list

	tambola_sheets_list = tambola_sheets_list.fromkeys(sheet_names_list)

	x = 0
	for name in tambola_sheets_list:
		tambola_sheets_list[name] = eval(sheet_value_list[x])
		x += 1

	return tambola_sheets_list

def persist_generated_sheets(db_name, tambola_sheets_list):
	with sqlite3.connect(db_name) as connection:
		c = connection.cursor()

		for name in tambola_sheets_list:
			value = tambola_sheets_list[name]
			query = 'INSERT INTO sheet_details values ("' + name + '", "' + '{0}'.format(value) + '");'
			result_set = c.execute(query)

def delete_generated_sheets_from_db(db_name):
	with sqlite3.connect(db_name) as connection:
		c = connection.cursor()
		query = 'DELETE from sheet_details;'
		result_set = c.execute(query)

#tambola_sheets_list = get_generated_sheets('tambola.db', 5)

#print (tambola_sheets_list)

#a_sheet = eval('[[1, 6, 7, 11, 14], [26, 29, 30, 34, 35], [51, 52, 53, 65, 67], [76, 78, 84, 85, 91], [101, 102, 106, 108, 111]]')

#print (a_sheet_html_table(a_sheet).__html__()) 

#print (a_sheet_html_table(tambola_sheets_list).__html__())
