#app.py
from flask import Flask, render_template, request, jsonify
import psycopg2 #pip install psycopg2 
import psycopg2.extras
    
app = Flask(__name__,template_folder='template')
    
app.secret_key = "caircocoders-ednalan"
    
DB_HOST = "localhost"
DB_NAME = "calendar"
DB_USER = "postgres"
DB_PASS = "namrata"
        
conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST) 
 
@app.route('/')
def index():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT * FROM events ORDER BY id")
    calendar = cur.fetchall()  
    return render_template('index.html', calendar = calendar)
  
@app.route("/insert",methods=["POST","GET"])
def insert():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        title = request.form['title']
        start = request.form['start']
        end = request.form['end']
        print(title)     
        print(start)  
        cur.execute("INSERT INTO events (title,start_event,end_event) VALUES (%s,%s,%s)",[title,start,end])
        conn.commit()       
        cur.close()
        msg = 'success' 
    return jsonify(msg)
  
@app.route("/update",methods=["POST","GET"])
def update():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        title = request.form['title']
        start = request.form['start']
        end = request.form['end']
        id = request.form['id']
        print(title)     
        print(start)  
        cur.execute("UPDATE events SET title = %s, start_event = %s, end_event = %s WHERE id = %s ", [title, start, end, id])
        conn.commit()       
        cur.close()
        msg = 'success' 
    return jsonify(msg)    
  
@app.route("/ajax_delete",methods=["POST","GET"])
def ajax_delete():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        getid = request.form['id']
        print(getid)
        cur.execute('DELETE FROM events WHERE id = {0}'.format(getid))
        conn.commit()       
        cur.close()
        msg = 'Record deleted successfully' 
    return jsonify(msg) 
  
if __name__ == "__main__":
    app.run(debug=True)
