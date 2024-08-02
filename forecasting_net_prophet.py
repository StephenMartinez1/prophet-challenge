# -*- coding: utf-8 -*-
"""forecasting_net_prophet.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1EP3hFlWUi_aljfxERky5K-9PxHa9J8XO

# Forecasting Net Prophet

You’re a growth analyst at [MercadoLibre](http://investor.mercadolibre.com/about-us). With over 200 million users, MercadoLibre is the most popular e-commerce site in Latin America. You've been tasked with analyzing the company's financial and user data in clever ways to make the company grow. So, you want to find out if the ability to predict search traffic can translate into the ability to successfully trade the stock.

The instructions for this Challenge are divided into four steps, as follows:

* Step 1: Find unusual patterns in hourly Google search traffic

* Step 2: Mine the search traffic data for seasonality

* Step 3: Relate the search traffic to stock price patterns

* Step 4: Create a time series model with Prophet

The following subsections detail these steps.

## Install and import the required libraries and dependencies
"""

# Install the required libraries
!pip install prophet
!pip install matplotlib

# Commented out IPython magic to ensure Python compatibility.
# Import the required libraries and dependencies
import pandas as pd
from prophet import Prophet
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
# %matplotlib inline

"""## Step 1: Find Unusual Patterns in Hourly Google Search Traffic

The data science manager asks if the Google search traffic for the company links to any financial events at the company. Or, does the search traffic data just present random noise? To answer this question, pick out any unusual patterns in the Google search data for the company, and connect them to the corporate financial events.

To do so, complete the following steps:

1. Read the search data into a DataFrame, and then slice the data to just the month of May 2020. (During this month, MercadoLibre released its quarterly financial results.) Visualize the results. Do any unusual patterns exist?

2. Calculate the total search traffic for the month, and then compare the value to the monthly median across all months. Did the Google search traffic increase during the month that MercadoLibre released its financial results?

"""



"""#### Step 1: Read the search data into a DataFrame, and then slice the data to just the month of May 2020. (During this month, MercadoLibre released its quarterly financial results.) Visualize the results. Do any unusual patterns exist?"""

# Store the data in a Pandas DataFrame
# Set the "Date" column as the Datetime Index.

df_mercado_trends = pd.read_csv(
    "https://static.bc-edx.com/ai/ail-v-1-0/m8/lms/datasets/google_hourly_search_trends.csv",
    index_col='Date',
    parse_dates=True
).dropna()

# Review the first and last five rows of the DataFrame
display(df_mercado_trends.head())
display(df_mercado_trends.tail())

# Review the data types of the DataFrame using the info function
df_mercado_trends.info()

# Slice the DataFrame to just the month of May 2020
df_may_2020 = df_mercado_trends.loc['2020-05']

# Plot to visualize the data for May 2020
plt.figure(figsize=(10,6))
plt.plot(df_may_2020.index, df_may_2020['Search Trends'], linestyle='-')
plt.title('Data for May 2020')
plt.xlabel('Date')
plt.ylabel('Search Trends')

plt.show()

"""#### Step 2: Calculate the total search traffic for the month, and then compare the value to the monthly median across all months. Did the Google search traffic increase during the month that MercadoLibre released its financial results?"""

# Calculate the sum of the total search traffic for May 2020
df_traffic_may_2020 = df_may_2020['Search Trends'].sum()

# View the traffic_may_2020 value
print("Search Trends", df_traffic_may_2020)

# Calcluate the monhtly median search traffic across all months
# Group the DataFrame by index year and then index month, chain the sum and then the median functions
monthly_traffic = df_mercado_trends.groupby([df_mercado_trends.index.year,df_mercado_trends.index.month]).sum()
monthly_traffic = round(monthly_traffic.median(),2)

# View the median_monthly_traffic value
print(monthly_traffic)

# Compare the seach traffic for the month of May 2020 to the overall monthly median value, Divide the may traffic total by the median monthly traffic
df_traffic_may_2020/monthly_traffic

