import pymysql
import csv
# database connection
connection = pymysql.connect(host="localhost", user="root", passwd="", database="nexttrain")
cursor = connection.cursor()

def main():
    # some other statements  with the help of cursor
    retrive = "Select LineID, LineName from raillines"
    # executing the quires
    cursor.execute(retrive)
    rows = cursor.fetchall()
    #if the quirey returns a result get the lines
    if rows != None:
        RetriveLine(rows)

def RetriveLine(rows):
    print("Available Lines:\n")
    count = 0
    lines = []
    #for each of the returned results
    for row in rows:
        count += 1
        #add line objects to a list
        lines.append(Line(row[1], row[0]))
        #provide user with a selection list
        print(f"{count}\t{row[1]}")
    #ask user for input
    val = input("Select Line (by number or 'all'): " )
    selection = 0
    if val != "all":
        selection = int(val)
        l = lines[selection - 1]
        val = input(f"{l.name} departure Time(eg 13:30): ")
        hours = val.split(":")
        time = (60 * int(hours[0]) + int(hours[1]))
        GenerateTimeTable(time, l)
    else:
        for l in lines:
            val = input(f"{l.name} departure Time(eg 13:30): ")
            hours = val.split(":")
            time = (60 * int(hours[0]) + int(hours[1]))
            GenerateTimeTable(time, l)

def GenerateTimeTable(startTime, line):
    time = startTime
    retrive = f"SELECT StationID FROM stationlines WHERE LineID = '{line.id}' ORDER BY StopNumber"
    cursor.execute(retrive)
    rows = [x[0] for x in cursor.fetchall()]
    stations = []
    for row in rows:
        retrive = f"SELECT StationName, StationID FROM stations WHERE StationID = '{row}'"
        cursor.execute(retrive)
        stationRows = cursor.fetchall()
        for sRow in stationRows:
            stations.append(Station(sRow[0], sRow[1]))
    retrive = f"SELECT RailID FROM linesegments WHERE LineID = '{line.id}'"
    cursor.execute(retrive)
    rows = [x[0] for x in cursor.fetchall()]
    rails = []
    for row in rows:
        retrive = f"SELECT * FROM rails WHERE RailID = '{row}'"
        cursor.execute(retrive)
        railRows = cursor.fetchall()
        print(railRows)
        for rR in railRows:
            rails.append(Rail(rR[0], rR[1], rR[2], rR[3], rR[4]))
    prior = ""
    timeTable = []
    for s in stations:
        if prior != "":
            for r in rails:
                print(r.startStation, r.endStation)
                if (r.startStation == prior and r.endStation == s.id) or (r.startStation == s.id and r.endStation == prior):
                    print(r.length)
                    time += int(r.length)
        timeTable += [[f"{s.name}, {time}"]]
        prior = s.id
    with open(f'{line.name}.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(timeTable)

class Line:
    def __init__(self, name, id):
        self.name = name
        self.id = id
class Station:
    def __init__(self, name, id):
        self.name = name
        self.id = id
class Rail:
    def __init__(self, id, length, width, startStation, endStation):
        self.id = id
        self.length = length
        self.width = width
        self.startStation = startStation
        self.endStation = endStation

if __name__ == "__main__":
    main()

# commiting the connection then closing it.
connection.commit()
connection.close()
