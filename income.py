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
st.markdown('<h2 class = "main-title">WORKFORCE INCOME VIEW</h2>', unsafe_allow_html=True)


# Define colors to match the image
custom_colors = ["#006E7F", "#e66c37","#461b09","#f8a785", "#CC3636",  '#FFC288', '#EFB08C', '#FAD3CF']
# Loading the data

df = pd.read_excel('Experiment Insurance Form (Responses) (2).xlsx')
# Ensure the 'Date' column is in datetime format if needed
df["Date"] = pd.to_datetime(df["Date onboarded"])

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


# Get minimum and maximum dates for the date input
startDate = df["Date"].min()
endDate = df["Date"].max()


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
def display_date_input(col, title, default_date, min_date, max_date, key):
    col.markdown(f"""
        <div class="date-input-box">
            <div class="date-input-title">{title}</div>
        </div>
        """, unsafe_allow_html=True)
    return col.date_input("", default_date, min_value=min_date, max_value=max_date, key=key)

# Display date inputs
with col1:
    date1 = pd.to_datetime(display_date_input(col1, "Start Date", startDate, startDate, endDate, key="start_date"))

with col2:
    date2 = pd.to_datetime(display_date_input(col2, "End Date", endDate, startDate, endDate, key="end_date"))


# Filter DataFrame based on the selected dates
df_filtered = df[(df["Date"] >= date1) & (df["Date"] <= date2)].copy()


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
df['Year'] = df['Date'].dt.year
df['Month'] = df['Date'].dt.strftime('%B')
sorted_months = sorted(df['Month'].dropna().unique(), key=lambda x: month_order[x])

year = st.sidebar.multiselect('Select Year', options=sorted(df['Year'].unique()))
month = st.sidebar.multiselect('Select Month', options=sorted_months)
educ = st.sidebar.multiselect('Select Educational Background', options=filtered_df['Educational Background'].unique())
status = st.sidebar.multiselect('Select Marital Status', options=filtered_df['Marital Status'].unique())
gender = st.sidebar.multiselect('Select Gender', options=filtered_df['Gender'].unique())
insurance = st.sidebar.multiselect('Select Insurance Interest', options=filtered_df['Workers Interest in Insurance Products'].unique())

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

if not filter_description:
    filter_description = "All df"


if not filtered_df.empty:  

    # Create 4-column layout for metric cards
    col1, col2, col3, col4 = st.columns(4)

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
    pre_insurance = len(filtered_df[filtered_df['Have the workers had insurance coverage before?'] == 'Previously Insurred'])
    percent_pre = (pre_insurance/total_part)*100
    

    display_metric(col1, "Total Workers", total_part)
    display_metric(col2, "Total Income", f"{total_income:.1f}M")
    display_metric(col3, "Workers with Previous Insurance", f"{percent_pre:.1f} %")
    display_metric(col4, "Average Income per Participant", f"{average_income:.1f}K")


   
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