"""##### Answer the following question:

**Question:** Did the Google search traffic increase during the month that MercadoLibre released its financial results?

**Answer:** **Yes, there was an increase during the month Mercadolibre released its financial results.**

## Step 2: Mine the Search Traffic Data for Seasonality

Marketing realizes that they can use the hourly search data, too. If they can track and predict interest in the company and its platform for any time of day, they can focus their marketing efforts around the times that have the most traffic. This will get a greater return on investment (ROI) from their marketing budget.

To that end, you want to mine the search traffic data for predictable seasonal patterns of interest in the company. To do so, complete the following steps:

1. Group the hourly search data to plot the average traffic by the hour of day. Does the search traffic peak at a particular time of day or is it relatively consistent?

2. Group the hourly search data to plot the average traffic by the day of the week (for example, Monday vs. Friday). Does the search traffic get busiest on any particular day of the week?

3. Group the hourly search data to plot the average traffic by the week of the year. Does the search traffic tend to increase during the winter holiday period (weeks 40 through 52)?

#### Step 1: Group the hourly search data to plot the average traffic by the hour of the day.
"""

# Group the hourly search data to plot the average traffic by the day of week, using `df.index.hour`
hourly=df_mercado_trends.index.hour

df_mercado_trends['Search Trends'].groupby(hourly).mean().plot(label='Search Trends')

plt.xlabel('Hour Of Day')

plt.ylabel('Number Of Searches')

plt.legend()

"""#### Step 2: Group the hourly search data to plot the average traffic by the day of the week (for example, Monday vs. Friday)."""

# Group the hourly search data to plot the average traffic by the day of week, using `df.index.isocalendar().day`.
weekly = df_mercado_trends.index.dayofweek

df_mercado_trends['Search Trends'].groupby(weekly).mean().plot(label='Search Trends')

plt.xlabel('Day Of Week')

plt.ylabel('Number Of Searches')

plt.legend()

"""#### Step 3: Group the hourly search data to plot the average traffic by the week of the year."""

# Group the hourly search data to plot the average traffic by the week of the year using `df.index.isocalendar().week`.
week_of_year = df_mercado_trends.index.isocalendar().week

average_traffic_by_week_of_year = df_mercado_trends.groupby(week_of_year)['Search Trends'].mean()

average_traffic_by_week_of_year.plot(label="Search Trends")

plt.xlabel('Week Of Year')

plt.ylabel('Number Of Searches')

plt.tight_layout()

plt.legend()

"""##### Answer the following question:

**Question:** Are there any time based trends that you can see in the data?

**Answer:** **Yes, there are peaks during hour of day chart, a slope during the day of week chart, and obvious visual difference between week of year chart. .**

## Step 3: Relate the Search Traffic to Stock Price Patterns

You mention your work on the search traffic data during a meeting with people in the finance group at the company. They want to know if any relationship between the search data and the company stock price exists, and they ask if you can investigate.

To do so, complete the following steps:

1. Read in and plot the stock price data. Concatenate the stock price data to the search data in a single DataFrame.

2. Market events emerged during the year of 2020 that many companies found difficult. But, after the initial shock to global financial markets, new customers and revenue increased for e-commerce platforms. Slice the data to just the first half of 2020 (`2020-01` to `2020-06` in the DataFrame), and then plot the data. Do both time series indicate a common trend that’s consistent with this narrative?

3. Create a new column in the DataFrame named “Lagged Search Trends” that offsets, or shifts, the search traffic by one hour. Create two additional columns:

    * “Stock Volatility”, which holds an exponentially weighted four-hour rolling average of the company’s stock volatility

    * “Hourly Stock Return”, which holds the percent change of the company's stock price on an hourly basis

4. Review the time series correlation, and then answer the following question: Does a predictable relationship exist between the lagged search traffic and the stock volatility or between the lagged search traffic and the stock price returns?

#### Step 1: Read in and plot the stock price data. Concatenate the stock price data to the search data in a single DataFrame.
"""

# Upload the "mercado_stock_price.csv" file into Colab, then store in a Pandas DataFrame
# Set the "date" column as the Datetime Index.
df_mercado_stock = pd.read_csv(
    "https://static.bc-edx.com/ai/ail-v-1-0/m8/lms/datasets/mercado_stock_price.csv",
    index_col="date",
    parse_dates=True
).dropna()

