#!/usr/bin/python

import os
import sqlite3, time, re
import subprocess
from Scan_lib import Scan_Receive_sms, Ana_Receive_smss
 
def Scansione(conn):
 cursor = conn.execute("SELECT Subdomain, Number FROM Anagrafica")
 cursor.fetchone()
 for row in cursor:
  if "receive-smss.com" in row:
   Scan_Receive_sms(conn,row[1].split("+")[1]) #### CONTROLLARE PERCHE SOLO UN GIRO
 
def DB_Ana(conn, Subdomain, Number, Alive, Nation):
 cursor = conn.execute("SELECT * FROM Anagrafica WHERE Number= '" + Number + "' AND Nation= '" +Nation+"'")
 row = cursor.fetchone()
 if row is None:
  query1= "INSERT INTO Anagrafica (Subdomain, Number, Alive, Nation) VALUES ('"+Subdomain+"', '"+Number+"',  '"+Alive+"', '"+Nation+"')"
  cursor = conn.execute(query1)
  conn.commit()
  print ("New finding: " + Number + " [" + Nation + "] - Records created successfully");

def Ana_Receive_smss():
 print ("ANAGRAFICA Receive-smss.com");
 conn = sqlite3.connect('SMS_DB.db')
 sup_file= 'receive-smss'
 os.system("wget -O " + sup_file + " " + 'https://receive-smss.com/')
 subdomain = "receive-smss.com"
 flag = 0
 with open(sup_file) as file:
  for line in file:
   if '<div class="number-boxes-itemm-number" style="color:black">' in line:
    number = line.split('<div class="number-boxes-itemm-number" style="color:black">')[1].split('</div>')[0]
    flag = flag+1
   if '<div class="number-boxes-item-country number-boxess-item-country">' in line:
    nation = line.split('<div class="number-boxes-item-country number-boxess-item-country">')[1].split('</div>')[0]  
    flag = flag+1
   if flag > 1:
    alive = "none"
    DB_Ana(conn, subdomain, number, alive, nation)
    flag = 0
    number = "NULL"
    nation = "NULL"
 os.system("rm "+sup_file)
 Scansione(conn)
 conn.close()

while True: 
 Ana_Receive_smss()
 Data_prompt= os.system("date +%k:%M.%S")
 print("---- "+str(Data_prompt)+" Execution Hold----")
 time.sleep(180)
