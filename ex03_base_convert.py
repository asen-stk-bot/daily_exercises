# -*- coding: utf-8 -*-
"""练习(PPT第24页)：进制转换
   接收输入的一个十进制数，把它转成二进制、十六进制输出(不使用 bin()/hex() 内置函数)
"""
HEX_DIGITS = "0123456789ABCDEF"   # 十六进制数字表


def dec_to_bin(n):
    """十进制转二进制，返回字符串(如 10 -> '1010')"""
    if n == 0:
        return "0"
    negative = n < 0
    n = abs(n)
    bits = ""
    while n > 0:
        bits = str(n % 2) + bits   # 余数逆序排列
        n //= 2
    return "-" + bits if negative else bits


def dec_to_hex(n):
    """十进制转十六进制，返回字符串(如 255 -> 'FF')"""
    if n == 0:
        return "0"
    negative = n < 0
    n = abs(n)
    digits = ""
    while n > 0:
        digits = HEX_DIGITS[n % 16] + digits
        n //= 16
    return "-" + digits if negative else digits


if __name__ == "__main__":
    s = input("请输入一个十进制整数: ")
    try:
        n = int(s)
    except ValueError:
        print("输入不是有效的整数！")
    else:
        print(f"十进制 {n}")
        print(f"二进制  = {dec_to_bin(n)}   (内置函数验证: {bin(abs(n))[2:]})")
        print(f"十六进制 = {dec_to_hex(n)}   (内置函数验证: {hex(abs(n))[2:].upper()})")