# View the first and last five rows of the DataFrame
display(df_mercado_stock.head())
display(df_mercado_stock.tail())

# Visualize the closing price of the df_mercado_stock DataFrame
df_mercado_stock.plot()

plt.xlabel('Year')

plt.ylabel('Closing Price')

plt.tight_layout()

plt.legend()

# Concatenate the df_mercado_stock DataFrame with the df_mercado_trends DataFrame
# Concatenate the DataFrame by columns (axis=1), and drop and rows with only one column of data
merged_df = pd.concat([df_mercado_stock, df_mercado_trends], axis=1).dropna()

# View the first and last five rows of the DataFrame
display(merged_df.head())

display(merged_df.tail())

"""#### Step 2: Market events emerged during the year of 2020 that many companies found difficult. But, after the initial shock to global financial markets, new customers and revenue increased for e-commerce platforms. Slice the data to just the first half of 2020 (`2020-01` to `2020-06` in the DataFrame), and then plot the data. Do both time series indicate a common trend that’s consistent with this narrative?"""

# For the combined dataframe, slice to just the first half of 2020 (2020-01 through 2020-06)
merged_df_2020 = merged_df.loc["2020-01":"2020-06" ]

# View the first and last five rows of first_half_2020 DataFrame
display(merged_df_2020.head())

display(merged_df_2020.tail())

# Visualize the close and Search Trends data
merged_df_2020.plot(subplots=True, figsize=(7, 5))

# Plot each column on a separate axes using the following syntax
# `plot(subplots=True)`
plt.show()

"""##### Answer the following question:

**Question:** Do both time series indicate a common trend that’s consistent with this narrative?

**Answer:** **I personally would like more data to provide more noticeable trends for comparison.  From this limited data provided i would say the common trend is consistent with the narrative.**

#### Step 3: Create a new column in the DataFrame named “Lagged Search Trends” that offsets, or shifts, the search traffic by one hour. Create two additional columns:

* “Stock Volatility”, which holds an exponentially weighted four-hour rolling average of the company’s stock volatility

* “Hourly Stock Return”, which holds the percent change of the company's stock price on an hourly basis
"""

# Create a new column in the mercado_stock_trends_df DataFrame called Lagged Search Trends
# This column should shift the Search Trends information by one hour
merged_df["lagged Search Trends"] = merged_df["Search Trends"].shift(1)

# Create a new column in the mercado_stock_trends_df DataFrame called Stock Volatility
# This column should calculate the standard deviation of the closing stock price return data over a 4 period rolling window
merged_df["Stock Volatility"] = merged_df["close"].pct_change().rolling(window=4).std()

# Visualize the stock volatility
plt.figure(figsize=(7,5))
plt.plot(merged_df.index, merged_df["Stock Volatility"], color="midnightblue" )
plt.grid(False)
plt.xticks(rotation=45)
plt.xlabel('Month-Year')
plt.show()

"""**Solution Note:** Note how volatility spiked, and tended to stay high, during the first half of 2020. This is a common characteristic of volatility in stock returns worldwide: high volatility days tend to be followed by yet more high volatility days. When it rains, it pours."""

# Create a new column in the mercado_stock_trends_df DataFrame called Hourly Stock Return
# This column should calculate hourly return percentage of the closing price
merged_df["Hourly Stock Return"]= merged_df["close"].pct_change()

# View the first and last five rows of the mercado_stock_trends_df DataFrame
display(merged_df.head())
display(merged_df.tail())

"""#### Step 4: Review the time series correlation, and then answer the following question: Does a predictable relationship exist between the lagged search traffic and the stock volatility or between the lagged search traffic and the stock price returns?"""

# Construct correlation table of Stock Volatility, Lagged Search Trends, and Hourly Stock Return
correlated_columns = ["Stock Volatility", "lagged Search Trends", "Hourly Stock Return"]

correlated_columns = merged_df[correlated_columns].corr()

display(correlated_columns)

