# Day5 · 样本标注、数据预处理与模型训练（作业）

> 对应讲义：`D:\Day5_样本标注_数据预处理_模型训练.pptx`，第 23 页「作业与练习」。
>
> 本目录按 PPT 要求提交四项作业。

## 作业清单

| 编号 | 作业内容 | 提交文件 |
| ---- | -------- | -------- |
| ① | 用参考工具预处理数据（必须） | `01_label2yoloseg.py` + `02_samplesplit.py` |
| ② | 用 YOLO 完成模型训练（必须） | `03_模型训练说明.md` |
| ③ | 解释模型的各种指标（必须） | `04_模型指标解释.md` |
| ④ | 自己写 Python 代码实现数据预处理工具（鼓励） | `01_label2yoloseg.py` + `02_samplesplit.py`（从零写） |

## 目录结构

```
Day5_样本标注_数据预处理_模型训练/
├── README.md                    # 本文件
├── 01_label2yoloseg.py          # 作业①④：labelme json → YOLO seg txt + split
├── 02_samplesplit.py            # 作业①④：labelimg xml → YOLO detect txt + split
├── 03_模型训练说明.md            # 作业②：yolo segment/detect train 的命令行与流程
├── 04_模型指标解释.md            # 作业③：loss / precision / recall / mAP / IoU 等
└── data.yaml.example            # 数据集配置示例（生成器会按此格式输出 data.yaml）
```

## 作业组别 & 标签（PPT slide 9）

| 组别 | 标签 | 标注软件 | 任务类型 |
| --- | --- | --- | --- |
| 皮带 | `belt` | **labelme**（画多边形） | 实例分割 |
| 安全帽 | `wear` / `nowear` | labelimg（框） | 目标检测 |
| 工程车 | `crane` / `towercrane` | labelimg（框） | 目标检测 |
| 烟火 | `smoke` / `fireworks` | labelimg（框） | 目标检测 |
| 异物 | `nest` / `plastic` / `kite` / `ballon` | labelimg（框） | 目标检测 |

## 环境

- Python ≥ 3.9
- PyTorch ≥ 1.8
- Ultralytics ≥ 8.x
- 无 GPU 也能跑预处理（CPU 足够），有 NVIDIA GPU 时训练速度会提升几十倍