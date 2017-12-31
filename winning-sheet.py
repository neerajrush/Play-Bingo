import sqlite3
import random
from flask_table import Table, Col

def winning_sheet_html_table(drawn_numbers_list):

	class ItemTable(Table):
		c1 = Col('H')
		c2 = Col('O')
		c3 = Col('U')
		c4 = Col('S')
		c5 = Col('E')

	# Get some objects
	class Item(object):
		def __init__(self, c1, c2, c3, c4, c5):
			self.c1 = c1
			self.c2 = c2
			self.c3 = c3
			self.c4 = c4
			self.c5 = c5

	items = [Item(' ', ' ', ' ', ' ', ' '),
		 Item(' ', ' ', ' ', ' ', ' '),
		 Item(' ', ' ', ' ', ' ', ' '),
		 Item(' ', ' ', ' ', ' ', ' '),
		 Item(' ', ' ', ' ', ' ', ' ')]

	sheet_column = []

	for x in range(0, 5):
		sheet_column.append([])
		for y in range(0, 5):
			sheet_column[x].append(' ')

	for a_number in drawn_numbers_list:
		if a_number < 26:
			if ' ' in sheet_column[0]:
				sheet_column[0].append(a_number)
				sheet_column[0].sort()
		if a_number > 25 and a_number < 51:
			if ' ' in sheet_column[1]:
				sheet_column[1].append(a_number)
				sheet_column[1].sort()
		if a_number > 50 and a_number < 76:
			if ' ' in sheet_column[2]:
				sheet_column[2].append(a_number)
				sheet_column[2].sort()
		if a_number > 75 and a_number < 101:
			if ' ' in sheet_column[3]:
				sheet_column[3].append(a_number)
				sheet_column[3].sort()
		if a_number > 100 and a_number < 126:
			if ' ' in sheet_column[4]:
				sheet_column[4].append(a_number)
				sheet_column[4].sort()
	idx = 0
	while idx < len(sheet_column):
		items[idx] = Item(sheet_column[idx][0], sheet_column[idx][1], sheet_column[idx][2], sheet_column[idx][3], sheet_column[idx][4])
		idx += 1

	return ItemTable(items)

#drawn_numbers_list = [ 21, 34, 45, 75 ]

#theTable = winning_sheet_html_table(drawn_numbers_list)
