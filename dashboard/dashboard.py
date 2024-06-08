import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='whitegrid')

def create_monthly_season_count(df):
    all_hour_df = df.groupby(by=['month', 'season']).agg({
        'count': 'sum'
        }).reset_index()
    return all_hour_df

def create_total_months(df):
    df['year'] = df['date'].dt.year
    total_months = df.groupby(['year', 'month'])[['casual', 'registered', 'count']].sum().reset_index()
    return total_months

def create_monthly_season(df):
    monthly_season = df.groupby(['month', 'season']).agg({
        'casual': 'sum',
        'registered': 'sum',
        'count': 'sum'
        }).reset_index()
    return monthly_season

# Load Cleaned Data
all_df = pd.read_csv("hour_data_clean.csv")

datetime_columns = ['date']
all_df.sort_values(by='date', inplace=True)
all_df.reset_index(drop=True, inplace=True)

for columns in datetime_columns:
    all_df[columns] = pd.to_datetime(all_df[columns])

max_date = all_df['date'].max()
min_date = all_df['date'].min()

with st.sidebar:
    # Logo Company
    # st.image("")

    # Take start_date & end_date from date_input
    start_date, end_date = st.date_input(
        label="Susceptible Time", min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

    st.markdown("""
                <style>
                .justified-text {
                    text-align: justify;
                }
                </style>
                
                <p class="justified-text">
                Bike sharing systems are new generation of traditional bike rentals where whole process from membership, rental and return 
                back has become automatic. Through these systems, user is able to easily rent a bike from a particular position and return 
                back at another position. Currently, there are about over 500 bike-sharing programs around the world which is composed of 
                over 500 thousands bicycles. Today, there exists great interest in these systems due to their important role in traffic, 
                environmental and health issues.</p>
                """, unsafe_allow_html=True)

main_df = all_df[(all_df['date'] >= pd.Timestamp(start_date)) & (all_df['date'] <= pd.Timestamp(end_date))]

# Prepare DataFrame
monthly_season_count = create_monthly_season_count(main_df)
monthly_yearly_count = create_total_months(main_df)
correlation_users_count = create_monthly_season(main_df)

# Display Table Data
st.header("Table of Data")

col1, col2, col3 = st.columns(3)
with col1:
    total_rentals = main_df['count'].sum()
    st.metric("Total User Rentals", value=total_rentals)

with col2:
    total_casuals = main_df['casual'].sum()
    st.metric("Total User Casual", value=total_casuals)

with col3:
    total_casuals = main_df['registered'].sum()
    st.metric("Total User Registered", value=total_casuals)

st.write(main_df)

# Display Visualization
st.header("E-Bike Rental Chart")
fig, ax = plt.subplots(figsize=(20, 10))
data=monthly_season_count.sort_values(by=['month', 'count'], ascending=[True, False])

fig, ax = plt.subplots(figsize=(20, 10))
months = data['month'].unique()
counts = data['count'].unique()
seasons = data['season'].unique()

# Membuat barchart menggunakan Matplotlib
for season in seasons:
    season_data = data[data['season'] == season]
    ax.bar(season_data['month'], season_data['count'], label=season)

ax.set_title("Total Rental Bikes per Months and Season", loc='center', fontsize=30)
ax.set_xlabel('Month', fontsize=20)
ax.set_ylabel('Total Rental Bikes', fontsize=20)  
ax.set_xticks(range(1, 13))
ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], fontsize=20)
ax.tick_params(axis='x', labelsize=20)
ax.tick_params(axis='y', labelsize=20)
ax.legend(title='Season', fontsize=15, title_fontsize='13')
st.pyplot(fig)

st.markdown("""
<p>The data above is the result of aggregating the number of bicycle rentals based on month and season. Presentation results of total bicycle rentals in a particular month during the corresponding season. The following is a more detailed explanation:

<ol>
<li>January (Winter Season): There were 134,933 bicycle rentals this month during the winter season.</li>
<li>February (Winter Season): The number of loans increased to 151,352 in February during the winter season.</li>
<li>March (Spring): Bicycle rentals continued to increase to 228,920 in March during spring.</li>
<li>April (Spring): The number of loans further increased to 269,094 in April during the spring season.</li>
<li>May (Spring): The peak number of loans occurred in May with 331,686 loans during the spring.</li>
<li>June (Summer Season): Although down from May, the number of loans remained high, reaching 346,342 loans during the summer.</li>
<li>July (Summer Season): The number of bicycle rentals in July decreased slightly to 344,948 during the summer.</li>
<li>August (Summer Season): Bicycle lending remained high in August with 351,194 borrowings during the summer.</li>
<li>September (Fall Season): The number of loans did not change significantly, reaching 345,991 in September during the fall season.</li>
<li>October (Fall Season): Borrowings decreased slightly to 322,352 in October during the fall season.</li>
<li>November (Fall Season): The number of loans continued to decline to 254,831 in November during the fall season.</li>
<li>December (Winter Season): The number of re-borrowings increased to 211,036 in December during the winter season.</li>
</ol>

This data provides results in the form of visual and quantitative data on the seasonal pattern of bicycle rentals each year. Apart from that, there are significant differences between months and seasons. Judging from these visual results, bicycle rental provides important information regarding the renter's activities in each season.
</p>""",  unsafe_allow_html=True)

