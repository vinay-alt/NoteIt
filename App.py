from flask import Flask, render_template, redirect, request, url_for, make_response
from flask_mysqldb import MySQL
import uuid
app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'keep'

mysql = MySQL(app)

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("select * from notes where u_id=%s", [request.cookies.get('id')] )
    data = cur.fetchall()
    cur.close()
    if not request.cookies.get('id'):
        resp = make_response(render_template('index.html', notes=data))
        resp.set_cookie('id', str(uuid.uuid4()), max_age=60 * 60 * 24 * 365 * 10)
        print(request.cookies.get('id'))
    else:
        resp = render_template('index.html', notes=data)
        print(request.cookies.get('id'))
    return resp

@app.route('/viewmore/<string:id>', methods=['GET','POST'])
def viewmore(id):
    cur = mysql.connection.cursor()
    cur.execute("select * from notes where id=%s", [id])
    data = cur.fetchall()
    cur.close()
    print(data)
    return render_template('note_desc.html', note_info=data)


@app.route('/insert', methods=['POST'])
def insert():
    if request.method=='POST':
        title=request.form['title']
        note = request.form['note']
        u_id = request.cookies.get('id')

        cur = mysql.connection.cursor()
        cur.execute("Insert into notes (title, note, u_id) values (%s, %s, %s)", (title, note, u_id))
        mysql.connection.commit()
        return redirect(url_for("index"))

@app.route('/edit/<string:id>', methods=['GET'])
def edit(id):
    if request.method=='GET':
        cur1 = mysql.connection.cursor()
        cur1.execute("select * from notes where id=%s", [id])
        data1 = cur1.fetchone()
        cur1.close()
        return render_template('edit.html', notes=data1, note_info=[data1])

@app.route('/update', methods=['POST'])
def update():
    if request.method=='POST':
        up_id = request.form['up_id']
        title = request.form['title']
        note = request.form['note']
        cur = mysql.connection.cursor()
        cur.execute("Update notes set title=%s, note=%s where id=%s", (title, note, up_id))
        mysql.connection.commit()
        return redirect(url_for('viewmore', id=up_id))


@app.route('/delete/<string:id>', methods=['GET','POST'])
def delete(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM notes where id = %s", [id])
    mysql.connection.commit()
    return redirect(url_for('index'))



if __name__=="__main__":
    app.run(debug=True)