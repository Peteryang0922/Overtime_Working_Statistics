Overtime Working Statistics
1. Introduction
    
    This algorithm is to count the overtime working times of the employees in Research and Development Department of Wuhan Hongxin Technical Services Co., Ltd, according to the check in information of every employee.
    
    The input is a csv (comma delighted) file, which contains Employee ID, Name, Check in time, and Check in location information of the employees.
    
    The first output file is the total overtime working times of every employee, and how much money the company should compensate to the employee.
    
    The second output file shows the detail information of every overtime working incident, the name, the date, and the overtime working times.
    
2. Explanation
    
    The overtime working has 2 situtations, which are weekdays and weekends.
    
    Weekdays:
    
    If the last check-in information of an employee is after 8:00 PM, the employee is considered as having an overtime working.
    
    Weekends:
    
    1) If the check-in information shows that an employee has fully worked from 9:30 AM to 12:00 AM, but end his/her work before 4:30 PM, this employee is considered as having 1 overtime working.
    2) If the check-in information shows that an employee has fully worked from 1:00 PM to 4:30 PM, but start his/her work before 9:00 AM, this employee is considered as having 1 overtime working.
    3) If the check-in information shows that an employee has fully worked from 9:30 AM to 4:30 PM, this employee is considered as having 2 overtime working.
    
    In addition, there are also invalid check-in information. For those Check in location are "WIFI Check In" or "Hongxin Wireless Communication Industrial Park", the information is considered as invalid.

 3. Additional Package:
 
     pandas, tkinter
