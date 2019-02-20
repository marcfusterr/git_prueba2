import numpy as np
import matplotlib.pylab as plt
import pandas as pd
from datetime import datetime

import calmap
import matplotlib.dates

""" Module for visualization: For now only contains two scripts.

    One of Calendar Maps and the other for errror plotting.

    Further functions will be added. For any doubts contact with Marc.
"""


def scatter_error_plot(y_true, y_predict, datelist,
                       xlab='Dates', ylab='Units sold', title='Error analysis',
                       ticks_separation='weeks'):
    """Create scatter error plot to compare the Prediction.
    There is an example of how to use it in the main function below

    Args:
        y_true {[List of values]} -- Array of Real values
        y_predict {[List of values]} -- Array of Predicted Values.
        datelist: {[List of Datetime.date()]} --
                Array of Datetime.date() dates that correspond to the
                dates where y_true and y_predict are.
        xlab: {[String]} -- Title of xlabel
        ylab: {[String]} -- Title of ylabel
        title: {[String]} -- Title of figure
        ticks_separation {[String]} -- Select the range where of the 
            ticks separation. Options are the following:

            -'days'
            -'weeks'
            -'months'
            -'years'

    Returns:
        Matplotlib Figure

    """
    plt.style.use('seaborn')

    #create plot
    fig=plt.figure(figsize=(15,10))
    
    #plot things
    plt.plot(datelist,y_true, label=r'True Values' ,
             linestyle='--', linewidth=2)
    plt.plot(datelist,y_predict, label=r'Predicted Values',
             linestyle='--', linewidth=2)
    plt.scatter(datelist,y_true)
    plt.scatter(datelist,y_predict)
    
    #labels
    plt.xlabel(xlab)
    plt.ylabel(ylab)
    plt.title(title)
    
    #set ticks every week
    if ticks_separation == 'days':
        plt.gca().xaxis.set_major_locator(matplotlib.dates.DayLocator())
        
    elif ticks_separation == 'weeks':
        plt.gca().xaxis.set_major_locator(matplotlib.dates.WeekdayLocator())
        
    elif ticks_separation == 'months':
        plt.gca().xaxis.set_major_locator(matplotlib.dates.MonthLocator())
        
    elif ticks_separation == 'days':
        plt.gca().xaxis.set_major_locator(matplotlib.dates.YearLocator())

    
    #set week format
    plt.gca().xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%d %b'))
    
    
    plt.legend(loc='best')
    
    #increase all text
    ax=plt.gca()
    for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] +
                 ax.get_xticklabels() + ax.get_yticklabels() + ax.legend().get_texts()):
        item.set_fontsize(18)
    
    
    return fig



    
def plot_calmap(df_serie, title='Calendar 2018'): 
    """
    Function that plots a Calendar Map
    
    Arguments:
        df_serie {Pandas series} -- Pandas series with the index in a day
         frequency: such as:
                2018-01-01     4959
                2018-01-02    55614
                2018-01-03    60449
                ...           ...
        
        title {string} -- Title of the figure
    """
    
    
    plt.style.use('seaborn')

    fig = plt.figure(figsize=(15,6))
    ax = fig.add_subplot(111)
    cax = calmap.yearplot(df_serie, ax=ax  )#, cmap='YlGn')
    cb=fig.colorbar(cax.get_children()[1], ax=cax, orientation='horizontal')
    
    plt.title(title)
    
    
    #increase all text
    ax=plt.gca()
    for item in ([ ax.xaxis.label, ax.yaxis.label] +
                 ax.get_xticklabels() + ax.get_yticklabels()  ):
        item.set_fontsize(16)
    
    cb.ax.tick_params(labelsize=14)     
    ax.title.set_fontsize(22)
       
    
    return fig



if __name__ == '__main__':

    """ Calendar Map"""
    
    # Create data 
    all_days = pd.date_range('1/1/2018', periods=365, freq='D')
    days = np.random.choice(all_days, 500)
    df_serie = pd.Series(np.random.randn(len(days)), index=days)

    # plot data
    fig=plot_calmap(df_serie)
    plt.show(fig)

    """ Scatter Error """
    
    # Create data
    y_true =    [0,1,2,3,4]
    y_predict = [1,0,3,3,5]

    dates = ['02/02/1991','02/03/1991','02/04/1991','02/08/1991','03/09/1991']
    datelist = [datetime.strptime(d,'%m/%d/%Y').date() for d in dates]

    # Plot
    fig = scatter_error_plot(y_true, y_predict, datelist,
                   '','Units Sold','Error Analysis')
    plt.show() # make f1 active again
