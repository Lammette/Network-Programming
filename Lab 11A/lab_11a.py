import urllib.request
import re
import sqlite3

# "(ch-\w*).*?schedule.*?\[(.*?)\] Get channel schedule
#{\\\\"descriptionRaw\\\\":\\\\"(?:(.*?))(?:\.|\\).*?"name\W*(.*?)\\\\.*?subHeading\\\\":\\\\"(?:(.*?))\\\\.*?startTime.*?(\d{2}:\d{2}).*?start.*?(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})#get programs

ch = {}
startDate = 1
dateforwards = 10
program = "Rapport"
channel = "ch-barnkanalen"

try:
   # Connect to DB and create a cursor
   sqliteConnection = sqlite3.connect('svt.db')
   cursor = sqliteConnection.cursor()
   print('DB Init')

   #List of setup querys
   #Make tables if they don't exists already
   #Persons table id is primary key so no diplicates will be made by ID
   #Scores tables gets unique index so scores are not duplicated aswell when re-running the code
   query = ["CREATE TABLE IF NOT EXISTS channels (id INTEGER PRIMARY KEY, ch_name TEXT);", 
            "CREATE TABLE IF NOT EXISTS programs (ch_id INTEGER NOT NULL, desc TEXT, name TEXT, subH TEXT, startTime TEXT, date TEXT,FOREIGN KEY (ch_id) REFERENCES channels (id));",
            "CREATE UNIQUE INDEX IF NOT EXISTS pro_id ON programs (ch_id, desc, name, subH, startTime, date);"]
   for q in query:
      cursor.execute(q)

   for i in range (startDate,(startDate + dateforwards)):
      req = urllib.request.Request(f'https://www.svtplay.se/kanaler?date=2024-11-{i}')
      with urllib.request.urlopen(req) as response:
         data = response.read().decode()
         channels = re.findall(r'"(ch-\w*).*?schedule.*?\[(.*?)\]', data )
         for c in channels:
            ch_name = c[0]
            if ch_name not in ch.values():
               id = len(ch)
               ch[id] = ch_name
               cursor.execute("INSERT OR IGNORE INTO channels VALUES (?,?)",(id, ch_name))
            programs = re.findall(r'{\\\\"descriptionRaw\\\\":\\\\"(?:(.*?))(?:\.|\\).*?"name\W*(.*?)\\\\.*?subHeading\\\\":\\\\"(?:(.*?))\\\\.*?startTime.*?(\d{2}:\d{2}).*?start.*?(\d{4}-\d{2}-\d{2})', str(c))
            ch_id = list(ch.keys())[list(ch.values()).index(ch_name)]
            for p in programs:
               desc, name, subh, start, date = p
               cursor.execute("INSERT OR IGNORE INTO programs VALUES(?,?,?,?,?,?)", (ch_id,desc,name,subh,start,date))
   sqliteConnection.commit()


   get_by_program = f"SELECT p.date, p.name, c.ch_name, p.startTime, p.subH, p.desc FROM channels c JOIN programs p on p.ch_id = c.id WHERE p.name = '{program}'"

   get_by_channel = f"SELECT p.date, p.name, c.ch_name, p.startTime, p.subH, p.desc FROM channels c JOIN programs p on p.ch_id = c.id WHERE c.ch_name = '{channel}'"

   got_programs = cursor.execute(get_by_program).fetchall()

   got_channels = cursor.execute(get_by_channel).fetchall()

   for p in got_programs:
      print("--------------------")
      print(f"date\t\t:{p[0]}")
      print(f"name\t\t:{p[1]}")
      print(f"channel\t\t:{p[2]}")
      print(f"startTime\t:{p[3]}")
      print(f"subHeading\t:{p[4]}")
      print(f"description\t:{p[5]}")

   print(f"\n\n--------------------------------------------------\n\n")

   for c in got_channels:
         print("--------------------")
         print(f"date\t\t:{c[0]}")
         print(f"name\t\t:{c[1]}")
         print(f"channel\t\t:{c[2]}")
         print(f"startTime\t:{c[3]}")
         print(f"subHeading\t:{c[4]}")
         print(f"description\t:{c[5]}")
      
   

   # Close the cursor
   cursor.close()

# Handle errors
except sqlite3.Error as error:
    print('Error occurred - ', error)
 
# Close DB Connection irrespective of success
# or failure

finally:
    
    if sqliteConnection:
        sqliteConnection.close()
        print('SQLite Connection closed')