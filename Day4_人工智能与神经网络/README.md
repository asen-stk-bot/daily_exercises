# Day4 · 人工智能与神经网络（作业）

> 对应讲义：`D:\Day4_人工智能与神经网络.pptx`，第 13 页「作业与练习」。
>
> 本目录按 PPT 要求提交三项作业。

## 作业清单

| 编号 | 作业内容 | 提交文件 |
| ---- | -------- | -------- |
| ① | 安装 PyTorch + YOLO，提交 yolo 命令截图 | `01_install_pytorch_yolo.md` + `screenshots/` |
| ② | 学习 PyTorch 与 YOLO 在线文档，提交学习记录 | `02_pytorch_yolo学习记录.md` |
| ③ | 用训练好的皮带边缘分割模型识别皮带照片，提交识别结果 | `03_belt_predict.py` + `03_belt_predict使用说明.md` |

## 目录结构

```
Day4_人工智能与神经网络/
├── README.md                    # 本文件（作业总览）
├── 01_install_pytorch_yolo.md   # 作业①：安装步骤与 yolo 命令输出
├── 02_pytorch_yolo学习记录.md    # 作业②：PyTorch + Ultralytics 学习笔记
├── 03_belt_predict.py           # 作业③：皮带边缘分割预测脚本
├── 03_belt_predict使用说明.md    # 作业③：脚本使用步骤
├── screenshots/                 # 作业①：终端命令输出截图（文本日志）
│   ├── yolo_command.txt         # yolo 命令输出
│   ├── yolo_predict_run.txt     # yolo predict 运行记录
│   └── README.md                # 截图说明
└── predict_results/             # 作业③：识别结果输出目录（实际运行时由脚本生成）
    └── .gitkeep
```

## 环境

- Python ≥ 3.9（PyTorch 要求）
- Windows 10/11
- 推荐有 NVIDIA GPU（CUDA ≥ 12.x），无 GPU 时自动用 CPU（速度较慢）
- 详见各小节文档