import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv','new york city': 'new_york_city.csv','washington': 'washington.csv' }
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
    (str) city - name of the city to analyze
    (str) month - name of the month to filter by, or "all" to apply no month filter
    (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    city = input('For which city would you like to explore bikeshare data?''\n')
    while city.title() not in ['Chicago','New York City', 'Washington']:
        print('Please select a city among Chicago, New York City, Washington')
        city = input('For which city would you like to explore bikeshare data?''\n')
        if city.title() in ['Chicago','New York City', 'Washington']:
            break

    month = input('Please enter the month for which you want to explore the data, if you wish not to filter data by month, enter all:''\n')
    while month.title() not in ['January','February','March','April','May','June','All']:
        print ('Please enter a month among January, February, March, April, May, June or enter all if you wish to see data for all of these months')
        month = input('Please enter the month for which you want to explore the data, if you wish not to filter data by month, enter all:''\n')
        if month.title() in ['January','February','March','April','May','June','All']:
            break


    day = input('Please enter the day for which you would like to explore the data,if you don\'t wish to filter by day, enter all:''\n')
    while day.title() not in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday','Sunday','All']:
        print ('Please enter a day among Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday')
        day = input('Please enter the day for which you would like to explore the data,if you don\'t wish to filter by day, enter all:''\n')
        if day.title() in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday','Sunday']:
            break
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """Loads data for the specified city and filters by month and day if applicable.
    Args:(str) city - name of the city to analyze
    (str) month - name of the month to filter by, or "all" to apply no month filter
    (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:df - Pandas DataFrame containing city data filtered by month and day"""
    df = pd.read_csv(CITY_DATA[city.lower()])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    if month.title() != 'All':
        months = ['January','February','March','April','May','June']
        month = months.index(month.title()) + 1
        df = df[df['Month'] == month]
    if day.title() != 'All':
        df = df[df['day_of_week'] == day.title()]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()


    most_common_month = df['Month'].value_counts().idxmax()
    print ('The most common month of travel is {}'.format(most_common_month))

    most_common_day_of_week = df['day_of_week'].value_counts().idxmax()
    print ('The most common day of the week is {}'.format(most_common_day_of_week))

    df['Hour'] = df['Start Time'].dt.hour
    most_popular_start_hour = df['Hour'].value_counts().idxmax()
    print('The most popular start hour for a day is {}'.format(most_popular_start_hour))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    most_commonly_used_start_station = df['Start Station'].mode()[0]
    print ('Most commonly used Start Station is {}'.format(most_commonly_used_start_station))

    most_commonly_used_end_station = df['End Station'].mode()[0]
    print ('Most commonly used End Station is {}'.format(most_commonly_used_end_station))

    combo_stations = df['Start Station'].str.cat(others = df['End Station'], sep = ' to ')

    most_popular_combos_of_start_and_end_station = combo_stations.mode()[0]
    print ('The most frequent combination of start station and end station trip is {}'.format(most_popular_combos_of_start_and_end_station))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_duration_for_all_trips = df['Trip Duration'].sum()
    print ('Total travel time for all trips is {} seconds'.format(total_duration_for_all_trips))

    mean_travel_time = df['Trip Duration'].mean()
    print('Average travel time is {} seconds'.format(mean_travel_time))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    try:
        user_category = df['User Type'].value_counts()
        print('The number of subscribers is {}'.format(user_category[0]), '\n' ,'The number of customers is {}'.format(user_category[1]), '\n', 'The number of dependent is {}'.format(user_category[2]))
    except:
        user_category = df['User Type'].value_counts()
        print('The number of subscribers is {}'.format(user_category[0]),'\n','The number of customers is {}'.format(user_category[1]))

    try:
        gender = df['Gender'].value_counts()
        print ('The total number of Males is {}'.format(gender[0]),'\n','The total number of females is {}'.format(gender[1]))
    except:
        print('Sorry, Gender data is not available for Washington')

    try:
        earliest_birth_year = df['Birth Year'].min()
        print('The oldest user was born in {}'.format(earliest_birth_year))
        most_recent_birth_year = df['Birth Year'].max()
        print('The youngest user was born in {}'.format(most_recent_birth_year))
        most_common_year = df['Birth Year'].mode()[0]
        print('Most users were born in {}'.format(most_common_year))
    except:
        print('Sorry, Birth year data is not available for Washington')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
