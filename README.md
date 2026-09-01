# Day2_exercises · Python 课堂练习（Day 2）

软件工程专业日常作业，包含 5 个独立练习 + 1 个单元测试文件。

## 练习清单

| 文件 | 主题 | 说明 |
| --- | --- | --- |
| `ex01_scores.py` | 字典与列表 | 用字典+列表表示班级成绩，求单科第一、总分第一、挂科名单 |
| `ex02_login.py` | 循环与条件 | 简单用户登录系统，限制最大尝试次数 |
| `ex03_base_convert.py` | 进制转换 | 十进制转二进制/十六进制（不使用 bin()/hex()） |
| `ex04_nested_depth.py` | 递归 | 计算嵌套列表的最大深度 |
| `ex05_user_admin.py` | 类与继承 | User 类与 Admin 子类（属性、方法、特权展示） |
| `test_ex04.py` | 单元测试 | 用 unittest 为 max_nested_depth 编写测试用例 |

## 运行方式

```bash
# 单独运行某个练习
python ex01_scores.py

# 运行单元测试
python -m unittest test_ex04.py
```

## 环境

- Python 3.x
- 依赖：仅标准库（unittest 等），无需额外安装
