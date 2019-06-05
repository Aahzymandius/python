from flask import Flask, request, jsonify,Response
from flask_restful import Resource, Api
import pymysql
import json
import os
import simplejson

uname = os.environ['USERNAME']
passwd = os.environ['PASSWORD']
db = os.environ['DATABASE']
readserver = os.environ['SERVER']
writeserver = os.environ['MASTER']

app = Flask(__name__)

readconn = pymysql.connect(readserver,uname,passwd,db)
masterconn = pymysql.connect(writeserver,uname,passwd,db)

@app.route('/people', methods=['GET'])
def get_all():
  
  conn = readconn.cursor()
  query = conn.execute("SELECT * FROM passengers")
  rows = conn.fetchall()
  
  resp = jsonify(rows)
  resp.status_code = 200
  return resp
  
@app.route('/people', methods=['POST'])
def post():

  survived = request.json["survived"]
  pclass = request.json["passengerClass"]
  name = request.json["name"]
  sex = request.json["sex"]
  age = request.json["age"]
  siblings = request.json["siblingsOrSpousesAboard"]
  parents = request.json["parentsOrChildrenAboard"]
  fare = request.json["fare"]

  sql = "INSERT INTO passengers (Survived, Pclass, Name, Sex, Age, `Siblings/Spouses Aboard`, `Parents/Children Aboard`, Fare) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
  data = (survived, pclass, name, sex, age, siblings, parents, fare)

  conn = masterconn.cursor()
  conn.execute(sql,data)
  masterconn.commit()
  
  conn.execute("SELECT * FROM passengers WHERE Name='%s'" % name)
  lastEntry = conn.fetchall()
  
  resp = jsonify(lastEntry)
  resp.status_code = 200
  return resp


if __name__ == "__main__":
    app.run(host='0.0.0.0')
