import pymysql
import csv
# database connection
connection = pymysql.connect(host="localhost", user="root", passwd="", database="nexttrain")
# Establish cursor
cursor = connection.cursor()

def main():
    # some other statements  with the help of cursor
    retrive = "Select LineID, LineName from raillines"
    # executing the quires
    cursor.execute(retrive)
    rows = cursor.fetchall()
    # if the quirey returns a result get the lines
    if rows != None:
        RetriveLine(rows)

def RetriveLine(rows):
    print("Available Lines:\n")
    count = 0
    lines = []
    # for each of the returned results
    for row in rows:
        count += 1
        # add line objects to a list
        lines.append(Line(row[1], row[0]))
        # provide user with a selection list
        print(f"{count}\t{row[1]}")
    # ask user for input
    val = input("Select Line (by number or 'all'): " )
    selection = 0
    # If user Imput was a specific line
    # NOTE TO SELF: Need to add input validation at some point
    if val.lower() != "all":
        # set selection to user imput value
        selection = int(val
        # get the requested line
        l = lines[selection - 1]
        # user imputs the departure time
        val = input(f"{l.name} departure Time(eg 13:30): ")
        # split the hours from the minutes
        hours = val.split(":")
        # Convert the hours into minutes and add them to minutes already there
        time = (60 * int(hours[0]) + int(hours[1]))
        # generate the timetable with changes
        GenerateTimeTable(time, l)
    # if user imput was 'all'
    else:
        for l in lines:
            # user imputs the departure time
            val = input(f"{l.name} departure Time(eg 13:30): ")
            # split the hours from the minutes
            hours = val.split(":")
            # Convert the hours into minutes and add them to minutes already there
            time = (60 * int(hours[0]) + int(hours[1]))
            # generate the timetable with changes
            GenerateTimeTable(time, l)

def GenerateTimeTable(startTime, line):
    # define time as the startime
    time = startTime
    # retrive is set as the stations from inputted line
    retrive = f"SELECT StationID FROM stationlines WHERE LineID = '{line.id}' ORDER BY StopNumber"
    # run the retrive function
    cursor.execute(retrive)
    rows = [x[0] for x in cursor.fetchall()]
    stations = []
    # for each row
    for row in rows:
        # get the station
        retrive = f"SELECT StationName, StationID FROM stations WHERE StationID = '{row}'"
        cursor.execute(retrive)
        stationRows = cursor.fetchall()
        # append to the station
        for sRow in stationRows:
            stations.append(Station(sRow[0], sRow[1]))
    # get the railID
    retrive = f"SELECT RailID FROM linesegments WHERE LineID = '{line.id}'"
    cursor.execute(retrive)
    rows = [x[0] for x in cursor.fetchall()]
    rails = []
    # for each row print rows data, then append the row
    for row in rows:
        retrive = f"SELECT * FROM rails WHERE RailID = '{row}'"
        cursor.execute(retrive)
        railRows = cursor.fetchall()
        print(railRows)
        for rR in railRows:
            rails.append(Rail(rR[0], rR[1], rR[2], rR[3], rR[4]))
    prior = ""
    timeTable = []
    # for each station, print the inforation for the station, set the last station as current staiton, write to the CSV file.
    for s in stations:
        if prior != "":
            for r in rails:
                print(r.startStation, r.endStation)
                if (r.startStation == prior and r.endStation == s.id) or (r.startStation == s.id and r.endStation == prior):
                    print(r.length)
                    time += int(r.length)
        # update the timetable
        timeTable += [[f"{s.name}, {time}"]]
        # set the prior station
        prior = s.id
    # write to csv
    with open(f'{line.name}.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(timeTable)

# defines of the classes for SQL
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
