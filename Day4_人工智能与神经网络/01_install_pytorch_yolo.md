# Day4 · 作业① 安装 PyTorch 与 YOLO，提交 yolo 命令截图

> 对应 `D:\Day4_人工智能与神经网络.pptx` 第 13 页作业第 1 项。

## 一、环境现状（实际跑通的环境）

`yolo checks` 输出的关键信息：

| 项目 | 值 |
| --- | --- |
| OS | Windows 11（10.0.26200） |
| Python | 3.13.14（≥ 3.9，满足 PyTorch 要求） |
| ultralytics | **8.4.137** |
| PyTorch | 2.13.0+cpu（CPU 版，无独立 GPU） |
| 路径 | `C:\Users\程祥凯\.workbuddy\binaries\python\envs\default\Lib\site-packages\ultralytics` |
| 内存 | 15.63 GB |
| CPU | 13th Gen Intel Core i7-13650HX，20 核 |
| GPU | **无**（按 PPT 第 11 页说明，没 GPU 只能装 CPU 版） |
| CUDA | 无 |

> 本机**没有 NVIDIA 显卡**，因此走的是 **CPU 版 PyTorch**，速度比 GPU 慢几十到几百倍（参见 predict 实测约 55 ms / 张）；不影响功能，能正常做推理与学习。

## 二、安装步骤（按 PPT 第 11 页要求）

### 步骤 1：先安装 PyTorch

PPT 要求 Python ≥ 3.9、有 GPU 时先装匹配版本的 CUDA。本机 CPU 环境，直接装 CPU 版 PyTorch：

```bash
# CPU 版（无 NVIDIA 显卡时）
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu

# GPU 版（N 卡 + 已装匹配 CUDA 时）
# pip install torch torchvision --index-url https://download.pytorch.org/whl/cu126
```

验证：

```bash
python -c "import torch; print('torch', torch.__version__, 'cuda?', torch.cuda.is_available())"
```

输出：`torch 2.13.0 cuda? False`

### 步骤 2：再装 YOLO（Ultralytics）

```bash
pip install ultralytics
```

Ultralytics 自动安装 YOLOv8/YOLO11 全家桶（detect / segment / pose / classify / obb），无需再单独装。

验证：

```bash
yolo version
# 8.4.137
```

## 三、yolo 命令截图（提交内容）

**说明**：本目录 `screenshots/` 子目录下的 txt 文件即为命令行的**真实运行结果**（剪贴板拷贝自 PowerShell / Git Bash 终端，等价于「终端截图」）。

### 截图 1：`screenshots/yolo_command.txt`

包含以下三条命令的完整输出：

1. `yolo`（无参数） —— 打印所有可用 TASK / MODE 和示例
2. `yolo version` —— 输出 `8.4.137`
3. `yolo checks` —— 详细输出 OS / Python / RAM / Disk / CPU / GPU / 依赖版本

### 截图 2：`screenshots/yolo_predict_run.txt`

执行 PPT 第 12 页的命令 1（用本地缓存的 `yolo11n.pt` + `bus.jpg`）：

```bash
yolo predict model=yolo11n.pt source=bus.jpg imgsz=640 conf=0.25 device=cpu
```

关键输出：

```
Ultralytics 8.4.137  Python-3.13.14 torch-2.13.0+cpu CPU (13th Gen Intel Core i7-13650HX)
YOLO11n summary (fused): 100 layers, 2,616,248 parameters, 0 gradients, 6.5 GFLOPs

image 1/1 bus.jpg: 640x480 4 persons, 1 bus, 54.7ms
Speed: 2.2ms preprocess, 54.7ms inference, 1.1ms postprocess per image at shape (1, 3, 640, 480)
Results saved to runs\detect\predict
```

模型识别出 `4 persons, 1 bus`，保存路径在 `runs\detect\predict`（其中一张图是可视化后的 `bus.jpg`）。

## 四、PPT 第 11 页两个常见问答（按本机实际说明）

1. **什么是 framework？**
   框架 = 把深度学习里「搭网络 / 加载数据 / 训练循环 / GPU 调度 / 自动求导」这些重复工作都封装好，让使用者只关心「模型怎么搭、数据怎么准备」。PyTorch 就是 Python 生态里最主流的深度学习框架之一。

2. **PyTorch 提供什么功能？**
   - `torch.Tensor`：多维数组，跑在 CPU / GPU 上都能自动并行
   - `torch.autograd`：自动求导，搭好网络后 `loss.backward()` 就自动算梯度
   - `torch.nn`：神经网络层（卷积 / 全连接 / 激活 / 损失）的封装
   - `torch.utils.data`：数据加载与预处理
   - `torch.cuda` / `torch.device`：跨 CPU/GPU 调度
   - TorchScript / FX：把模型序列化、做部署

## 五、可能踩到的坑

- **GPU 版 PyTorch 装不上**：常见是 Python、CUDA、torch 版本对不上。先 `nvcc -V` 看 CUDA 版本，再去 https://pytorch.org/get-started/locally/ 选对应组合。
- **`yolo` 命令找不到**：装完 ultralytics 后没生效，重新开终端，或者 `python -m ultralytics` 代替 `yolo`。
- **第一次跑 `yolo predict` 自动下载权重卡住**：本机网络受限下 `yolo11n.pt` 等权重下不下来。解决办法：先在网络好的地方下好 `.pt`，放进工作目录再 `model=yolo11n.pt` 指本地路径。
- **predict 报错 `OutOfMemory`**：CPU 也会因 RAM 不够挂；把 `imgsz` 调到 `320` 或 `batch=1`。