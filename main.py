import csv
from datetime import datetime
from pandas import read_csv
from pandas import DataFrame
import warnings
from tkinter import Tk
from tkinter.filedialog import askopenfilename

root = Tk()
root.withdraw()

#Select the csv file
filename = askopenfilename()
warnings.filterwarnings("ignore")

def delete(filename):
    csv_file = open(filename)
    csv_reader = csv.reader(csv_file, delimiter=",")
    next(csv_reader)
    
    df = read_csv(filename, encoding='gbk')

    Location = []
    index = -1
    
    #Remove Invalid Sign In Location
    Location = df['Sign In Location']
    
    for row in Location:
        index += 1
        if 'WIFI' in row or 'Hongxin Wireless Communication Industrial Park' in row:
            df = df.drop(index)
    return df

#Overtime Working Time Count
def count_work_times(df):
    #Find the Day of the Sign In Date
    Time = df['Sign In Time']
    Name = df['Name']
    Week_Day = []
    
    for row in Time:
        whatday = int(datetime.strptime(row,'%Y-%m-%d %H:%M:%S').strftime("%w"))
        if whatday == 0:
            whatday = 7
        Week_Day.append(whatday)
    
    data = df[['Employee ID','Name','Sign In Time','Sign In Date']]
    data['Day'] = [i for i in Week_Day]
    
    #Find if Overtime Working During the Weekdays
    weekday = data[data['Day'] < 6]
    weekday_time = weekday['Sign In Time']
    weekday_hour = []
    
    weekday_Name = {}.fromkeys(weekday['Name']).keys()
    weekday_Date = {}.fromkeys(weekday['Sign In Date']).keys()
    weekday_ID = {}.fromkeys(weekday['Employee ID']).keys()
    
    for row in weekday_time:
        whichhour = int(datetime.strptime(row,'%Y-%m-%d %H:%M:%S').strftime("%H"))
        weekday_hour.append(whichhour)
    
    weekday['Hour'] = [i for i in weekday_hour]
    weekday['Overtime'] = [i >= 20 for i in weekday_hour]
    weekday['Overtime'] += 0
    
    a = [] #Name
    b = [] #Date
    c = [] #Overtime Working Times
    count = 0
    
    for i in weekday_Name:
        for j in weekday_Date:
            work = weekday[(weekday['Name'] == i) & (weekday['Sign In Date'] == j)]
            work_time = work['Hour']
            if len(work_time) > 0:
                if (max(work_time) >= 20):
                    count += 1
                else:
                    count += 0
            a.append(i)
            b.append(j)
            c.append(count)
            count = 0
    
    #Find if Overtime Working During the Weekends
    weekend = data[data['Day'] > 5]
    weekend_time = weekend['Sign In Time']
    weekend_hour = []
    weekend_minute = []
    decimal_time = []
    
    #Load the Sign In Time
    for row in weekend_time:
        whichhour = int(datetime.strptime(row,'%Y-%m-%d %H:%M:%S').strftime("%H"))
        whichminute = int(datetime.strptime(row,'%Y-%m-%d %H:%M:%S').strftime("%M"))
        whichsecond = int(datetime.strptime(row,'%Y-%m-%d %H:%M:%S').strftime("%S"))
        decimal = float(whichhour + whichminute/60 + whichsecond/3600)
        weekend_hour.append(whichhour)
        weekend_minute.append(whichminute)
        decimal_time.append(decimal)
    
    weekend['Time'] = [i for i in decimal_time]
    
    weekend_Name = {}.fromkeys(weekend['Name']).keys()
    weekend_Date = {}.fromkeys(weekend['Sign In Date']).keys()
    count = 0
    
    #Count the Overtime Working Times
    for i in weekend_Name:
        for j in weekend_Date:
            work = weekend[(weekend['Name'] == i) & (weekend['Sign In Date'] == j)]
            work_time = work['Time']
            if len(work_time) > 0:
                if (min(work_time) < 9.5) & (max(work_time) > 12) & (max(work_time) < 16.5):
                    count += 1
                elif (min(work_time) < 13) & (min(work_time) > 9.5) & (max(work_time) > 16.5):
                    count += 1
                elif (min(work_time) < 9.5) & (max(work_time) > 16.5):
                    count += 2
                else:
                    count += 0
            a.append(i)
            b.append(j)
            c.append(count)
            count = 0
    
    loc = []
    
    #Count the Total Overtime Working Times
    Name = {}.fromkeys(a).keys()
    
    for i in Name:
        index = [j for j, x in enumerate(a) if x == i]
        loc.append(index)
    
    work_times = []
    for i in loc:
        times = 0
        for j in i:
            times += c[j]
        work_times.append(times)
    
    Name = list(Name)
    
    #Output the Result csv File
    output = DataFrame(Name, columns = ['Name'])
    output['Employee ID'] = ['0' + str(i) for i in weekday_ID]
    output['Overtime Working Times'] = [i for i in work_times]
    output['Subsidy'] = [25*i for i in work_times]
    
    date = list(df['Sign In Date'])
    begin = min(date)
    end = max(date)
    
    output.to_excel("Total Overtime Working Times (" + begin[0:4] + begin[5:7] + begin[8:] + ' - ' + end[0:4] + end[5:7] + end[8:] + ").xlsx", encoding = "utf_8_sig", index = False)

