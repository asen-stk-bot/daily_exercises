#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""
Day4 · 作业③：皮带边缘分割识别脚本

对应讲义 D:\Day4_人工智能与神经网络.pptx 第 13 页作业第 3 项：
    "以下是训练好的皮带的边缘分割的模型，以及几张皮带的照片，
     请用 yolo 识别这几张照片中的皮带边缘，提交识别后的照片。"

使用方法：
    python 03_belt_predict.py \
        --model  path/to/belt_seg_model.pt \
        --source path/to/belt_photos/  \
        --save_dir predict_results \
        --imgsz  640 \
        --conf   0.25

参数说明：
    --model      训练好的皮带边缘分割模型（必填）
    --source     一张图 / 一个目录 / 一个 URL / 一段视频（必填）
    --save_dir   识别结果输出目录，默认 ./predict_results
    --imgsz      推理时缩放的方形边长，默认 640
    --conf       置信度阈值，默认 0.25
    --device     推理设备，'cpu' / '0' (GPU)，自动检测
    --project    YOLO runs 输出目录名（默认 runs/segment/predict_belt）

依赖：
    pip install ultralytics opencv-python pillow
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from ultralytics import YOLO


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="用训练好的 YOLO 分割模型识别皮带边缘",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--model",
        type=str,
        required=True,
        help="训练好的皮带边缘分割模型 (.pt)",
    )
    parser.add_argument(
        "--source",
        type=str,
        required=True,
        help="输入：图片路径 / 目录 / glob / URL / 视频",
    )
    parser.add_argument(
        "--save_dir",
        type=str,
        default="predict_results",
        help="本脚本汇总的结果输出目录",
    )
    parser.add_argument(
        "--imgsz",
        type=int,
        default=640,
        help="推理时图片缩放边长",
    )
    parser.add_argument(
        "--conf",
        type=float,
        default=0.25,
        help="置信度阈值",
    )
    parser.add_argument(
        "--device",
        type=str,
        default="",
        help="cuda device, 如 0 / 0,1 / cpu；留空则自动选择",
    )
    parser.add_argument(
        "--project",
        type=str,
        default="runs/segment",
        help="Ultralytics runs 项目目录",
    )
    parser.add_argument(
        "--name",
        type=str,
        default="predict_belt",
        help="Ultralytics runs 任务名",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    model_path = Path(args.model)
    if not model_path.exists():
        print(f"[ERROR] 找不到模型文件: {model_path}", file=sys.stderr)
        print("        请检查 PPT 老师发的 .pt 路径是否正确", file=sys.stderr)
        return 1

    save_dir = Path(args.save_dir)
    save_dir.mkdir(parents=True, exist_ok=True)

    print(f"[INFO] 加载模型: {model_path}")
    model = YOLO(str(model_path))

    print(f"[INFO] 推理输入: {args.source}")
    print(f"[INFO] imgsz={args.imgsz}  conf={args.conf}  device={args.device or 'auto'}")

    # 推理
    results = model.predict(
        source=args.source,
        imgsz=args.imgsz,
        conf=args.conf,
        device=args.device or None,
        save=True,                   # 让 YOLO 把带 mask 的可视化图保存到 runs/segment/predict_belt/
        project=args.project,
        name=args.name,
        exist_ok=True,
    )

    # 汇总：把每张图的核心指标写到终端 + 文本报告
    summary_lines = []
    print("\n========== 识别结果汇总 ==========")
    for r in results:
        names = r.names
        n = len(r.boxes) if r.boxes is not None else 0
        line = f"图片: {Path(r.path).name}  检出皮带数: {n}"
        if r.masks is not None and r.masks.data is not None:
            line += f"  分割轮廓数: {len(r.masks)}"
        print(line)
        summary_lines.append(line)

        # 打印每个 box 的置信度
        if r.boxes is not None:
            for box in r.boxes:
                cls_id = int(box.cls.item())
                cls_name = names.get(cls_id, str(cls_id))
                conf = float(box.conf.item())
                xyxy = [round(float(v), 1) for v in box.xyxy[0].tolist()]
                print(f"   └─ {cls_name}  conf={conf:.3f}  bbox={xyxy}")

    # 写报告
    report_path = save_dir / "report.txt"
    report_path.write_text(
        f"# Day4 作业③ 皮带边缘分割识别报告\n"
        f"模型: {model_path}\n"
        f"输入: {args.source}\n"
        f"imgsz: {args.imgsz}    conf: {args.conf}\n"
        f"device: {args.device or 'auto'}\n"
        f"\n--- 结果 ---\n" + "\n".join(summary_lines) + "\n",
        encoding="utf-8",
    )

    # 把 YOLO 自己的输出目录里的可视化图复制/链接到 save_dir
    runs_dir = Path(args.project) / args.name
    if runs_dir.exists():
        # 找最新一张图
        images_dir = runs_dir / "images" if (runs_dir / "images").exists() else runs_dir
        pngs = sorted(images_dir.glob("*.jpg")) + sorted(images_dir.glob("*.png"))
        print(f"\n[INFO] 识别后照片保存在: {runs_dir.resolve()}")
        print(f"[INFO] 共 {len(pngs)} 张可视化结果")
        print(f"[INFO] 报告已写入: {report_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())