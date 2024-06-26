import calendar
from datetime import date
from enum import Enum
import logging

class HonbashoCalendar():
    """
    This module allows users to retrieve data related to the Ozumo Honbasho (Grand Sumo Tournament) schedules.

    1. 6 (six) tournaments are held every year, in odd-number months.
    2. A tournament starts on the 2nd Sunday of a month and lasts for 15 (fifteen) consecutive days.
    Therefore the last day of a tournament will be on the 4th Sunday of the month.
    """

    class Basho(Enum):
        """
        The tournaments in a year.

        The numeral value indicates the month the corresponding tournament is held in,
        eg. Hatsu Basho is in January.
        """
        HATSU = 1
        HARU = 3
        NATSU = 5
        NAGOYA = 7
        AKI = 9
        KYUSHU = 11

        def get_name(self):
            """
            Returns the tournament name as the enumeration name as-is.
            """
            return self.name
        
        def get_month(self):
            """
            Returns the month this tournament is in.
            """
            return self.value
        
        def get_month_name(self):
            """
            Returns the name of the month this tournament is in.
            """
            return calendar.month_name[self.value]


    def calculate_schedule(year: int) -> list:
        """
        Determines the tournament schedule for a given year.

        :param year: The specified year.
        """

        schedule = []
        for basho in HonbashoCalendar.Basho:
            schedule.append({
                "basho" : basho,
                "dates" : HonbashoCalendar.get_dates(year, basho)
            })
        logging.debug(f"Schedule for year {year}:\n{schedule}")
        return schedule
    
    def get_dates(year: int, basho: Basho) -> list:
        """
        Gets the tournament dates (in chronical order) of a specific tournament in a given year.

        :param year: The specified year.
        :param basho: The specified tournament.
        """

        month = basho.value

        cal = calendar.monthcalendar(year, month)
        dates = [ date(year, month, cal[1][calendar.SUNDAY]) ] # Day 1 = 2nd Sunday of the month
        for w in range(2, 4):
            for day in cal[w]:
                dates.append(date(year, month, day))
        return dates