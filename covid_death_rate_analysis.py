import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Load the main data table
print("Loading data...")
worldometer_df = pd.read_csv('worldometer_snapshots_April18_to_May18.csv')
print("Data shape:", worldometer_df.shape)
print("\nFirst few rows of the dataset:")
print(worldometer_df.head())

# Example of filtering by country
country_name = 'USA'
country_df = worldometer_df.loc[worldometer_df['Country'] == country_name, :].reset_index(drop=True)
print(f"\nData for {country_name}:")
print(country_df.head())

# Example of filtering by date
selected_date = datetime.strptime('18/05/2020', '%d/%m/%Y')
selected_date_df = worldometer_df.loc[worldometer_df['Date'] == selected_date.strftime('%Y-%m-%d'), :].reset_index(drop=True)
print(f"\nData for {selected_date.strftime('%Y-%m-%d')}:")
print(selected_date_df.head())

# Analysis using the last date
last_date = datetime.strptime('18/05/2020', '%d/%m/%Y')
last_date_df = worldometer_df.loc[worldometer_df['Date'] == last_date.strftime('%Y-%m-%d'), :].reset_index(drop=True)
print(f"\nData for the last date {last_date.strftime('%Y-%m-%d')}:")
print(last_date_df.head())

# Calculate naive death rate for each country
last_date_df['Case Fatality Ratio'] = last_date_df['Total Deaths'] / last_date_df['Total Cases']

# Plot histogram of death rates
plt.figure(figsize=(12,8))
plt.hist(100 * np.array(last_date_df['Case Fatality Ratio']), bins=np.arange(35))
plt.xlabel('Death Rate (%)', fontsize=16)
plt.ylabel('Number of Countries', fontsize=16)
plt.title('Histogram of Death Rates for various Countries', fontsize=18)
plt.savefig('death_rate_histogram.png')
print("\nCreated death rate histogram")

# Filter out countries with small number of cases
min_number_of_cases = 1000
greatly_affected_df = last_date_df.loc[last_date_df['Total Cases'] > min_number_of_cases,:]

# Plot histogram for countries with significant cases
plt.figure(figsize=(12,8))
plt.hist(100 * np.array(greatly_affected_df['Case Fatality Ratio']), bins=np.arange(35))
plt.xlabel('Death Rate (%)', fontsize=16)
plt.ylabel('Number of Countries', fontsize=16)
plt.title('Histogram of Death Rates for Countries with >1000 Cases', fontsize=18)
plt.savefig('death_rate_histogram_filtered.png')
print("\nCreated filtered death rate histogram")

# Plot scatter of death rate as function of testing quality
last_date_df['Num Tests per Positive Case'] = last_date_df['Total Tests'] / last_date_df['Total Cases']

# Use the filtered dataframe for greatly affected countries
min_number_of_cases = 1000
greatly_affected_df = last_date_df.loc[last_date_df['Total Cases'] > min_number_of_cases,:]

x_axis_limit = 80

death_rate_percent = 100 * np.array(greatly_affected_df['Case Fatality Ratio'])
num_test_per_positive = np.array(greatly_affected_df['Num Tests per Positive Case'])
num_test_per_positive[num_test_per_positive > x_axis_limit] = x_axis_limit
total_num_deaths = np.array(greatly_affected_df['Total Deaths'])
population = np.array(greatly_affected_df['Population'])

plt.figure(figsize=(16,12))
plt.scatter(x=num_test_per_positive, y=death_rate_percent, 
            s=0.5*np.power(np.log(1+population),2), 
            c=np.log10(1+total_num_deaths))
plt.colorbar()
plt.ylabel('Death Rate (%)', fontsize=16)
plt.xlabel('Number of Tests per Positive Case', fontsize=16)
plt.title('Death Rate as function of Testing Quality', fontsize=18)
plt.xlim(-1, x_axis_limit + 12)
plt.ylim(-0.2,17)

# Plot country names on the scatter plot
countries_to_display = ['USA', 'Russia', 'Spain', 'Brazil', 'UK', 'Italy', 'France', 
                        'Germany', 'India', 'Canada', 'Belgium', 'Mexico', 'Netherlands', 
                        'Sweden', 'Portugal', 'UAE', 'Poland', 'Indonesia', 'Romania', 
                        'Israel','Thailand','Kyrgyzstan','El Salvador', 'S. Korea', 
                        'Denmark', 'Serbia', 'Norway', 'Algeria', 'Bahrain','Slovenia',
                        'Greece','Cuba','Hong Kong','Lithuania', 'Australia', 'Morocco', 
                        'Malaysia', 'Nigeria', 'Moldova', 'Ghana', 'Armenia', 'Bolivia', 
                        'Iraq', 'Hungary', 'Cameroon', 'Azerbaijan']

for country_name in countries_to_display:
    country_indices = greatly_affected_df.index[greatly_affected_df['Country'] == country_name].tolist()
    if country_indices:  # Check if the country exists in the dataframe
        country_index = country_indices[0]
        plt.text(x=num_test_per_positive[country_index] + 0.5,
                y=death_rate_percent[country_index] + 0.2,
                s=country_name, fontsize=10)
plt.savefig('death_rate_vs_testing.png')
print("\nCreated scatter plot of death rate vs testing quality")

# Look at data from best testing countries
good_testing_threshold = 50
good_testing_df = greatly_affected_df.loc[greatly_affected_df['Num Tests per Positive Case'] > good_testing_threshold,:]
print("\nCountries with good testing (>50 tests per positive case):")
print(good_testing_df[['Country', 'Total Cases', 'Total Deaths', 'Total Tests', 'Num Tests per Positive Case', 'Case Fatality Ratio']].head())

# Calculate the death rate for these countries
estimated_death_rate_percent = 100 * good_testing_df['Total Deaths'].sum() / good_testing_df['Total Cases'].sum()
print(f'\nDeath Rate only for "good testing countries" is {estimated_death_rate_percent:.2f}%') 