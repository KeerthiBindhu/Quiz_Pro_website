from flask import  Flask, render_template, redirect, url_for, session, request
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, and_
from flask_migrate import Migrate
from sqlalchemy.orm import relationship, backref
import re

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz_pro_db.db'
app.config['SECRET_KEY'] = 'my_randam_db_key'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy()
db.init_app(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

# Models
class Quiz_creator(db.Model, UserMixin):
    __tablename__ = 'Quiz_creator'
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(100), nullable=False)
    mobile_number = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique= True)
    password = db.Column(db.String(10), nullable=False)
    
    
        
class Quiz_player(db.Model, UserMixin):
    __tablename__ = 'Quiz_player'
    id= db.Column(db.Integer, primary_key=True)
    player_name = db.Column(db.String(100), nullable=False)
    mobile_number = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique= True)
    password = db.Column(db.String(10), nullable=False)
    
    
        
class Quiz_category_name(db.Model):
    __tablename__ = 'Quiz_category_name'
    id = db.Column(db.Integer, primary_key=True)
    QCId = db.Column(db.Integer, ForeignKey('Quiz_creator.id'), nullable=False)
    Q_category_name = db.Column(db.String(200), nullable=False)
    No_of_players = db.Column(db.Integer, nullable=False)
    
    # Relationship to Quiz_creator 
    qc = relationship("Quiz_creator", backref=db.backref('Quiz_category_name', lazy=True))
   
    

class Quiz_ques_opts_ans(db.Model):
    __tablename__ = 'Quiz_ques_opts_ans'
    id = db.Column(db.Integer, primary_key=True)
    QcnId = db.Column(db.Integer, ForeignKey('Quiz_category_name.id'), nullable=False)
    Question_text = db.Column(db.String(350), nullable=False)
    Option1 = db.Column(db.String(250), nullable=False)
    Option2 = db.Column(db.String(250), nullable=False)
    Option3 = db.Column(db.String(250), nullable=False)
    Option4 = db.Column(db.String(250), nullable=False)
    Answer = db.Column(db.String(100), nullable=False)
    
    # Relationship to Quiz_category_name with back_populates
    qcn = relationship("Quiz_category_name", backref=db.backref('Quiz_ques_opts_ans', lazy=True))
    

class Quiz_result(db.Model):
    __tablename__ = 'Quiz_result'
    id = db.Column(db.Integer, primary_key=True)
    QPId = db.Column(db.Integer, ForeignKey('Quiz_player.id'), nullable=False)
    QcnId = db.Column(db.Integer, ForeignKey('Quiz_category_name.id'), nullable=False)
    QCId = db.Column(db.Integer, ForeignKey('Quiz_creator.id'), nullable=False)
    Score = db.Column(db.Integer, nullable=False)
    Total_Score = db.Column(db.Integer, nullable=False)
    
    # Relationship to Quiz_category_name, Quiz_creator, Quiz_player with back_populates
    qcn = relationship("Quiz_category_name", backref=db.backref('Quiz_result', lazy=True))
    qc = relationship("Quiz_creator", backref=db.backref('Quiz_result', lazy=True))
    qp = relationship("Quiz_player", backref=db.backref('Quiz_result', lazy=True))
  
  

# Initialize Flask app and create tables
with app.app_context():
    db.create_all()
    
# To load user
@login_manager.user_loader
def load_user(user_id):
    user_type = session.get('user_type')

    if user_type == 'quiz_creator' and session.get('QCloggedin') == True :
        return Quiz_creator.query.get(int(user_id))
    elif user_type == 'quiz_pplayer' and session.get('QPloggedin') == True :
        return Quiz_player.query.get(int(user_id))
    return None

# Route to redirect to home pages
@app.route('/')
def home():
    return render_template('home.html')

