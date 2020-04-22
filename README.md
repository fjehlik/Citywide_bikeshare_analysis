### Date created
Created on Thu Jan 10 08:13:34 2019

### Project Title
Bikeshare analysis project

### Description
The following project analyzes bikeshare data from three city and returns simplified statistical information on the
programs. 

INPUT:
Asks user to specify a city, month, and day to analyze. Also, the program asks the user if they want to reduce the file size by eliminating rows of data.

Users have the choice to select a city and time period to analyze.  The three cities are Chicago, New York, and Washington DC. The data was collected from January through June (actual data provided).     

In this program the user is asked if they wish to reduce the size of the file they are analyzing.
Rather than by simply removing data from the beginning or end of the dataframe, this code randomly removes lines of data. This was done as to not possibly bias the time based analysis as times of month, week, etc can have an impact on the results. By randomly removing lines the reduced data set would be expected to be a better representation of the time period while simultaneously reducing the total data output.

OUTPUT:
Statistical data on:
    -timings stats on most popular times of travel
    -timings stats (most popular start, end, and combined stop end stations)   
    -stats on total aggregate trip times and average trip times per customer (note: Washington stats excluded)
    -simplified age and gender stats on users of the programs

### Files used
chicago.csv
washington.csv
new_york_city.csv

### Credits
1. Udacity Bikeshare starter source code 'bikeshare_2.py'
2. Udacity 'Programming for Data Science', Python chapter
3. groupby documentation:  https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.groupby.html
4. groupby example: https://stackoverflow.com/questions/50848454/pulling-most-frequent-combination-from-csv-columns
5. random removal of rows using numpy random: https://stackoverflow.com/questions/28556942/pandas-remove-rows-at-random-without-shuffling-dataset
