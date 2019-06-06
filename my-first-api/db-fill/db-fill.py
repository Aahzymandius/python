import pymysql
import os

passwd = ''
db = os.environ['DATABASE']
writeserver = os.environ['MASTER']

##Wait for the db to initialize
x=0
while x==0:
  try:
    master = pymysql.connect(writeserver,'root',passwd,db,local_infile=1)
    conn = master.cursor()
    ready = conn.execute("SELECT 1")
  except:
    ready = 0
    error = "waiting on db"
    print(error)
  
  if ready == 1:
    x=1

#Prepare the db connection
master = pymysql.connect(writeserver,'root',passwd,db,local_infile=1)
conn = master.cursor()

table = "CREATE TABLE passengers (UUID VARCHAR(40) PRIMARY KEY NOT NULL, Survived BOOLEAN NOT NULL, \
           Pclass INT NOT NULL, Name VARCHAR(255) NOT NULL, Sex ENUM('male','female','other') NOT NULL, \
           Age INT NOT NULL, `Siblings/Spouses Aboard` INT NOT NULL, `Parents/Children Aboard` INT NOT NULL, \
           Fare DECIMAL(10,5) NOT NULL)"

trigger = "CREATE TRIGGER generate_uuid BEFORE INSERT ON passengers FOR EACH ROW SET new.UUID=uuid()"

try:
  conn.execute(table)
except:
  print('table already exists')

conn.execute(trigger)

load = "LOAD DATA LOCAL INFILE './titanic.csv' INTO TABLE passengers \
           FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' IGNORE 1 ROWS \
           (Survived,Pclass,Name,Sex,Age,`Siblings/Spouses Aboard`,`Parents/Children Aboard`,Fare)"

conn.execute(load)

master.commit()
master.close()
