f = open(r"Lab 2\score2.txt", "r") #Change if needed

res = {}

for row in f:
    first,last,points = row.strip().split()[-3:]
    name = first + " " + last
    if name not in res: #Add the person to the dictionary if they aren't already in there
        res[name] = 0
    res[name] += int(points)
    
points = max(res.values())                                  #Get the highest points
mvp = [person for person in res if res[person] == points]   #Get the people with the highest points
if len(mvp) > 1:
    print("The people with the most points are", " and ".join(mvp), "with ", points," points")
else:
    print("The person with the most points is", "".join(mvp), "with ", points," points")

    
