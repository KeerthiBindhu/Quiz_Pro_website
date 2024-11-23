from flask import Flask, render_template, redirect, url_for, request, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)
 
app.secret_key = 'myfirsteverfullstackapp'


app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_PASSWORD'] = 'Mysql_02'
app.config['MYSQL_DB'] = 'quiz_pro'

mysql = MySQL(app)

# Route to redirect to home pages
@app.route('/')
def home():
    return render_template('home.html')

# Route to login page
@app.route('/login/<user>', methods=['GET','POST'])
def login(user):
    msg = ''
    if request.method == 'POST' and user == 'quiz_creator' and 'username' in request.form and 'password' in request.form:
        QCusername = request.form['username']
        QCpassword = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute(
            'SELECT * FROM quiz_creator WHERE user_name = % s \
            AND password = % s', (QCusername, QCpassword, ))
        account = cursor.fetchone()
        if account:
            session['QCloggedin'] = True
            session['QCId'] = account[0]
            session['QCusername'] = account[1]
            return redirect(url_for('profile', user = user))
        else:
            msg = 'Incorrect username / password !'
    elif request.method == 'POST' and user == 'quiz_player' and 'username' in request.form and 'password' in request.form:
        QPusername = request.form['username']
        QPpassword = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute(
            '''SELECT * FROM quiz_player WHERE player_name = % s \
            AND password = % s''', (QPusername, QPpassword, ))
        account = cursor.fetchone()
        if account:
            session['QPloggedin'] = True
            session['QPId'] = account[0]
            session['QPusername'] = account[1]
            return redirect(url_for('profile', user = user))
        else:
            msg = 'Incorrect username / password !'
    elif 'QCloggedin' in session and user == 'quiz_creator':
        return redirect(url_for('profile', user = user))
    elif 'QPloggedin' in session and user == 'quiz_player':
        return redirect(url_for('profile', user = user))
    return render_template('login.html', msg = msg, user = user)

# Route to register / signup page
@app.route('/signup/<user>', methods=['GET', 'POST'])
def signup(user):
    msg = ''
    print(type(user))
    if request.method == 'POST' and 'username' in request.form and \
        'mobilenumber'in request.form and 'email' in request.form and \
       'password' in request.form :
        username = request.form['username']
        mobilenumber = request.form['mobilenumber']
        email = request.form['email']
        password = request.form['password']
        # print(user)
        cursor = mysql.connection.cursor()
        if(user == 'quiz_creator'):
            cursor.execute(
            'SELECT * FROM '+user+' WHERE user_name = % s', (username, ))
        else:
            cursor.execute(
            'SELECT * FROM '+user+' WHERE player_name = % s', (username, ))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'name must contain only characters and numbers !'
        else:
            cursor.execute('INSERT INTO '+user+' VALUES \
            (NULL, % s, % s, % s, % s)',
                           (username, mobilenumber, email, password, ))
            mysql.connection.commit()
            # msg = 'You have successfully created account !'
            if user == 'quiz_creator':
                cursor.execute('''SELECT * FROM quiz_creator WHERE user_name = % s \
                                  AND password = % s''', (username, password, ))
                account = cursor.fetchone()
                session['QCloggedin'] = True
                session['QCId'] = account[0]
                session['QCusername'] = account[1]
            elif user == 'quiz_player':
                cursor.execute('''SELECT * FROM quiz_player WHERE player_name = % s \
                                  AND password = % s''', (username, password, ))
                account = cursor.fetchone()
                session['QPloggedin'] = True
                session['QPId'] = account[0]
                session['QPusername'] = account[1]
            return redirect(url_for('profile', user = user))
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('signup.html', msg=msg, user = user)
 
# Route to update page

# Route to logout
@app.route('/logout/<user>', methods=['GET'])
def logout(user):
    if user == 'quiz_creator':
        session.pop('QCloggedin', None)
        session.pop('QCId', None)
        session.pop('QCusername', None)
        return redirect(url_for('login', user = user))
    elif user == 'quiz_player':
        session.pop('QPloggedin', None)
        session.pop('QPId', None)
        session.pop('QPusername', None)
        return redirect(url_for('login', user = user))

