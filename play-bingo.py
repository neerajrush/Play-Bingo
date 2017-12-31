import sqlite3
#import Queue
import queue
import threading, time
import random
import players_db_list
import assign_sheets
import draw_a_number
import generate_sheets
from generate_sheets import gridSize, MAX_GRID_VALUE;
from flask_table import Table, Col

drawNumberQ = queue.Queue()

def init_hitters_list(hitters_list, hitters_row_list, players_names_list):
	for player_name in players_names_list:
    		hitters_list[player_name] = []
    		hitters_row_list[player_name] = []

def firstHouse(hitters_list, winners_names):
    	gridsCount = gridSize * gridSize

    	for name in hitters_list:
        	xlen = len(hitters_list[name])
        	if xlen == gridsCount:
            		print("WON ==> FULL FOUND MATCH FOUND, Player's Name: ", name)
            		winners_names.append(name)
            		return True
    	return False

def findAnyTwoRowsMatch(hitters_row_list, winners_names):
    	for name in hitters_row_list:
        	h = hitters_row_list[name]
        	matchCount = 0
        	for x in range(0, gridSize):
            		if h.count(x) == gridSize:
                		matchCount += 1
            		if matchCount == 2:
                		print("WON ==> TWO COLUMNS MATCH FOUND, Player's Name: ", name)
                		winners_names.append(name)
                		return True
    	return False

def mark_hitters(value_drawn, hitters_list, hitters_row_list, players_assigned_sheets):
	for name in players_assigned_sheets:
		player_sheet = players_assigned_sheets[name]
		match_found = False
		for column in player_sheet:
			if value_drawn in column:
				#print ("Draw: ", value_drawn, " MATCH:", name,  player_sheet)
				hitters_list[name].append(value_drawn)
				for row in range(0, len(column)):
					if column[row] == value_drawn:
						hitters_row_list[name].append(row)
						match_found = True
					if match_found == True:
						break
			if match_found == True:
				break
	return

def add_winner_to_db(db_name, player_name, player_sheet):
	with sqlite3.connect(db_name) as connection:
		c = connection.cursor()
		query = 'INSERT INTO winners values ("' + player_name + '", "' + '{0}'.format(player_sheet) + '");'
		result_set = c.execute(query)

def delete_winners_from_db(db_name):
	with sqlite3.connect(db_name) as connection:
		c = connection.cursor()
		query = "DELETE FROM winners;" 
		result_set = c.execute(query)

def get_winners_from_db(db_name):
	with sqlite3.connect(db_name) as connection:
		c = connection.cursor()
		#c.execute("""DROP TABLE winners""")
		#c.excute("""CREATE TABLE winners (NAME TEXT, VALUE BLOB)""")

		result_set = c.execute('SELECT * from winners;')

		winner_names  = []
		winner_sheets = []

		for row in result_set:
			winner_names.append('{0}'.format(row[0]))
			winner_sheets.append(eval('{0}'.format(row[1])))

		#winning_sheets = winning_sheets.fromkeys(winner_names)

		#x = 0
		#for name in winning_sheets:
			#winning_sheets[name] = eval(winner_sheets[x])
			#x += 1

		return winner_names, winner_sheets

def verify_winners(value_drawn, hitters_list, hitters_row_list, winners_names, players_assigned_sheets, xCount):

	mark_hitters(value_drawn, hitters_list, hitters_row_list, players_assigned_sheets)

	if len(winners_names) == 0 and findAnyTwoRowsMatch(hitters_row_list, winners_names) == True:
		print ("KUDES ...BLAST..TWO COLUMNS DRAW OVER..Draw Count: ", xCount, "Lucky number: ", value_drawn)
		add_winner_to_db('tambola.db', winners_names[0], players_assigned_sheets[winners_names[0]])
	if firstHouse(hitters_list, winners_names) == True:
		print ("KUDES ...BLAST..FULL HOUSE DRAW OVER..Draw Count: ", xCount, " Lucky number: ", value_drawn)
		add_winner_to_db('tambola.db', winners_names[1], players_assigned_sheets[winners_names[1]])

def play_tambola():
	hitters_list = {}
	hitters_row_list = {}
	winners_names = []
	drawn_numbers_list = []
	players_assigned_sheets = {}
	x = 0
	value_drawn = 0
	initialize = True
	print ("INFO: Thread created to find the winner.")
	while True:
		if not drawNumberQ.empty():
			value_drawn = drawNumberQ.get()
			#print("D:", value_drawn)

		if value_drawn == 0 or value_drawn in drawn_numbers_list:
			continue

		if initialize == True:
			print ("INFO: Thread initializing lists to find the winner.")
			players_names_list = players_db_list.get_players_list('tambola.db')
			nplayers = len(players_names_list)

			init_hitters_list(hitters_list, hitters_row_list, players_names_list)

			tambola_sheets_list = generate_sheets.get_generated_sheets('tambola.db', nplayers)
			players_assigned_list, assigned_sheets = assign_sheets.get_assigned_sheets('tambola.db')

			players_assigned_sheets = players_assigned_sheets.fromkeys(players_assigned_list.keys())

			for player_sheet_name in assigned_sheets:
				player_name, sheet_id = player_sheet_name.split('--')
				players_assigned_sheets[player_name] = tambola_sheets_list[sheet_id]

			initialize = False

        	#print (players_assigned_sheets)

		x += 1
		drawn_numbers_list.append(value_drawn)
		print("DRAW NUMBER LIST: ", drawn_numbers_list)
		verify_winners(value_drawn, hitters_list, hitters_row_list, winners_names, players_assigned_sheets, x)
		if len(winners_names) == 2:
			break

	print(winners_names)

def enque_the_drawn_number(drawNumberQ, drawn_number):
	drawNumberQ.put(drawn_number) 
	#print ("INFO: Enque ==> ", drawn_number)

def create_play_tambola_thread():
	threading.Thread(target=play_tambola).start()

def draw_a_number():
	for x in range(1, MAX_GRID_VALUE):
		enque_the_drawn_number(x)
		time.sleep(1)

#create_play_tambola_thread(drawQ)

#for x in range(1, 10):
	#enque_the_drawn_number(drawQ, x)
