from flask import Flask, render_template, request, jsonify
import mysql.connector
import json
# import pymysql
# from flaskext.mysql import MySQL

from datetime import datetime

application = Flask(__name__, static_url_path='/static')


# application = Flask(__name__)


@application.route('/')
def index():
    return render_template('index.html')

# def db_connection():
#     mysql = MySQL()
#
#     application.config['MYSQL_DATABASE_HOST'] = "localhost"
#     application.config['MYSQL_DATABASE_PORT'] = 3306
#     application.config['MYSQL_DATABASE_USER'] = "root"
#     application.config['MYSQL_DATABASE_PASSWORD'] = "edgedemo"  # voucherapp
#     application.config['MYSQL_DATABASE_DB'] = "edgedemo"
#
#
#     mysql.init_app(app=application)
#
#     return mysql.get_db().cursor()

def db_connection():
    mydb = mysql.connector.connect(host='192.168.1.100',  # 192.168.1.100
								   user='cqy',
								   port='3306',
								   database='edgedemo',
								   passwd='123456',
								   autocommit=True)
    return mydb


def executeSQL(sql_statement, arg=None):
    connection = db_connection()
    cursor = connection.cursor()
    print("Opened database successfully")
    try:
        print("the statement and arguments are",sql_statement,arg)
        if arg:
            cursor.execute(sql_statement, (arg,))
        else:
            cursor.execute(sql_statement)
        data = cursor.fetchall()
        print("Data is ", data)
        if len(data) > 0:
            print("Found records in Database", data)
            return jsonify(data), 200
        else:
            response = {'message': 'No data found'}
            return jsonify(response), 404
    except connection.IntegrityError:
        print("Failed to obtain values from database")
        response = {'message': 'No data found'}
        return jsonify(response), 404

    finally:
        cursor.close()


@application.route('/query', methods=['POST', 'GET'])
def query():
    if request.method == "POST":
        print("Request is",request.form)
        personID = request.form['person']
        print("Person is", personID)
        sql_persons = """SELECT person,ctime, camera FROM REID WHERE PERSON = %s"""
        return executeSQL(sql_persons, personID)


@application.route('/queryPersons', methods=['GET'])
def queryPersons():
    sql_persons = """SELECT PERSON FROM REID """
    return executeSQL(sql_persons)


if __name__ == '__main__':
    application.run(port=5000, debug=True)