# Count the occurrences of each Status
    insurance_counts = df["Monthly Income Range"].value_counts().reset_index()
    insurance_counts.columns = ["insurrance", "Count"]

    with cols1:
        # Display the header
        st.markdown('<h3 class="custom-subheader">Workers Income Range</h3>', unsafe_allow_html=True)

        # Create a donut chart
        fig = px.pie(insurance_counts, names="insurrance", values="Count", hole=0.5, template="plotly_dark", color_discrete_sequence=custom_colors)
        fig.update_traces(textposition='inside', textinfo='value+percent')
        fig.update_layout(height=450, margin=dict(l=0, r=10, t=30, b=50))

        # Display the chart in Streamlit
        st.plotly_chart(fig, use_container_width=True)


    # Group data by 'Worker age range' and 'Educational Background' and calculate the average income
    grouped_df = df.groupby(['Worker age range', 'Educational Background'])['Average Monthly Income'].mean().unstack().fillna(0)

    # Format the average income to one decimal place
    grouped_df = grouped_df.applymap(lambda x: round(x, 1))


    with cols2:
        fig_income_age_edu = go.Figure()

        # Add a bar trace for each educational background
        for idx, edu_background in enumerate(grouped_df.columns):
            fig_income_age_edu.add_trace(go.Bar(
                x=grouped_df.index,
                y=grouped_df[edu_background],
                name=edu_background,
                text=grouped_df[edu_background].apply(lambda x: f'{x:.1f}'),
                textposition='inside',
                textfont=dict(color='white'),
                hoverinfo='x+y+name',
                marker_color=custom_colors[idx % len(custom_colors)]  # Cycle through custom colors
            ))

        # Set layout for the Income vs Age Range and Educational Background chart
        fig_income_age_edu.update_layout(
            xaxis_title="Worker Age Range",
            yaxis_title="Average Monthly Income",
            barmode='group',  # Group bars together
            font=dict(color='Black'),
            xaxis=dict(title_font=dict(size=14), tickfont=dict(size=12)),
            yaxis=dict(title_font=dict(size=12), tickfont=dict(size=12)),
            margin=dict(l=0, r=0, t=30, b=50),
        )

        # Display the Income vs Age Range and Educational Background chart in Streamlit
        st.markdown('<h3 class="custom-subheader">Average Monthly Income by Worker Age Range and Educational Background</h3>', unsafe_allow_html=True)
        st.plotly_chart(fig_income_age_edu, use_container_width=True)
        
    cols1, cols2 = st.columns(2)

    # Group data by 'Worker age range' and 'Gender' and calculate the average income
    grouped_df = df.groupby(['Worker age range', 'Gender'])['Average Monthly Income'].mean().unstack().fillna(0)

    # Format the average income to one decimal place
    grouped_df = grouped_df.applymap(lambda x: round(x, 1))

    with cols1:
        fig_income_gender_age = go.Figure()

        # Add a bar trace for each gender
        for idx, gender in enumerate(grouped_df.columns):
            fig_income_gender_age.add_trace(go.Bar(
                x=grouped_df.index,
                y=grouped_df[gender],
                name=gender,
                text=grouped_df[gender].apply(lambda x: f'{x:.1f}'),
                textposition='inside',
                textfont=dict(color='white'),
                hoverinfo='x+y+name',
                marker_color=custom_colors[idx % len(custom_colors)]  # Cycle through custom colors
            ))

        # Set layout for the Income vs Gender and Age Range chart
        fig_income_gender_age.update_layout(
            xaxis_title="Worker Age Range",
            yaxis_title="Average Monthly Income",
            barmode='group',  # Group bars together
            font=dict(color='Black'),
            xaxis=dict(title_font=dict(size=14), tickfont=dict(size=12)),
            yaxis=dict(title_font=dict(size=12), tickfont=dict(size=12)),
            margin=dict(l=0, r=0, t=30, b=50),
        )

        # Display the Income vs Gender and Age Range chart in Streamlit
        st.markdown('<h3 class="custom-subheader">Average Monthly Income by Gender and Worker Age Range</h3>', unsafe_allow_html=True)
        st.plotly_chart(fig_income_gender_age, use_container_width=True)


    # Group data by 'Worker age range' and 'Skilled or Unskilled worker' and calculate the average income
    grouped_df = df.groupby(['Worker age range', 'Skilled or Unskilled worker'])['Average Monthly Income'].mean().unstack().fillna(0)

    # Format the average income to one decimal place
    grouped_df = grouped_df.applymap(lambda x: round(x, 1))

    with cols2:
        fig_income_skill_age = go.Figure()

        # Add a bar trace for each worker type
        for idx, worker_type in enumerate(grouped_df.columns):
            fig_income_skill_age.add_trace(go.Bar(
                x=grouped_df.index,
                y=grouped_df[worker_type],
                name=worker_type,
                text=grouped_df[worker_type].apply(lambda x: f'{x:.1f}'),
                textposition='inside',
                textfont=dict(color='white'),
                hoverinfo='x+y+name',
                marker_color=custom_colors[idx % len(custom_colors)]  # Cycle through custom colors
            ))

        # Set layout for the Income vs Worker Skill and Age Range chart
        fig_income_skill_age.update_layout(
            xaxis_title="Worker Age Range",
            yaxis_title="Average Monthly Income",
            barmode='group',  # Group bars together
            font=dict(color='Black'),
            xaxis=dict(title_font=dict(size=14), tickfont=dict(size=12)),
            yaxis=dict(title_font=dict(size=12), tickfont=dict(size=12)),
            margin=dict(l=0, r=0, t=30, b=50),
        )

        # Display the Income vs Worker Skill and Age Range chart in Streamlit
        st.markdown('<h3 class="custom-subheader">Average Monthly Income by Worker Skill and Age Range</h3>', unsafe_allow_html=True)
        st.plotly_chart(fig_income_skill_age, use_container_width=True)


# Count the occurrences of each Status
    coverage_counts = df.groupby('Marital Status')['Average Monthly Income'].mean().reset_index()
    coverage_counts.columns = ["premiums", "Count"]

    with cols1:
        # Display the header
        st.markdown('<h3 class="custom-subheader">Workers Affordability Payment Frequency</h3>', unsafe_allow_html=True)

        # Create a donut chart
        fig = px.pie(coverage_counts, names="premiums", values="Count", hole=0.5, template="plotly_dark", color_discrete_sequence=custom_colors)
        fig.update_traces(textposition='inside', textinfo='value+percent')
        fig.update_layout(height=450, margin=dict(l=0, r=10, t=30, b=50))

        # Display the chart in Streamlit
        st.plotly_chart(fig, use_container_width=True)

    # Group data by 'Worker age range' and 'Marital Status' and calculate the average income
    grouped_df = df.groupby(['Worker age range', 'Marital Status'])['Average Monthly Income'].mean().unstack().fillna(0)

    # Format the average income to one decimal place
    grouped_df = grouped_df.applymap(lambda x: round(x, 1))

    with cols2:
        fig_income_marital_age = go.Figure()

        # Add a bar trace for each marital status
        for idx, marital_status in enumerate(grouped_df.columns):
            fig_income_marital_age.add_trace(go.Bar(
                x=grouped_df.index,
                y=grouped_df[marital_status],
                name=marital_status,
                text=grouped_df[marital_status].apply(lambda x: f'{x:.1f}'),
                textposition='inside',
                textfont=dict(color='white'),
                hoverinfo='x+y+name',
                marker_color=custom_colors[idx % len(custom_colors)]  # Cycle through custom colors
            ))

        # Set layout for the Income vs Marital Status and Age Range chart
        fig_income_marital_age.update_layout(
            title='Average Monthly Income by Marital Status and Age Range',
            xaxis_title="Worker Age Range",
            yaxis_title="Average Monthly Income",
            barmode='group',  # Group bars together
            font=dict(color='Black'),
            xaxis=dict(title_font=dict(size=14), tickfont=dict(size=12)),
            yaxis=dict(title_font=dict(size=12), tickfont=dict(size=12)),
            margin=dict(l=0, r=0, t=30, b=50),
        )

        # Display the Income vs Marital Status and Age Range chart in Streamlit
        st.markdown('<h3 class="custom-subheader">Average Monthly Income by Marital Status and Age Range</h3>', unsafe_allow_html=True)
        st.plotly_chart(fig_income_marital_age, use_container_width=True)