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
api = Api(app)

readconn = pymysql.connect(readserver,uname,passwd,db)
masterconn = pymysql.connect(writeserver,uname,passwd,db)

class People(Resource):
  def get(self,uuid):

    try:
      conn = readconn.cursor()
      conn.execute("SELECT * FROM passengers WHERE UUID='%s'" % uuid)

      resp = jsonify(conn.fetchall())
      resp.response_code = 200
      return resp

    except:
      resp = jsonify("Passenger not found")
      resp.status_code = 404
      return resp


  def delete(self,uuid):

    try:
      conn = masterconn.cursor()
      conn.execute("DELETE FROM passengers WHERE UUID='%s'" % uuid)
      masterconn.commit()

    except:
      resp = jsonify("Not found")
      resp.status_code = 404
      return resp

  def put(self,uuid):

    survived = request.json["survived"]
    pclass = request.json["passengerClass"]
    name = request.json["name"]
    sex = request.json["sex"]
    age = request.json["age"]
    siblings = request.json["siblingsOrSpousesAboard"]
    parents = request.json["parentsOrChildrenAboard"]
    fare = request.json["fare"]

    sql = "UPDATE passengers SET Survived='%s', Pclass='%s', Name='%s', Sex='%s', Age='%s', `Siblings/Spouses Aboard`='%s', `Parents/Children Aboard`='%s', Fare='%s' WHERE UUID='%s'"
    data = (survived,pclass,name,sex,age,siblings,parents,fare,uuid) 

    try:
      conn = masterconn.cursor()
      conn.execute(sql,data)
      masterconn.commit()

      resp = jsonify('updated')
      resp.status_code = 200

    except:
      resp = jsonify('Not found')
      resp.status_code = 404
      return resp
      
##Something to respond to health checks that won't bombard the db
class Health(Resource):
 def get(self):
   return(TRUE)

api.add_resource(People, '/people/<string:uuid>')
api.add_resource(Health, '/health')

if __name__ == '__main__':
     app.run(host='0.0.0.0')
