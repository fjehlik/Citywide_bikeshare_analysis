# -*- coding: utf-8 -*-
"""
Created on Thu Jan 10 08:13:34 2019

@author: fjehlik

The following project analyzes bikeshare data from three city and returns simplified statistical information on the 
programs.  

CITATIONS:
   1. Udacity Bikeshare starter source code 'bikeshare_2.py' 
   2. Udacity 'Programming for Data Science', Python chapter 
   3. groupby documentation:  https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.groupby.html
   4. groupby example: https://stackoverflow.com/questions/50848454/pulling-most-frequent-combination-from-csv-columns
   5. random removal of rows using numpy random: https://stackoverflow.com/questions/28556942/pandas-remove-rows-at-random-without-shuffling-dataset
   6. examples of using iloc: https://www.shanelynn.ie/select-pandas-dataframe-rows-and-columns-using-iloc-loc-and-ix/#iloc-selection 
   
   
INPUT:
Asks user to specify a city, month, and day to analyze. Also, the program asks the user if they want to reduce the file size 
by eliminating rows of data. 
Users have the choice to select a city and time period to analyze.  
The three cities are Chicago, New York, and Washington DC
The data was collected from January through June.     
    
OUTPUT:
Statistical data on:
    -timings stats on most popular times of travel
    -timings stats (most popular start, end, and combined stop end stations)   
    -stats on total aggregate trip times and average trip times per customer (note: Washington stats excluded)
    -simplified age and gender stats on users of the programs

"""
import os 
import time
import numpy as np
import pandas as pd
np.random.seed(72)

os.chdir(r'C:\Users\fjehlik\Desktop\udacity\udacity-git-course\pdsnd_github')

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
   
    
    city_ = ['chicago', 'new york city', 'washington']
    month_ = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    day_ =['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday' ,'saturday' ,'sunday'] 
    # get user input for city (chicago, new york city, washington)  
   
    while True:
        city = input('Please enter the city you\'d like to analyze. Chicago, New York City, or Washington: ').lower()       
        if city in city_:            
            break
        else:
            print('\n"{}" is an incorrect input. Please enter only Chicago, New York City, or Washington:  '.format(city))
    
    # get user input for month (all, january, february, ... , june)
    while True:    
        month = input('Please enter the month you\'d like to analyze: (All, January, February, ... , June): ').lower()               
        if month in month_:
            break
        else:
            print('\n')
            print('"{}" is an incorrect month. Please enter only (All, January, February, ... , June):  '.format(month))
    
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:   
        day = input('Please enter the day(s) you\'d like to analyze (All, Monday-Sunday): ').lower()       
        if day in day_:            
            break       
        else:
            print('\n')
            print('"{}" is an incorrect day. Please enter only Monday through Sunday or "All":  '.format(day))
        
    return city, month, day
    print('-'*40)
   
    
def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # Change the directory to where the city files are stored. 
    os.chdir(r'C:\Users\fjehlik\Desktop\udacity\udacity-git-course\pdsnd_github')
    
    # removes the spaces from the New York City csv
    if city == 'new york city':
        city = 'new_york_city'
    
    filename = city + '.csv'

    # load data file into a dataframe    
    df = pd.read_csv(filename, sep=',', header=0)
        

    # Asks the user if they wish to view lines of the data set   
    y = 5
    while True:
        view_y_n = input('Would you like to view the first {} lines of the dataset (yes/no)? '.format(y)).lower()
        if view_y_n == 'yes' or view_y_n == 'y':        
            print(df.iloc[1:y+1])
            y +=5
        else:
            break
       
    
    # Reduces the DataFrame if the user chooses. this randomly removes rows to the length the chooser wishes to analyze
    while True:
        df_y_n = input('Would you like to reduce data length by randomly removing rows (yes/no)? ').lower()
        
        if df_y_n == 'yes' or df_y_n == 'y':
            df_length = int(input('How long do you want the dataset to be? Min = 1, Max = {}: '.format(len(df))))
            while df_length < 1 or df_length > len(df):
                  df_length = int(input('Please enter a number between 1 and {}: '.format(len(df))))                         
            #else:
            #df = df[:df_length]            
            remove_n = len(df) - df_length
            drop_indices = np.random.choice(df.index, remove_n, replace=False)
            df = df.drop(drop_indices)
            break           
        elif df_y_n == 'no' or df_y_n == 'n':
            break
        else:
            print('Please only enter "yes", or "no".')
    
    # reduce the dataframe relative to the month and day selected 
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    
    if month != 'all':
        # use the index of the months list to get the corresponding int
        
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1 

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # convert the Start Time column to datetime 
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # Establish hours, days, and months df columns
    df['hour'] = df['Start Time'].dt.hour
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['month'] = df['Start Time'].dt.month
     
    # display the most common month
    month_num = [ ['January'], ['February'], ['March'], ['April'], ['May'], ['June'] ]
    popular_month = df.month.mode()[0]       
    print('Most Frequent Month is:', month_num[popular_month-1])
    
    # display the most common day of week    
    popular_day = df.day_of_week.mode()[0]       
    print('Most Frequent day is:', popular_day)
    
    # display the most common start hour
    popular_hour = df.hour.mode()[0]       
    if popular_hour >=12:
        print('Most Frequent Start Hour:', str(popular_hour - 12) + "PM")
    else:
        print('Most Frequent Start Hour:', str(popular_hour) + "AM")
    
    
    # calculates the time required for calculations
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start = df['Start Station'].mode()[0]       
    print('Most popular start station is:', popular_start)
    
#    # Double theck the mode apporach using groupby 
#    popular_start = df.groupby(['Start Station']).size().nlargest(1)
#    print('Most popular start and end station is:', popular_start)
        
    # display most commonly used end station
    popular_end = df['End Station'].mode()[0]       
    print('Most popular end station is:', popular_end)
    
    # display most frequent combination of start station and end station trip
    popular_start_end = df.groupby(['Start Station','End Station']).size().nlargest(1)
    print('Most popular start and end station is:', popular_start_end)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time in hours
    travel_time_tot = sum(df['Trip Duration'] / 3600)
    print('Total travel time for all users in this period is {} hours'.format(round(travel_time_tot),0))
    
    # display mean travel time    
    travel_time_mean = (df['Trip Duration'].mean(skipna = True) / 3600)
    print('The mean travel time is {} hours'.format(round(travel_time_mean, 4)))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users.""" 
    
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    subscriber = df['User Type'].str.count('Subscriber').sum() 
    customer = df['User Type'].str.count('Customer').sum() 
    print('There are {} Subscribers and {} Customers.'.format(subscriber, customer))
        
    try:
        # Display counts of gender
        female = df['Gender'].str.count('Female').sum()
        male = df['Gender'].str.count('Male').sum()  
        unknown = (df['Gender'].isnull().sum())
        #df = df.dropna()
        print('There are {} females, {} males, and {} unknown Customers.'.format(int(female), int(male), int(unknown)))
        
        # Display earliest, most recent, and most common year of birth
        oldest = min(df['Birth Year'])
        youngest = max(df['Birth Year'])
        avg_age = df['Birth Year'].mean(skipna = True)
        
        print('Oldest DOB is {}. The youngest DOB is {}. Avg DOB is {}.' \
              .format(int(oldest), int(youngest), round(avg_age),2))
        
    except:
        print('No gender or DOB data is available.')    
    
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def plots(city, month, day, df):
    """Creates analysis plots of the data"""
 
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            return city, month, day, df
            break


# The following line of code runs the functions and returns the variables for checking program 
city, month, day, df = main()

