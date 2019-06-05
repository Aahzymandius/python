from flask import Flask, request, jsonify,Response
from flask_restful import Resource, Api
import pymysql
import json
import os

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

  def get(self):
    conn = readconn.cursor()
    query = conn.execute("SELECT * FROM passengers")

    response=[]
    results = conn.fetchall()
    for row in results:
      UUID = row[0]
      Survived = row[1]
      Pclass = row[2]
      Name = row[3]
      Sex = row[4]
      Age = row[5]
      Siblings = row[6]
      Parents = row[7]
      Fare = row[8]
      x = "UUID=%s,Survived=%s,Pclass=%d,Name=%s,Sex=%s,Age=%s,SiblingsOrSpouses=%s,ParentsOrChildren=%s,Fare=%d" % (UUID, Survived, Pclass, Name, Sex,Age, Siblings, Parents, Fare)
      response.append([x])
    
    return jsonify(response)
    
  def post(self):
    conn = masterconn.cursor()
    
    survived = request.json["survived"]
    pclass = request.json["passengerClass"]
    name = request.json["name"]
    sex = request.json["sex"]
    age = request.json["age"]
    siblings = request.json["siblingsOrSpousesAboard"]
    parents = request.json["parentsOrChildrenAboard"]
    fare = request.json["fare"]
    
    sql = "INSERT INTO passengers (Survived, Pclass, Name, Sex, Age, `Siblings/Spouses Aboard`, `Parents/Children Aboard`, Fare) \
      VALUES ('%s','%s','%s','%s','%s','%s','%s','%s')" % (survived, pclass, name, sex, age, siblings, parents, fare)
    
    update = conn.execute(sql)
    query = conn.execute("SELECT * FROM passengers WHERE Name = '%s'" % name)
    lastEntry = conn.fetchone()
    
    UUID = lastEntry[0]
    Survived = lastEntry[1]
    Pclass = lastEntry[2]
    Name = lastEntry[3]
    Sex = lastEntry[4]
    Age = lastEntry[5]
    Siblings = lastEntry[6]
    Parents = lastEntry[7]
    Fare = lastEntry[8]
    
    response = {UUID: %s, Survived: %s, Pclass: %s, Name: %s, Sex: %s, Age: %s, SiblingsOrSpouses: %s, ParentsOrChildren: %s, Fare: %d} % (UUID, Survived, Pclass, Name, Sex,Age, Siblings, Parents, Fare)
    
    return jsonify(response)

##Something to respond to health checks that won't bombard the db
class Health(Resource):
 def get(self):
   return(TRUE)

api.add_resource(People, '/people')
api.add_resource(Health, '/health')

if __name__ == '__main__':
     app.run(host='0.0.0.0',port=5000)
