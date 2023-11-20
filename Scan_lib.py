#!/usr/bin/python

import os
import sqlite3, time, re
import subprocess

def DB_Extr(conn, Subdomain, number, Service, Message, Time):
 query = "SELECT * FROM Extraction WHERE Message= '" + Message + "'"
 try:
  cursor = conn.execute(query)
 except:
  Bad_query ='echo "'+query+'" >> BAD_QUERIES.txt'
  os.system(Bad_query)
 else:
  row = cursor.fetchone()
  Date_query = "date +%e/%0m/%Y-%k:%M"
  rc = subprocess.run( [ Date_query ], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  Time_stamp= rc.stdout.decode().strip()
  if row is None:
   query1= "INSERT INTO Extraction (Subdomain, Number, Service, Message, Time, Time_stamp) VALUES ('"+Subdomain+"',  '"+number+"', '"+Service+"', '"+Message+"', '"+Time+"', '"+Time_stamp+"')"
   try:
    cursor = conn.execute(query1)
    conn.commit()
   except:
    Bad_query ='echo "'+query1+'" >> BAD_QUERIES.txt'
    os.system(Bad_query)
   else:
    print ("New finding: " + Message + " [" + Service + "] - Records created successfully");

def Scan_Receive_sms(conn, number):
 print("Let's start Receive_smss SCAN of "+number)
 url = "https://receive-smss.com/sms/" + number + "/"
 sup_file= 'SMS-' + number
 os.system("wget -O " + sup_file + " -q " + url)
 Subdomain = "receive-smss.com"
 flag = 0
 with open(sup_file) as file:
  for line in file:
   if '<label>Sender</label><br><a href="/receive-sms-from-' in line:
    Service_sup = line.split('<label>Sender</label><br><a href="/receive-sms-from-')[1].split('"')[0]
    Service = Service_sup
    flag = flag+1
   if '<label>Message</label><br><span>' in line:
    Message = line.split('<label>Message</label><br><span>')[1].split('</span></div>')[0]  
    flag = flag+1
   if '<label>Time</label><br>' in line:
    Time = line.split('<label>Time</label><br>')[1].split('</div>')[0]  
    flag = flag+1
   if flag > 2:
    escaped = Message.translate(str.maketrans({"-":  r"\-",
                                          "]":  r"\]",
                                          "\\": r"\\",
                                          "^":  r"\^",
                                          "$":  r"\$",
                                          "*":  r"\*",
                                          "'":  r"''",
                                          "@":  r"\@",
                                          "\x00":  r"",
                                          ".":  r"\."}))
    DB_Extr(conn, Subdomain, number, Service, escaped, Time)
    flag = 0
 os.system("rm "+sup_file)

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