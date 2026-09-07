# Day4 · 作业② PyTorch 与 Ultralytics 学习记录

> 对应 `D:\Day4_人工智能与神经网络.pptx` 第 13 页作业第 2 项。
> 参考官方文档：
> - PyTorch：<https://pytorch.org/docs/stable/index.html>
> - Ultralytics YOLO：<https://docs.ultralytics.com/>

---

## 第一部分：PyTorch 学习记录

### 1.1 PyTorch 是什么

PyTorch 是一个基于 Python 的科学计算框架，**核心定位是「GPU 加速的张量计算 + 自动求导 + 深度学习网络构建」**。可以把 PyTorch 看作 NumPy 的 GPU 升级版 + 自动求导版。

官网：<https://pytorch.org/>

### 1.2 三个核心概念

#### （1）`Tensor`（张量）

- 多维数组，类似 `numpy.ndarray`，但能放到 GPU 上计算
- 创建方式：`torch.tensor([1, 2, 3])`、`torch.zeros((3, 4))`、`torch.randn(2, 3)`
- 关键属性：`.shape` / `.dtype` / `.device`

```python
import torch
x = torch.tensor([[1., 2.], [3., 4.]])     # 2x2 张量
print(x.shape, x.dtype, x.device)          # torch.Size([2, 2]) torch.float32 cpu
print(x @ x.T)                              # 矩阵乘法
print(x.cuda())                             # 移到 GPU（如有）
```

#### （2）`autograd`（自动求导）

PyTorch 会**自动追踪所有对 Tensor 的运算**，最后 `loss.backward()` 自动算出梯度，这是反向传播（BP）的物理基础。

```python
x = torch.tensor([2.0], requires_grad=True)
y = x ** 2 + 3 * x          # y = x² + 3x
y.backward()                # 反向传播
print(x.grad)               # tensor([7.])  ← dy/dx = 2x+3 = 7
```

#### （3）`nn.Module`（网络模块）

- 所有自定义网络都继承 `torch.nn.Module`
- 在 `__init__` 里定义层（`nn.Linear`、`nn.Conv2d` 等），在 `forward` 里写前向传播

```python
import torch.nn as nn

class SimpleNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(784, 128)
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        return self.fc2(x)

model = SimpleNet()
```

### 1.3 神经网络的「五件套」

PPT 第 4~5 页提到的所有概念，在 PyTorch 里都有对应 API：

| 概念 | PyTorch 实现 |
| --- | --- |
| 神经元 / 全连接层 | `torch.nn.Linear(in, out)` |
| 卷积层（CNN） | `torch.nn.Conv2d(in_c, out_c, kernel)` |
| 池化层 | `torch.nn.MaxPool2d(2)` / `nn.AvgPool2d(2)` |
| 激活函数 | `torch.relu(x)` / `torch.sigmoid(x)` / `torch.softmax(x)` |
| 损失函数 | `nn.CrossEntropyLoss()` / `nn.MSELoss()` / `nn.BCEWithLogitsLoss()` |
| 优化器 | `torch.optim.SGD` / `torch.optim.Adam` |
| 学习率调度 | `optim.lr_scheduler.StepLR` / `CosineAnnealingLR` |

### 1.4 训练循环模板（必须背下来）

```python
import torch
from torch.utils.data import DataLoader
from torch import nn, optim

device = "cuda" if torch.cuda.is_available() else "cpu"
model = SimpleNet().to(device)
opt = optim.Adam(model.parameters(), lr=1e-3)
loss_fn = nn.CrossEntropyLoss()
loader = DataLoader(dataset, batch_size=32, shuffle=True)

for epoch in range(epochs):
    model.train()
    for x, y in loader:
        x, y = x.to(device), y.to(device)
        pred = model(x)
        loss = loss_fn(pred, y)
        opt.zero_grad()      # 梯度清零
        loss.backward()      # 反向传播（autograd）
        opt.step()           # 梯度下降更新权重
```

**关键三行**：`opt.zero_grad()` → `loss.backward()` → `opt.step()`，对应 PPT 第 5 页的「梯度下降 + BP 算法」。

### 1.5 常用工具 API 速查

