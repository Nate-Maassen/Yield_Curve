import matplotlib.pyplot as plt
from lxml import html
import requests
from datetime import date, datetime

# x axis is borrowing period (typically in years)
# y axis is interest rate
date = date.today()
now = datetime.now()
today = str(date.strftime('%m/%d/%y'))
time = now.strftime('%H:%M:%S')
data = requests.get('https://www.treasury.gov/resource-center/data-chart-center/interest-rates/Pages/TextView.aspx?data=yield')
tree = html.fromstring(data.content)
interest_rates = tree.xpath('//td[@class="text_view_data"]/text()')
maturity = tree.xpath('//th[@scope="col"]/text()')
maturity.remove('Date')
def sort_lists(interest_rate):
    '''Sorts list of interest rates in order to plot them accurately
        Precondition: interest_rate is a list of interest rates and dates scraped
        from the US treasury site
        Postcondition: returns a list of the most recent T-Bill rates with as tuples
        with borrowing period (in years) as the x-values and interest rates as the
        y-values
    
    '''
    
    # here we place the data in our list for plotting based off the date of data
    interest_rate_list = []
    for value in interest_rate:
        if value == today:
            location = interest_rate.index(value)
            todays_rates = interest_rate[(location + 5):]
            for rate in todays_rates:
                if rate != today:
                    rate = float(rate)
                    interest_rate_list.append(rate)
    # since the treasury does not report data on weekends or hollidays i have
    # to run code to display the most recent data points
    if interest_rate_list == []:
        for value in interest_rate[-8:]:
            rate = float(value)
            interest_rate_list.append(rate)
    # I have decided to only plot the rates associated with 1 year through 30 years            
    borrowing_period = [1, 2, 3, 5, 7, 10, 20, 30]
    
    plot_points = []
    
    for (x, y) in zip(borrowing_period, interest_rate_list):
        plot_points.append((x, y))
    
    return plot_points
    
        
# this is where we present the details for the graph in matplotlib
plt.title(f'Yield Curve as of {today} at {time}')
plt.xlabel('Borrowing Period (in years)')
plt.ylabel('Interest Rate')
plot_points = sort_lists(interest_rates)
# this is where we actually plot the points
for x, y in plot_points:
    plt.scatter(x, y, c = 'blue')
    plt.plot(*zip(*plot_points), '-b')
plt.show()