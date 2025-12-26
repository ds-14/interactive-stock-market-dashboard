import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Set page config first (must be first Streamlit command)
st.set_page_config(page_title="Stock Analysis Dashboard", layout="wide")

# Load data
company_list = [r"C:\Users\DELL\OneDrive\Desktop\Telegram Desktop\individual_stocks_5yr\AAPL_data.csv",
                r"C:\Users\DELL\OneDrive\Desktop\Telegram Desktop\individual_stocks_5yr\AMZN_data.csv",
                r"C:\Users\DELL\OneDrive\Desktop\Telegram Desktop\individual_stocks_5yr\GOOGL_data.csv",
                r"C:\Users\DELL\OneDrive\Desktop\Telegram Desktop\individual_stocks_5yr\MSFT_data.csv"]

all_data = pd.DataFrame()

for file in company_list:
    current_df = pd.read_csv(file)
    all_data = pd.concat([all_data, current_df], ignore_index=True)

all_data['date'] = pd.to_datetime(all_data['date'])

# Title
st.title("Tech Stocks Analysis Dashboard")

# Sidebar
tech_list = all_data['Name'].unique()
st.sidebar.title("Choose a company")
selected_company = st.sidebar.selectbox("Select a stock", tech_list)

# Filter data for selected company - ADD .copy() HERE
company_df = all_data[all_data["Name"] == selected_company].copy()
company_df.sort_values('date', inplace=True)

# 1st Plot - Closing Price
st.subheader(f"1. Closing Price of {selected_company} over Time")
fig1 = px.line(company_df, x="date", y="close",
               title=f"{selected_company} Closing Prices Over Time")
st.plotly_chart(fig1, use_container_width=True)

# 2nd Plot - Moving Average
st.subheader(f"2. Moving Average (10, 20, 50 days) - {selected_company}")

ma_day = [10, 20, 50]

for ma in ma_day:
    company_df['close_' + str(ma)] = company_df['close'].rolling(ma).mean()

fig2 = px.line(company_df, x="date", y=["close", 'close_10', 'close_20', 'close_50'],
               title=f"{selected_company} Closing Prices with Moving Averages",
               labels={'value': 'Price', 'variable': 'Metric'})
st.plotly_chart(fig2, use_container_width=True)

# 3rd Plot - Daily Returns
st.subheader(f"3. Daily Returns for {selected_company}")
company_df['Daily returns(in %)'] = company_df['close'].pct_change() * 100

fig3 = px.line(company_df, x="date", y="Daily returns(in %)",
               title=f'{selected_company} Daily Returns (%)')
st.plotly_chart(fig3, use_container_width=True)

# 4th Plot - Resampled Data
st.subheader(f"4. Resampled Closing Price (Monthly/Quarterly/Yearly) - {selected_company}")
company_df.set_index('date', inplace=True)
resample_option = st.radio("Select Resample Frequency", ["Monthly", "Quarterly", "Yearly"])

if resample_option == "Monthly":
    resampled = company_df['close'].resample('M').mean()
elif resample_option == "Quarterly":
    resampled = company_df['close'].resample('Q').mean()
else:
    resampled = company_df['close'].resample('Y').mean()

fig4 = px.line(resampled,
               title=f"{selected_company} {resample_option} Average Closing Price")
st.plotly_chart(fig4, use_container_width=True)

# 5th Plot - Correlation Heatmap
st.subheader("5. Correlation Heatmap of Tech Stocks Closing Prices")

# Load individual company data
aapl = pd.read_csv(company_list[0])
amzn = pd.read_csv(company_list[1])
googl = pd.read_csv(company_list[2])
msft = pd.read_csv(company_list[3])

closing_price = pd.DataFrame()
closing_price['AAPL'] = aapl['close']
closing_price['AMZN'] = amzn['close']
closing_price['GOOGL'] = googl['close']
closing_price['MSFT'] = msft['close']

fig5, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(closing_price.corr(), annot=True, cmap='coolwarm', ax=ax, 
            fmt='.2f', linewidths=0.5, square=True)
ax.set_title('Correlation Matrix of Tech Stocks', fontsize=16, pad=20)
st.pyplot(fig5)

# Footer
st.markdown("---")
st.markdown("**Note:** This Dashboard provides basic technical analysis of major tech stocks using Python and Streamlit")