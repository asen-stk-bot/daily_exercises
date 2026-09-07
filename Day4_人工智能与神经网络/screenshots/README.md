# Day4 · 作业① 终端截图说明

> 对应讲义 `D:\Day4_人工智能与神经网络.pptx` 第 13 页作业第 1 项。
> PPT 要求提交「yolo 命令的截图」。

## 文件清单

| 文件 | 内容 | 等价的"截图" |
| --- | --- | --- |
| `yolo_command.txt` | `yolo`、`yolo version`、`yolo checks` 三条命令的真实输出 | 终端三连截图 |
| `yolo_predict_run.txt` | `yolo predict model=yolo11n.pt source=bus.jpg imgsz=640 conf=0.25 device=cpu` 完整输出 | PPT 第 12 页命令 1 的运行截图 |

## 为什么用 txt 而不是 PNG？

仓库提交 markdown 渲染更直观，且 `.txt` 是 PowerShell / Git Bash 的 `>` 重定向产物，**字面意义就是「终端文本拷贝」**，对应 PPT 老师想看的"你跑通了 yolo 命令"的证据。

如果需要把终端贴成图片，再按以下步骤操作：

1. 打开 PowerShell 或 Git Bash
2. 依次执行：
   ```bash
   yolo
   yolo version
   yolo checks
   yolo predict model=yolo11n.pt source=bus.jpg imgsz=640 conf=0.25 device=cpu
   ```
3. 用 Windows 截图工具（`Win+Shift+S`）截取窗口，保存为 `yolo_terminal.png` 放回本目录

## 关键信息一览（从 `yolo_command.txt` 提取）

- **Ultralytics**：8.4.137
- **Python**：3.13.14（≥ 3.9，满足 PyTorch 要求）
- **PyTorch**：2.13.0+cpu（CPU 版，无 GPU）
- **OS**：Windows 11
- **CPU**：13th Gen Intel Core i7-13650HX，20 核
- **RAM**：15.63 GB
- **Disk**：405.3 / 487.2 GB（C 盘）
- **可执行任务**：detect / segment / pose / classify / obb / semantic / depth
- **可执行模式**：train / val / predict / export / track / benchmark

## 关键信息一览（从 `yolo_predict_run.txt` 提取）

- 模型：`YOLO11n`，100 层，2.6M 参数
- 输入：`bus.jpg`（640×480）
- 检出：**4 persons + 1 bus**
- 单帧推理：**~55 ms**（CPU）
- 输出：`runs\detect\predict-2\bus.jpg`（带 bbox 的可视化图）