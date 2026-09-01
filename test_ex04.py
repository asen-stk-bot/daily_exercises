# -*- coding: utf-8 -*-
"""练习(PPT第35页)：用 unittest 为 max_nested_depth 写至少 5 个单元测试用例并执行"""
import unittest

from ex04_nested_depth import max_nested_depth


class TestMaxNestedDepth(unittest.TestCase):

    def test_flat_list(self):
        """[1, 2, 3] 的嵌套深度为 1"""
        self.assertEqual(max_nested_depth([1, 2, 3]), 1)

    def test_ppt_example(self):
        """PPT 例子 [[1], [2, [3]]] 的嵌套深度为 3"""
        self.assertEqual(max_nested_depth([[1], [2, [3]]]), 3)

    def test_empty_list(self):
        """空列表 [] 的嵌套深度为 1"""
        self.assertEqual(max_nested_depth([]), 1)

    def test_deep_nesting(self):
        """多层嵌套 [[[[42]]]] 的嵌套深度为 4"""
        self.assertEqual(max_nested_depth([[[[42]]]]), 4)

    def test_mixed_branches(self):
        """不同分支深度不同时取最大值 [1, [2], [3, [4]]] 深度为 3"""
        self.assertEqual(max_nested_depth([1, [2], [3, [4]]]), 3)

    def test_long_chain(self):
        """链式嵌套 [1, [2, [3, [4, [5]]]], 6] 深度为 5"""
        self.assertEqual(max_nested_depth([1, [2, [3, [4, [5]]]], 6]), 5)


if __name__ == "__main__":
    unittest.main(verbosity=2)
