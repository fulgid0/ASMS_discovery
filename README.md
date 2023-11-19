# ASMS_discovery
Public available SMS scraper - Ver 0.2


HOW TO USE:
Download both Python codes (python3):

-The DB creation runs first in order to create the database;

-ASMS_discovery.py scan all sites (for now only receive-smss.com) and fetch all available number and visible messages (taking in account also the sender and avoiding entry duplication). It fetch the webservices pool every 3 minutes.

To do:

-comand line setup of refresh time

-colorful prompt

-Make the script more modular

-make a list of other interesting sites (ReadME page)

-implement other sites parser


------Improvements already covered:

-change time_stamp format

-Execpetion handling (bad queries, unexpected data format)
