import sqlite3
from flask_table import Table, Col

def get_players_list(db_name):
    players_list = []
    with sqlite3.connect(db_name) as connection:
        c = connection.cursor()
        #c.execute("""DROP TABLE players_list""")
        #c.excute("""CREATE TABLE players_list (PLAYER_NAME TEXT)""")

        result_set = c.execute('SELECT * from players_list') # results set is tuples

        for row in result_set:
            players_list.append('{0}'.format(row[0]))

    return players_list

def add_player(db_name, player_name):
    with sqlite3.connect(db_name) as connection:
        c = connection.cursor()
        query = "INSERT INTO players_list values (" + "'" + player_name + "'" + ")" 
        result_set = c.execute(query)

def delete_players(db_name):
    with sqlite3.connect(db_name) as connection:
        c = connection.cursor()
        result_set = c.execute('DELETE FROM PLAYERS_LIST')

def html_table(players_list):
	class ItemTable(Table):
    		c1 = Col('*** CURRENT PLAYERS ARE ***')

	class Item(object):
    		def __init__(self, c1):
        		self.c1 = c1

	items = []
	for player in players_list:
		items.append(Item(player))
	return ItemTable(items)

#add_player('tambola.db', 'NKS')
#add_player('tambola.db', 'AKS')
#add_player('tambola.db', 'PKS')

players_list = get_players_list('tambola.db')

#print(players_list)

#delete_players('tambola.db')
#players_list = get_players_list('tambola.db')

#print(players_list)
