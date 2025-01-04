import os
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import yfinance as yf
import streamlit as st
from datetime import datetime

# Load user data from JSON file
USER_DATA_FILE = "user_data.json"

def load_user_data():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "r") as file:
            return json.load(file)
    return {}

USER_DATA = load_user_data()

# Predefined list of stock symbols for dropdown
STOCK_SYMBOLS = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "TSLA",
    "META", "NFLX", "NVDA", "JPM", "V",
    "JNJ", "WMT", "DIS", "BAC", "PG"
]

# Function to get stock data for the next 7 days from the given start date
def get_stock_data(symbol, start_date):
    end_date = start_date + pd.Timedelta(days=7)
    stock_data = yf.download(symbol, start=start_date, end=end_date)
    return stock_data

# Function to prepare data for Multilinear Regression
def prepare_data(stock_data):
    stock_data['Date'] = stock_data.index
    stock_data['Date'] = pd.to_numeric(stock_data['Date'])
    X = stock_data[['Date', 'Open']]
    y = stock_data['Close']
    return X, y

# Function to train Multilinear Regression model
def train_model(X, y):
    if len(X) < 2:  # Check if we have enough data to split into train and test sets
        return None, None, None, None, None
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    
    return model, mse, X_test, y_test, y_pred

# Dashboard (Main Application after login)
if st.session_state.logged_in:
    st.title("Stock Price Prediction Dashboard")
    st.write(f"Logged in as: {st.session_state.username}")

    # Sidebar for user inputs
    st.sidebar.header("User Inputs")

    stock_symbol = st.sidebar.selectbox("Select Stock Symbol", STOCK_SYMBOLS)
    start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2020-01-01"))

    if stock_symbol and start_date:
        if st.sidebar.button("Predict"):
            if stock_symbol not in STOCK_SYMBOLS:
                st.error("Stock symbol not present. Please enter a valid stock symbol.")
            else:
                stock_data = get_stock_data(stock_symbol, start_date)
                if not stock_data.empty:
                    st.write(f"Showing stock data for {stock_symbol} from {start_date} for 7 days")
                    st.dataframe(stock_data.tail())

                    X, y = prepare_data(stock_data)
                    model, mse, X_test, y_test, y_pred = train_model(X, y)

                    st.subheader("Stock Price Prediction (7 Days)")
                    fig, ax = plt.subplots(figsize=(10, 6))
                    ax.plot(stock_data.index, stock_data['Close'], color='blue', label='Actual Prices')
                    ax.plot(stock_data.index, model.predict(X), color='red', label='Predicted Prices')
                    ax.set_title(f"{stock_symbol} Stock Price Prediction (7 Days)")
                    ax.set_xlabel("Date")
                    ax.set_ylabel("Stock Price")
                    ax.legend()
                    st.pyplot(fig)

                    st.write(f"Mean Squared Error of the model: {mse:.2f}")
                else:
                    st.error("Failed to retrieve stock data. Please check the stock symbol or start date.")
        
        if st.sidebar.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.experimental_rerun()  # Redirect back to login
