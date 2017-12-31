from flask import Flask, render_template, redirect, request, session, flash, url_for
from functools import wraps
from flask_table import Table, Col
import json
import players_db_list
import generate_sheets
import assign_sheets
import draw_a_number
import winning_sheet
import play_tambola
from play_tambola import drawNumberQ

app = Flask(__name__)
app.secret_key = "Play-Bingo-Tambola"

#login required decorator
def login_required(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return f(*args, **kwargs)
		else:
		   	flash('You need to login first.')
		   	return redirect(url_for('login'))
	return wrap

@app.route("/")
@login_required
def home():
	return render_template('index.html')

@app.route('/welcome')
@login_required
def welcome():
	error = None
	if 'logged_in' in session:
		drawn_number = draw_a_number.get_last_drawn_number('tambola.db')
		drawn_numbers_list = draw_a_number.get_drawn_numbers_list('tambola.db')
		#print(drawn_numbers_list)
		grid_size = "5"
		winning_table = winning_sheet.winning_sheet_html_table(drawn_numbers_list)
		winner_names, winner_sheets = play_tambola.get_winners_from_db('tambola.db')
		win_1_name = '( Two Columns Match -- Winner -- YTD)' 
		win_2_name = '( Full House Match -- Winner -- YTD)'
		win_1_table = winning_sheet.winning_sheet_html_table([])
		win_2_table = winning_sheet.winning_sheet_html_table([])
		if len(winner_names) == 1:
			win_1_name = winner_names[0]
			win_1_table = generate_sheets.a_sheet_html_table(winner_sheets[0])
		if len(winner_names) == 2:
			win_1_name = winner_names[0]
			win_1_table = generate_sheets.a_sheet_html_table(winner_sheets[0])
			win_2_name = winner_names[1]
			win_2_table = generate_sheets.a_sheet_html_table(winner_sheets[1])
		return render_template('welcome.html', drawn_number=drawn_number, grid_size=grid_size, table=winning_table, winner_1_name=win_1_name, winner_1_table=win_1_table, winner_2_name=win_2_name, winner_2_table=win_2_table)
	else:
		flash('Sorry: loggin required.')
		return render_template('login.html', error=error)

@app.route('/players', methods=['GET', 'POST'])
@login_required
def players():
	#print(request)
	error = None
	playername = None
	if 'logged_in' in session:
		if request.method == 'POST':
			playername = request.form['playername'] 
			if request.form['playername'] is None:
				error = "Invalid Player's Name. Please try again."
				return render_template('players.html', error=error)
			else:
				playername = request.form['playername']
				players_db_list.add_player('tambola.db', playername)
				flash('You just entered new player: ' + playername)
				players_list = players_db_list.get_players_list('tambola.db')
				#print(players_list)
				return render_template('players.html', error=error, players_list=players_db_list.html_table(players_list))
		if request.method == 'GET':
			#print("MSG: Found logged in. GET")
			#return json.dumps({'status':'OK','players_list':players_list)
			players_list = players_db_list.get_players_list('tambola.db')
			#print(players_list)
			return render_template('players.html', error=error, players_list=players_db_list.html_table(players_list))
	else:
		flash('Sorry: loggin required.')
		return render_template('login.html', error=error)

	return render_template('players.html', error=error)

@app.route('/sheets', methods=['GET', 'POST'])
@login_required
def sheets():
	#print(request)
	error = None
	if 'logged_in' in session:
		if request.method == 'POST':
			#flash('You just about to create new tambola sheets.')
			players_list = players_db_list.get_players_list('tambola.db')
			#print(players_list)
			nplayers = len(players_list)
			tambola_sheets_list = generate_sheets.get_generated_sheets('tambola.db', nplayers)
			tambola_sheets = tambola_sheets_list.keys()
			first_sheet_name = tambola_sheets[0]
			a_sheet = tambola_sheets_list[first_sheet_name]
			return render_template('tambola_sheets.html', error=error, players_list=players_db_list.html_table(players_list), sheets=generate_sheets.sheets_list_html_table(tambola_sheets), a_sheet=generate_sheets.a_sheet_html_table(a_sheet), first_sheet_name=first_sheet_name)
		if request.method == 'GET':
			#return json.dumps({'status':'OK','players_list':players_list)
			players_list = players_db_list.get_players_list('tambola.db')
			#print(players_list)
			nplayers = len(players_list)
			tambola_sheets_list = generate_sheets.get_generated_sheets('tambola.db', nplayers)
			tambola_sheets = tambola_sheets_list.keys()
			first_sheet_name = tambola_sheets[0]
			a_sheet = tambola_sheets_list[first_sheet_name]
			return render_template('tambola_sheets.html', error=error, players_list=players_db_list.html_table(players_list), sheets=generate_sheets.sheets_list_html_table(tambola_sheets), a_sheet=generate_sheets.a_sheet_html_table(a_sheet), first_sheet_name=first_sheet_name)
	else:
		flash('Sorry: loggin required.')
		return render_template('login.html', error=error)

	return render_template('tambola_sheets.html', error=error)

@app.route('/assign_sheets', methods=['GET', 'POST'])
@login_required
def assign_sheets_to_players():
	#print(request)
	error = None
	if 'logged_in' in session:
		if request.method == 'POST':
			players_list = players_db_list.get_players_list('tambola.db')
			#print(players_list)
			nplayers = len(players_list)
			tambola_sheets_list = generate_sheets.get_generated_sheets('tambola.db', nplayers)
			tambola_sheets = tambola_sheets_list.keys()
			players_assigned_list, assigned_sheets = assign_sheets.assign_sheets_to_players(players_list, tambola_sheets)
			return render_template('assign_sheets.html', error=error, players_list=players_db_list.html_table(players_list), sheets=generate_sheets.sheets_list_html_table(tambola_sheets), assigned_sheets=assign_sheets.assigned_sheets_list_html_table(assigned_sheets))
		if request.method == 'GET':
			#return json.dumps({'status':'OK','players_list':players_list)
			players_list = players_db_list.get_players_list('tambola.db')
			#print(players_list)
			nplayers = len(players_list)
			tambola_sheets_list = generate_sheets.get_generated_sheets('tambola.db', nplayers)
			tambola_sheets = tambola_sheets_list.keys()
			players_assigned_list, assigned_sheets = assign_sheets.assign_sheets_to_players(players_list, tambola_sheets)
			return render_template('assign_sheets.html', error=error, players_list=players_db_list.html_table(players_list), sheets=generate_sheets.sheets_list_html_table(tambola_sheets), assigned_sheets=assign_sheets.assigned_sheets_list_html_table(assigned_sheets))
	else:
		flash('Sorry: loggin required.')
		return render_template('login.html', error=error)

	return render_template('assign_sheets.html', error=error)

@app.route('/display_sheets', methods=['GET', 'POST'])
@login_required
def display_sheets_assigned_to_players():
	#print(request)
	error = None
	if 'logged_in' in session:
		if request.method == 'POST':
			requested_sheet_name = request.get_data()
			players_list = players_db_list.get_players_list('tambola.db')
			nplayers = len(players_list)
			tambola_sheets_list = generate_sheets.get_generated_sheets('tambola.db', nplayers)
			tambola_sheets = tambola_sheets_list.keys()
			players_assigned_list, assigned_sheets = assign_sheets.get_assigned_sheets('tambola.db')
			#print(requested_sheet_name)
			player_name, sheet_id = requested_sheet_name.split("--")
			a_sheet = tambola_sheets_list[sheet_id]
			generated_new_sheet = generate_sheets.a_sheet_html_table(a_sheet)
			return json.dumps({'status':'OK','a_sheet':generated_new_sheet.__html__(), 'selected_sheet_name':requested_sheet_name})
		if request.method == 'GET':
			players_list = players_db_list.get_players_list('tambola.db')
			#print(players_list)
			nplayers = len(players_list)
			tambola_sheets_list = generate_sheets.get_generated_sheets('tambola.db', nplayers)
			tambola_sheets = tambola_sheets_list.keys()
			selected_sheet_name = tambola_sheets[0]
			a_sheet = tambola_sheets_list[selected_sheet_name]
			players_assigned_list, assigned_sheets = assign_sheets.assign_sheets_to_players(players_list, tambola_sheets)
			assign_sheets.persist_all_assigned_sheets('tambola.db', assigned_sheets)
			selected_sheet_name = assigned_sheets[0]
			return render_template('display_sheets.html', error=error, assigned_sheets=assign_sheets.assigned_sheets_list_html_table(assigned_sheets), a_sheet=generate_sheets.a_sheet_html_table(a_sheet), selected_sheet_name=selected_sheet_name)
	else:
		flash('Sorry: loggin required.')
		return render_template('login.html', error=error)

	return render_template('display_sheets.html', error=error)

@app.route('/draw_number', methods=['POST'])
@login_required
def draw_number():
	#print(request)
	drawn_number = draw_a_number.draw_a_number()
	drawn_numbers_list = draw_a_number.get_drawn_numbers_list('tambola.db')
	table = winning_sheet.winning_sheet_html_table(drawn_numbers_list)
	play_tambola.enque_the_drawn_number(drawNumberQ, drawn_number)
	winner_names, winner_sheets = play_tambola.get_winners_from_db('tambola.db')
	win_1_name = '( Two Columns Match -- Winner -- YTD)' 
	win_2_name = '( Full House Match -- Winner -- YTD)'
	win_1_table = winning_sheet.winning_sheet_html_table([])
	win_2_table = winning_sheet.winning_sheet_html_table([])
	if len(winner_names) == 1:
		win_1_name = winner_names[0]
		win_1_table = generate_sheets.a_sheet_html_table(winner_sheets[0])
	if len(winner_names) == 2:
		win_1_name = winner_names[0]
		win_1_table = generate_sheets.a_sheet_html_table(winner_sheets[0])
		win_2_name = winner_names[1]
		win_2_table = generate_sheets.a_sheet_html_table(winner_sheets[1])
	return json.dumps({'status':'OK','drawn_number':drawn_number, 'winning_table':table.__html__(), 'winner_1_name':win_1_name, 'winner_1_table':win_1_table.__html__(), 'winner_2_name':win_2_name, 'winner_2_table':win_2_table.__html__()});

@app.route('/logout')
@login_required
def logout():
	session.pop('logged_in', None)
	flash('You are just logged out.')
	return render_template('logout.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		if request.form['username'] != 'admin' or request.form['password'] != 'admin':
			error = 'Invalid credentials. Please try again.'
		else:
			session['logged_in'] = True
			flash('You are just logged in.')
			players_db_list.delete_players('tambola.db')
			generate_sheets.delete_generated_sheets_from_db('tambola.db')
			draw_a_number.delete_drawn_numbers('tambola.db')
			assign_sheets.delete_assigned_sheets('tambola.db')
			play_tambola.delete_winners_from_db('tambola.db')
			play_tambola.create_play_tambola_thread()
			return redirect(url_for('players'))
	return render_template('login.html', error=error)

if __name__ == "__main__":
    app.run(debug=True)
