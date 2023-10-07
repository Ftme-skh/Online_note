
from flask import Flask, url_for, render_template, request, flash, redirect
import json
from markupsafe import escape
import datetime
from datetime import date
import psycopg2
conn = psycopg2.connect(host="localhost",database="notes_db",user="postgres",password="postgres")
cur = conn.cursor()
# my_notes = [
#     {"text" : "sample note", "content" : "Don't forget to buy mushrooms", "date" : '2023-09-11 18:34:56.741911'},
#     {"text" : "another sample note", "content" : "Today I feel happy above the sky", "date" : '2023-09-11 18:28:56.741911'},
# ]
my_data = []

app = Flask(__name__)


# @app.route("/<my_notes>")
@app.route("/")
def zereshk(note=None, length=None):
    cur.execute("""SELECT "id" ,"text" FROM notes;""")
    data=cur.fetchall()
    data_length = len(data)
        
    return render_template('index.html', note=data, length=data_length)
    


@app.route("/add", methods=('GET', 'POST'))
def add():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not content:
            print("SADFSDFDS")
        else:
            query = f"""insert into notes ("text") values ('{content}')"""
            cur.execute(query)
            conn.commit()
            print("sssssssssssssss")
            return redirect(url_for('zereshk'))

    return render_template('add.html')      


@app.route("/delete/<int:id>", methods=('GET', 'POST'))
def delete(id):
    my_id = id
    delete_query = f"""DELETE FROM notes WHERE "id" = ('{my_id}')"""
    cur.execute(delete_query)
    return redirect('/')


@app.route("/edit/<int:id>", methods=('GET', 'POST'))
def edit(id, data=None):
    my_id = id
    query = f"""SELECT "text" FROM notes WHERE "id" = ('{my_id}')"""
    cur.execute(query)
    to_be_edited = cur.fetchall()
    return render_template('edit.html', data = to_be_edited)  
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']   
    if not content:
        print("SADFSDFDS")
    else:
        query = f"""insert into notes ("text") values ('{content}')"""
        cur.execute(query)
        conn.commit()
        print("sssssssssssssss")
        return redirect(url_for('zereshk'))

    return render_template('add.html')     

if __name__ == '__main__':
    app.run(debug=True)    