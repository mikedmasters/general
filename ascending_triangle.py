# This function takes a pandas DataFrame data containing the high, low, and close price
# and returns a binary array indicating where an ascending triangle pattern is detected. 
# The function first calculates the upper and lower trendlines of the ascending triangle by iterating over 
# the data and comparing the price values. Then, it checks whether the close prices of each data point fall 
# within the bounds of the upper and lower trendlines, and assigns a value of 1 where the condition is true 
# and 0 where it is false. 
# The resulting is_asc_triangle array can be used for further analysis or to plot the pattern on a chart.

import numpy as np

def ascending_triangle_pattern(data):
    highs = data['High']
    lows = data['Low']
    closes = data['Close']
    n = len(highs)
    upper_trendline = []
    lower_trendline = []
    for i in range(1, n):
        if highs[i] == highs[i-1]:
            upper_trendline.append(highs[i])
            lower_trendline.append(lows[i])
        elif highs[i] > highs[i-1]:
            upper_trendline.append(highs[i])
            lower_trendline.append(max(lows[i], lows[i-1]))
        else:
            upper_trendline.append(max(highs[i], highs[i-1]))
            lower_trendline.append(lows[i])
    is_asc_triangle = np.where((closes > lower_trendline) & (closes < upper_trendline), 1, 0)
    return is_asc_triangle

