
# Use !pip install -q xlrd to open excel file(xlsx)

# Load the excel file
import pandas as pd

# Replace file path 
df = pd.read_excel('/content/drive/MyDrive/Jar Project/BA Assignment Walmart Sales.xlsx')
print(df)

# Checking for null values
df.isnull().values.any()

# Adding new column Order Value
df['Order Value'] = df['Quantity']*df['Unit price']
print(df)

# Q1 - Part A
# Dictionaries to store the sales and revenue values
revenue_analysis = {}
sales_analysis = {}
city_sales_split = {}
city_revenue_split = {}
branch_sales_split = {}
branch_revenue_split = {}
avg_price_values = {}

# Sales and Revenue Breakup at city level
for city in df['City'].unique():
  df_city = df[df['City'] == city]

  city_sales = df_city['Quantity'].sum()
  city_revenue = df_city['Order Value'].sum()

  key = (city)
  city_sales_split[key] = city_sales
  city_revenue_split[key] = city_revenue

  # Sales and Revenue Breakup at branch level
  for branch in df_city['Branch'].unique():
    df_branch = df_city[df_city['Branch'] == branch]

    branch_sales = df_branch['Quantity'].sum()
    branch_revenue = df_branch['Order Value'].sum()
    avg_sale_price = df_branch['Unit price'].mean()

    key = (city, branch)
    branch_sales_split[key] = branch_sales
    branch_revenue_split[key] = branch_revenue
    avg_price_values[key] = avg_sale_price


    # Sales and Revenue for each product line
    for product_line in df_branch['Product line'].unique():
            df_product_line = df_branch[df_branch['Product line'] == product_line]

            sales = df_product_line['Quantity'].sum()
            revenue = df_product_line['Order Value'].sum()

            # Adding values to dictionary
            key = (city, branch, product_line)
            revenue_analysis[key] = revenue
            sales_analysis[key] = sales

print(f"City Sales Split: {city_sales_split}")
print(f"City Revenue Split: {city_revenue_split}")
print(f"Branch Sales Split: {branch_sales_split}")
print(f"Branch Revenue Split: {branch_revenue_split}")
print(f"Average Price Values: {avg_price_values}")


# Sales comparision on city and branch level
import numpy as np
import matplotlib.pyplot as plt
# %matplotlib inline

cities = df['City'].unique()
branches = df['Branch'].unique()

# A dictionary to hold sales data for each city and branch
city_branch_sales_data = {city: {branch: [] for branch in branches} for city in cities}

# Populate dictionary with sales data for each city and branch
for (city, branch), sales in branch_sales_split.items():
    city_branch_sales_data[city][branch].append(sales)

bar_width = 0.1
bar_positions = np.arange(len(cities))

# Plot grouped bar chart
plt.figure(figsize=(10, 6))
for i, branch in enumerate(branches):
    branch_sales = [np.mean(city_branch_sales_data[city][branch]) for city in cities]
    plt.bar(bar_positions + i * bar_width, branch_sales, width=bar_width, label=branch)

plt.xlabel('Cities')
plt.ylabel('Sales')
plt.title('Sales Across Branches in All Cities')
plt.xticks(bar_positions + bar_width / 2, cities)
plt.legend()

#Q1 - Part B
# Distribution of average prices across branches
cities = df['City'].unique()
branches = df['Branch'].unique()

# Color map with different colors for each gender
colors = plt.cm.tab10.colors[:len(cities)]

for i, city in enumerate(cities):
  avg_prices = [avg_price_values[(city, branch)] for branch in branches]
  plt.plot(branches, avg_prices, label=city, color=colors[i])

plt.xlabel('Branches')
plt.ylabel('Average Prices')
plt.title('Average price distribution')
plt.legend()

plt.show()

#Q1 - Part C
product_monthly_sales = {}
product_monthly_revenue = {}
gender_monthly_sales = {}
gender_monthly_revenue = {}
payment_monthly_sales = {}
payment_monthly_revenue = {}

# Convert date column to datetime format for month on month analysis
df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')

# Month on month sales and revenue across Product line
for product_line in df['Product line'].unique():
  df_product_line = df[df['Product line'] == product_line]

  for month in range(1, 4):
    monthly_sales = df_product_line.loc[df_product_line['Date'].dt.month == month, 'Quantity'].sum()
    monthly_revenue = df_product_line.loc[df_product_line['Date'].dt.month == month, 'Order Value'].sum()

    key = (month, product_line)
    product_monthly_sales[key] = monthly_sales
    product_monthly_revenue[key] = monthly_revenue

