import holidays
from datetime import timedelta
from datetime import datetime
import pandas as pd
import sqlalchemy

"""  
This code creates a calendar with the holidays of different Countries
It is usefull to know which days to predict special forecast. I.e. Black 
Friday or other events that are not always the same day of the year.

It outputs a dataframe named "holidays_table_df" which contains contains
everyday of the year from StartingYear to LastYear. The other columns
are binaries of whether this day is a holiday in each of the countries

The code automatically sends the table to SQL under the name:
    marc_calendar_is_holiday

"""



engine = sqlalchemy.create_engine \
("mssql+pyodbc://marc.fuster:access.to.sql19@database.kernel-analytics.local/byl_supply_chain?driver=ODBC+Driver+13+for+SQL+Server")


# When to start the calendar and when to finish
Starting_Year=2010
Last_Year=2025

# Some events make a wider impact than just in a day
# we will consider that the effect of black friday is 3 days more, until cybermonday
# we will consider that the mothers day affects 5 days before. Because it is during the
# week that people buy the presents for the mother's day
number_of_days_after_black_friday=3
number_of_days_before_dia_de_la_madre=5


#Create list of dates with a 1 day step
datelist = pd.date_range(datetime(Starting_Year,1,1), datetime(Last_Year,1,1)).strftime('%Y-%m-%d')

#create df from where we will write
holidays_table_df = pd.DataFrame({'ds':datelist})

#load calendars
holidays_Spain_library = holidays.Spain()
holidays_Portugal_library = holidays.Portugal()
holidays_Mexico_library = holidays.Mexico()
holidays_France_library = holidays.France()


""" Add Black Friday and Dia de la Madre """
# compute the days to add


# ----- Black Friday----- 
# We predict the 4th Thursday of November which is THanksGiving
# And then we add 1 day.
# IMPORTANT! Predicting the 4th Friday Would be Different!
# 4th friday is between the 22 and 28 inclusive
# Day after 4th Thursday is between the 23 and 29 inclusive

# We consider the Weekend and cyberMonday also as
# importan (upper_window = 3)

black_friday_list=[]

datelist = pd.date_range(datetime(Starting_Year,1,1), datetime(Last_Year,1,1))

for d in datelist:
    if d.weekday() == 3 and 22 <= d.day <= 28 and d.month == 11:
        d = d + timedelta(days=1)
        black_friday_list.append(d.strftime("%Y-%m-%d"))
        
        # let's count all the effect on the weekend
        for i in range(number_of_days_after_black_friday):
            d = d + timedelta(days=1)
            black_friday_list.append(d.strftime("%Y-%m-%d"))
            

# ---- Dia de la Madre ----
# We predict the 1st Sunday of May which is El dia de la madre
# THIS DAY IS IN SPAIN, PORTUGAL!

dia_de_la_madre_list=[]
datelist = pd.date_range(datetime(Starting_Year,1,1), datetime(Last_Year,1,1)).tolist()
for d in datelist:
    if d.weekday() == 6 and 1 <= d.day <= 7 and d.month == 5:
        dia_de_la_madre_list.append(d.strftime("%Y-%m-%d"))
        
        # let's count all the effect on previous week
        for i in range(number_of_days_before_dia_de_la_madre):
            d = d - timedelta(days=1)
            dia_de_la_madre_list.append(d.strftime("%Y-%m-%d"))
        
        
# Add to Calendars
for calendars in ([holidays_Spain_library, holidays_Portugal_library
                   , holidays_France_library, holidays_Mexico_library]):
    for i in range(len(black_friday_list)):
        calendars.append({black_friday_list[i]: 'Black Friday'})
    
# Dia de la madre only in Spain and Portugal    
for calendars in ([holidays_Spain_library, holidays_Portugal_library]):   
    for j in range(len(dia_de_la_madre_list)):
        calendars.append({dia_de_la_madre_list[j]: 'Dia de la Madre'})



"""Spain"""
holidays_table_df['Spain'] = holidays_table_df['ds'].apply(
         lambda x: 1 if (x in holidays_Spain_library) else 0)


"""Portugal"""
holidays_table_df['Portugal'] = holidays_table_df['ds'].apply(
         lambda x: 1 if (x in holidays_Portugal_library) else 0)


"""Mexico"""
holidays_table_df['Mexico'] = holidays_table_df['ds'].apply(
         lambda x: 1 if (x in holidays_Mexico_library) else 0)


"""France"""
holidays_table_df['France'] = holidays_table_df['ds'].apply(
         lambda x: 1 if (x in holidays_France_library) else 0)


"""Description"""


holidays_table_df['Description_Spain'] = holidays_table_df['ds'].apply(
         lambda x: holidays_Spain_library.get(x))
holidays_table_df['Description_Portugal'] = holidays_table_df['ds'].apply(
         lambda x: holidays_Portugal_library.get(x))
holidays_table_df['Description_Mexico'] = holidays_table_df['ds'].apply(
         lambda x: holidays_Mexico_library.get(x))
holidays_table_df['Description_France'] = holidays_table_df['ds'].apply(
         lambda x: holidays_France_library.get(x))



""" Save table to sql """

engine = sqlalchemy.create_engine \
("mssql+pyodbc://marc.fuster:access.to.sql19@database.kernel-analytics.local/byl_supply_chain?driver=ODBC+Driver+13+for+SQL+Server")

from pandas.io import sql
sql.execute('DROP TABLE IF EXISTS %s'%'marc_calendar_is_holiday', engine)


holidays_table_df.to_sql('marc_calendar_is_holiday', con=engine)


