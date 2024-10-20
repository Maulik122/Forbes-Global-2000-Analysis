import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import matplotlib.pyplot as plt

# Title
st.title("Forbes Global 2000 Companies Analysis (2022)")
st.write("""This app allows you to explore the Forbes Global 2000 dataset, focusing on key financial metrics like Sales, Profits, Assets, and Market Value.
You can interact with the data through graphs, filters, and dynamic visualizations.""")

# Loading Data
@st.cache_data
def load_data():
    data = pd.read_csv('Forbes Global 2000 (Year 2022).xlsx - Sheet1 (1).csv')
    return data

data = load_data()

#Sidebar Filter
st.sidebar.header("Filter Options")
selected_countries = st.sidebar.multiselect("Select Countries", options=data["Country"].unique(), default=data["Country"].unique())
selected_industry = st.sidebar.multiselect("Select Industries", options=data["Industry"].unique(), default=data["Industry"].unique())

#Filters country based on side by selection
filtered_data = data[(data["Country"].isin(selected_countries)) & (data["Industry"].isin(selected_industry))]

#Table title
st.header("Key Metrics Overview")
metrics = ['Sales', 'Profits', 'Assets', 'Market_Value']

#data table
st.write("Filtered Data Table")
st.dataframe(filtered_data)


# Sales vs. Profits Scatter Plot
st.subheader("Sales vs. Profits of Companies")
fig1 = px.scatter(filtered_data, x="Sales", y="Profits", color="Country", hover_name="Company", title="Sales vs. Profits")
st.plotly_chart(fig1)


# Assets vs. Market Value Scatter Plot
st.subheader("Assets vs. Market Value of Companies")
fig2 = px.scatter(filtered_data, x="Assets", y="Market_Value", color="Country", hover_name="Company", title="Assets vs. Market Value")
st.plotly_chart(fig2)


# Interactive KPI display
st.header("Interactive Company KPI")
company_name = st.selectbox("Select a Company", options=filtered_data["Company"].unique())
company_data = filtered_data[filtered_data["Company"] == company_name]

# displaying value based on the company name
st.write(f"**Selected Company: {company_name}**")
st.metric(label="Sales", value=company_data["Sales"].values[0])
st.metric(label="Profits", value=company_data["Profits"].values[0])
st.metric(label="Assets", value=company_data["Assets"].values[0])
st.metric(label="Market_Value", value=company_data["Market_Value"].values[0])


# Correlation metrics
st.subheader("Correlation between Financial Metrics")
correlation_fig = ff.create_annotated_heatmap(z=data[['Sales', 'Profits', 'Assets', 'Market_Value']].corr(method='pearson').values,
                                              x=['Sales', 'Profits', 'Assets', 'Market_Value'], y=['Sales', 'Profits', 'Assets', 'Market_Value'], colorscale='Viridis')
st.plotly_chart(correlation_fig)


# colors for graphs
custom_colors = ['blue', 'green', 'orange', 'red', 'purple', 'cyan']

# Industry wise count
st.subheader("Industry Wise Count of Companies")
industry_counts = data['Industry'].value_counts()
fig_industry = px.bar(industry_counts, x=industry_counts.index, y=industry_counts.values, title="Industry Wise Count of Companies", labels={'x': 'Industry', 'y': 'Number of Companies'})
fig_industry.update_layout(xaxis_tickangle=-45)
fig_industry.update_traces(marker_color=custom_colors[0])
st.plotly_chart(fig_industry)


# Top Countries by total no. of companies
st.subheader("Top 10 Countries by Number of Companies")
country_counts = data['Country'].value_counts().head(10)
fig_countries = px.bar(country_counts, x=country_counts.index, y=country_counts.values, title="Top 10 Countries by Number of Companies", labels={'x': 'Country', 'y': 'Number of Companies'})
fig_countries.update_layout(xaxis_tickangle=-30)
fig_countries.update_traces(marker_color=custom_colors[1])
st.plotly_chart(fig_countries)


#Top 10 companies by sales
st.subheader("Top 10 Companies by Sales")
top10bysales = data.sort_values(by="Sales", ascending=False).head(10)
fig_sales = px.bar(top10bysales, x='Company', y='Sales', title="Top 10 Companies by Sales", labels={'Company': 'Company', 'Sales': 'Sales'})
fig_sales.update_layout(xaxis_tickangle=-30)
fig_sales.update_traces(marker_color=custom_colors[2])
st.plotly_chart(fig_sales)


# Top 10 companies by profits
st.subheader("Top 10 Companies by Profits")
top10byprofit = data.sort_values(by="Profits", ascending=False).head(10)
fig_profits = px.bar(top10byprofit, x='Company', y='Profits', title="Top 10 Companies by Profits", labels={'Company': 'Company', 'Profits': 'Profits'})
fig_profits.update_layout(xaxis_tickangle=-30)
fig_profits.update_traces(marker_color=custom_colors[3]) 
st.plotly_chart(fig_profits)


# Top 10 companies by Assets
st.subheader("Top 10 Companies by Assets")
top10byasset = data.sort_values(by="Assets", ascending=False).head(10)
fig_assets = px.bar(top10byasset, x='Company', y='Assets', title="Top 10 Companies by Assets", labels={'Company': 'Company', 'Assets': 'Assets'})
fig_assets.update_layout(xaxis_tickangle=-30)
fig_assets.update_traces(marker_color=custom_colors[4])
st.plotly_chart(fig_assets)


# Top 10 companies by Market Value
st.subheader("Top 10 Companies by Market Value")
top10bymv = data.sort_values(by="Market_Value", ascending=False).head(10)
fig_market_value = px.bar(top10bymv, x='Company', y='Market_Value', title="Top 10 Companies by Market Value", labels={'Company': 'Company', 'Market_Value': 'Market Value'})
fig_market_value.update_layout(xaxis_tickangle=-30)
fig_market_value.update_traces(marker_color=custom_colors[5])  
st.plotly_chart(fig_market_value)


#return on Assets (ROA)
data['ROA'] = (data['Profits'] / data['Assets']) * 100
top_roa_companies = data[['Company', 'ROA']].sort_values(by='ROA', ascending=False).head(10)

st.subheader('Top 10 Companies by Return on Assets (ROA)')
fig_roa = px.bar(top_roa_companies, x='ROA', y='Company', orientation='h', title='Top 10 Companies by Return on Assets (ROA)',
                 labels={'ROA': 'ROA (%)', 'Company': 'Company'})
fig_roa.update_traces(marker_color='lightblue')
st.plotly_chart(fig_roa)
 

# Profit Margin
data['Profit_Margin'] = (data['Profits'] / data['Sales']) * 100
industry_profit_margin = data.groupby('Industry')['Profit_Margin'].mean().sort_values(ascending=False).head(10)

st.subheader('Top 10 Industries by Average Profit Margin')
fig_profit_margin = px.bar(industry_profit_margin, x=industry_profit_margin.index, y=industry_profit_margin.values, title='Top 10 Industries by Average Profit Margin',
                           labels={'x': 'Industry', 'y': 'Profit Margin (%)'})
fig_profit_margin.update_traces(marker_color='cyan')
fig_profit_margin.update_layout(xaxis_tickangle=-35)
st.plotly_chart(fig_profit_margin)



st.write("Developed with ❤️ using Streamlit")