| 任务 | API |
| --- | --- |
| 模型保存 | `torch.save(model.state_dict(), "model.pt")` |
| 模型加载 | `model.load_state_dict(torch.load("model.pt"))` |
| 数据并行（多 GPU） | `model = nn.DataParallel(model)` |
| 推理关闭梯度 | `with torch.no_grad():` |
| Tensor 与 NumPy 互转 | `x.numpy()` / `torch.from_numpy(arr)` |
| 设备搬运 | `tensor.to(device)` |

---

## 第二部分：Ultralytics YOLO 学习记录

### 2.1 Ultralytics 是什么

Ultralytics 是 YOLOv5 / YOLOv8 / **YOLO11** / YOLO26 的官方维护者，把「训练、推理、验证、导出、跟踪」打包成同一个 `yolo` CLI 和 `ultralytics` Python 包。**一个库搞定 YOLO 全流程**。

官网：<https://docs.ultralytics.com/>

### 2.2 `yolo` 命令结构（PPT 第 11 页）

```
yolo  TASK  MODE  ARGS

TASK (可选): detect / segment / semantic / depth / classify / pose / obb
MODE (必填): train / val / predict / export / track / benchmark
ARGS:        任意 arg=value，如 imgsz=640 conf=0.25
```

例：`yolo segment predict model=yolo11n-seg.pt source=img.jpg imgsz=640`

### 2.3 五种 MODE 对应的工作流（PPT 第 10 页完整流程）

```
┌────────┐   ┌─────────┐   ┌────────┐   ┌─────────┐
│ 标注   │ → │ 划分    │ → │ 训练   │ → │ 验证    │ → 应用
│labelme │   │ split   │   │ train  │   │ val     │
│labelimg│   │ train/  │   │ train  │   │ predict │
└────────┘   │ val/test│   └────────┘   └─────────┘
             └─────────┘
```

Ultralytics 的命令对应：

| 阶段 | 命令 |
| --- | --- |
| 训练（detect） | `yolo detect train model=yolo11n.pt data=data.yaml epochs=100 imgsz=640` |
| 训练（segment） | `yolo segment train model=yolo11n-seg.pt data=data.yaml epochs=100 imgsz=640` |
| 验证 | `yolo val model=runs/detect/train/weights/best.pt data=data.yaml` |
| 推理 | `yolo predict model=best.pt source=img.jpg conf=0.25` |
| 导出 | `yolo export model=best.pt format=onnx` |

### 2.4 Python API（比 CLI 更灵活）

```python
from ultralytics import YOLO

# 1) 加载模型（首次自动下载权重；网络不通时可手动放 weights/yolo11n.pt）
model = YOLO("yolo11n.pt")

# 2) 推理（detect）
results = model.predict(source="img.jpg", imgsz=640, conf=0.25, save=True)
# results 是 Results 列表，每项 .boxes / .masks / .names / .plot()

# 3) 训练
model = YOLO("yolo11n-seg.pt")
results = model.train(
    data="data.yaml",          # 数据集配置
    epochs=100,
    imgsz=640,
    batch=16,
    device=0,                  # GPU 编号；CPU 时写 "cpu"
    project="runs/segment",
    name="train",
)

# 4) 验证
metrics = model.val(data="data.yaml")
print(metrics.box.map, metrics.box.map50, metrics.box.map75)  # mAP50-95 / 50 / 75
```

### 2.5 YOLO 系列速览（PPT 第 6 页）

| 网络 | 用途 | 任务 |
| --- | --- | --- |
| FNN | 前馈全连接 | 简单表格数据 |
| CNN | 卷积 | 图像（最经典） |
| RNN / LSTM | 循环 | 序列（文本、语音） |
| GAN | 生成对抗 | 图像生成 |
| GNN | 图 | 关系数据（社交网络、分子） |
| Transformer / GPT | 注意力 | 文本生成、跨模态 |
| YOLO | 单阶段目标检测 | 实时检测 / 分割 |

Ultralytics 的 `yolo11` 系列对应该表中的 CNN + Transformer 混合，**单阶段（one-stage）实时检测**。

### 2.6 数据集配置 `data.yaml`

