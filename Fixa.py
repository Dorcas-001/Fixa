import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
from PIL import Image
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
teal_color = '#009DAE'  # Teal green color code
green_EC = '#138024'
tangerine_color = '#E66C37'  # Tangerine orange color code
st.markdown(
    """
    <style>
    .main-title{
        color: #e66c37
        text_align: center;
        font_size: 3rem;
        font_wight: bold;
        margin_bottom=.5rem;
        text_shadow: 1px 1px 2px rgba(0,0,0.1);
    }
    .reportview-container {
        background-color: #013220;
        color: white;
    }
    .sidebar .sidebar-content {
        background-color: #013220;
        color: white;
    }
    .metric .metric-value {
        color: #009DAE;
    }
    .metric .mertic-title {
        color: #FFA500;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown('''
    <style>
        .main-title {
            color: #E66C37; /* Title color */
            text-align: center; /* Center align the title */
            font-size: 3rem; /* Title font size */
            font-weight: bold; /* Title font weight */
            margin-bottom: .5rem; /* Space below the title */
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1); /* Subtle text shadow */
        }
        div.block-container {
            padding-top: 2rem; /* Padding for main content */
        }
    </style>
''', unsafe_allow_html=True)
# Your Streamlit app content
st.markdown('<h1 class = "main-title">MEMBER DISTRIBUTION View</h1>', unsafe_allow_html=True)


# Define colors to match the image
color_palette = ["#006E7F", "#e66c37","#461b09","#f8a785", "#CC3636",  '#FFC288', '#EFB08C', '#FAD3CF']
# Loading the data

df = pd.read_excel('Experiment Insurance Form (Responses) (2).xlsx')


# Sidebar styling and logo
st.markdown("""
    <style>
    .sidebar .sidebar-content {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    .sidebar .sidebar-content h2 {
        color: #007BFF; /* Change this color to your preferred title color */
        font-size: 1.5em;
        margin-bottom: 20px;
        text-align: center;
    }
    .sidebar .sidebar-content .filter-title {
        color: #e66c37;
        font-size: 1.2em;
        font-weight: bold;
        margin-top: 20px;
        margin-bottom: 10px;
        text-align: center;
    }
    .sidebar .sidebar-content .filter-header {
        color: #e66c37; /* Change this color to your preferred header color */
        font-size: 2.5em;
        font-weight: bold;
        margin-top: 20px;
        margin-bottom: 20px;
        text-align: center;
    }
    .sidebar .sidebar-content .filter-multiselect {
        margin-bottom: 15px;
    }
    .sidebar .sidebar-content .logo {
        text-align: center;
        margin-bottom: 20px;
    }
    .sidebar .sidebar-content .logo img {
        max-width: 80%;
        height: auto;
        border-radius: 50%;
    }
            
    </style>
    """, unsafe_allow_html=True)


# Ensure the 'Start Date' column is in datetime format if needed
df["START DATE"] = pd.to_datetime(df["Date onboarded"], errors='coerce')


# Get minimum and maximum dates for the date input
startDate = df["START DATE"].min()
endDate = df["START DATE"].max()

# Define CSS for the styled date input boxes
st.markdown("""
    <style>
    .date-input-box {
        border-radius: 10px;
        text-align: left;
        margin: 5px;
        font-size: 1.2em;
        font-weight: bold;
    }
    .date-input-title {
        font-size: 1.2em;
        margin-bottom: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

# Create 2-column layout for date inputs
col1, col2 = st.columns(2)

# Function to display date input in styled boxes
def display_date_input(col, title, default_date, min_date, max_date):
    col.markdown(f"""
        <div class="date-input-box">
            <div class="date-input-title">{title}</div>
        </div>
        """, unsafe_allow_html=True)
    return col.date_input("", default_date, min_value=min_date, max_value=max_date)

# Display date inputs
with col1:
    date1 = pd.to_datetime(display_date_input(col1, "Start Date", startDate, startDate, endDate))

with col2:
    date2 = pd.to_datetime(display_date_input(col2, "End Date", endDate, startDate, endDate))

# Filter DataFrame based on the selected dates
df = df[(df["START DATE"] >= date1) & (df["START DATE"] <= date2)].copy()

# Define CSS for styling
st.markdown("""
    <style>
    .main-title {
        color: #E66C37;
        text-align: center;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: .5rem;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
    }
    .slider-box {
        border-radius: 10px;
        text-align: left;
        margin: 5px;
        font-size: 1.2em;
        font-weight: bold;
    }
    .slider-title {
        font-size: 1.2em;
        margin-bottom: 5px;
    }
    .custom-subheader {
        color: #E66C37;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
        padding: 10px;
        border-radius: 5px;
        display: inline-block;
    }
    .metric-box {
        padding: 10px;
        border-radius: 10px;
        text-align: center;
        margin: 10px;
        font-size: 1.2em;
        font-weight: bold;
        box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
        border: 1px solid #ddd;
    }
    .metric-title {
        color: #E66C37;
        font-size: 1.2em;
        margin-bottom: 10px;
    }
    .metric-value {
        color: #009DAE;
        font-size: 2em;
    }
    </style>
""", unsafe_allow_html=True)

# Function to extract min and max age
def extract_min_age(age_range):
    if 'and above' in age_range:
        return int(age_range.split()[0])
    else:
        return int(age_range.split('-')[0])

def extract_max_age(age_range):
    if 'and above' in age_range:
        return '56 and above'  # Standardize the string
    else:
        return int(age_range.split('-')[1])

df['Min Age'] = df['Worker age range'].apply(extract_min_age)
df['Max Age'] = df['Worker age range'].apply(extract_max_age)

min_age = df['Min Age'].min()
max_age = df[df['Max Age'] != '56 and above']['Max Age'].max()  # Get the max age excluding '56 and above'

# Slider for age range
age_range = st.slider("Select Age Range", min_age, max_age, (min_age, max_age))

# Display the selected age range with custom label for maximum value
selected_min_age = age_range[0]
selected_max_age = age_range[1]

if selected_max_age == max_age:
    selected_max_age_label = "56 and above"
else:
    selected_max_age_label = selected_max_age

st.write(f"{selected_min_age} - {selected_max_age_label}")

filtered_df = df


# Sidebar filters
st.sidebar.header('Filters')
# Convert date columns to datetime format
month_order = {
    "January": 1, "February": 2, "March": 3, "April": 4, 
    "May": 5, "June": 6, "July": 7, "August": 8, 
    "September": 9, "October": 10, "November": 11, "December": 12
}

# Year filter
df['Year'] = df['START DATE'].dt.year
df['Month'] = df['START DATE'].dt.strftime('%B')
sorted_months = sorted(df['Month'].dropna().unique(), key=lambda x: month_order[x])

year = st.sidebar.multiselect('Select Year', options=sorted(df['Year'].unique()))
month = st.sidebar.multiselect('Select Month', options=sorted_months)
educ = st.sidebar.multiselect('Select Educational Background', options=filtered_df['Educational Background'].unique())
status = st.sidebar.multiselect('Select Marital Status', options=filtered_df['Marital Status'].unique())
gender = st.sidebar.multiselect('Select Gender', options=filtered_df['Gender'].unique())
insurance = st.sidebar.multiselect('Select Insurance Interest', options=filtered_df['Workers’ Interest in Insurance Products'].unique())

# Apply sidebar filters
if year:
    filtered_df = filtered_df[filtered_df['Year'].isin(year)]
if month:
    filtered_df = filtered_df[filtered_df['Month'].isin(month)]
if educ:
    filtered_df = filtered_df[filtered_df['Plan'].isin(educ)]
if status:
    filtered_df = filtered_df[filtered_df['Status'].isin(status)]
if gender:
    filtered_df = filtered_df[filtered_df['Gender'].isin(gender)]
if insurance:
    filtered_df = filtered_df[filtered_df['Employer Group'].isin(insurance)]


# Determine the filter description
filter_description = ""
if year:
    filter_description += f"{', '.join(map(str, year))} "
if month:
    filter_description += f"{', '.join(map(str, month))} "
if educ:
    filter_description += f"{', '.join(map(str, educ))} "
if status:
    filter_description += f"{', '.join(map(str, status))} "
if gender:
    filter_description += f"{', '.join(map(str, gender))} "
if insurance:
    filter_description += f"{', '.join(insurance)} "
if not filter_description:
    filter_description = "All df"


if not filtered_df.empty:  

    # Create 4-column layout for metric cards
    col1, col2, col3 = st.columns(3)

    # Define CSS for the styled boxes
    st.markdown("""
        <style>
        .custom-subheader {
            color: #e66c37;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
            padding: 5px;
            border-radius: 5px;
            display: inline-block;
        }
        .metric-box {
            padding: 10px;
            border-radius: 10px;
            text-align: center;
            margin: 10px;
            font-size: 1.2em;
            font-weight: bold;
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
            border: 1px solid #ddd;
        }
        .metric-title {
            color: #e66c37; /* Change this color to your preferred title color */
            font-size: 0.9em;
            margin-bottom: 10px;
        }
        .metric-value {
            color: #009DAE;
            font-size: 1.2em;
        }
        </style>
        """, unsafe_allow_html=True)

    # Function to display metrics in styled boxes
    def display_metric(col, title, value):
        col.markdown(f"""
            <div class="metric-box">
                <div class="metric-title">{title}</div>
                <div class="metric-value">{value}</div>
            </div>
            """, unsafe_allow_html=True)

     # Calculate metrics
    scaling_factor = 1_000_000  # For millions
    scaled = 1_000
    total_part = len(filtered_df)
    total_dependents = filtered_df["Total Dependent"].sum()
    total_income = (filtered_df["Average Monthly Income"].sum())/scaling_factor
    total__child_dependents = filtered_df["Number of child dependents"].sum()
    average_dep = filtered_df["Number of child dependents"].mean()
    average_income = (filtered_df["Average Monthly Income"].mean())/scaled

    

    display_metric(col1, "Total Workers", total_part)
    display_metric(col2, "Total Income", f"{total_income:.1f}M")
    display_metric(col3, "Number of Child Dependents", f"{total__child_dependents:.0f}")
    display_metric(col1, "Total Dependents", f"{total_dependents:.0f}")
    display_metric(col2, "Average Dependent per Participant", f"{average_dep:.0f}")
    display_metric(col3, "Average Income per Participant", f"{average_income:.1f}K")

   
    # Sidebar styling and logo
    st.markdown("""
        <style>
        .sidebar .sidebar-content {
            background-color: #f0f2f6;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        .sidebar .sidebar-content h2 {
            color: #007BFF; /* Change this color to your preferred title color */
            font-size: 1.5em;
            margin-bottom: 20px;
            text-align: center;
        }
        .sidebar .sidebar-content .filter-title {
            color: #e66c37;
            font-size: 1.2em;
            font-weight: bold;
            margin-top: 20px;
            margin-bottom: 10px;
            text-align: center;
        }
        .sidebar .sidebar-content .filter-header {
            color: #e66c37; /* Change this color to your preferred header color */
            font-size: 2.5em;
            font-weight: bold;
            margin-top: 20px;
            margin-bottom: 20px;
            text-align: center;
        }
        .sidebar .sidebar-content .filter-multiselect {
            margin-bottom: 15px;
        }
        .sidebar .sidebar-content .logo {
            text-align: center;
            margin-bottom: 20px;
        }
        .sidebar .sidebar-content .logo img {
            max-width: 80%;
            height: auto;
            border-radius: 50%;
        }
                
        </style>
        """, unsafe_allow_html=True)

    custom_colors = ["#006E7F", "#e66c37", "#461b09", "#f8a785", "#CC3636"]

    cols1, cols2 = st.columns(2)

    # Group data by day and count visits
    daily_visits = filtered_df.groupby(filtered_df['Date onboarded'].dt.to_period('D')).size()
    daily_visits.index = daily_visits.index.to_timestamp()

    # Create a DataFrame for the daily visits
    daily_visits_df = daily_visits.reset_index()
    daily_visits_df.columns = ['Day', 'Number of Workforce']

    with cols1:
        st.markdown('<h3 class="custom-subheader">Number of Onboarded Workforce Over </h3>', unsafe_allow_html=True)

        # Create area chart for visits per day
        fig_area = go.Figure()

        fig_area.add_trace(go.Scatter(
            x=daily_visits_df['Day'],
            y=daily_visits_df['Number of Workforce'],
            fill='tozeroy',
            mode='lines',
            marker=dict(color='#009DAE'),
            line=dict(color='#009DAE'),
            name='Number of Employees'
        ))

        fig_area.update_layout(
            xaxis_title="Days of the Month",
            yaxis_title="Number of Workforce",
            font=dict(color='black'),
            width=1200, 
            height=600  
        )

        # Display the plot
        st.plotly_chart(fig_area, use_container_width=True)

 # Count the occurrences of each Status
    age_counts = df["Worker age range"].value_counts().reset_index()
    age_counts.columns = ["Age", "Count"]

    with cols2:
        # Display the header
        st.markdown('<h3 class="custom-subheader">Age Distribution of Workforce</h3>', unsafe_allow_html=True)

        # Create a donut chart
        fig = px.pie(age_counts, names="Age", values="Count", template="plotly_dark", color_discrete_sequence=custom_colors)
        fig.update_traces(textposition='inside', textinfo='value+percent')
        fig.update_layout(height=450, margin=dict(l=0, r=10, t=30, b=50))

        # Display the chart in Streamlit
        st.plotly_chart(fig, use_container_width=True)

    cls1, cls2 = st.columns(2)
# Count the occurrences of each Status
    gender_counts = df["Gender"].value_counts().reset_index()
    gender_counts.columns = ["Gender", "Count"]

    with cls1:
        # Display the header
        st.markdown('<h3 class="custom-subheader">Gender Distribution of Workforce</h3>', unsafe_allow_html=True)

        # Create a donut chart
        fig = px.pie(gender_counts, names="Gender", values="Count", hole=0.5, template="plotly_dark", color_discrete_sequence=custom_colors)
        fig.update_traces(textposition='inside', textinfo='value+percent')
        fig.update_layout(height=450, margin=dict(l=0, r=10, t=30, b=50))

        # Display the chart in Streamlit
        st.plotly_chart(fig, use_container_width=True)

# Count the occurrences of each Status
    status_counts = df["Marital Status"].value_counts().reset_index()
    status_counts.columns = ["Status", "Count"]

    with cls2:
        # Display the header
        st.markdown('<h3 class="custom-subheader">Marital Status of Workforce</h3>', unsafe_allow_html=True)

        # Create a donut chart
        fig = px.pie(status_counts, names="Status", values="Count", hole=0.5, template="plotly_dark", color_discrete_sequence=custom_colors)
        fig.update_traces(textposition='inside', textinfo='value+percent')
        fig.update_layout(height=450, margin=dict(l=0, r=10, t=30, b=50))

        # Display the chart in Streamlit
        st.plotly_chart(fig, use_container_width=True)

    # Group by month and educational background, then count the number of workers
    monthly_workers = df.groupby(['Month', 'Educational Background']).size().unstack().fillna(0)

    # Create the layout columns
    cls1, cls2 = st.columns(2)

    with cls1:
        fig_monthly_workers = go.Figure()


        for idx, education in enumerate(monthly_workers.columns):
            fig_monthly_workers.add_trace(go.Bar(
                x=monthly_workers.index,
                y=monthly_workers[education],
                name=education,
                textposition='inside',
                textfont=dict(color='white'),
                hoverinfo='x+y+name',
                marker_color=custom_colors[idx % len(custom_colors)]  # Cycle through custom colors
            ))

        # Set layout for the Workers chart
        fig_monthly_workers.update_layout(
            barmode='group',  # Grouped bar chart
            xaxis_title="Month",
            yaxis_title="Number of Workers",
            font=dict(color='Black'),
            xaxis=dict(title_font=dict(size=14), tickfont=dict(size=12)),
            yaxis=dict(title_font=dict(size=14), tickfont=dict(size=12)),
            margin=dict(l=0, r=0, t=30, b=50),
        )

        # Display the Workers chart in Streamlit
        st.markdown('<h3 class="custom-subheader">Educational Background of Workers Onboarded Monthly</h3>', unsafe_allow_html=True)
        st.plotly_chart(fig_monthly_workers, use_container_width=True)


    monthly_workers = df.groupby(['Month', 'Skilled or Unskilled worker']).size().unstack().fillna(0)

    custom_colors_re = ["#006E7F", "#e66c37", "#f8a785"]
    with cls2:
        fig_monthly_workers = go.Figure()


        for idx, education in enumerate(monthly_workers.columns):
            fig_monthly_workers.add_trace(go.Bar(
                x=monthly_workers.index,
                y=monthly_workers[education],
                name=education,
                textposition='inside',
                textfont=dict(color='white'),
                hoverinfo='x+y+name',
                marker_color=custom_colors_re[idx % len(custom_colors_re)]  # Cycle through custom colors
            ))

        # Set layout for the Workers chart
        fig_monthly_workers.update_layout(
            barmode='group',  # Grouped bar chart
            xaxis_title="Month",
            yaxis_title="Number of Workers",
            font=dict(color='Black'),
            xaxis=dict(title_font=dict(size=14), tickfont=dict(size=12)),
            yaxis=dict(title_font=dict(size=14), tickfont=dict(size=12)),
            margin=dict(l=0, r=0, t=30, b=50),
        )

        # Display the Workers chart in Streamlit
        st.markdown('<h3 class="custom-subheader">Type of Workers Onboarded Monthly</h3>', unsafe_allow_html=True)
        st.plotly_chart(fig_monthly_workers, use_container_width=True)

    clus1, clus2 = st.columns(2)
# Count the occurrences of each Status
    gender_counts = df["Spouse dependents"].value_counts().reset_index()
    gender_counts.columns = ["Spouse", "Count"]

    with clus1:
        # Display the header
        st.markdown('<h3 class="custom-subheader">Workers with Spouses</h3>', unsafe_allow_html=True)

        # Create a donut chart
        fig = px.pie(gender_counts, names="Spouse", values="Count", template="plotly_dark", color_discrete_sequence=custom_colors)
        fig.update_traces(textposition='inside', textinfo='value+percent')
        fig.update_layout(height=450, margin=dict(l=0, r=10, t=30, b=50))

        # Display the chart in Streamlit
        st.plotly_chart(fig, use_container_width=True)

    # Count the occurrences of each Status
    spouse_gender_counts = df["Dependents Gender"].value_counts().reset_index()
    spouse_gender_counts.columns = ["Status", "Count"]

    with clus2:
        # Display the header
        st.markdown('<h3 class="custom-subheader">Gender Distribution of Spouses</h3>', unsafe_allow_html=True)

        # Create a donut chart
        fig = px.pie(spouse_gender_counts, names="Status", values="Count", hole=0.5, template="plotly_dark", color_discrete_sequence=custom_colors)
        fig.update_traces(textposition='inside', textinfo='value+percent')
        fig.update_layout(height=450, margin=dict(l=0, r=10, t=30, b=50))

        # Display the chart in Streamlit
        st.plotly_chart(fig, use_container_width=True)

    # Group data by "Start Date Month" and "Client Segment" and sum the Total Lives
    spouse_age_range = filtered_df.groupby(['Spouse dependent age range', 'Child dependent age range'])['Number of child dependents'].sum().unstack().fillna(0)

    # Create the layout columns
    cls1, cls2 = st.columns(2)

    with cls1:
        fig_monthly_premium = go.Figure()

        for idx, Client_Segment in enumerate(spouse_age_range.columns):
            fig_monthly_premium.add_trace(go.Bar(
                x=spouse_age_range.index,
                y=spouse_age_range[Client_Segment],
                name=Client_Segment,
                textposition='inside',
                textfont=dict(color='white'),
                hoverinfo='x+y+name',
                marker_color=custom_colors[idx % len(custom_colors)]  # Cycle through custom colors
            ))

        # Set layout for the Total Premium chart
        fig_monthly_premium.update_layout(
            barmode='group',  # Grouped bar chart
            xaxis_title="Spouse Dependent Age Range",
            yaxis_title="Number of Workers",
            font=dict(color='Black'),
            xaxis=dict(title_font=dict(size=14), tickfont=dict(size=12)),
            yaxis=dict(title_font=dict(size=14), tickfont=dict(size=12)),
            margin=dict(l=0, r=0, t=30, b=50),
        )

        # Display the Total Premium chart in Streamlit
        st.markdown('<h2 class="custom-subheader">Age Range Distribution of Child Dependents by Spouse</h2>', unsafe_allow_html=True)
        st.plotly_chart(fig_monthly_premium, use_container_width=True)

    # Create a pivot table to get the sum of Total Dependent for each Spouse Age Range and Spouse dependents
    spouse_dep = filtered_df.pivot_table(
        index='Spouse dependent age range',
        columns='Spouse dependents',
        values='Number of child dependents',
        aggfunc='sum',
        fill_value=0
    )

    with cls2:
        # Initialize the figure
        fig_monthly_premium = go.Figure()

        # Create the bar chart
        for idx, Client_Segment in enumerate(spouse_dep.columns):
            fig_monthly_premium.add_trace(go.Bar(
                x=spouse_dep.index,
                y=spouse_dep[Client_Segment],
                name=Client_Segment,
                textposition='inside',
                textfont=dict(color='white'),
                hoverinfo='x+y+name',
                marker_color=custom_colors[idx % len(custom_colors)]  # Cycle through custom colors
            ))

        # Set layout for the Total Premium chart
        fig_monthly_premium.update_layout(
            barmode='group',  # Grouped bar chart
            xaxis_title="Spouse Dependent Age Range",
            yaxis_title="Total Dependents",
            font=dict(color='Black'),
            xaxis=dict(title_font=dict(size=14), tickfont=dict(size=12)),
            yaxis=dict(title_font=dict(size=14), tickfont=dict(size=12)),
            margin=dict(l=0, r=0, t=30, b=50),
        )

        # Display the Total Premium chart in Streamlit
        st.markdown('<h3 class="custom-subheader">Number of Child Dependents by Spouse</h3>', unsafe_allow_html=True)
        st.plotly_chart(fig_monthly_premium, use_container_width=True)

    clus1, clus2 = st.columns(2)
# Count the occurrences of each Status
    em_counts = df["Are the dependents employed or financially dependent on the worker? "].value_counts().reset_index()
    em_counts.columns = ["dependents", "Count"]

    with clus1:
        # Display the header
        st.markdown('<h3 class="custom-subheader">Employment Status of Dependent</h3>', unsafe_allow_html=True)

        # Create a donut chart
        fig = px.pie(em_counts, names="dependents", values="Count", template="plotly_dark", color_discrete_sequence=custom_colors)
        fig.update_traces(textposition='inside', textinfo='value+percent')
        fig.update_layout(height=450, margin=dict(l=0, r=10, t=30, b=50))

        # Display the chart in Streamlit
        st.plotly_chart(fig, use_container_width=True)

    # Count the occurrences of each Status
    spouse_gender_counts = df["Do the dependents live with the worker, or are they located elsewhere?  "].value_counts().reset_index()
    spouse_gender_counts.columns = ["Status", "Count"]

    with clus2:
        # Display the header
        st.markdown('<h3 class="custom-subheader">Living Status of Dependents</h3>', unsafe_allow_html=True)

        # Create a donut chart
        fig = px.pie(spouse_gender_counts, names="Status", values="Count", hole=0.5, template="plotly_dark", color_discrete_sequence=custom_colors)
        fig.update_traces(textposition='inside', textinfo='value+percent')
        fig.update_layout(height=450, margin=dict(l=0, r=10, t=30, b=50))

        # Display the chart in Streamlit
        st.plotly_chart(fig, use_container_width=True)


    clus1, clus2 = st.columns(2)
    # Count the occurrences of each combination of living status and employment status
    combined_counts = df.groupby(['Do the dependents live with the worker, or are they located elsewhere?  ', 'Are the dependents employed or financially dependent on the worker? ']).size().reset_index(name='Count')

    with clus1:
        # Initialize the figure
        fig_combined_status = go.Figure()

        # Create the bar chart
        for idx, employment_status in enumerate(combined_counts['Are the dependents employed or financially dependent on the worker? '].unique()):
            filtered_data = combined_counts[combined_counts['Are the dependents employed or financially dependent on the worker? '] == employment_status]
            fig_combined_status.add_trace(go.Bar(
                x=filtered_data['Do the dependents live with the worker, or are they located elsewhere?  '],
                y=filtered_data['Count'],
                name=employment_status,
                textposition='inside',
                textfont=dict(color='white'),
                hoverinfo='x+y+name',
                marker_color=custom_colors[idx % len(custom_colors)]  # Cycle through custom colors
            ))

        # Set layout for the combined status chart
        fig_combined_status.update_layout(
            barmode='group',  # Grouped bar chart
            xaxis_title="Living Status",
            yaxis_title="Count",
            font=dict(color='Black'),
            xaxis=dict(title_font=dict(size=14), tickfont=dict(size=12)),
            yaxis=dict(title_font=dict(size=14), tickfont=dict(size=12)),
            margin=dict(l=0, r=0, t=30, b=50),
        )

        # Display the combined status chart in Streamlit
        st.markdown('<h3 class="custom-subheader">Dependents: Employment vs. Living Status</h3>', unsafe_allow_html=True)
        st.plotly_chart(fig_combined_status, use_container_width=True)

    # Count the occurrences of each Status
    spouse_gender_counts = df["Have the workers had insurance coverage before? "].value_counts().reset_index()
    spouse_gender_counts.columns = ["Status", "Count"]

    with clus2:
        # Display the header
        st.markdown('<h3 class="custom-subheader">Workers with Previous Insurance Coverage</h3>', unsafe_allow_html=True)

        # Create a donut chart
        fig = px.pie(spouse_gender_counts, names="Status", values="Count", hole=0.5, template="plotly_dark", color_discrete_sequence=custom_colors)
        fig.update_traces(textposition='inside', textinfo='value+percent')
        fig.update_layout(height=450, margin=dict(l=0, r=10, t=30, b=50))

        # Display the chart in Streamlit
        st.plotly_chart(fig, use_container_width=True)
