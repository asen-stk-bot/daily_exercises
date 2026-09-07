# Day4 · 作业③ 皮带边缘分割识别 — 使用说明

> 对应 `D:\Day4_人工智能与神经网络.pptx` 第 13 页作业第 3 项。
> 配套脚本：`03_belt_predict.py`

## 一、目标

用 PPT 里提供的**训练好的皮带边缘分割模型**（`.pt` 文件），对几张皮带照片做**实例分割**，输出带 mask 的可视化图。

YOLO 区分两个相近概念，**用错就报错**：

| 任务 | 模型类型 | 命令 |
| --- | --- | --- |
| 目标检测（框） | `yolo11n.pt` / `yolo11s.pt` | `yolo detect predict` |
| **实例分割（边缘）** | `yolo11n-seg.pt` / `yolo11s-seg.pt` / 老师训的模型 | `yolo segment predict` |

皮带边缘属于**分割**，所以模型名一般带 `-seg`。老师给的模型 `.pt` 应当是用 `yolo segment train` 训出来的。

## 二、准备工作

1. 拿到老师发的两个东西：
   - 训练好的模型文件：`xxx_belt_seg.pt`（或类似命名）
   - 几张皮带照片：`belt_01.jpg` `belt_02.jpg` ... 放在一个文件夹里

2. 准备环境（已经装过可跳过）：

```bash
pip install ultralytics opencv-python pillow
```

## 三、运行

### 方式 A：用本目录的脚本（推荐）

```bash
cd Day4_人工智能与神经网络

python 03_belt_predict.py \
    --model  D:\老师发的模型\belt_seg_best.pt \
    --source D:\老师发的照片\belt_photos \
    --save_dir predict_results \
    --imgsz  640 \
    --conf   0.25
```

参数含义：

- `--model`：训练好的皮带分割模型（必填，绝对路径最稳）
- `--source`：一张图路径 / 一个目录 / 通配符 / URL / 视频
- `--save_dir`：本脚本汇总报告输出位置（默认 `predict_results`）
- `--imgsz`：推理图片边长，**和训练时保持一致**最好
- `--conf`：置信度阈值，0.25 是常用默认值，越高越严格

### 方式 B：纯 yolo 命令行

```bash
yolo segment predict \
    model=D:\老师发的模型\belt_seg_best.pt \
    source=D:\老师发的照片\belt_photos \
    imgsz=640 conf=0.25 \
    save=True
```

结果直接保存在 `runs/segment/predict/` 里（脚本方式 A 行为一致）。

## 四、查看结果

### 1. 终端输出示例

```
========== 识别结果汇总 ==========
图片: belt_01.jpg  检出皮带数: 1  分割轮廓数: 1
   └─ belt  conf=0.873  bbox=[125.0, 380.5, 920.3, 710.8]
图片: belt_02.jpg  检出皮带数: 1  分割轮廓数: 1
   └─ belt  conf=0.901  bbox=[150.2, 410.7, 880.9, 690.4]
```

### 2. 可视化图

识别后带 mask 的照片保存在：

```
runs/segment/predict_belt/
├── belt_01.jpg       # 识别后的图（带彩色 mask）
├── belt_02.jpg
└── ...
```

或者脚本方式 A 会同时把汇总报告写到：

```
predict_results/
└── report.txt        # 每张图的检出统计
```

### 3. 提交清单（按 PPT 要求）

最终要提交到 GitHub 的 `Day4_人工智能与神经网络/` 目录下：

| 提交内容 | 文件 |
| --- | --- |
| 识别脚本 | `03_belt_predict.py` |
| 使用说明 | `03_belt_predict使用说明.md`（本文件） |
| **识别后的照片** | `runs/segment/predict_belt/*.jpg`（如果使用 git 提交，建议把这几个图单独提 PR；模型权重本身不上 git，太大） |
| 报告 | `predict_results/report.txt` |

> **重要**：识别后的图是用 `save=True` 让 YOLO 自动写出的，建议 `git add` 时只挑要提交的图，不要把 `runs/` 整个目录都加（已在仓库根目录 `.gitignore` 中忽略 `runs/`）。

## 五、常见问题

1. **报错 `model=YOLO(...).predict(...)` 找不到 task**
   - 模型是 `detect` 训的还是 `segment` 训的？皮带边缘是 **segment**。
   - 检查方法：在 Python 里 `YOLO("model.pt")` 后看 `model.task` 字段（应返回 `segment`）。

2. **检出全是 mask 但没有 box**
   - 说明 `--conf` 阈值过高，调低到 0.15 试一下。

3. **检出 0 个**
   - 模型与数据不匹配（不是皮带，或者训练分辨率差很多）。先跑一张训练集里的图确认模型本身没问题。

4. **CPU 太慢**
   - 减小 `--imgsz` 到 320；或者改成 GPU 推理（需要 NVIDIA 卡 + 配套 CUDA + GPU 版 PyTorch）。

5. **可视化图想关掉 label 文字 / 改 mask 颜色**
   - 在脚本里改 `model.predict(..., show_labels=False, show_conf=False)`，或在 `model.plot()` 后自己用 `cv2` 改色。