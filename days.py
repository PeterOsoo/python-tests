"""
This function checks if a given year is a leap year.

Args:
    year: An integer representing the year to be checked.

Returns:
    True if the year is a leap year, False otherwise.
"""


def is_leap_year(year):
    if year % 4 == 0:
        if year % 100 == 0:
            return year % 400 == 0
        else:
            return True
    else:
        return False


def days_in_month(year, month):
    """
    This function determines the number of days in a given month.

    Args:
        year: An integer representing the year.
        month: An integer representing the month (1-12).

    Returns:
        An integer representing the number of days in the month.
    """

    if month in (1, 3, 5, 7, 8, 10, 12):
        return 31
    elif month == 2:
        if is_leap_year(year):
            return 29
        else:
            return 28
    else:
        return 30


# Example usage
year = 2020
month = 2

months = ["January", "February", "March", "April", "May", "June",
          "July", "August", "September", "October", "November", "December"]

if is_leap_year(year):
    print(f"{year} is a leap year.")
else:
    print(f"{year} is not a leap year.")

print(f"{months[month-1]} has {days_in_month(year, month)} days.")

print("Code is working")
