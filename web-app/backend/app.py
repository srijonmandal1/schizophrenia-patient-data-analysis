from flask import Flask, request, jsonify, render_template
import sqlite3
from sqlite3 import Error
import openai 
import os
from werkzeug.utils import secure_filename


app = Flask(__name__)

DATABASE = 'user_profiles.db'

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn

def create_table():
    conn = create_connection(DATABASE)
    create_table_sql = """ CREATE TABLE IF NOT EXISTS user_profile (
                                        id integer PRIMARY KEY,
                                        username text NOT NULL,
                                        email text NOT NULL,
                                        age integer NOT NULL
                                    ); """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)
    finally:
        conn.close()

def save_user_profile(user_profile):
    conn = create_connection(DATABASE)
    sql = ''' INSERT INTO user_profile(username,email,age)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, user_profile)
    conn.commit()
    return cur.lastrowid

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET'])
def login():
    return render_template('LoginPage.html')

@app.route('/user_profile', methods=['GET'])
def user_profile():
    return render_template('UserProfile.html')

@app.route('/analyze_expressions', methods=['GET'])
def analyze_expressions():
    return render_template('UserExpressions.html')

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp3', 'mp4', 'wav'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

openai.api_key = 'Enter_KEY'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload_data_file', methods=['POST'])
def upload_file():
    if 'dataFile' not in request.files:
        return jsonify({'message': 'No file part'}), 400
    file = request.files['dataFile']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return jsonify({'message': 'File uploaded successfully', 'path': filepath}), 200



@app.route('/analyze_data', methods=['GET'])
def analyze_data():
    # Example
    filepath = '/Users/SrijonMaster1/Documents/schizophrenia-patient-data-analysis-main/web-app/backend/testfile.txt'
    try:
        with open(filepath, 'r') as file:
            text_content = file.read()
            response = openai.Completion.create(engine="gpt-3.5-turbo-instruct", prompt=text_content, max_tokens=50)
            return jsonify({'analysis': response.choices[0].text}), 200
    except Exception as e:
        return jsonify({'message': 'Analysis failed', 'error': str(e)}), 500


if __name__ == '__main__':
    create_table()
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