```yaml
# 路径可以是绝对路径或相对于 yaml 文件位置
path: D:\belt_shift_split1
train: train/images        # 训练集图片目录（相对 path）
val:   val/images          # 验证集图片目录（相对 path）
test:  ''                  # 测试集（可选，留空表示没有）

# 类别：id 与 label 一一对应
names:
  0: belt
  1: crack
```

YOLO 如何找到标签？把 `xxx.jpg` 扩展名换成 `.txt` + 路径里的 `images` 换成 `labels` 即可（PPT 第 15 页）。即：

```
split/
├── train/
│   ├── images/0001.jpg  ← → labels/0001.txt
│   └── labels/0001.txt
└── val/
    ├── images/0002.jpg
    └── labels/0002.txt
```

### 2.7 YOLO 标签格式（PPT 第 12-13 页）

- **目标检测（detect）**：每行 `cls cx cy w h`，全是 0~1 的归一化值
  ```
  13 0.817 0.462 0.350 0.265   # 第 13 类, 中心 x/y, 宽/高（都已 /原图宽高）
  ```
- **实例分割（segment）**：每行 `cls x1 y1 x2 y2 ... xn yn`，归一化的多边形顶点
  ```
  0 0.158 0.998 0.296 0.421 0.486 0.410 0.616 0.999
  ```

### 2.8 训练中断续训（PPT 第 22 页）

```bash
yolo train resume model=path/to/last.pt
# 如：yolo train resume model=./runs/detect/train4/weights/last.pt
```

`last.pt` 每代保存一次，`best.pt` 只在 val 上指标最佳时更新。

### 2.9 速查：典型错误与处理

| 现象 | 原因 | 处理 |
| --- | --- | --- |
| `CUDA out of memory` | GPU 显存不够 | 减 `batch`，减 `imgsz` |
| `No labels found` | data.yaml 的 path 错了 | 改成绝对路径 |
| `AssertionError: train: ...labels... 0 < 1` | train 集为空或标签路径错 | 检查 split 目录结构 |
| `mAP=0` | 类别映射错 / 标签全空 | 用 `yolo val` 看 confusion matrix |
| 训练卡在第 1 个 epoch | Windows 上 worker 多死锁 | `workers=0` |

---

## 第三部分：我的学习心得

1. **PyTorch 的核心不是 API，而是「计算图 + 自动求导」**：理解了 `loss.backward()` 怎么算出每个参数的梯度，再看 YOLO 训练就只是「在 PyTorch 上搭好的一个网络」，不会再有黑盒感。
2. **Ultralytics 把繁琐工程都封装掉了**：自己用 PyTorch 写目标检测训练循环要几百行；Ultralytics 一行 `model.train()` 搞定，**代价是你得懂 PPT 第 15~17 页的目录结构与 yaml**，否则改不动数据集。
3. **CPU 也能跑，但很慢**：本机没 GPU，CPU 跑 `yolo11n` 推理约 50 ms/张，能满足作业要求；**训练就别想了**，100 epoch 大概要十几个小时。
4. **一定要先看 PPT 的目录结构再跑**：很多新手错误是「图片在 `images/`，标签在 `labels/`，目录拼不上 `path`」。本目录 Day5 的 `samplesplit.py` 已经把这件事写好，按格式跑就完事。
5. **官方文档是最准的**：遇到任何参数问题（比如 `mosaic`、`mixup`、`close_mosaic`），**先看 <https://docs.ultralytics.com/usage/cfg>** 比看博客靠谱。

---

## 参考资料

- PyTorch 官方教程：<https://pytorch.org/tutorials/>
- PyTorch 中文文档（非官方）：<https://pytorch-cn.readthedocs.io/>
- Ultralytics 文档：<https://docs.ultralytics.com/>
- Ultralytics Quickstart：<https://docs.ultralytics.com/quickstart/>
- YOLO 配置全集：<https://docs.ultralytics.com/usage/cfg>
- 损失函数 / 优化器讲解（PPT 第 5 页）：<https://www.bilibili.com/video/BV1ev411p7jf9>
- 神经网络科普（PPT 第 2 页）：<https://www.bilibili.com/video/BV1uL4y1J7qA>