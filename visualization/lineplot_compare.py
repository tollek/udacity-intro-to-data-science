
import pandas

from ggplot import *


def lineplot_compare(hr_by_team_year_sf_la_csv):
    # Write a function, lineplot_compare, that will read a csv file
    # called hr_by_team_year_sf_la.csv and plot it using pandas and ggplot.
    #
    # This csv file has three columns: yearID, HR, and teamID. The data in the
    # file gives the total number of home runs hit each year by the SF Giants 
    # (teamID == 'SFN') and the LA Dodgers (teamID == "LAN"). Produce a 
    # visualization comparing the total home runs by year of the two teams. 
    # 
    # You can see the data in hr_by_team_year_sf_la_csv
    # at the link below:
    # https://www.dropbox.com/s/wn43cngo2wdle2b/hr_by_team_year_sf_la.csv
    #
    # Note that to differentiate between multiple categories on the 
    # same plot in ggplot, we can pass color in with the other arguments
    # to aes, rather than in our geometry functions. For example, 
    # ggplot(data, aes(xvar, yvar, color=category_var)). This should help you 
    # in this exercise.

    df = pandas.read_csv(hr_by_team_year_sf_la_csv)
    gg = ggplot(aes(x='yearID', y='HR', color='teamID'), data=df) \
        + geom_point() \
        + geom_line() \
        + ggtitle('Total HRs by Year by Team') \
        + xlab('year') \
        + ylab('HRs (homeruns)')
    return gg


gg = lineplot_compare('hr_by_team_year_sf_la.csv')
print(gg)
