import pandas as pd
import sys
import time

start=time.time()

# Check if the Excel file path is provided as a command-line argument
if len(sys.argv) < 2:
    print("Please provide the path to the Excel file as a command-line argument.")
    sys.exit(1)

# Get the Excel file path from the command-line argument
excel_file_path = sys.argv[1]

# Read the Excel file
df = pd.read_excel(excel_file_path, header=None)

# Calculate the sum of each year's months
df['Yearly Sum'] = df.iloc[:, 1:].sum(axis=1)

# Calculate the sum for each season
df['Winter']=df.iloc[:,[12,1,2]].sum(axis=1)
df['Spring']=df.iloc[:,[3,4,5]].sum(axis=1)
df['Summer']=df.iloc[:,[6,7,8]].sum(axis=1)
df['Autumn']=df.iloc[:,[9,10,11]].sum(axis=1)


# Create a new DataFrame with the yearly sums and seasonal sums
result_df = pd.DataFrame({
    'Year': df.iloc[:, 0],
    'Yearly Sum': df['Yearly Sum'],
    'Winter Sum': df['Winter'],
    'Spring Sum': df['Spring'],
    'Summer Sum': df['Summer'],
    'Autumn Sum': df['Autumn']
})

# Write the data to a new Excel file
result_df.to_excel('output_file.xlsx', index=False)

# Read the output Excel file
output_df = pd.read_excel('output_file.xlsx')

# Find the minimum and maximum yearly sums
min_sum = output_df['Yearly Sum'].min()
max_sum = output_df['Yearly Sum'].max()
average_sum=result_df['Yearly Sum'].mean()

season_columns = ['Winter Sum', 'Spring Sum', 'Summer Sum', 'Autumn Sum']

# Initialize variables to store the maximum and minimum seasons and their corresponding years and values
max_season = None
max_year = None
max_value = None
min_season = None
min_year = None
min_value = None
max_season_year=None
min_season_year=None

# Iterate over the columns and find the season with the maximum and minimum sums
for column in season_columns:
    max_index = output_df[column].idxmax()
    min_index = output_df[column].idxmin()

    if max_season is None or output_df.loc[max_index, column] > max_value:
        max_season = column
        max_season_year = output_df.loc[max_index, 'Year']
        max_value = output_df.loc[max_index, column]

    if min_season is None or output_df.loc[min_index, column] < min_value:
        min_season = column
        min_season_year = output_df.loc[min_index, 'Year']
        min_value = output_df.loc[min_index, column]


# Find the year associated with the minimum and maximum sums
min_year = output_df.loc[output_df['Yearly Sum'] == min_sum, 'Year'].values[0]
max_year = output_df.loc[output_df['Yearly Sum'] == max_sum, 'Year'].values[0]


# Find the column index for the highest and lowest month
max_month_index = df.iloc[:, 1:13].sum(axis=0).idxmax() - 1
min_month_index = df.iloc[:, 1:13].sum(axis=0).idxmin() - 1

# Find the year associated with the highest and lowest months
max_month_year = df[df.iloc[:, max_month_index+1] == df.iloc[:, max_month_index+1].max()][0].values[0]
min_month_year = df[df.iloc[:, min_month_index+1] == df.iloc[:, min_month_index+1].min()][0].values[0]



# Print the results
# Print the results on the same line
print("Average Yearly Sum:", average_sum)
print("Year for Minimum Precipitation:", min_year,"Precipitation:", min_sum)
print("Year for Maximum Percipitation:", max_year,"Precipitation:", max_sum)

#Print
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
print()
# Get the actual value of the highest month
max_month_value = df.iloc[:, max_month_index+1].max()

# Find the months with lowest values
lowest_months = []
for month in range(1, 13):
    if (df.iloc[:, month] == min_value).any():
        lowest_months.append(month)

# Print the months with a value of 0 and their associated years
for month in lowest_months:
    month_name = df.columns[month]
    years_with_zero = df[df.iloc[:, month] == min_value][0]
    print("Month:", months[month_name-1])
    print("Years with the lowest month Precipitation:", years_with_zero.values)
    print()

# Find the months with lowest values
highest_months = []
for month in range(1, 13):
    if (df.iloc[:, month] == max_month_value).any():
        highest_months.append(month)

# Print the months with a value of 0 and their associated years
for month in highest_months:
    month_name = df.columns[month]
    years_with_highest = df[df.iloc[:, month] == max_month_value][0]
    print("Month:", months[month_name - 1])
    print("Years with the highest month Precipitation:", years_with_highest.values)
    print()

# Check for three consecutive years with sum lower than average
drought_years = []
for i in range(len(result_df) - 2):
    if (
        result_df.loc[i, 'Yearly Sum'] < average_sum and
        result_df.loc[i+1, 'Yearly Sum'] < average_sum and
        result_df.loc[i+2, 'Yearly Sum'] < average_sum
    ):
        drought_years.append(result_df.loc[i, 'Year'])
        drought_years.append(result_df.loc[i+1, 'Year'])
        drought_years.append(result_df.loc[i+2, 'Year'])

# Print the years if found
drought_years = sorted(list(set(drought_years)))
if drought_years:
    print("Drought Years:", drought_years)
else:
    print("No three consecutive years with sum lower than average found.")


# Print the season with the maximum sum
print()
print("Season with Maximum Precipitation:")
print("Season:", max_season)
print("Year:", max_season_year)
print("Value:", max_value)
print()

# Print the season with the minimum sum
print("Season with Minimum Precipitation:")
print("Season:", min_season)
print("Year:", min_season_year)
print("Value:", min_value)
end=time.time()
print("elapsed time",end-start)