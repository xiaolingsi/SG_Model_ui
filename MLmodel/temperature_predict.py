import pandas as pd
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset
from sklearn.preprocessing import MinMaxScaler

# # 加载CSV文件并处理数据
# data = pd.read_csv('./weather_stations_All.csv') # 根据实际文件路径进行修改
# temperatures = data['TEMPERATURE'].values.reshape(-1, 1)
# scaler = MinMaxScaler()
# temperatures_scaled = scaler.fit_transform(temperatures)
# timestamps = pd.to_datetime(data['lOC_TIME'])

# 定义数据集类
class TemperatureDataset(Dataset):
    def __init__(self, data, sequence_length, target_length):
        self.data = data
        self.sequence_length = sequence_length
        self.target_length = target_length

    def __len__(self):
        return len(self.data) - self.sequence_length - self.target_length + 1

    def __getitem__(self, idx):
        seq_start = idx
        seq_end = idx + self.sequence_length
        target_start = seq_end
        target_end = seq_end + self.target_length

        sequence = self.data[seq_start:seq_end]
        target = self.data[target_start:target_end]
        target = target.reshape((20,))
        return sequence, target

# 定义 GRU 模型
class GRUModel(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers, output_size):
        super(GRUModel, self).__init__()
        self.gru = nn.GRU(input_size=input_size, hidden_size=hidden_size, num_layers=num_layers, batch_first=True)
        self.linear = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        out, _ = self.gru(x)
        out = self.linear(out[:, -1, :])
        return out

# # 参数设置
# input_size = 1
# hidden_size = 64
# num_layers = 2
# output_size = 20
# sequence_length = 120  # 过去两小时的数据，每30秒一个数据点
# target_length = 20  # 未来20分钟的数据，每30秒一个数据点
# batch_size = 64
# epochs = 10
# learning_rate = 0.001
#
# # 创建数据加载器
# dataset = TemperatureDataset(temperatures_scaled, sequence_length, target_length)
# dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True, drop_last=True)
#
# # 创建模型、损失函数和优化器
# model = GRUModel(input_size, hidden_size, num_layers, output_size)
# criterion = nn.MSELoss()
# optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
#
# # 模型训练
# for epoch in range(epochs):
#     for inputs, targets in dataloader:
#         optimizer.zero_grad()
#         inputs = inputs.float()
#         targets = targets.float()
#         outputs = model(inputs)
#         loss = criterion(outputs, targets)
#         loss.backward()
#         optimizer.step()
#     print(f"Epoch [{epoch+1}/{epochs}], Loss: {loss.item():.6f}")
#
# # 实际预测
# model.eval()
# with torch.no_grad():
#     last_sequence = temperatures_scaled[-sequence_length:].reshape(1, sequence_length, 1)
#     predictions = []
#     for _ in range(target_length):
#         prediction = model(torch.tensor(last_sequence))
#         predictions.append(prediction.item())
#         last_sequence = np.concatenate((last_sequence[:, 1:, :], prediction.reshape(1, 1, 1)), axis=1)
#
# # 还原预测结果的缩放
# predictions_scaled = np.array(predictions).reshape(-1, 1)
# predictions_original = scaler.inverse_transform(predictions_scaled)
#
# # 打印预测结果
# for i, timestamp in enumerate(pd.date_range(start=timestamps.iloc[-1], periods=target_length, freq='30S')):
#     print(f"{timestamp}: {predictions_original[i][0]:.2f} °C")