fig, ax = plt.subplots(figsize=(20, 10))
sns.lineplot(
    x='month',
    y='count',
    hue='year',
    data=monthly_yearly_count,
    markers=True,
    palette='tab10',
    ax=ax
)

ax.set_title("Total Rental Bikes per Months and Season", loc='center', fontsize=30)
ax.set_xlabel('Month', fontsize=20)
ax.set_ylabel('Total Rental Bikes', fontsize=20)  
ax.set_xticks(range(1, 13))
ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], fontsize=20)
ax.tick_params(axis='x', labelsize=20)
ax.tick_params(axis='y', labelsize=20)
ax.legend(title='Year', fontsize=15, title_fontsize='13')
st.pyplot(fig)

st.markdown("""
<p>There is a trend pattern of bicycle rental users increasing overall in 2012 compared to 2011. This can be seen from the trend line which shows an increase every month.

The following are several important points regarding the trend pattern of bicycle rental users in 2011 and 2012:

Rental User Improvements:
<ol>
<li>Overall, the number of bicycle rentals in 2012 was higher compared to 2011. This shows that more people are choosing to rent bicycles in 2012.
<li>The highest increase in the number of bicycle rentals occurred in July and August, namely during the summer season. This is likely because sunny and warm weather encourages people to do more outdoor activities, including cycling.
<li>An increase in the number of bicycle rentals also occurs in April and May, namely during spring. This is likely because people start cycling more often as the weather starts to warm up.
</ol>

</p>""",  unsafe_allow_html=True)

pivot_table = monthly_season_count.pivot(index='month', columns='season', values='count')
correlation = pivot_table.corr()

fig, ax = plt.subplots(figsize=(5, 5))
sns.heatmap(correlation,
            annot=True,
            cmap='viridis',
            linewidths=0.5,
            vmin=0,
            vmax=1)
ax.set_title("Table of Correlations")
ax.set_xlabel(None)
ax.set_ylabel(None)
st.pyplot(fig)

fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(20, 5))
sns.scatterplot(data=correlation_users_count, 
                x='casual', y='registered', 
                hue='season', 
                style='season', 
                palette='Set2', 
                s=100, 
                ax=ax[0])
ax[0].set_xlabel('Casual')
ax[0].set_ylabel('Registered')
ax[0].legend(title='Season')

sns.scatterplot(data=correlation_users_count, 
                x='casual', y='count', 
                hue='season', 
                style='season', 
                palette='Set2', 
                s=100, 
                ax=ax[1])
ax[1].set_xlabel('Casual')
ax[1].set_ylabel('Count')
ax[1].legend(title='Season')

sns.scatterplot(data=correlation_users_count, 
                x='count', y='registered', 
                hue='season', 
                style='season', 
                palette='Set2', 
                s=100, 
                ax=ax[2])
ax[2].set_xlabel('Count')
ax[2].set_ylabel('Registered')
ax[2].legend(title='Season')

st.pyplot(fig)

st.markdown("""
<p>This correlation is measured using the Pearson correlation coefficient, whose value can range between -1 and 1. A positive correlation coefficient value indicates a positive correlation, while a negative value indicates a negative correlation.

Based on the figure, the correlation coefficient between the number of bicycle users and the season is 0.95. This value shows a very strong correlation between the two variables.

Explanation:</P>

<ol>
<li>Summer: The number of bicycle users is highest in the summer. This is likely because sunny and warm weather encourages people to cycle more often.
<li>Spring: The number of bicycle users is still high in spring. People may start cycling more often as the weather starts to warm up.
<li>Fall: The number of bicycle users decreases in the fall. This is probably because the weather is starting to get cold and rainy.
<li>Winter: The number of bicycle users is lowest in winter. People may not want to bike in cold, snowy weather.
</ol>

<ol>
<li>Casual Bicycle Users: This graph shows that the number of Casual bicycle users is highest in summer and lowest in winter.
<li>Casual x Registered Bicycle Users: This graph shows that the number of Casual Registered bicycle users is highest in summer and lowest in winter.
<li>Registered Bicycle Users: This graph shows that the number of Registered bicycle users is highest in summer and lowest in winter.
</ol>

<p>The figure shows that there is a very strong correlation between the number of bicycle users and the season. The number of bicycle users is highest in summer and lowest in winter. This is likely due to the weather affecting people's desire to cycle.</p>""",  unsafe_allow_html=True)

st.caption("Copyright © Tomy Ivan Sugiharto 2024")
