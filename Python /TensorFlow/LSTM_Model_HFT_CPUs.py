import os
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler #trying other scaler to minize errors
from collections import deque

# Force CPU usage
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"  # Disable GPU
tf.config.set_visible_devices([], 'GPU')  # Disable GPU explicitly
tf.config.threading.set_intra_op_parallelism_threads(4)  # Optimize for CPU
tf.config.threading.set_inter_op_parallelism_threads(4)

# Load sample Function for HFT order book data
def load_data():
    df = pd.read_csv("hft_order_book.csv")  # Example file
    df["mid_price"] = (df["best_bid"] + df["best_ask"]) / 2  # Mid-price calculation
    return df

# Feature engineering: Create time-series sequences
def preprocess_data(df):
    features = ["best_bid", "best_ask", "bid_volume", "ask_volume", "spread"]
    df["spread"] = df["best_ask"] - df["best_bid"]
    print("LEN DF IS:" , len(df))
    #scaler = StandardScaler()
    #df[features] = scaler.fit_transform(df[features])  # Normalize data
    scaler = MinMaxScaler()
    df[features] = scaler.fit_transform(df[features])

    sequence_length = min(100, len(df) - 1)

    sequences, labels = [], deque(maxlen=sequence_length) #deque: Double-Ended Queue. It is a data structure that allows adding and removing elements from both ends
    for i in range(len(df)):
        labels.append(df["mid_price"].iloc[i]) #append the mid-price for each row
        if len(labels) == sequence_length:
            sequences.append((np.array(df[features].iloc[i-sequence_length+1:i+1]), labels[-1])) #This takes X  (["best_bid", "best_ask", "bid_volume", "ask_volume", "spread"]), and y (last computed labels value) values.
    
    if not sequences:
        raise ValueError("Not enough data for even one sequence. Increase dataset size.")    
            
    X, y = zip(*sequences) # unzipping the data into X and y
    return np.array(X), np.array(y), scaler

# Define the LSTM model optimized for CPU
def build_model(input_shape):
    model = Sequential([
        LSTM(32, return_sequences=True, input_shape=input_shape),  # Reduce LSTM size for CPU efficiency
        Dropout(0.1),  # Lower dropout rate for faster CPU training
        LSTM(16, return_sequences=False),
        Dense(8, activation="relu"),
        Dense(1)  # Predict next mid-price
    ])
    #model.compile(loss="mse", optimizer="adam")
    model.compile(loss="mae", optimizer="adam")
    return model

# Load and preprocess data
df = load_data()
print(df)
X, y, scaler = preprocess_data(df)

# Split data into train/test sets
split = int(0.8 * len(X))
X_train, y_train = X[:split], y[:split]
X_test, y_test = X[split:], y[split:]

# Build and train the model
model = build_model((X_train.shape[1], X_train.shape[2]))
model.fit(X_train, y_train, epochs=20, batch_size=4, validation_data=(X_test, y_test), verbose=1)

# Make predictions
predictions = model.predict(X_test)

# Convert predictions back to price scale
predictions_rescaled = scaler.inverse_transform(np.hstack((np.zeros((len(predictions), 4)), predictions.reshape(-1, 1))))[:, -1]

# Strategy: Trade when predicted price change > threshold
def execute_trades(predictions, actual_prices, threshold=0.01):
    positions = []
    for i in range(len(predictions) - 1):
        if predictions[i+1] > actual_prices[i] * (1 + threshold):
            positions.append("BUY")
        elif predictions[i+1] < actual_prices[i] * (1 - threshold):
            positions.append("SELL")
        else:
            positions.append("HOLD")
    return positions

trade_signals = execute_trades(predictions_rescaled, y_test)

# Print first 10 trade signals
print(trade_signals[:10])