def whether_week_day(df):
    Decimal_Time = []
    Week_Day = []
    
    for i in df['Employee ID']:
        i = str(i)
    #Find the Day
    Time = df['Sign In Time']
    ID = list(df['Employee ID'])
    
    for row in Time:
        whatday = int(datetime.strptime(row,'%Y-%m-%d %H:%M:%S').strftime("%w"))
        whichhour = int(datetime.strptime(row,'%Y-%m-%d %H:%M:%S').strftime("%H"))
        whichminute = int(datetime.strptime(row,'%Y-%m-%d %H:%M:%S').strftime("%M"))
        whichsecond = int(datetime.strptime(row,'%Y-%m-%d %H:%M:%S').strftime("%S"))
        decimal = float(whichhour + whichminute/60 + whichsecond/3600)
        
        Decimal_Time.append(decimal)
    
    whether_Name = {}.fromkeys(df['Name']).keys()
    whether_Date = {}.fromkeys(df['Sign In Date']).keys()
    
    df['Hour'] = [i for i in Decimal_Time]
    
    a = [] #Name
    b = [] #Date
    c = [] #Overtime Working Times
    n = [] #ID
    count = 0
    index = 0
    
    for i in whether_Name:
        for j in whether_Date:
            work = df[(df['Name'] == i) & (df['Sign In Date'] == j)]
            work_time = work['Hour']
            day = int(datetime.strptime(j,'%Y-%m-%d').strftime("%w"))
            if (day > 0) & (day < 6):
                whatday = 'Weekday'
                if len(work_time) > 0:
                    if (max(work_time) >= 20):
                        count += 1
                    else:
                        count += 0
            else:
                whatday = 'Weekend'
                if len(work_time) > 0:
                    if (min(work_time) <= 9.5) & (max(work_time) >= 12) & (max(work_time) <= 16.5):
                        count += 1
                    elif (min(work_time) <= 13) & (min(work_time) >= 9.5) & (max(work_time) >= 16.5):
                        count += 1
                    elif (min(work_time) <= 9.5) & (max(work_time) >= 16.5):
                        count += 2
                    else:
                        count += 0
            
            Week_Day.append(whatday)
            a.append(i)
            b.append(j)
            c.append(count)
            n.append(ID[list(df['Name']).index(i)])
            count = 0
            index += 1
    
    output = DataFrame(a, columns = ['Name'])
    output['Employee ID'] = ['0' + str(i) for i in n]
    output['Sign In Date'] = [str(i) for i in b]
    output['Overtime Working Times'] = [i for i in c]
    output['Overtime Working Day'] = [i for i in Week_Day]
    output['Subsidy'] = [25*i for i in c]
    
    Times = output['Overtime Working Times']
    
    index = 0
    for row in Times:
        if row == 0:
            output = output.drop(index)
        index += 1
    
    date = list(df['Sign In Date'])
    begin = min(date)
    end = max(date)
    
    output.to_excel("Overtime Working Detail (" + begin[0:4] + begin[5:7] + begin[8:] + ' - ' + end[0:4] + end[5:7] + end[8:] + ").xlsx", encoding = "utf_8_sig", index = False)

df = delete(filename)
count_work_times(df)
whether_week_day(df)