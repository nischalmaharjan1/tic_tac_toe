from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Needed for session management

def check_winner(board):
    # All winning combinations
    wins = [(0,1,2), (3,4,5), (6,7,8),  # rows
            (0,3,6), (1,4,7), (2,5,8),  # columns
            (0,4,8), (2,4,6)]           # diagonals
    for a, b, c in wins:
        if board[a] == board[b] == board[c] and board[a] != "":
            return board[a]
    if "" not in board:
        return "Draw"
    return None

@app.route('/')
def index():
    # Initialize game if needed
    if 'board' not in session:
        session['board'] = [""] * 9
        session['turn'] = "X"
        session['winner'] = None
    return render_template("index.html", board=session['board'], turn=session['turn'], winner=session['winner'])

@app.route('/move/<int:cell>')
def move(cell):
    if session.get('winner'):
        return redirect(url_for('index'))

    board = session['board']
    turn = session['turn']

    if board[cell] == "":
        board[cell] = turn
        session['board'] = board
        winner = check_winner(board)
        if winner:
            session['winner'] = winner
        else:
            session['turn'] = "O" if turn == "X" else "X"
    return redirect(url_for('index'))

@app.route('/reset')
def reset():
    session.pop('board', None)
    session.pop('turn', None)
    session.pop('winner', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(port=7010)

