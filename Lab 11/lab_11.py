import sqlite3

persons = {}
scores = []

try:
    # Connect to DB and create a cursor
    sqliteConnection = sqlite3.connect('sql.db')
    cursor = sqliteConnection.cursor()
    print('DB Init')
 
    #List of setup querys
    #Make tables if they don't exists already
    #Persons table id is primary key so no diplicates will be made by ID
    #Scores tables gets unique index so scores are not duplicated aswell when re-running the code
    query = ["CREATE TABLE IF NOT EXISTS persons (id INTEGER PRIMARY KEY, f_name TEXT NOT NULL, l_name TEXT NOT NULL);", "CREATE TABLE IF NOT EXISTS scores (p_id INTEGER NOT NULL, task INTEGER,points INTEGER,FOREIGN KEY (p_id) REFERENCES persons (id));","CREATE UNIQUE INDEX IF NOT EXISTS upg ON scores(p_id,task,points);"]
    for q in query:
        cursor.execute(q)
    
    with open(r'Lab 11\score2.txt', 'r') as file:
        for line in file:
            if line:
                _, task, first, last, point = line.strip().split()
                person = {"f_name":first, "l_name":last}
                if person not in persons.values():
                    id = len(persons)
                    persons[id] = person
                p_id = list(persons.keys())[list(persons.values()).index(person)]
                scores.append([p_id,task,point])
                
    for id in persons.keys():
        f = persons.get(id).get('f_name')
        l = persons.get(id).get('l_name')
        cursor.execute("INSERT OR IGNORE INTO persons VALUES (?,?,?)",(id,f,l))
    
    for score in scores:
        p_id, task, point = score
        cursor.execute("INSERT OR IGNORE INTO scores VALUES(?,?,?)",(p_id,task,point))
        
    sqliteConnection.commit()

    #Get stuff querys
    q_get_scores = "SELECT p.f_name, p.l_name, SUM(s.points) AS top FROM persons p JOIN scores s ON s.p_id = p.id GROUP BY p.f_name, p.l_name, p.id ORDER BY top DESC LIMIT 10"
    q_most_diff = "SELECT task, SUM(points) AS hardest FROM scores GROUP BY task ORDER BY hardest ASC LIMIT 10"
    
    cursor.execute(q_get_scores)
    get_scores = cursor.fetchall()
    
    cursor.execute(q_most_diff)
    most_diff = cursor.fetchall()
    
    print("\n")
    for q in get_scores:
        f,l,s = q
        print(f"{f} {l} has {s} points")
    print("\n")
    for p in most_diff:
        t,s = p
        print(f"Task:{t} had {s} total points")
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