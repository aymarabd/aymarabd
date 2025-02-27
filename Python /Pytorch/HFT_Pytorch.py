import torch
import torch.nn as nn
import torch.optim as optim
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from torch.utils.data import DataLoader, TensorDataset

# Load dataset
file_path = "hft_order_book.csv"  # Replace with actual path
df = pd.read_csv(file_path)

# Select features and target
features = ["best_bid", "best_ask", "bid_volume", "ask_volume", "spread"]
target = "best_bid"  # Predicting next best bid

# Normalize features
scaler = MinMaxScaler()
df[features] = scaler.fit_transform(df[features])

# Convert to sequences
sequence_length = 50  # Can be adjusted
X, y = [], []

for i in range(len(df) - sequence_length):
    X.append(df[features].iloc[i : i + sequence_length].values)
    y.append(df[target].iloc[i + sequence_length])

X, y = np.array(X), np.array(y)

# Convert to PyTorch tensors
X_tensor = torch.tensor(X, dtype=torch.float32)
y_tensor = torch.tensor(y, dtype=torch.float32).view(-1, 1)

# Split into training and validation
train_size = int(0.8 * len(X))
X_train, X_val = X_tensor[:train_size], X_tensor[train_size:]
y_train, y_val = y_tensor[:train_size], y_tensor[train_size:]

# Create PyTorch DataLoaders
batch_size = 16
train_loader = DataLoader(TensorDataset(X_train, y_train), batch_size=batch_size, shuffle=True)
val_loader = DataLoader(TensorDataset(X_val, y_val), batch_size=batch_size)

# Define the LSTM model
class HFTLSTM(nn.Module):
    def __init__(self, input_size, hidden_size=64, num_layers=2):
        super(HFTLSTM, self).__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, 1)
    
    def forward(self, x):
        lstm_out, _ = self.lstm(x)
        return self.fc(lstm_out[:, -1, :])  # Take last LSTM output

# Initialize model
input_size = len(features)
model = HFTLSTM(input_size)
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Training loop
num_epochs = 10
for epoch in range(num_epochs):
    model.train()
    total_loss = 0
    
    for batch_X, batch_y in train_loader:
        optimizer.zero_grad()
        predictions = model(batch_X)
        loss = criterion(predictions, batch_y)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    
    # Validation
    model.eval()
    val_loss = 0
    with torch.no_grad():
        for batch_X, batch_y in val_loader:
            predictions = model(batch_X)
            val_loss += criterion(predictions, batch_y).item()
    
    print(f"Epoch {epoch+1}/{num_epochs} - Loss: {total_loss/len(train_loader):.4f} - Val Loss: {val_loss/len(val_loader):.4f}")

# Save the model
torch.save(model.state_dict(), "hft_lstm_model.pth")
print("Model saved successfully.")
