import sqlite3
import random
from flask_table import Table, Col

def assign_sheets_to_players(players_list, sheets_list):
	players_sheets = {}
	assigned_list = []
	players_sheets = players_sheets.fromkeys(players_list)
	nPlayers = len(players_list)
	x = 0
	for player in players_list:
		val = random.randint(0, nPlayers)
		if val in players_sheets:
        		continue
		else:
			players_sheets[player] = sheets_list[x]
			assigned_list.append(player + "--" + sheets_list[x])
		x += 1

	return players_sheets, assigned_list

def assigned_sheets_list_html_table(assigned_sheets_list):
	class ItemTable(Table):
		classes = ['assigned_sheets_table']
		c1 = Col('*** ASSIGNED SHEETS ARE ***')

	class Item(object):
    		def __init__(self, c1):
        		self.c1 = c1

	items = []
	for sheet in assigned_sheets_list:
		items.append(Item(sheet))
	return ItemTable(items)

def get_assigned_sheets(db_name):
	assigned_sheets_list = {}
	with sqlite3.connect(db_name) as connection:
		c = connection.cursor()
		#c.execute("""DROP TABLE assigned_sheets_list""")
		#c.excute("""CREATE TABLE assigned_sheets_list (PLAYER_NAME TEXT, SHEET_ID TEXT)""")

		result_set = c.execute('SELECT * from assigned_sheets_list') # results set is tuples

		assigned_sheets_keys = []

		for row in result_set:
			assigned_sheets_keys.append('{0}'.format(row[0]))

		assigned_sheets_list = assigned_sheets_list.fromkeys(assigned_sheets_keys)

		result_set = c.execute('SELECT * from assigned_sheets_list') # results set is tuples

		assigned_list = []

		for row in result_set:
			assigned_sheets_list['{0}'.format(row[0])] = '{0}'.format(row[1])
			assigned_list.append('{0}'.format(row[0]) + "--" + '{0}'.format(row[1]))

	return assigned_sheets_list, assigned_list

def add_assigned_sheet(db_name, player_name, sheet_id):
	with sqlite3.connect(db_name) as connection:
		c = connection.cursor()
		query = "INSERT INTO assigned_sheets_list values (" + "'" + player_name + "'" + "," + "'" + sheet_id + "'" + ")" 
		result_set = c.execute(query)

def delete_assigned_sheets(db_name):
	with sqlite3.connect(db_name) as connection:
		c = connection.cursor()
		result_set = c.execute('DELETE FROM assigned_sheets_list')

def persist_all_assigned_sheets(db_name, assinged_sheets):
	with sqlite3.connect(db_name) as connection:
		c = connection.cursor()
		for assigned_sheet in assinged_sheets:
			player_name, sheet_id = assigned_sheet.split("--")
			query = "INSERT INTO assigned_sheets_list values (" + "'" + player_name + "'" + "," + "'" + sheet_id + "'" + ")" 
			result_set = c.execute(query)

#players_list = [ 'N Sharma', 'R Sharma', 'A Sharma' ]
#sheets_list = [ 'SHEET-10', 'SHEET-1', 'SHEET-5', 'SHEET-7', 'SHEET-11' ]
#players_assinged_sheets, assigned_list = assign_sheets_to_players(players_list, sheets_list)
#print(players_assinged_sheets)
#print(assigned_list)

#for assigned_sheet in assigned_list:
	#player_name, sheet_id = assigned_sheet.split("--")
	#add_assigned_sheet('tambola.db', player_name, sheet_id)

#assigned_sheets_list, assigned_list = get_assigned_sheets('tambola.db')
#print(assigned_sheets_list)
#print(assigned_list)

#delete_assigned_sheets('tambola.db')
