from pandas import *
from ggplot import *
import pandasql
import numpy
import random


def histogram(turnstile_weather):
    gg = ggplot(aes(x='ENTRIESn_hourly', color='rain'), data=df) \
         + geom_histogram(alpha=0.3)
    print gg

def grouped_by_hour(turnstile_weather):
    grouped = turnstile_weather.groupby(['Hour', 'rain'])
    stats = grouped['ENTRIESn_hourly'].agg([numpy.sum, numpy.mean, numpy.std])
    # print stats
    stats = stats.reset_index()

    # Optionally, use geom_area(alpha=0.5) instaed of geom_point + geom_line
    gg = ggplot(aes(x='Hour', y='sum', color='rain'), data=stats) \
        + geom_point() \
        + geom_line() \
        + ggtitle('Subway total Entries per hour') \
        + xlab('Hour') \
        + ylab('Total entries')
    return gg

def grouped_by_unit(turnstile_weather):
    # pick X% of random units
    units = turnstile_weather['UNIT'].unique()
    plot_units = random.sample(units, 25)

    turnstile_weather = turnstile_weather[turnstile_weather['UNIT'].isin(plot_units)]
    # print turnstile_weather

    grouped = turnstile_weather.groupby(['UNIT', 'rain'])
    stats = grouped['ENTRIESn_hourly'].agg([numpy.sum, numpy.mean, numpy.std])
    stats = stats.reset_index()
    # print stats

    # Sorting by sum of entries looks like good approximation of most used units.
    # NOTE: we're not using sum of rain && no-rain as for most units, no-rain entry numbers are higher.
    # Thus, the non-rain value will work as the 'index'; ggplot will bring together the 2nd value (rain).
    stats.sort(['sum'], ascending=False, inplace=True)
    stats = stats.reset_index()
    # print stats

    gg = ggplot(aes(x='UNIT', y='sum', fill='rain'), data=stats) \
         + geom_bar(stat='identity', position='dodge') \
         + ggtitle('Subway total Entries per unit') \
         + xlab('Unit') \
         + ylab('Total Entries') \
         + theme(axis_text_x  = element_text(angle = 90, hjust = 0.4))
    return gg


def plot_weather_data(turnstile_weather):
    '''
    You are passed in a dataframe called turnstile_weather. 
    Use turnstile_weather along with ggplot to make a data visualization
    focused on the MTA and weather data we used in assignment #3.
    You should feel free to implement something that we discussed in class 
    (e.g., scatterplots, line plots, or histograms) or attempt to implement
    something more advanced if you'd like.  

    Here are some suggestions for things to investigate and illustrate:
     * Ridership by time of day or day of week
     * How ridership varies based on Subway station (UNIT)
     * Which stations have more exits or entries at different times of day
       (You can use UNIT as a proxy for subway station.)

    If you'd like to learn more about ggplot and its capabilities, take
    a look at the documentation at:
    https://pypi.python.org/pypi/ggplot/
     
    You can check out:
    https://www.dropbox.com/s/meyki2wl9xfa7yk/turnstile_data_master_with_weather.csv
     
    To see all the columns and data points included in the turnstile_weather 
    dataframe. 
     
    However, due to the limitation of our Amazon EC2 server, we are giving you a random
    subset, about 1/3 of the actual data in the turnstile_weather dataframe.
    '''

    #return grouped_by_unit(turnstile_weather)
    return grouped_by_unit(turnstile_weather)


df = pandas.read_csv('turnstile_data_master_with_weather.csv')
plot = plot_weather_data(df)
print(plot)