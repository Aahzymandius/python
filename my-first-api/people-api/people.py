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

##Establish Mysql connections, one for read/write and one for just reads
readconn = pymysql.connect(readserver,uname,passwd,db)
masterconn = pymysql.connect(writeserver,uname,passwd,db)

##Create  the format for the json API response
def json_format(x):
  
  uuid = x[0]
  survived = x[1]
  pclass = x[2]
  name = x[3]
  sex = x[4]
  age = x[5]
  sibl = x[6]
  parents = x[7]
  fare = x[8]
  
  dict = {"UUID":uuid, "survived":survived, "passengerClass": pclass, "name":name, "sex":sex, "age":age, "siblingsOrSpousesAboard":sibl, "parentsOrChildrenAboard":parents, "fare":fare}
  
  return dict


@app.route('/people', methods=['GET'])
def get_all():
  
  sql = "SELECT * FROM passengers"
  
  conn = readconn.cursor()
  query = conn.execute(sql)
  results = conn.fetchall()
  
  rows = []
  for row in results:
    y = json_format(row)
    rows.append(y)
  
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
  
  sql2 = "SELECT * FROM passengers WHERE Name='%s'" % name
  
  conn.execute(sql2)
  lastEntry = conn.fetchone()
  format = json_format(lastEntry)
  
  resp = jsonify(format)
  return resp


##Create a path to respond to health checks
@app.route('/health')
def get():
  healthy = "true"
    return(healthy=="true")

if __name__ == "__main__":
    app.run(host='0.0.0.0')
