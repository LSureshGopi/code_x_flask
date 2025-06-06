from flask import Flask, render_template, request, redirect, url_for, session, jsonify, abort, g, send_file
from werkzeug.security import check_password_hash, generate_password_hash
from io import BytesIO
from datetime import datetime, timedelta
import pandas as pd
from threading import Thread
import os, signal, atexit


#Modules
from auth import authLog
from config import sqliteConfig
from modules import main, tableConfig

app = Flask(__name__)
app.secret_key = '4f3d6e9a5f4b1c8d7e6a2b3c9d0e8f1a5b7c2d4e6f9a1b3c8d0e6f2a9b1d3c4'

@app.route('/')
@app.route('/home')
def home():
    if 'username' in session:
        return redirect(url_for('dashboard', user=session['username'], role=session.get('role')))
    else:
        return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    return render_template('home.html')

@app.route('/logs')
def logs():
    return render_template('logs.html')

@app.route('/generate')
def generate():
    Data = main.drpdwn_data()
    return render_template('generate.html', Data=Data)

@app.route('/configuration')
def configuration():
    df_fun_view = main.tbl_fun_View()
    df_fun_data = main.tbl_fun_data()
    Data = main.drpdwn_data()

    tbl_fun_view = df_fun_view.to_html(classes='table table-striped', index=False, escape=False, table_id='inventory-table')

    return render_template('configuration.html', table1=tbl_fun_view, table2="", Data=Data)

#tbl CRUD
@app.route('/update_fun_view_row', methods=['POST'])
def update_fun_view():
    data = request.get_json()
    id = data.get('id')
    fun = data.get('functionname')
    fundec = data.get('functiondescription')

    if not id or fun is None or fundec is None:
        return jsonify(success=False, error="Missing data")

    success = tableConfig.edit_fun_tbl(id, fun, fundec)
    return jsonify(success=success)

@app.route('/delete_fun_view_row', methods=['POST'])
def delete_fun_view():
    data = request.get_json()
    id = data.get('id')

    if not id:
        return jsonify(success=False, error="ID not provided")

    success =  tableConfig.delete_fun_tbl(id)
    return jsonify(success=success)
  
@app.route('/add_fun_view_row', methods=['POST'])
def add_fun_view_row():
    data = request.get_json()
    fun = data.get('functionname')
    fundec = data.get('functiondescription')

    if not fun or not fundec:
        return jsonify(success=False, error="Missing data")

    success = tableConfig.insert_fun_tbl(fun, fundec)
    return jsonify(success=success)


@app.route('/dropdown_filter', methods=['POST'])
def get_data_for_function():
    data = request.get_json()
    function_name = data.get('function_name')

    df_fun_data = tableConfig.dropdwn_filter(function_name)
    html_table = df_fun_data.to_html(classes='table table-striped', index=False, escape=False, table_id='tbl2')
    
    return jsonify({'html': html_table})


###########################################
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/super_admin')
def super_admin():
    user_logged_in = 'username' in session
    df = sqliteConfig.dfUser()
    table_html = df.to_html(classes='table table-striped', index=False, escape=False, table_id='inventory-table')
    return render_template('super_admin.html', table=table_html, user_logged_in=user_logged_in)

@app.route('/update_user_password', methods=['POST'])
def update_user_password():
    data = request.get_json()
    username = data.get('username')
    new_password = data.get('new_password')

    if not username or not new_password:
        return jsonify(success=False, error="Invalid data")

    try:
        conn = sqliteConfig.get_db_connection()
        cur = conn.cursor()
        hashed = generate_password_hash(new_password)

        cur.execute("UPDATE users SET password_hash = ? WHERE username = ?", (hashed, username))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify(success=True)
    except Exception as e:
        return jsonify(success=False, error=str(e))

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    user = authLog.get_user(username)
    if user and check_password_hash(user[2], password):
        session.permanent = True
        session['username'] = user[1]
        session['role'] = user[3]
        return jsonify(success=True)
    else:
        return jsonify(success=False, error="Invalid Credentials"), 403

@app.route('/change_password', methods=['POST'])
def change_password():
    if 'username' not in session:
        return jsonify(success=False, error="Not logged in"), 403

    data = request.get_json()
    old_password = data.get('oldPassword')
    new_password = data.get('newPassword')

    username = session['username']

    conn = sqliteConfig.get_db_connection()
    if conn is None:
        return jsonify(success=False, error="Database connection error"), 500

    try:
        cur = conn.cursor()
        # Fetch the stored password hash
        cur.execute('SELECT password_hash FROM users WHERE username = ?', (username,))
        row = cur.fetchone()

        if not row:
            return jsonify(success=False, error="User not found"), 404

        stored_password_hash = row[0]

        if check_password_hash(stored_password_hash, old_password):
            # If old password matches, update with new password
            new_password_hash = generate_password_hash(new_password)

            cur.execute('UPDATE users SET password_hash = ? WHERE username = ?', (new_password_hash, username))
            conn.commit()

            return jsonify(success=True)
        else:
            return jsonify(success=False, error="Old password is incorrect."), 400

    except Exception as e:
        print("Error during password change:", e)
        return jsonify(success=False, error=str(e)), 500

    finally:
        cur.close()
        conn.close()


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403

@app.before_request
def load_user():
    g.user = session.get('username')
    g.role = session.get('role')

@app.context_processor
def inject_user():
    return dict(user=session.get('username'), role=session.get('role'))

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)