import pymysql
import csv
from os import system, name
from time import sleep
# database connection
connection = pymysql.connect(host="localhost", user="root", passwd="", database="nexttrain")
# Establish cursor
cursor = connection.cursor()

def main():
    CheckAvailiablity()
    # some other statements  with the help of cursor
    retrive = "Select LineID, LineName from raillines"
    # executing the quires
    cursor.execute(retrive)
    rows = cursor.fetchall()
    # if the quirey returns a result get the lines
    if rows != None:
        RetriveLine(rows)

def CleanSchedule():
    action = "DELETE from schedule"
    cursor.execute(action)

def CheckAvailiablity():
    retrive = "Select StationID from stations"
    cursor.execute(retrive)
    rows = cursor.fetchall()
    if rows != None:
        for r in rows:
            retrive = f"SELECT COUNT(PlatformNumber) FROM platforms WHERE Occupied = 0 AND StationID = '{r}'"
            cursor.execute(retrive)
            count = cursor.fetchall()
            retrive = "Select StationID, AvailableSpaces, Time from schedule"
            cursor.execute(retrive)
            sched = cursor.fetchall()
            for s in sched:
                if r == s[0]:
                    input(f"{s[0]}, {r}")
                    hours = s[2].split(":")
                    time = (60 * int(hours[0]) + int(hours[1]))
                    sAvailibilities.append(r, s[1], time)


def RetriveLine(rows):
    print("Available Lines:\n")
    lines = []
    val = ""
    while val.lower() != "exit":
        count = 0
        # for each of the returned results
        for row in rows:
            count += 1
            # add line objects to a list
            lines.append(Line(row[1], row[0]))
            # provide user with a selection list
            print(f"{count}\t{row[1]}")
        # ask user for input
        val = input("Select Line or type 'exit' (by number or 'all'): ")
        selection = 0
        # If user Imput wants a specific line
        if val.isdigit():
            # set selection to user imput value
            selection = int(val)
            # get the requested line
            l = lines[selection - 1]
            # user imputs the departure time
            val = input(f"{l.name} departure Time(eg 13:30): ")
            # split the hours from the minutes
            hours = val.split(":")
            # Convert the hours into minutes and add them to minutes already there
            time = (60 * int(hours[0]) + int(hours[1]))
            # generate the timetable with changes
            if GenerateTimeTable(time, l):
                val2 = input("Continue? (y/n)")
                if val2.lower() == "yes" or "y":
                    Clear()
                elif val2.lower() == "no" or "n":
                    val = "exit"
                    print("Goodbye")
                    sleep(1)
        # if user imput was 'all'
        elif val.lower() == "all":
            for l in lines:
                # user imputs the departure time
                val = input(f"{l.name} departure Time(eg 13:30): ")
                # split the hours from the minutes
                hours = val.split(":")
                # Convert the hours into minutes and add them to minutes already there
                time = (60 * int(hours[0]) + int(hours[1]))
                # generate the timetable with changes
                if GenerateTimeTable(time, l):
                    val2 = input("Continue? (y/n)")
                    if val2.lower() == "yes" or "y":
                        Clear()
                    elif val2.lower() == "no" or "n":
                        val = "exit"
                        print("Goodbye")
                        sleep(1)
        elif val.lower() == "clear":
            CleanSchedule()
        elif val.lower() == "exit":
            print("Goodbye")
            sleep(1)
        else:
            print(f"{val} is not a recognised input, please enter a valid input")
            input("Press enter to continue")
            Clear()

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
        retrive = f"SELECT COUNT(PlatformNumber) FROM platforms WHERE Occupied = 0 AND StationID = '{row}'"
        cursor.execute(retrive)
        tempRows = [x[0] for x in cursor.fetchall()]
        # append to the station
        for sRow in stationRows:
            stations.append(Station(sRow[0], sRow[1], tempRows[0]))
    # get the railID
    retrive = f"SELECT RailID FROM linesegments WHERE LineID = '{line.id}'"
    cursor.execute(retrive)
    rows = [x[0] for x in cursor.fetchall()]
    rails = []
    # for each row append the row
    for row in rows:
        retrive = f"SELECT * FROM rails WHERE RailID = '{row}'"
        cursor.execute(retrive)
        railRows = cursor.fetchall()
        for rR in railRows:
            rails.append(Rail(rR[0], rR[1], rR[2], rR[3], rR[4]))
    prior = ""
    timeTable = []
    # for each station, print the inforation for the station, set the last station as current staiton, write to the CSV file.
    canGen = 1
    for s in stations:
        if prior != "":
            for r in rails:
                if (r.startStation == prior and r.endStation == s.id) or (r.startStation == s.id and r.endStation == prior):
                    time += int(r.length)
        for sa in sAvailibilities:
            if (sa.stationID == s.id and sa.time == time):
                if (sa.freePlatforms > 0):
                    sa.TrainArrival()
                    canGen = 1
                else:
                    canGen = 0
                    for a in sAvailibilities:
                        if (a.stationID == s.id and ((a.time == time + 5 and a.freePlatforms > 0) or (a.time == time - 5 and a.freePlatforms > 0))):
                            if(a.time == time - 5):
                                startTime -= 5
                            else:
                                startTime += 5
                        else:
                            startTime -= 5
                    break
            else:
                sAvailibilities.append(StationAvailability(s.id, s.platforms, time))
        # update the timetable
        timeTable += [[f"{s.name}, {time}"]]
        # set the prior station
        prior = s.id
    # write to csv
    if (canGen == 1):
        for s in stations:
            for sa in sAvailibilities:
                if sa.stationID == s.stationID:

                    hours, minutes = divmod(sa.time/60, 1)

                    write = f"INSERT INTO `schedule` (`StationID`, `Time`, `AvailableSpaces`) VALUES ('{s.stationID}', '', '{hours}:{minutes}:00', '{sa.freePlatforms}')"
                    cursor.execute(write)
                    input("_")
        with open(f'{line.name}.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(timeTable)
        return bool(timeTable)
    else:
        return GenerateTimeTable(starTime, line)

def Clear():
    # for windows
    if name == 'nt':
        _ = system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')

sAvailibilities = []

# defines of the classes for SQL
class StationAvailability:
    def __init__(self, stationID, freePlatforms, time):
        self.stationID = stationID
        self.freePlatforms = freePlatforms
        self.time = time
    def TrainArrival(self):
        self.freePlatforms -= 1
class Line:
    def __init__(self, name, id):
        self.name = name
        self.id = id
class Station:
    def __init__(self, name, id, platforms):
        self.name = name
        self.id = id
        self.platforms = platforms
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
