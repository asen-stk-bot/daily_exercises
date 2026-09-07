#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Day5 · 作业①/④：labelimg XML → YOLO detect TXT + 数据集划分

对应讲义 D:\Day5_样本标注_数据预处理_模型训练.pptx slide 19 的"参考实现"，
本脚本是**自己从零实现**的版本（满足作业④鼓励要求）。

参考实现命令（slide 19）：
    python samplesplit.py --image D:/样本及标注/烟火  --xml  D:/样本及标注/烟火 \
        --savedir d:/smoke_fire_split1

PPT slide 13 中给出的转换示例（labelimg 框）：
    <bndbox>
        <xmin>181</xmin><ymin>53</ymin>
        <xmax>279</xmax><ymax>95</ymax>
    </bndbox>
    ↓
    13 0.817857 0.462025 0.350000 0.265823
    格式: cls_id,  cx/W, cy/H, w/W, h/H   全部归一化

用法：
    python 02_samplesplit.py \
        --image_dir D:\烟火\images \
        --xml_dir   D:\烟火\xmls \
        --save_dir  D:\烟火\smoke_fire_split1 \
        --train_ratio 0.8 \
        --label "smoke:0" "fireworks:1"
"""

from __future__ import annotations

import argparse
import random
import shutil
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Tuple


# ----------------------------- 核心工具 ----------------------------- #

def parse_label_args(items: List[str]) -> Dict[str, int]:
    label_map: Dict[str, int] = {}
    for item in items:
        if ":" not in item:
            raise ValueError(f"--label 格式应为 'name:id', 收到: {item}")
        name, idx = item.split(":", 1)
        label_map[name.strip()] = int(idx.strip())
    return label_map


def load_labelimg_xml(xml_path: Path) -> Tuple[int, int, list]:
    """
    解析 labelimg 的 VOC 格式 xml。
    返回 (width, height, [(name, xmin, ymin, xmax, ymax), ...])
    """
    tree = ET.parse(xml_path)
    root = tree.getroot()
    size = root.find("size")
    if size is None:
        return 0, 0, []
    w = int(size.findtext("width", "0"))
    h = int(size.findtext("height", "0"))
    boxes = []
    for obj in root.findall("object"):
        name = obj.findtext("name", default="").strip()
        if not name:
            continue
        difficult = obj.findtext("difficult", default="0").strip()
        truncated = obj.findtext("truncated", default="0").strip()
        # 默认行为：difficult/truncated 都保留为正样本（YOLO 自身会处理）
        _ = difficult, truncated
        bnd = obj.find("bndbox")
        if bnd is None:
            continue
        try:
            xmin = float(bnd.findtext("xmin", "0"))
            ymin = float(bnd.findtext("ymin", "0"))
            xmax = float(bnd.findtext("xmax", "0"))
            ymax = float(bnd.findtext("ymax", "0"))
        except ValueError:
            continue
        if xmax <= xmin or ymax <= ymin:
            continue
        boxes.append((name, xmin, ymin, xmax, ymax))
    return w, h, boxes


def to_yolo_det_line(name: str, xmin: float, ymin: float, xmax: float, ymax: float,
                     W: int, H: int, label_to_id: Dict[str, int]) -> str | None:
    if name not in label_to_id:
        return None
    cx = (xmin + xmax) / 2.0 / W
    cy = (ymin + ymax) / 2.0 / H
    bw = (xmax - xmin) / W
    bh = (ymax - ymin) / H
    cx, cy, bw, bh = (max(0.0, min(1.0, v)) for v in (cx, cy, bw, bh))
    return f"{label_to_id[name]} {cx:.6f} {cy:.6f} {bw:.6f} {bh:.6f}"


def convert_one(xml_path: Path, label_to_id: Dict[str, int]) -> Tuple[str, str] | None:
    W, H, boxes = load_labelimg_xml(xml_path)
    if not W or not H or not boxes:
        return None
    lines = []
    for name, xmin, ymin, xmax, ymax in boxes:
        line = to_yolo_det_line(name, xmin, ymin, xmax, ymax, W, H, label_to_id)
        if line:
            lines.append(line)
    if not lines:
        return None
    return "\n".join(lines) + "\n", xml_path.stem


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
    try:
        if dst.exists():
            dst.unlink()
        dst.symlink_to(src.resolve())
    except (OSError, NotImplementedError):
        shutil.copy2(src, dst)


def write_yaml(save_dir: Path, label_to_id: Dict[str, int], task: str = "detect") -> None:
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
        description="labelimg xml → YOLO detect txt + 数据集划分",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--image_dir", type=str, required=True,
                        help="图片所在目录（与 xml 同名不同后缀）")
    parser.add_argument("--xml_dir", type=str, required=True,
                        help="labelimg xml 所在目录")
    parser.add_argument("--save_dir", type=str, required=True,
                        help="划分后数据集输出目录")
    parser.add_argument("--train_ratio", type=float, default=0.8)
    parser.add_argument("--label", nargs="+",
                        default=["smoke:0", "fireworks:1"],
                        help='标签映射，如 --label "smoke:0" "fireworks:1"')
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    image_dir = Path(args.image_dir)
    xml_dir = Path(args.xml_dir)
    save_dir = Path(args.save_dir)

    if not image_dir.exists():
        print(f"[ERROR] image_dir 不存在: {image_dir}", file=sys.stderr)
        return 1
    if not xml_dir.exists():
        print(f"[ERROR] xml_dir 不存在: {xml_dir}", file=sys.stderr)
        return 1

    label_to_id = parse_label_args(args.label)
    print(f"[INFO] 标签映射: {label_to_id}")

    xml_paths = sorted(xml_dir.glob("*.xml"))
    if not xml_paths:
        print(f"[ERROR] {xml_dir} 下没有 xml 文件", file=sys.stderr)
        return 1
    print(f"[INFO] 发现 {len(xml_paths)} 个 xml")

    converted: List[Tuple[str, str, Path]] = []  # (txt, stem, img_path)
    for xp in xml_paths:
        result = convert_one(xp, label_to_id)
        if not result:
            continue
        txt, stem = result
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
        print("[ERROR] 一个 xml 都没成功转换，请检查 label 与数据", file=sys.stderr)
        return 1
    print(f"[INFO] 有效样本: {len(converted)}")

    train_set, val_set = split_train_val(converted, args.train_ratio, args.seed)
    print(f"[INFO] train: {len(train_set)},  val: {len(val_set)}")

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
    print("\n下一步：进入该目录运行 yolo detect train ...")
    print(f"  cd {save_dir}")
    print("  yolo detect train model=yolo11n.pt data=data.yaml epochs=100 imgsz=640")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())