#!/usr/bin/python

import sqlite3

conn = sqlite3.connect('SMS_DB.db')
print ("Opened database successfully");

conn.execute('''CREATE TABLE "Extraction" (
        "SubDomain"     TEXT NOT NULL,
        "Number"   TEXT,
        "Service"        TEXT,
        "Message"	TEXT,
        "Time"	TEXT DEFAULT NULL,
        "Time_stamp" TEXT DEFAULT NULL,
       	"Key"	INTEGER NOT NULL,
	PRIMARY KEY("Key" AUTOINCREMENT)
);''')

conn.execute('''CREATE TABLE "Anagrafica" (
        "SubDomain"     TEXT NOT NULL,
        "Number"   	TEXT,
        "Alive"        	TEXT,
        "Nation"	TEXT,
       	"Key"	INTEGER NOT NULL,
	PRIMARY KEY("Key" AUTOINCREMENT)
);''')


print ("Tables created successfully");

conn.close()