# Route to login page
@app.route('/login/<user>', methods=['GET','POST'])
def login(user):
    msg = ''
    if request.method == 'POST' and user == 'quiz_creator' and 'email' in request.form and 'password' in request.form:
        email = request.form.get("email")
        password = request.form.get("password")
        
        account = Quiz_creator.query.filter_by(email = email).first()
        print(account)
        if account and account.password == password:
            login_user(account)
            session['user_type'] = user
            session['QCloggedin'] = True
            session['QCId'] = account.id
            session['QCusername'] = account.user_name
            return redirect(url_for('profile', user = user))
            # return render_template('user_profile.html',user = user, account = account)
        else:
            # msg = Quiz_creator.query.all()
            # msg = Quiz_creator.password
            msg = 'Incorrect username / password !'
    elif request.method == 'POST' and user == 'quiz_player' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        
        account = Quiz_player.query.filter_by(email = email).first()
        print(account)
        if account and account.password == password:
            session['user_type'] = user
            session['QPloggedin'] = True
            session['QPId'] = account.id
            session['QPusername'] = account.player_name
            return redirect(url_for('profile', user = user))
            # return render_template('player_profile.html',user = user, account = account)
        else:
            # msg = account.player_name
            msg = 'Incorrect username / password !'
    elif 'QCId' in session and user == 'quiz_creator':
        qcid = session['QCId']
        account = Quiz_creator.query.filter_by(id = qcid).first()
        return redirect(url_for('profile', user = user))
        # return render_template('user_profile.html', user = user, account = account)
    elif 'QPloggedin' in session and user == 'quiz_player':
        qpid = session['QPId']
        account = Quiz_player.query.filter_by(id = qpid).first()
        return redirect(url_for('profile', user = user))
        # return render_template('player_profile.html', user = user, account = account)
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
        
        if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Name must contain only characters and numbers !'
        
        else:
            if user == 'quiz_creator':
            
                account = Quiz_creator.query.filter_by(email = email).first()
                if account:
                    msg = 'Account already exists !'
                else:
                    user_account = Quiz_creator(user_name = username, 
                                                mobile_number = mobilenumber, 
                                                email = email, 
                                                password =password)
                    db.session.add(user_account)
                    db.session.commit()
                    # msg = 'You have successfully created account !'
                    account = Quiz_creator.query.filter_by(email = email).first()
                    session['user_type'] = user
                    session['QCloggedin'] = True
                    session['QCId'] = account.id
                    session['QCusername'] = username
                # return render_template('user_profile.html', user = user, account = account)
                return redirect(url_for('profile', user = user))
                
            elif user == 'quiz_player':
                
                account = Quiz_player.query.filter_by(email = email).first()
                if account:
                    msg = 'Account already exists !'
                else:
                    user_account = Quiz_player( player_name = username, 
                                                mobile_number = mobilenumber, 
                                                email = email, 
                                                password =password)
                    db.session.add(user_account)
                    db.session.commit()
                    # msg = 'You have successfully created account !'
                    account = Quiz_player.query.filter_by(email = email).first()
                    session['user_type'] = user
                    session['QPloggedin'] = True
                    session['QPId'] = account.id
                    session['QPusername'] = username
                # return render_template('player_profile.html', user = user,account = account)
                return redirect(url_for('profile', user = user))
            # return redirect(url_for('profile', user = user))
    elif request.method == 'POST': 
        msg = 'Please fill out the form !'
    return render_template('signup.html', msg=msg, user = user)
 
 
# Route to update page
@app.route('/update/<user>/<int:user_id>', methods=['GET', 'POST'])
def update(user, user_id):
    msg = ''
    print(type(user))
    if 'QPloggedin' in session or 'QCloggedin' in session:
        if user == 'quiz_creator':
            user_acc = Quiz_creator.query.filter_by( id = user_id).first()
        elif user == 'quiz_player':
            user_acc = Quiz_player.query.filter_by( id = user_id).first()
        if request.method == 'POST' and 'username' in request.form and \
            'mobilenumber'in request.form and 'email' in request.form and \
           'password' in request.form :
            username = request.form['username']
            mobilenumber = request.form['mobilenumber']
            password = request.form['password']
            # print(user)
            
            if not re.match(r'[A-Za-z0-9]+', username):
                msg = 'Name must contain only characters and numbers !'
            
            else:
                if user == 'quiz_creator':
                
                    account = Quiz_creator.query.filter_by(id = user_id).first()
                    if account:
                        account.id = user_id
                        account.user_name = username
                        account.mobile_number = mobilenumber
                        account.password = password
                        db.session.commit()
                        # msg = 'You have successfully created account !'
                    # return render_template('user_profile.html', user = user, account = account)
                        return redirect(url_for('profile', user = user))
                    else: 
                        msg = "Account doesn't exists !"
                        
                elif user == 'quiz_player':
                    
                    account = Quiz_player.query.filter_by(id = user_id).first()
                    if account:
                        account.id = user_id
                        account.player_name = username
                        account.mobile_number = mobilenumber
                        account.password = password
                        db.session.commit()
                        # msg = 'You have successfully created account !'
                    # return render_template('player_profile.html', user = user,account = account)
                        return redirect(url_for('profile', user = user))
                    else: 
                        msg = "Account doesn't exists !"
                # return redirect(url_for('profile', user = user))
        elif request.method == 'POST': 
            msg = 'Please fill out the form !'
        return render_template('update.html', msg=msg, user = user, account = user_acc)
    return redirect(url_for('login', user = user))
 
# Route to logout   ###HAS TO CHECK###
@app.route('/logout/<user>/<int:user_id>')
# @login_required  # Ensure user is logged in
def logout(user, user_id):
    print(user)
    # logout_user()# Logs out the user and removes session data
    if user == 'quiz_creator':
        # logout_user()  # Logs out the user and removes session data
        session.pop('QCusername', None)
        session.pop('QCId', None)
        session.pop('QCloggedin', None)
        # return redirect(url_for('login', user = 'quiz_creator'))
    elif user == 'quiz_player':
    #     user_to_logout = Quiz_player.query.get(user_id)
    #     if user_to_logout:
        # logout_user()  # Logs out the user and removes session data
        session.pop('QPloggedin', None)
        session.pop('QPId', None)
        session.pop('QPusername', None)
        # return render_template('login.html', user = 'quiz_player')
    return render_template('home.html')  # Redirect to a page after logout


