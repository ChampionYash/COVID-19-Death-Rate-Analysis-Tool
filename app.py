import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import altair as alt

# Set page title and favicon
st.set_page_config(
    page_title="COVID-19 Death Rate Analysis",
    layout="wide"
)

# Header
st.title("COVID-19 Death Rate Analysis")
st.markdown("Analyzing the relationship between testing quality and reported death rates")

# Load data
@st.cache_data
def load_data():
    return pd.read_csv('worldometer_snapshots_April18_to_May18.csv')

# Load data with a progress indicator
with st.spinner('Loading data...'):
    worldometer_df = load_data()

# Sidebar filters
st.sidebar.header("Filters")

# Date filter
available_dates = sorted(worldometer_df['Date'].unique().tolist())
selected_date = st.sidebar.selectbox(
    "Select Date", 
    available_dates,
    index=len(available_dates)-1  # Default to the last date
)

# Case threshold filter
min_cases_threshold = st.sidebar.slider("Minimum Cases Threshold", 
                                       min_value=100, 
                                       max_value=10000, 
                                       value=1000,
                                       step=100)

# Testing quality threshold filter
testing_quality_threshold = st.sidebar.slider("Testing Quality Threshold (tests per positive case)", 
                                            min_value=5, 
                                            max_value=100, 
                                            value=50,
                                            step=5)

# Filter data based on selected date
date_df = worldometer_df.loc[worldometer_df['Date'] == selected_date, :].reset_index(drop=True)

# Main content area
st.header(f"Data for {selected_date}")

# Display raw data if checkbox is selected
if st.checkbox("Show raw data"):
    st.dataframe(date_df)

# Calculate death rate
date_df['Case Fatality Ratio'] = date_df['Total Deaths'] / date_df['Total Cases']
date_df['Num Tests per Positive Case'] = date_df['Total Tests'] / date_df['Total Cases']

# Filter countries by case threshold
filtered_df = date_df.loc[date_df['Total Cases'] > min_cases_threshold, :].copy()
st.write(f"Countries with more than {min_cases_threshold} cases: {len(filtered_df)}")

# Create two columns for charts
col1, col2 = st.columns(2)

with col1:
    st.subheader("Death Rate Histogram")
    
    # Create histogram using matplotlib
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(100 * np.array(filtered_df['Case Fatality Ratio']), bins=np.arange(35))
    ax.set_xlabel('Death Rate (%)', fontsize=14)
    ax.set_ylabel('Number of Countries', fontsize=14)
    ax.set_title('Histogram of Death Rates', fontsize=16)
    st.pyplot(fig)

with col2:
    st.subheader("Testing Quality vs Death Rate")
    
    # Calculate parameters for scatter plot
    x_axis_limit = 80
    
    chart_df = filtered_df.copy()
    chart_df['Death Rate (%)'] = 100 * chart_df['Case Fatality Ratio']
    chart_df['Tests Per Case'] = chart_df['Num Tests per Positive Case'].copy()
    chart_df.loc[chart_df['Tests Per Case'] > x_axis_limit, 'Tests Per Case'] = x_axis_limit
    chart_df['log_population'] = np.log(1 + chart_df['Population'])
    chart_df['log_deaths'] = np.log10(1 + chart_df['Total Deaths'])
    
    # Create scatter plot using Altair
    scatter = alt.Chart(chart_df).mark_circle().encode(
        x=alt.X('Tests Per Case', title='Number of Tests per Positive Case'),
        y=alt.Y('Death Rate (%)', scale=alt.Scale(domain=[-0.2, 17])),
        size=alt.Size('log_population', legend=None),
        color=alt.Color('log_deaths', legend=None),
        tooltip=['Country', 'Death Rate (%)', 'Tests Per Case', 'Total Cases', 'Total Deaths']
    ).properties(
        height=400
    ).interactive()
    
    # Add country labels
    text = alt.Chart(chart_df).mark_text(
        align='left',
        baseline='middle',
        dx=7,
        fontSize=10
    ).encode(
        x='Tests Per Case',
        y='Death Rate (%)',
        text='Country'
    )
    
    st.altair_chart(scatter + text, use_container_width=True)

# Good testing countries section
st.header("Analysis of Countries with Good Testing")
good_testing_df = filtered_df.loc[filtered_df['Num Tests per Positive Case'] > testing_quality_threshold, :].copy()

st.write(f"Countries with testing quality > {testing_quality_threshold} tests per positive case: {len(good_testing_df)}")

# Display table of good testing countries
if not good_testing_df.empty:
    st.dataframe(good_testing_df[['Country', 'Total Cases', 'Total Deaths', 'Total Tests', 
                               'Num Tests per Positive Case', 'Case Fatality Ratio']]
                .sort_values(by='Num Tests per Positive Case', ascending=False)
                .reset_index(drop=True)
                .style.format({
                    'Case Fatality Ratio': '{:.4f}',
                    'Num Tests per Positive Case': '{:.2f}'
                }))
    
    # Calculate the estimated death rate for good testing countries
    if good_testing_df['Total Cases'].sum() > 0:  # Avoid division by zero
        estimated_death_rate = 100 * good_testing_df['Total Deaths'].sum() / good_testing_df['Total Cases'].sum()
        
        st.metric(
            label="Estimated COVID-19 Death Rate (countries with good testing)", 
            value=f"{estimated_death_rate:.2f}%"
        )
        
        st.markdown("""
        ### Conclusion
        
        This analysis suggests that differences in testing strategies significantly impact the reported death rates across countries.
        Countries with better testing tend to have more consistent and lower death rates.
        """)
else:
    st.write("No countries meet the selected testing quality threshold. Try adjusting the filters.")

# Add footer with data source information
st.markdown("---")
st.markdown("Data source: Worldometer COVID-19 data from April 18 to May 18, 2020") 