import numpy as np
import random


def plucker(a, b):
    l0 = a[0] * b[1] - b[0] * a[1]
    l1 = a[0] * b[2] - b[0] * a[2]
    l2 = a[0] - b[0]
    l3 = a[1] * b[2] - b[1] * a[2]
    l4 = a[2] - b[2]
    l5 = b[1] - a[1]
    return [l0, l1, l2, l3, l4, l5]


def sideOp(a, b):
    res = a[0] * b[4] + a[1] * b[5] + a[2] * b[3] + a[3] * b[2] + a[4] * b[0] + a[5] * b[1]
    return res


# 定义点
cnt = 0
for j in range(1):
    a = (-0, -0, -1)
    b = [-0.51488, 95.151423, -30.85161]

    v0 = (34.652218, 68.443845, 23.021445)
    v1 = (34.652218, 68.443845, -24.959573)
    v2 = (-29.658962, 68.443845, -26.349818)
    # for i in range(3):
    #     a.append(random.random(1000, 5000))
    #     b.append(random.randint(-1000, 1000))
    #     v0.append(random.randint(-1000, 1000))
    #     v1.append(random.randint(-1000, 1000))
    #     v2.append(random.randint(-1000, 1000))
    # 计算
    e1 = plucker(v1, v0)
    e2 = plucker(v2, v1)
    e3 = plucker(v0, v2)
    L = plucker(a, b)

    s1 = sideOp(L, e1)
    s2 = sideOp(L, e2)
    s3 = sideOp(L, e3)
    if abs(s1) > 0 and abs(s2) > 0 and abs(s3) > 0:
        L2 = plucker(a, v0)
        L3 = plucker(v0, b)
        L4 = plucker(v1, v2)
        s1 = sideOp(L4, L3)
        s2 = sideOp(L4, L2)
        if s1 * s2 > 0:
            cnt += 1
print(cnt)