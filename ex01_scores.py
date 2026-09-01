# -*- coding: utf-8 -*-
"""练习(PPT第13页)：用字典和列表表示一个班的期末考试成绩
   求单科第一、总分第一的学生名单，以及挂科的学生名单
"""
# 全班成绩：列表 + 字典，每个学生一个字典
students = [
    {"学号": "2025001", "姓名": "张三",   "班级": "1班", "高数": 85, "英语": 78, "Java编程": 92},
    {"学号": "2025002", "姓名": "李四",   "班级": "1班", "高数": 59, "英语": 66, "Java编程": 71},
    {"学号": "2025003", "姓名": "王五",   "班级": "2班", "高数": 90, "英语": 95, "Java编程": 88},
    {"学号": "2025004", "姓名": "赵六",   "班级": "2班", "高数": 72, "英语": 55, "Java编程": 64},
    {"学号": "2025005", "姓名": "钱七",   "班级": "1班", "高数": 68, "英语": 82, "Java编程": 45},
    {"学号": "2025006", "姓名": "孙八",   "班级": "3班", "高数": 96, "英语": 88, "Java编程": 93},
    {"学号": "2025007", "姓名": "周九",   "班级": "3班", "高数": 58, "英语": 52, "Java编程": 49},
    {"学号": "2025008", "姓名": "吴十",   "班级": "2班", "高数": 76, "英语": 84, "Java编程": 80},
]

subjects = ["高数", "英语", "Java编程"]

print("=" * 50)
print("一、单科第一的学生名单")
print("=" * 50)
for subject in subjects:
    top = max(students, key=lambda s: s[subject])
    print(f"{subject} 第一名: {top['姓名']}({top['班级']}) 成绩 {top[subject]} 分")

print()
print("=" * 50)
print("二、总分第一的学生名单")
print("=" * 50)
total_scores = {s["姓名"]: sum(s[sub] for sub in subjects) for s in students}
top_total = max(students, key=lambda s: sum(s[sub] for sub in subjects))
print("各学生总分:", total_scores)
print(f"总分第一: {top_total['姓名']}({top_total['班级']}) "
      f"总分 {sum(top_total[sub] for sub in subjects)} 分")

print()
print("=" * 50)
print("三、挂科的学生名单(任一科目低于60分)")
print("=" * 50)
failed = [s for s in students if any(s[sub] < 60 for sub in subjects)]
if failed:
    for s in failed:
        bad = [f"{sub}({s[sub]}分)" for sub in subjects if s[sub] < 60]
        print(f"{s['学号']} {s['姓名']}({s['班级']}): " + ", ".join(bad))
else:
    print("没有挂科学生")
