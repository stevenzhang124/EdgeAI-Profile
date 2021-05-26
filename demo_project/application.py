from flask import Flask, render_template, request, jsonify
import sqlite3
import json

application = Flask(__name__, static_url_path='/static')
#app = Flask(__name__)



@application.route('/')
def index():
	return render_template('index.html')


@application.route('/query',methods=['POST','GET'])
def query():
	conn = sqlite3.connect('edgedemo.db', isolation_level=None)
	print("Opened database successfully")
	cur = conn.cursor()

	if request.method == "POST":

		PersonID = request.form['PersonID']
		print(PersonID)
		print(type(PersonID))
		info = "select * from REID"
		cur.execute(info)
		data = cur.fetchall()
		print(type(data))

		results = ""
		for item in data:
			results += "<tr><td>"+ str(item[0])+"</td>"+"<td>"+ str(item[1])+"</td>"+"<td>"+str(item[2])+"</td>"+"</tr>"

		return results

if __name__ == '__main__':
	application.run(port=5000, debug = True)