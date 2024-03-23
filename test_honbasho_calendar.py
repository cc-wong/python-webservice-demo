import unittest
from honbasho_calendar import HonbashoCalendar
from datetime import date

## Test case(s) for the HonbashoCalendar module.
class TestHonbashoCalendar(unittest.TestCase):

    ## Test case on calculate_schedule(year).
    def test_calculate_schedule(self):
        year = 2024
        expected = [
            {
                "basho" : HonbashoCalendar.Basho.HATSU,
                "dates" : [ date(year, 1, d) for d in range(14, 29) ]             
            },
            {
                "basho" : HonbashoCalendar.Basho.HARU,
                "dates" : [ date(year, 3, d) for d in range(10, 25) ]             
            },
            {
                "basho" : HonbashoCalendar.Basho.NATSU,
                "dates" : [ date(year, 5, d) for d in range(12, 27) ]             
            },
            {
                "basho" : HonbashoCalendar.Basho.NAGOYA,
                "dates" : [ date(year, 7, d) for d in range(14, 29) ]             
            },
            {
                "basho" : HonbashoCalendar.Basho.AKI,
                "dates" : [ date(year, 9, d) for d in range(8, 23) ]             
            },
            {
                "basho" : HonbashoCalendar.Basho.KYUSHU,
                "dates" : [ date(year, 11, d) for d in range(10, 25) ]             
            }
        ]
        result = HonbashoCalendar.calculate_schedule(year)
        assert expected == result