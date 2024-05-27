from flask import Flask, render_template, redirect, url_for, request, jsonify
from flask_mysqldb import MySQL, MySQLdb
import pandas as pd
import os
import openpyxl


app = Flask(__name__)

app.secret_key = 'key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL-PASSWORD'] = ''
app.config['MYSQL_DB'] = 'test'

mysql = MySQL(app)

@app.route('/')
@app.route('/admin')
def admin():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM ecommerce")
    data = cur.fetchall()
    cur.execute("SELECT COUNT(*) FROM ecommerce")
    admin_count = cur.fetchone()[0]
    cur.close()
    return render_template('admin.html', data=data, admin_count=admin_count)

@app.route('/teacher')
def teacher():
    cur = mysql.connection.cursor()
    cur.execute("SELECT  username, phone, email FROM timed")
    data = cur.fetchall()
    cur.execute("SELECT COUNT(*) FROM timed")
    teacher_count = cur.fetchone()[0]
    cur.close()
    return render_template('teacher.html', data=data, teacher_count=teacher_count)

@app.route('/student')
def student():
    cur = mysql.connection.cursor()
    cur.execute("SELECT username, phone, email FROM timed")
    data = cur.fetchall()
    cur.execute("SELECT COUNT(*) FROM timed")
    student_count = cur.fetchone()[0]
    cur.close()
    return render_template('student.html', data=data, student_count=student_count)


@app.route('/view/<int:id>')
def view(id):
    return f'Viewing row  with ID {id}'

@app.route('/modify/<int:id>')
def modify(id):
    return f'Modifying row  with ID {id}'

@app.route('/upload', methods=['GET'])
def upload():
    return render_template('upload.html',)


@app.route('/reg', methods=['GET', 'POST'])
def reg():
    if request.method == 'POST' and 'id' in request.form and 'firstname' in request.form and 'lastname' in request.form and 'address' in request.form and 'mobile' in request.form and 'age' in request.form and 'email' in request.form and 'password' in request.form:
        id = request.form['id']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        address = request.form['address']
        mobile = request.form['mobile']
        age = request.form['age']
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO register VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', (id, firstname, lastname, address, mobile, age, email, password))        
        mysql.connection.commit()
        msg = 'Registration Successfully'
        return render_template('table.html')
    elif request.method == 'POST':
        msg = 'Please Fill out form'
    return render_template('register.html')
    


if '__main__' == __name__:
    app.run(debug=True)