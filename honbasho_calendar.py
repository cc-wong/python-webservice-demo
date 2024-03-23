import calendar
from datetime import date
from enum import Enum
import logging

## This module allows users to retrieve data related to 
## the Ozumo Honbasho (Grand Sumo Tournament) schedules.
##
## 1. 6 (six) tournaments are held every year, in odd-number months.
## 2. A tournament starts on the 2nd Sunday of a month and
##    lasts for 15 (fifteen) consecutive days.
##    Therefore the last day of a tournament will be on the 4th Sunday of the month.
class HonbashoCalendar():

    ## The tournaments in a year.
    ## The numeral value indicates the month the corresponding tournament is held in.
    class Basho(Enum):
        HATSU = 1
        HARU = 3
        NATSU = 5
        NAGOYA = 7
        AKI = 9
        KYUSHU = 11

        # Returns the basho name in proper case.
        def get_name(self):
            return self.name.title()
        
        # Returns the month number of this basho.
        def get_month(self):
            return self.value
        
        # Returns the month name of this basho.
        def get_month_name(self):
            return calendar.month_name[self.value]


    ## Gets the tournament schedule for a given year.
    def calculate_schedule(year: int) -> list:
        schedule =  []
        for basho in HonbashoCalendar.Basho:
            logging.debug(f"Month: {basho.get_month_name()}")
            schedule.append({
                "basho" : basho,
                "dates" : HonbashoCalendar.get_dates(year, basho)
            })
        return schedule
    
    ## Gets the tournament dates (in chronical order) of a given Honbasho year and month.
    def get_dates(year: int, basho) -> list:
        month = basho.value

        cal = calendar.monthcalendar(year, month)
        dates = [ date(year, month, cal[1][calendar.SUNDAY]) ] # Day 1 = 2nd Sunday of the month
        for w in range(2, 4):
            for day in cal[w]:
                dates.append(date(year, month, day))
        return dates