import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' } #dictonary for identifying the name of the CSV-file

months_list = ["january", "february", "march", "april", "may", "june", "all"] #list for checking the month input for validity

days_list = ["monday", "tuesday", "wednesday", "friday", "saturday", "sunday", "all"] #list for checking the day input for validity


def user_input(message):
    """
    Makes sure that no exception occures when a KeyboardInterrupt is provoced.
    """

    try:
        entered = input(message)
    except KeyboardInterrupt:
        print(" Program cancelled.")
        exit()
    return(entered)


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('Hello! Let\'s explore some US bikeshare data!')
    #get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    invalid = True
    while invalid:
        city = user_input("Please enter a city (Chicago, New York City, Washington) that you would like to get evaluations from: ").lower()
        if city in ("chicago", "new york city", "washington"):
            print("Thank you for the input.\n")
            invalid = False
        else:
            print("No valid city was entered. Please try again.")
            invalid = True

    #get user input for month (all, january, february, ... , june)
    invalid = True
    while invalid:
        month = user_input("Please enter a month (full word) that you would like to get evaluations from (from January to June).\nAlternatively type \"all\": ").lower()
        if month in months_list:
            invalid = False
            print("Thank you for the input.\n")
        else:
            print("No valid month was entered. Please try again.")
            invalid = True

    #get user input for day of week (all, monday, tuesday, ... sunday)
    invalid = True
    while invalid:
        day = user_input("Please enter a week day (full word) that you would like to get evaluations from.\nAlternatively type \"all\": ").lower()
        if day in days_list:
            print("Thank you for the input.\n")
            invalid = False
        else:
            print("No valid day was entered. Please try again.")
            invalid = True 

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
        df_original - Pandas DataFrame containing original bike sharing data for illustration at the program's end if the user wishes
    """

    filename = CITY_DATA[city]
    df = pd.read_csv(filename)
    df_original = df.copy() #storing the original DataFrame for illustration

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['Start Time'])

    df["Month"] = df["Start Time"].dt.month_name()
    df["Day"] = df["Start Time"].dt.day_name()

    if month != "all": #filter the month according the user input
        df = df[df["Month"] == month.title()]

    if day != "all": #filter the month according the user input
        df = df[df["Day"] == day.title()]

    #print(df.info())
    #print(df.head())
    return df, df_original


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    #if month is selected by user most common month will not be determined
    if month == "all":
        common_month = df["Month"].mode()[0]
        print("The most common month of bike rental is: {}".format(common_month))
    else:
        print("You chose the month {}. Therefore, no month evaluation takes place.".format(month.title()))

    # display the most common day of week
    #if day is selected by user most common day will not be determined
    if day == "all":
        common_day = df["Day"].mode()[0]
        print("The most common day of bike rental is: {}".format(common_day))
    else:
        print("You chose the day {}. Therefore, no day evaluation takes place.".format(day.title()))

    #display the most common start hour
    df["Hour"] = df["Start Time"].dt.hour
    common_hour = df["Hour"].mode()[0]
    print("The most common hour of bike rental is: between {} o'clock and {} o'clock".format(common_hour, common_hour + 1))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    #display most commonly used start station
    common_start_station = df["Start Station"].mode()[0]
    print("The most common start station of bike rental is: {}".format(common_start_station))

    #display most commonly used end station
    common_end_station = df["End Station"].mode()[0]
    print("The most common end station of bike rental is: {}".format(common_end_station))

    #display most frequent combination of start station and end station trip
    df["Common route"] = df["Start Station"] + " to " + df["End Station"]
    common_route = df["Common route"].mode()[0]
    print("The most common route of bike rental is: from {}".format(common_route))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    #display total travel time
    total_time = df["Trip Duration"].sum()/3600 #conversion of seconds in hours
    print("The total travel time is: {:.2f} hours or {:.0f} days and {:.2f} hours".format(total_time, total_time//24, total_time%24))

    #display mean travel time
    mean_time = df["Trip Duration"].mean()/60 #conversion of seconds in minutes
    print("The mean travel time is: {:.2f} minutes".format(mean_time))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    #Display counts of user types
    user_types = df["User Type"].value_counts()
    print("Count of user types:\n{}\n".format(user_types))

    #Display counts of gender
    if city == "washington": #washington.csv does not contain person-related information
        gender = "The Washington file does not cantain any gender information."
    else:
        gender = df["Gender"].value_counts()
    print("Count of genders:\n{}\n".format(gender))


    #Display earliest, most recent, and most common year of birth
    if city == "washington": #washington.csv does not contain person-related information
        yob = "The Washington file does not cantain any year of birth information."
    else:
        yob = df["Birth Year"].describe()[[1,3,4,5,6,7]]
    print("Year of birth information:\n{}\n".format(yob))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def show_table_original(df_original, city):
    """ Gives the user the chance to check the original DataFrame """

    show_df = user_input("\nDo you want to see the first 5 rows of the ORGINAL DataFrame for {}?\nEnter \"yes\" or \"no\": ".format(city.title()))
    i = 0
    while show_df == "yes":
        print(df_original[i:i + 5])
        show_df = user_input("\nDo you want to see 5 more rows?\n")
        i += 5

def show_table(df, city):
    """ Gives the user the chance to check the modified DataFrame """

    show_df = user_input("\nDo you want to see the first 5 rows of the MODIFIED (filtered, additional functional columns) DataFrame for {}?\nEnter \"yes\" or \"no\": ".format(city.title()))
    i = 0
    while show_df == "yes":
        print(df[i:i + 5])
        show_df = user_input("\nDo you want to see 5 more rows?\n")
        i += 5

def main():
    while True:
        city, month, day = get_filters() #can be disabled if no data shall be entered for testing purposes
        #city, month, day = "chicago", "february", "all" #can be enabled if no data shall be entered for testing purposes
        df, df_original = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        show_table_original(df_original, city)
        show_table(df, city)

        restart = user_input('\nWould you like to restart? Enter \"yes\" or \"no\":\n')
        if restart.lower() != 'yes':
            break
        else:
            print("\nRestart:")


if __name__ == "__main__":
	main()