# Route to display quiz_cretor profile
@app.route('/profile/<user>')
def profile(user):
    cursor = mysql.connection.cursor()
    
    if 'QCloggedin' in session and user == 'quiz_creator':
        cursor.execute(''' SELECT * FROM quiz_category_name WHERE QCId = % s''', (session['QCId'],))
        qc_data = cursor.fetchall()
        return render_template('user_profile.html', user = user, qc_data = qc_data)
    
    elif 'QPloggedin' in session and user == 'quiz_player':
        cursor.execute(''' SELECT * FROM quiz_category_name ''')
        qc_data = cursor.fetchall()
        qpid = session['QPId']
        cursor.execute(''' SELECT * FROM quiz_category_name, quiz_result 
                           WHERE quiz_category_name.QId = quiz_result.QId and 
                           QPId = %s and isPlayerPlayed = 1;''', (qpid, ))
        qp_data = cursor.fetchall()
        return render_template('player_profile.html', user = user, qc_data = qc_data, qp_data = qp_data)
 
# Route to add quiz_category
@app.route('/<user>/add_quiz', methods=['POST'])
def add_quiz_category(user):
    if 'QCloggedin' in session and request.method == 'POST' and 'qc_name' in request.form:
        qc_name = request.form['qc_name']
        qcid = session['QCId']
        print(type(qcid))
        cursor = mysql.connection.cursor()
        cursor.execute('''INSERT INTO quiz_category_name VALUES 
                (NULL, % s, % s, 0)''', (qcid, qc_name, ))
        mysql.connection.commit()
        cursor.execute(''' SELECT QId FROM quiz_category_name 
                           WHERE Q_catagory_name = % s''', (qc_name,))
        qid = cursor.fetchone()
        return render_template('quiz.html', user = user, QId = qid[0])

# Route to add quiz
@app.route('/<user>/submit_quiz/<int:QId>', methods=['POST'])
def submit_quiz(user,QId):
    cursor = mysql.connection.cursor()
    if 'QCloggedin' in session and request.method == 'POST' and user == 'quiz_creator':
        questions = request.form.getlist('questions')
        
        for i , ques in enumerate(questions):
            
            # To insert options and answer in db
            option1 = request.form[f'questions[{i}][options][0]']
            option2 = request.form[f'questions[{i}][options][1]']
            option3 = request.form[f'questions[{i}][options][2]']
            option4 = request.form[f'questions[{i}][options][3]']
            ans = request.form.get(f'questions[{i}][answer]')
            
            # to get QSId from db
            cursor.execute('''INSERT INTO quiz_ques_options_ans VALUES 
                (NULL, % s, % s, % s, % s, % s, % s, % s)''', (QId, ques, option1, option2, option3, option4, ans))
            mysql.connection.commit()
    elif 'QPloggedin' in session and request.method== 'POST' and user == 'quiz_player':
        data = request.form.to_dict(flat=False) 
        score = 0
        qpid = session['QPId']
        cursor.execute('''SELECT count(*) AS Number_of_records,Answer FROM quiz_ques_options_ans 
                          WHERE QId = %s GROUP BY Answer''', (QId, ))
        count =  cursor.fetchall()
        cursor.execute('''SELECT QCId FROM quiz_category_name WHERE QId = %s''', (QId, ))
        qcid =  cursor.fetchone()
        # qcid = qcid['QCId']
        cursor.execute('''SELECT No_of_players FROM quiz_category_name WHERE QId = %s''', (QId, ))
        no_of_players =  cursor.fetchone()
        no_of_players = no_of_players[0]+1
        # player_ans = data.get(f'questions[{1}][answer]')
        for i in range(len(count)):
            player_ans = data.get(f'questions[{i+1}][answer]')
            if count[i][1] == player_ans[0]:
                score = int(score) + 1
        cursor.execute('''INSERT INTO quiz_result VALUES 
        (NULL, % s, % s, % s, % s, 1)''', (qpid, QId, qcid, score,))
        mysql.connection.commit()
        cursor.execute('''UPDATE quiz_category_name SET No_of_players = % s
                          WHERE QId = % s''', (no_of_players, QId, ))
        mysql.connection.commit()
        
    return render_template('temp.html', user = user)

# Route to play quiz
@app.route('/<user>/play_quiz/<int:Qid>', methods=['GET'])
def play_quiz(user,Qid):
    
    if 'QPloggedin' in session:
        cursor = mysql.connection.cursor()
        cursor.execute('''SELECT * FROM quiz_ques_options_ans 
                       WHERE QId = % s''', (Qid, )) 
        quiz = cursor.fetchall()
        return render_template('play.html', quiz = quiz, Qid = Qid, user = user)
    return redirect(url_for('profile', user=user))


if __name__ == '__main__':
    app.run(debug=True)
