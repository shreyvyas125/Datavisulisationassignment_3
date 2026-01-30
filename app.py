import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Washington D.C. Bike Rental Analysis", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv('train.csv') # [cite: 6]
    df['datetime'] = pd.to_datetime(df['datetime']) # [cite: 26]
    df['year'] = df['datetime'].dt.year # [cite: 29]
    df['month'] = df['datetime'].dt.month
    df['hour'] = df['datetime'].dt.hour
    
    # Task 4: Rename seasons [cite: 30]
    season_names = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
    df['season'] = df['season'].map(season_names)
    
    # Task 11: Day Period binning [cite: 42, 43]
    def get_period(h):
        if 0 <= h < 6: return 'Night'
        elif 6 <= h < 12: return 'Morning'
        elif 12 <= h < 18: return 'Afternoon'
        else: return 'Evening'
    df['day_period'] = df['hour'].apply(get_period)
    return df

df = load_data()

# 2. Interactive Widgets (Assignment III: At least 3 widgets) [cite: 65]
st.sidebar.header("Dashboard Filters")
selected_year = st.sidebar.multiselect("Select Year", options=[2011, 2012], default=[2011, 2012])
selected_seasons = st.sidebar.multiselect("Select Season", options=df['season'].unique(), default=df['season'].unique())
day_type = st.sidebar.radio("Day Type", options=["All", "Working Day", "Weekend/Holiday"])

# Filter logic
filtered_df = df[(df['year'].isin(selected_year)) & (df['season'].isin(selected_seasons))]
if day_type == "Working Day":
    filtered_df = filtered_df[filtered_df['workingday'] == 1]
elif day_type == "Weekend/Holiday":
    filtered_df = filtered_df[filtered_df['workingday'] == 0]

# 3. Visualizations (Assignment II Tasks) [cite: 65]
st.title("🚲 Washington D.C. Bike Rental Dashboard")

# Row 1: Trends
col1, col2 = st.columns(2)
with col1:
    st.subheader("Hourly Rental Trends (Task 7)") # [cite: 56]
    fig1, ax1 = plt.subplots()
    sns.lineplot(data=filtered_df, x='hour', y='count', ax=ax1)
    st.pyplot(fig1)

with col2:
    st.subheader("Weather Impact (Task 6)") # [cite: 54]
    fig2, ax2 = plt.subplots()
    sns.barplot(data=filtered_df, x='weather', y='count', ax=ax2)
    st.pyplot(fig2)

# Row 2: Distributions & Correlations
col3, col4 = st.columns(2)
with col3:
    st.subheader("Rentals by Day Period (Task 10)") # [cite: 60]
    fig3, ax3 = plt.subplots()
    sns.boxplot(data=filtered_df, x='day_period', y='count', ax=ax3)
    st.pyplot(fig3)

with col4:
    st.subheader("Correlation Heatmap (Task 11)") # [cite: 63]
    fig4, ax4 = plt.subplots()
    numeric_cols = filtered_df[['temp', 'atemp', 'humidity', 'windspeed', 'count']]
    sns.heatmap(numeric_cols.corr(), annot=True, cmap='coolwarm', ax=ax4)
    st.pyplot(fig4)