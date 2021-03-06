import numpy as np
import pandas
import matplotlib
import matplotlib.pyplot as plt
matplotlib.style.use('ggplot')
import pylab

def entries_histogram(turnstile_weather):
    '''
    Before we perform any analysis, it might be useful to take a
    look at the data we're hoping to analyze. More specifically, let's 
    examine the hourly entries in our NYC subway data and determine what
    distribution the data follows. This data is stored in a dataframe
    called turnstile_weather under the ['ENTRIESn_hourly'] column.
    
    Let's plot two histograms on the same axes to show hourly
    entries when raining vs. when not raining. Here's an example on how
    to plot histograms with pandas and matplotlib:
    turnstile_weather['column_to_graph'].hist()
    
    Your histograph may look similar to bar graph in the instructor notes below.
    
    You can read a bit about using matplotlib and pandas to plot histograms here:
    http://pandas.pydata.org/pandas-docs/stable/visualization.html#histograms
    
    You can see the information contained within the turnstile weather data here:
    https://www.dropbox.com/s/meyki2wl9xfa7yk/turnstile_data_master_with_weather.csv
    '''

    tw = turnstile_weather

    sunny_hist = tw[(tw['rain'] == 0.0) & (tw['ENTRIESn_hourly'] <= 6000)]
    plt.hist(sunny_hist['ENTRIESn_hourly'].tolist(), 20, alpha=0.5, label='sunny')
    rain_hist = tw[(tw['rain'] == 1.0) & (tw['ENTRIESn_hourly'] <= 6000)]
    plt.hist(rain_hist['ENTRIESn_hourly'].tolist(), 20, alpha=0.5, label='rainy')
    plt.legend(loc='upper right')
    plt.show()

    # alternatively, 2 figures
    #sunny_hist = tw[(tw['rain'] == 0.0) & (tw['ENTRIESn_hourly'] <= 6000)]
    #sunny_hist.hist(column='ENTRIESn_hourly', stacked=True, bins=20)
    #rain_hist = tw[(tw['rain'] == 1.0) & (tw['ENTRIESn_hourly'] <= 6000)]
    #rain_hist.hist(column='ENTRIESn_hourly', stacked=True, bins=20)

    return plt


turnstile_weather = pandas.read_csv('turnstile_data_master_with_weather.csv')
x = entries_histogram(turnstile_weather)
pylab.show()