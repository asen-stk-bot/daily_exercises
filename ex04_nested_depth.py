# -*- coding: utf-8 -*-
"""练习(PPT第35页)：写一个函数，传入的参数是一个列表(元素可能也是列表)，
   返回该列表最大的嵌套深度。
   例如 [1, 2, 3] 深度为 1；[[1], [2, [3]]] 深度为 3。
"""


def max_nested_depth(lst):
    """返回列表的最大嵌套深度"""
    depth = 1                       # 最外层列表本身算第 1 层
    for item in lst:
        if isinstance(item, list):  # 元素还是列表，则递归往下找
            depth = max(depth, 1 + max_nested_depth(item))
    return depth


if __name__ == "__main__":
    cases = [
        [1, 2, 3],
        [[1], [2, [3]]],
        [],
        [[[[42]]]],
        [1, [2, [3, [4, [5]]]], 6],
    ]
    for c in cases:
        print(f"max_nested_depth({c!r}) = {max_nested_depth(c)}")
