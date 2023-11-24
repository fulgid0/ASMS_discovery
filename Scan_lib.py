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
    print ("New finding: " + Message + " [" + Service.strip() + "] - Records created successfully");

def escaping(var_str):
 escaped = var_str.translate(str.maketrans({"-":  r"\-",
                                          "]":  r"\]",
                                          "\\": r"\\",
                                          "^":  r"\^",
                                          "$":  r"\$",
                                          "*":  r"\*",
                                          "'":  r"''",
                                          "@":  r"\@",
                                          "\x00":  r"",
                                          ".":  r"\."}))
 return escaped
 
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
    escaped = escaping(Message)
    DB_Extr(conn, Subdomain, number, Service, escaped, Time)
    flag = 0
 os.system("rm "+sup_file)

'''
                                            <tr>
                            <td>
                                67XXX
                            </td>
                            <td>
                                5 hours ago
                            </td>
                            <td>
                                PayPal: Thanks for confirming your phone number. Log in or get the app to manage your account information: https://py.pl/53xEDXoWQsC
                            </td>
                        </tr>
                        '''

def Scan_Smstome_sms(conn, number_link):
 number = number_link.split('phone/')[1].split('/')[0]
 print("Let's start smstome SCAN of "+number+" from [ "+number_link.split('/')[1].split('/')[0]+" ]")
 url = "https://smstome.com" + number_link
 sup_file= 'SMS-' + number
 os.system("wget -O " + sup_file + " -q " + url)
 Subdomain = "smstome.com"
 flag = 0
 with open(sup_file) as file:
  for line in file:
   if '                                            <tr>' in line and flag == 0:
    flag = flag+1
   elif 'td>' in line and flag !=0:
    flag = flag+1
   elif 'td>' not in line and flag !=0:
    if flag==2:
     Service_sup = line.split('                                ')[1].split('"')[0]
     Service = Service_sup
     flag=flag+1
    elif flag == 5:
     Time = line.split('                                ')[1] 
     flag = flag+1
    elif flag == 8:
     Message = line.split('                                ')[1]
     flag = flag+1
    elif flag > 9:
     escaped = escaping(Message)
     DB_Extr(conn, Subdomain, number, Service, escaped, Time)
     flag = 0
 os.system("rm "+sup_file)

