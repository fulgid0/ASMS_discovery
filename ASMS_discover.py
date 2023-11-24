#!/usr/bin/python

import os
import sqlite3, time, re
import subprocess
from random import randint
from Scan_lib import Scan_Receive_sms, Scan_Smstome_sms
 
def Scansione(conn):
 cursor = conn.execute("SELECT Subdomain, Number FROM Anagrafica")
 cursor.fetchone()
 for row in cursor:
  if "receive-smss.com" in row:
   Scan_Receive_sms(conn,row[1].split("+")[1])
  if "smstome.com" in row:
   Scan_Smstome_sms(conn,row[1]) #### CONTROLLARE PERCHE SOLO UN GIRO
 
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

def Ana_SMStome():
 print ("ANAGRAFICA smstome.com");
 conn = sqlite3.connect('SMS_DB.db')
 sup_file= 'SMStome'
 os.system("wget -O " + sup_file + " " + 'https://smstome.com/')
 subdomain = "smstome.com"
 flag = 0
 flag2 = 0
 with open(sup_file) as file:
  for line in file:
   if '                            <a href="' in line and '/country/' in line:
    sup_2 = line.split('                            <a href="')[1].split('" class="button button-clear">')[0]
    nation = sup_2.split('/country/')[1].split('/')[0]
    flag = flag+1
   if flag > 1:
    flag = 0
    sup_file2 = "SMStome_"+nation
    os.system("wget -O " + sup_file2 + " " + 'https://smstome.com'+sup_2+"?page="+str(randint(1, 30)))
    with open(sup_file2) as file:
     for line2 in file:
      if 'button button-outline button-small numbutton' in line2:
       number_link = line2.split('<a href="https://smstome.com')[1].split('" class=')[0]
       flag2 = flag2+1
      if flag2 > 1:
       alive = "none"
       DB_Ana(conn, subdomain, number_link, alive, nation)
       flag2 = 0    
    os.system("rm "+sup_file2)
 Scansione(conn)
 os.system("rm "+sup_file)
 conn.close()
 
while True: 
 Ana_Receive_smss()
 Ana_SMStome()
 print("---- Execution Hold ---- at time: ")
 str(os.system("date +%k:%M.%S")).strip()
 time.sleep(180)
