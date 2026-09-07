#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Day5 · 作业①/④：labelme JSON → YOLO segment TXT + 数据集划分

对应讲义 D:\Day5_样本标注_数据预处理_模型训练.pptx slide 18 的"参考实现"，
本脚本是**自己从零实现**的版本（满足作业④鼓励要求），结构与可读性更佳。

参考实现命令（slide 18）：
    python label2yoloseg.py --image_dir d:\belt_shift --json_dir d:\belt_shift \
        --save_dir d:\belt_shift_split2 --train_ratio 0.8

PPT slide 12 中给出的转换示例（belt 多边形）：
    labelme shapes: 多边形 4 个点 (304,1078), (568,455), (934,443), (1183,1079)
    yolo seg txt:   0 0.158 0.998 0.296 0.421 0.486 0.410 0.616 0.999
    转换规则：cls_id, 然后每对 (x/width, y/height)，全部归一化到 0~1

用法：
    python 01_label2yoloseg.py \
        --image_dir D:\皮带监控\images \
        --json_dir  D:\皮带监控\jsons \
        --save_dir  D:\皮带监控\belt_seg_split \
        --train_ratio 0.8 \
        --label "belt:0" \
        [--seed 42]
"""

from __future__ import annotations

import argparse
import json
import random
import shutil
import sys
from pathlib import Path
from typing import Dict, List, Tuple


# ----------------------------- 核心工具 ----------------------------- #

def parse_label_args(items: List[str]) -> Dict[str, int]:
    """解析 --label "belt:0" "crack:1" 形式的参数。"""
    label_map: Dict[str, int] = {}
    for item in items:
        if ":" not in item:
            raise ValueError(f"--label 格式应为 'name:id', 收到: {item}")
        name, idx = item.split(":", 1)
        label_map[name.strip()] = int(idx.strip())
    return label_map


def load_labelme_json(json_path: Path) -> dict:
    with json_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def shape_to_yolo_seg(shape: dict, img_w: int, img_h: int, label_to_id: Dict[str, int]
                      ) -> str | None:
    """
    把 labelme 的一个 shape 转成 YOLO seg 的一行。
    输入 shape 形如：
        {"label": "belt", "shape_type": "polygon", "points": [[x1, y1], [x2, y2], ...]}
    输出（ppt slide 12 的格式）：
        cls_id x1/W y1/H x2/W y2/H ... xn/W yn/H
    """
    if shape.get("shape_type") != "polygon":
        return None
    label = shape.get("label")
    if label not in label_to_id:
        return None
    points = shape.get("points") or []
    if len(points) < 3:
        # 至少 3 个点才是一个合法多边形
        return None
    cls_id = label_to_id[label]
    coords: List[str] = []
    for x, y in points:
        nx = max(0.0, min(1.0, x / img_w))
        ny = max(0.0, min(1.0, y / img_h))
        coords.append(f"{nx:.6f}")
        coords.append(f"{ny:.6f}")
    return f"{cls_id} " + " ".join(coords)


def convert_one(json_path: Path, image_dir: Path, label_to_id: Dict[str, int]
                ) -> Tuple[str, str] | None:
    """
    转换一个 labelme json：返回 (txt 字符串, 对应图片文件名)。
    图片文件必须和 json 同名（同名不同后缀，如 xxx.json / xxx.jpg）。
    """
    data = load_labelme_json(json_path)
    img_h = data.get("imageHeight")
    img_w = data.get("imageWidth")
    if not img_h or not img_w:
        return None

    lines: List[str] = []
    for shape in data.get("shapes", []):
        line = shape_to_yolo_seg(shape, img_w, img_h, label_to_id)
        if line:
            lines.append(line)

    if not lines:
        # 该图无任何目标，跳过
        return None
    return "\n".join(lines) + "\n", json_path.stem


# ----------------------------- 划分 + 输出 ----------------------------- #

def split_train_val(items: List, train_ratio: float, seed: int) -> Tuple[List, List]:
    rng = random.Random(seed)
    items = list(items)
    rng.shuffle(items)
    n_train = max(1, int(len(items) * train_ratio))
    if n_train >= len(items):
        n_train = len(items) - 1
    return items[:n_train], items[n_train:]


def safe_link_or_copy(src: Path, dst: Path) -> None:
    """优先软链接，失败则复制。"""
    try:
        if dst.exists():
            dst.unlink()
        dst.symlink_to(src.resolve())
    except (OSError, NotImplementedError):
        shutil.copy2(src, dst)


def write_yaml(save_dir: Path, label_to_id: Dict[str, int]) -> None:
    """生成 dataset/data.yaml（PPT slide 16 格式）。"""
    yaml_path = save_dir / "data.yaml"
    names_lines = "\n".join(f"  {i}: {name}" for name, i in
                            sorted(label_to_id.items(), key=lambda kv: kv[1]))
    yaml_path.write_text(
        f"path: {save_dir.resolve().as_posix()}\n"
        f"train: train/images\n"
        f"val:   val/images\n"
        f"test:  ''\n"
        f"\n"
        f"names:\n{names_lines}\n",
        encoding="utf-8",
    )


# ----------------------------- 主流程 ----------------------------- #

def main() -> int:
    parser = argparse.ArgumentParser(
        description="labelme json → YOLO segment txt + 数据集划分",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--image_dir", type=str, required=True,
                        help="图片所在目录（与 json 同名不同后缀）")
    parser.add_argument("--json_dir", type=str, required=True,
                        help="labelme json 所在目录")
    parser.add_argument("--save_dir", type=str, required=True,
                        help="划分后数据集输出目录")
    parser.add_argument("--train_ratio", type=float, default=0.8,
                        help="训练集比例，余下为 val")
    parser.add_argument("--label", nargs="+", default=["belt:0"],
                        help='标签映射，可多个，格式 "name:id"，如 --label "belt:0" "crack:1"')
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    image_dir = Path(args.image_dir)
    json_dir = Path(args.json_dir)
    save_dir = Path(args.save_dir)

    if not image_dir.exists():
        print(f"[ERROR] image_dir 不存在: {image_dir}", file=sys.stderr)
        return 1
    if not json_dir.exists():
        print(f"[ERROR] json_dir 不存在: {json_dir}", file=sys.stderr)
        return 1

    label_to_id = parse_label_args(args.label)
    print(f"[INFO] 标签映射: {label_to_id}")

    # 找所有 json
    json_paths = sorted(json_dir.glob("*.json"))
    if not json_paths:
        print(f"[ERROR] {json_dir} 下没有 json 文件", file=sys.stderr)
        return 1
    print(f"[INFO] 发现 {len(json_paths)} 个 json")

    converted: List[Tuple[str, str, Path]] = []  # (txt, stem, json_path)
    for jp in json_paths:
        result = convert_one(jp, image_dir, label_to_id)
        if not result:
            continue
        txt, stem = result
        # 找图片
        img_path = None
        for ext in (".jpg", ".jpeg", ".png", ".bmp", ".webp"):
            cand = image_dir / f"{stem}{ext}"
            if cand.exists():
                img_path = cand
                break
        if img_path is None:
            print(f"[WARN] 没找到 {stem} 对应图片，跳过", file=sys.stderr)
            continue
        converted.append((txt, stem, img_path))

    if not converted:
        print("[ERROR] 一个 json 都没成功转换，请检查 label 与数据", file=sys.stderr)
        return 1
    print(f"[INFO] 有效样本: {len(converted)}")

    # 划分
    train_set, val_set = split_train_val(converted, args.train_ratio, args.seed)
    print(f"[INFO] train: {len(train_set)},  val: {len(val_set)}")

    # 输出目录
    for sub in ("train/images", "train/labels", "val/images", "val/labels"):
        (save_dir / sub).mkdir(parents=True, exist_ok=True)

    for split, items in (("train", train_set), ("val", val_set)):
        for txt, stem, img_path in items:
            (save_dir / split / "labels" / f"{stem}.txt").write_text(txt, encoding="utf-8")
            safe_link_or_copy(img_path, save_dir / split / "images" / img_path.name)

    write_yaml(save_dir, label_to_id)

    print(f"\n[OK] 数据集已生成: {save_dir}")
    print(f"     ├─ train: {len(train_set)} 张")
    print(f"     ├─ val:   {len(val_set)} 张")
    print(f"     └─ data.yaml 已写入")
    print("\n下一步：进入该目录运行 yolo segment train ...")
    print(f"  cd {save_dir}")
    print("  yolo segment train model=yolo11n-seg.pt data=data.yaml epochs=100 imgsz=640")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())