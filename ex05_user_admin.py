# -*- coding: utf-8 -*-
"""练习(PPT第35页)：User 类与 Admin 类(继承)
   User: first_name/last_name 属性, describe_user/greet_user 方法
   Admin: 继承 User, privileges 属性 + show_privileges() 方法
"""


class User:
    """普通用户类"""

    def __init__(self, first_name, last_name):
        self.first_name = first_name   # 名
        self.last_name = last_name     # 姓

    def describe_user(self):
        """打印用户的信息"""
        print(f"用户信息: {self.last_name} {self.first_name}")

    def greet_user(self):
        """打印问候语"""
        print(f"你好, {self.last_name}{self.first_name}, 欢迎回来!")


class Admin(User):
    """管理员类，是 User 的一种特殊用户(继承)"""

    def __init__(self, first_name, last_name, privileges=None):
        super().__init__(first_name, last_name)      # 调用父类构造
        # privileges 存储由字符串组成的权限列表
        self.privileges = privileges if privileges is not None else [
            "can add post",
            "can delete post",
            "can ban user",
        ]

    def show_privileges(self):
        """显示管理员的权限"""
        print(f"管理员 {self.last_name}{self.first_name} 拥有以下权限:")
        for privilege in self.privileges:
            print(f"  - {privilege}")


if __name__ == "__main__":
    print("--- 创建普通用户 ---")
    user = User("San", "Zhang")
    user.describe_user()
    user.greet_user()

    print()
    print("--- 创建管理员 ---")
    admin = Admin("Wei", "Li")
    admin.describe_user()        # 继承自 User 的方法
    admin.greet_user()           # 继承自 User 的方法
    admin.show_privileges()      # Admin 自己的方法
