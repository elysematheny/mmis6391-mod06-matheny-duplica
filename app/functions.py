import pandas as pd

# Function 1: Calculate total sales by region
def total_sales_by_region(df):
    """
    Calculate the total sales for each region.
    :param df: Pandas DataFrame with columns 'monthly_amount' and 'region'.
    :return: DataFrame with total sales by region.
    """
    total_sales = df.groupby('region')['monthly_amount'].sum().reset_index()
    total_sales = total_sales.rename(columns={'monthly_amount': 'total_sales'})
    return total_sales

# Function 2: Analyze monthly sales trends
def monthly_sales_trend(df):
    """
    Analyze the sales trends on a monthly basis.
    :param df: Pandas DataFrame with columns 'monthly_amount' and 'date'.
    :return: DataFrame showing total sales per month.
    """
    # Convert 'date' column to datetime if it's not already
    df['date'] = pd.to_datetime(df['date'])
    # Extract year-month period for grouping
    df['month_year'] = df['date'].dt.to_period('M')
    monthly_trend = df.groupby('month_year')['monthly_amount'].sum().reset_index()
    monthly_trend = monthly_trend.rename(columns={'monthly_amount': 'total_sales'})
    return monthly_trend

# Function 3: Identify the top-performing region based on total sales
def top_performing_region(df):
    """
    Identify the top-performing region based on total sales.
    :param df: Pandas DataFrame with columns 'monthly_amount' and 'region'.
    :return: The region with the highest total sales.
    """
    total_sales = total_sales_by_region(df)
    top_region = total_sales.sort_values(by='total_sales', ascending=False).head(1)
    return top_region
