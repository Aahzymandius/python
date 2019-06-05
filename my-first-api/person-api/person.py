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


class People(Resource):
  def get(self,uuid):

    sql = "SELECT * FROM passengers WHERE UUID='%s'" % uuid

    try:

      conn = readconn.cursor()
      conn.execute(sql)
      query = conn.fetchone()
      result = json_format(query)

      resp = jsonify(result)
      resp.response_code = 200
      return resp

    except:
      resp = jsonify("Passenger not found")
      resp.status_code = 404
      return resp


  def delete(self,uuid):

    sql = "DELETE FROM passengers WHERE UUID='%s'" % uuid

    try:

      conn = masterconn.cursor()
      conn.execute(sql)
      masterconn.commit()

      resp = jsonify('OK')
      resp.status_code = 200
      return resp

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
      return resp

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
