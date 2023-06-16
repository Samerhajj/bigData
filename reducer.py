#!/usr/bin/env python3

import sys

def get_season(month):
    if month in [12, 1, 2]:
        return "Winter"
    elif month in [3, 4, 5]:
        return "Spring"
    elif month in [6, 7, 8]:
        return "Summer"
    elif month in [9, 10, 11]:
        return "Autumn"
    else:
        return "Unknown"


def get_month_name(month):
    month_names = {
        1: "January",
        2: "February",
        3: "March",
        4: "April",
        5: "May",
        6: "June",
        7: "July",
        8: "August",
        9: "September",
        10: "October",
        11: "November",
        12: "December"
    }
    return month_names.get(month, "Unknown")

def reducer():
    current_key = None
    total_sum = 0
    season_sums = {"Winter": 0, "Spring": 0, "Summer": 0, "Autumn": 0}
    year = None
    min_year = None
    min_value = float('inf')
    max_year = None
    max_sum = float('-inf')
    min_season = None
    max_season = None
    month_data = {}
    year_count = 0  # Number of years
    yearly_sum = 0  # Total sum of yearly precipitation

    print("Year\tTotal\tWinter\tSpring\tSummer\tAutumn")  # Add header

    for line in sys.stdin:
        key, month, value = line.strip().split('\t')

        if current_key is None:
            current_key = key
            year = key

        if key != current_key:
            print(f"{current_key}\t{total_sum}\t{season_sums['Winter']}\t{season_sums['Spring']}\t{season_sums['Summer']}\t{season_sums['Autumn']}")

            # Update minimum and maximum values if applicable
            if total_sum < min_value:
                min_value = total_sum
                min_year = current_key
            if total_sum > max_sum:
                max_sum = total_sum
                max_year = current_key

            yearly_sum += total_sum
            year_count += 1
            current_key = key
            total_sum = 0
            season_sums = {"Winter": 0, "Spring": 0, "Summer": 0, "Autumn": 0}

        total_sum += float(value)

        season = get_season(int(month))
        season_sums[season] += float(value)

        if month in month_data:
            month_data[month].append((current_key, float(value)))
        else:
            month_data[month] = [(current_key, float(value))]

    if current_key is not None:
        print(f"{current_key}\t{total_sum}\t{season_sums['Winter']}\t{season_sums['Spring']}\t{season_sums['Summer']}\t{season_sums['Autumn']}")

        # Update minimum and maximum values if applicable
        if total_sum < min_value:
            min_value = total_sum
            min_year = current_key
        if total_sum > max_sum:
            max_sum = total_sum
            max_year = current_key
        yearly_sum += total_sum
        year_count += 1

    average_yearly_sum = yearly_sum / year_count
    print("Average Yearly Sum:", average_yearly_sum)
    print("Year with lowest Precipitation:", min_year, "Precipitation:", min_value)
    print("Year with highest Precipitation:", max_year, "Precipitation:", max_sum)

    min_precipitation = min([value for data in month_data.values() for year, value in data])
    max_precipitation = max([value for data in month_data.values() for year, value in data])

    print("Months with lowest precipitation:")
    for month, data in month_data.items():
        values = [value for year, value in data]
        min_value = min(values)
        if min_value != min_precipitation:
            continue
        min_years = [year for year, value in data if value == min_value]
        month_name = get_month_name(int(month))
        print("Month:", month_name, "Value:", min_value, "Years:", min_years)

    print("Months with highest precipitation:")
    for month, data in month_data.items():
        values = [value for year, value in data]
        max_value = max(values)
        if max_value != max_precipitation:
            continue
        max_years = [year for year, value in data if value == max_value]
        month_name = get_month_name(int(month))
        print("Month:", month_name, "Value:", max_value, "Years:", max_years)

    # Check for drought years
    drought_counter = 0  # Counter for consecutive drought years
    drought_years = []  # List to store drought years
    year_sums = {}  # Dictionary to store the sum of values for each year

    for year_data in month_data.values():
        for year, value in year_data:
            if year in year_sums:
                year_sums[year] += value
            else:
                year_sums[year] = value

    # Calculate season sums for each year
    season_sums = {"Winter": {}, "Spring": {}, "Summer": {}, "Autumn": {}}

    for month, data in month_data.items():
        for year, value in data:
            season = get_season(int(month))
            if year not in season_sums[season]:
                season_sums[season][year] = 0
            season_sums[season][year] += value

     # Find the overall minimum and maximum seasons with their corresponding years
    min_season = min(season_sums, key=lambda season: min(season_sums[season].values()))
    max_season = max(season_sums, key=lambda season: max(season_sums[season].values()))
    min_year = min(season_sums[min_season], key=season_sums[min_season].get)
    max_year = max(season_sums[max_season], key=season_sums[max_season].get)
    min_season_value = season_sums[min_season][min_year]
    max_season_value = season_sums[max_season][max_year]

    # Print the overall minimum and maximum seasons with their corresponding years and precipitation values
    print("Season with lowest precipitation:", min_season, "Year:", min_year, "Precipitation:", min_season_value)
    print("Season with highest precipitation:", max_season, "Year:", max_year, "Precipitation:", max_season_value)


    # Find drought years
    consecutive_years = []  # List to store consecutive drought years

    for year, total_sum in year_sums.items():
        if total_sum < average_yearly_sum:
            drought_counter += 1
            drought_years.append(year)
        else:
            if drought_counter >= 3:
                consecutive_years.extend(drought_years[-drought_counter:])
            drought_counter = 0
            drought_years = []

    if consecutive_years:
        print("Drought Years:")
        print(", ".join(consecutive_years))


if __name__ == "__main__":
    reducer()