"""##### Answer the following question:

**Question:** Does a predictable relationship exist between the lagged search traffic and the stock volatility or between the lagged search traffic and the stock price returns?

**Answer:** **Yes, there appears to be a small relationship between the lagged search traffic and both the stock volatility and stock price returns.**

## Step 4: Create a Time Series Model with Prophet

Now, you need to produce a time series model that analyzes and forecasts patterns in the hourly search data. To do so, complete the following steps:

1. Set up the Google search data for a Prophet forecasting model.

2. After estimating the model, plot the forecast. How's the near-term forecast for the popularity of MercadoLibre?

3. Plot the individual time series components of the model to answer the following questions:

    * What time of day exhibits the greatest popularity?

    * Which day of the week gets the most search traffic?

    * What's the lowest point for search traffic in the calendar year?

#### Step 1: Set up the Google search data for a Prophet forecasting model.
"""

# Using the df_mercado_trends DataFrame, reset the index so the date information is no longer the index
reset_df = df_mercado_trends.reset_index()

# Label the columns ds and y so that the syntax is recognized by Prophet
reset_df = reset_df.rename(columns={'Date': 'ds', 'Search Trends': 'y'})


# Drop an NaN values from the prophet_df DataFrame
reset_df.dropna(inplace=True)

# View the first and last five rows of the mercado_prophet_df DataFrame
print("First five rows:")
display(reset_df.head())

print("\nLast five rows:")
display(reset_df.tail())

# Call the Prophet function, store as an object
prophet_model = Prophet()

# Fit the time-series model.
prophet_model.fit(reset_df)

# Create a future dataframe to hold predictions
# Make the prediction go out as far as 2000 hours (approx 80 days)
future_mercado_trends = prophet_model.make_future_dataframe(periods=2000, freq='H')

# View the last five rows of the future_mercado_trends DataFrame
print('Last five rows of the future dataframe:')
display(future_mercado_trends)

# Make the predictions for the trend data using the future_mercado_trends DataFrame
forecast_mercado_trends = prophet_model.predict(future_mercado_trends)

# Display the first five rows of the forecast_mercado_trends DataFrame
print('First five rows of the forcast dataframe:')
display(forecast_mercado_trends.head())

"""#### Step 2: After estimating the model, plot the forecast. How's the near-term forecast for the popularity of MercadoLibre?"""

# Plot the Prophet predictions for the Mercado trends data
prophet_model.plot(forecast_mercado_trends)

"""##### Answer the following question:

**Question:**  How's the near-term forecast for the popularity of MercadoLibre?

**Answer:** **The near-term forecast looks to trend slightly downwards.**

#### Step 3: Plot the individual time series components of the model to answer the following questions:

* What time of day exhibits the greatest popularity?

* Which day of the week gets the most search traffic?

* What's the lowest point for search traffic in the calendar year?
"""

# Set the index in the forecast_mercado_trends DataFrame to the ds datetime column
forecast_mercado_trends.set_index("ds", inplace=True)
forecast_selected_columns = forecast_mercado_trends[['yhat', 'yhat_lower', 'yhat_upper']]

# View the only the yhat,yhat_lower and yhat_upper columns from the DataFrame
display(forecast_selected_columns.head())

"""Solutions Note: `yhat` represents the most likely (average) forecast, whereas `yhat_lower` and `yhat_upper` represents the worst and best case prediction (based on what are known as 95% confidence intervals)."""

# From the forecast_mercado_trends DataFrame, plot the data to visualize
#  the yhat, yhat_lower, and yhat_upper columns over the last 2000 hours
forecast_mercado_trends[['yhat','yhat_lower','yhat_upper']].iloc[-2000:].plot()

plt.xlabel('Day Of Month')

# Reset the index in the forecast_mercado_trends DataFrame
forecast_mercado_trends_reset = forecast_mercado_trends.reset_index()

# Use the plot_components function to visualize the forecast results for the forecast_canada DataFrame
prophet_model.plot_components(forecast_mercado_trends_reset)
plt.show()

"""##### Answer the following questions:

**Question:** What time of day exhibits the greatest popularity?

**Answer:** **12am/midnight**

**Question:** Which day of week gets the most search traffic?
   
**Answer:** **Tuesday**

**Question:** What's the lowest point for search traffic in the calendar year?

**Answer:** **October**
"""