# Month on month sales and revenue across Gender
for gender in df['Gender'].unique():
  df_gender = df[df['Gender'] == gender]

  for month in range(1, 4):
    monthly_sales = df_gender.loc[df_gender['Date'].dt.month == month, 'Quantity'].sum()
    monthly_revenue = df_gender.loc[df_gender['Date'].dt.month == month, 'Order Value'].sum()

    key = (month, gender)
    gender_monthly_sales[key] = monthly_sales
    gender_monthly_revenue[key] = monthly_revenue

# Month on month sales and revenue across Payment method
for payment_method in df['Payment'].unique():
  df_payment = df[df['Payment'] == payment_method]

  for month in range(1, 4):
    monthly_sales = df_payment.loc[df_payment['Date'].dt.month == month, 'Quantity'].sum()
    monthly_revenue = df_payment.loc[df_payment['Date'].dt.month == month, 'Order Value'].sum()

    key = (month, payment_method)
    payment_monthly_sales[key] = monthly_sales
    payment_monthly_revenue[key] = monthly_revenue

# Print dictionaries

print(f"Product-wise Monthly Sales: {product_monthly_sales}")
print(f"Product-wise Monthly Revenue: {product_monthly_revenue}")
print(f"Gender-wise Monthly Sales: {gender_monthly_sales}")
print(f"Gender-wise Monthly Revenue: {gender_monthly_revenue}")
print(f"Payment-wise Monthly Sales: {payment_monthly_sales}")
print(f"Payment-wise Monthly Revenue: {payment_monthly_revenue}")


# All graphs for month on month sales and revene data visualization

#Plot for month on month sales across product line

product_lines = df['Product line'].unique()
months = [1, 2, 3]

# Color map with different colors for each product line
colors = plt.cm.tab10.colors[:len(product_lines)]

# Plot month-on-month sales for each unique product line
for i, product_line in enumerate(product_lines):
    # Filter dictionary for the current product line
    product_sales = [product_monthly_sales[(month, product_line)] for month in months]

    # Plot the sales data
    plt.plot(months, product_sales, label=product_line, color=colors[i])

plt.xlabel('Month')
plt.ylabel('Sales')
plt.title('Month-on-Month Sales for Different Products')
plt.legend()

plt.show()

#Plot for month on month sales across genders

gender = df['Gender'].unique()
months = [1, 2, 3]

# Color map with different colors for each gender
colors = plt.cm.tab10.colors[:len(gender)]

# Plot month-on-month sales for each gender
for i, gender in enumerate(gender):
    # Filter dictionary for the current gender
    gender_sales = [gender_monthly_sales[(month, gender)] for month in months]

    # Plot the sales data
    plt.plot(months, gender_sales, label=gender, color=colors[i])

plt.xlabel('Month')
plt.ylabel('Sales')
plt.title('Month-on-Month Sales for Different Genders')
plt.legend()

plt.show()

#Plot for month on month revenue across genders

gender = df['Gender'].unique()
months = [1, 2, 3]

# Color map with different colors for each gender
colors = plt.cm.tab10.colors[:len(gender)]

# Plot month-on-month sales for each gender
for i, gender in enumerate(gender):
    # Filter dictionary for the current gender
    gender_revenue = [gender_monthly_revenue[(month, gender)] for month in months]

    # Plot the sales data
    plt.plot(months, gender_revenue, label=gender, color=colors[i])

plt.xlabel('Month')
plt.ylabel('Revenue')
plt.title('Month-on-Month Revenue for Different Genders')
plt.legend()

plt.show()

#Plot for month on month sales across payment methods

payment_methods = df['Payment'].unique()
months = [1, 2, 3]

# Color map with different colors for each payment method
colors = plt.cm.tab10.colors[:len(payment_methods)]

# Plot month-on-month sales for each payment method
for i, payment_method in enumerate(payment_methods):
    # Filter dictionary for the current payment method
    payment_sales = [payment_monthly_sales[(month, payment_method)] for month in months]

    # Plot the sales data
    plt.plot(months, payment_sales, label=payment_method, color=colors[i])

plt.xlabel('Month')
plt.ylabel('Sales')
plt.title('Month-on-Month Sales for Different Payment Methods')
plt.legend()

plt.show()

#Plot for month on month revenue across payment methods

payment_methods = df['Payment'].unique()
months = [1, 2, 3]

# Color map with different colors for each payment method
colors = plt.cm.tab10.colors[:len(payment_methods)]

# Plot month-on-month sales for each payment method
for i, payment_method in enumerate(payment_methods):
    # Filter dictionary for the current payment method
    payment_revenue = [payment_monthly_revenue[(month, payment_method)] for month in months]

    # Plot the sales data
    plt.plot(months, payment_revenue, label=payment_method, color=colors[i])

plt.xlabel('Month')
plt.ylabel('Revenue')
plt.title('Month-on-Month Revenue for Different Payment Methods')
plt.legend()

plt.show()