# Route to display quiz_cretor profile
@app.route('/profile/<user>')
def profile(user):
    
    if 'QCloggedin' in session and user == 'quiz_creator':
        qcid = session['QCId']
        qc_data = Quiz_category_name.query.filter_by(id = qcid).all()
        
        account = Quiz_creator.query.filter_by(id = qcid).first()
        return render_template('user_profile.html', user = user, account = account, qc_data = qc_data)
    
    elif 'QPloggedin' in session and user == 'quiz_player':
        qc_data = Quiz_category_name.query.all()
        qpid = session['QPId']
        account = Quiz_player.query.filter_by(id = qpid).first()
        
        # qp_data to hold both Quiz_category_name and Quiz_result data
        qp_data = db.session.query(Quiz_category_name, Quiz_result).join(
                                    Quiz_result, 
                                    and_(Quiz_category_name.id == Quiz_result.QcnId, Quiz_result.QPId == qpid)
                                    ).all()
        total_score = Quiz_ques_opts_ans.query.filter_by()
        return render_template('player_profile.html', user = user, account = account, qc_data = qc_data, qp_data = qp_data)
 
 
# Route to add quiz_category
@app.route('/add_quiz/<int:qc_id>', methods=['POST'])
def add_quiz_category(qc_id):
    if 'QCloggedin' in session and request.method == 'POST' and 'qc_name' in request.form:
        qc_name = request.form['qc_name']
        qcid = session['QCId']
        print(type(qcid))
        
        qcn = Quiz_category_name(Q_category_name = qc_name,
                                 QCId = qc_id,
                                 No_of_players = 0)
        db.session.add(qcn)
        db.session.commit()
        
        # To get quiz from user
        quiz = Quiz_category_name.query.filter(
            and_(
                Quiz_category_name.Q_category_name == qc_name,
                Quiz_category_name.QCId == qcid
        )).first()
        return render_template('quiz.html', QId = quiz.id)

# Route to submit quiz in db as well as in web
@app.route('/<user>/submit_quiz/<int:QId>', methods=['POST'])
def submit_quiz(user,QId):
    
    # To add quiz in db by quiz_creator
    if 'QCloggedin' in session and request.method == 'POST' and user == 'quiz_creator':
        questions = request.form.getlist('questions')
        
        for i , ques in enumerate(questions):
            
            # To insert options and answer in db
            option1 = request.form[f'questions[{i}][options][0]']
            option2 = request.form[f'questions[{i}][options][1]']
            option3 = request.form[f'questions[{i}][options][2]']
            option4 = request.form[f'questions[{i}][options][3]']
            ans = request.form.get(f'questions[{i}][answer]')
            
            # to add ques, opts and ans to db
            quiz_ques_ans = Quiz_ques_opts_ans(
                QcnId = QId,
                Question_text = ques,
                Option1 = option1,
                Option2 = option2,
                Option3 = option3,
                Option4 = option4,
                Answer = ans
            )
            db.session.add(quiz_ques_ans)
            db.session.commit()
            
    # To submit quiz by quiz_player
    elif 'QPloggedin' in session and request.method== 'POST' and user == 'quiz_player':
        data = request.form.to_dict(flat=False) 
        score = 0
        qpid = session['QPId']
        
        org_ans = Quiz_ques_opts_ans.query.filter_by( QcnId = QId).all()
        
        qcid = Quiz_category_name.query.filter_by( id = QId).first()
        
        no_of_players = qcid.No_of_players+1
        player_ans = data.get(f'questions[{1}][answer]')
        for i in range(len(org_ans)):
            player_ans = data.get(f'questions[{i+1}][answer]')
            if org_ans[i].Answer == player_ans[0]:
                score = int(score) + 1
       
        quiz_result = Quiz_result(
            QPId = qpid,
            QcnId = qcid.id,
            QCId = qcid.QCId,
            Score = score,
            Total_Score = len(org_ans)
        )
        db.session.add(quiz_result)
        db.session.commit()
        
        qcid.No_of_players = no_of_players
        db.session.commit()
        
    return render_template('temp.html', user = user)


# Route to play quiz
@app.route('/<user>/play_quiz/<int:Qid>', methods=['GET'])
def play_quiz(user,Qid):
    
    if 'QPloggedin' in session:
        quiz = Quiz_ques_opts_ans.query.filter_by(QcnId = Qid)
        return render_template('play.html', quiz = quiz, Qid = Qid, user = user)
    return redirect(url_for('profile', user=user))



if __name__ == '__main__':
    app.run(debug=True)
    