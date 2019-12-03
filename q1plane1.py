import xlrd
import operator
import numpy as np
import math
import time

time_start=time.time()
class point():
    def __init__(self, number, x, y, z, type = -1, pmark = - 1, distance = None):
        self.Number = number
        self.X = x
        self.Y = y
        self.Z = z
        self.Type = type
        self.Pmark = pmark
        self.Distance = distance
        self.XYZ = (x,y,z)

class showdata():
    def __init__(self, point):
        self.now_point = point
        self.h = 0
        self.v = 0
        self.ans_list = [0]
        self.h_list = [0]
        self.v_list = [0]


def space_distance(A, B):
    return math.sqrt(math.pow(A[0] - B[0], 2) + math.pow(A[1] - B[1], 2) + math.pow(A[2] - B[2], 2))


def read_excel(filename, sheetname):
    book = xlrd.open_workbook(filename)
    sheet = book.sheet_by_name(sheetname)
    array = []
    rows = sheet.nrows  # 获取行数
    for r in range(rows):  # 读取每一行的数据
        r_values = sheet.row_values(r)
        array.append(r_values)
    return array


def read_text(filename):
    f = open(filename)
    line = f.readline()
    data_list = []
    while line:
        num = list(map(float, line.split()))
        data_list.append(num)
        line = f.readline()
    f.close()
    data_array = np.array(data_list)
    return data_array


def getPoint():
    Point = []
    for i in range(2, len(p)):
        _point = point(int(p[i][0]), round(p[i][1], 2), round(p[i][2], 2), round(p[i][3], 2), p[i][4], int(p[i][5]),
                       distance[i - 2].tolist())
        Point.append(_point)
    for i in range(len(Point)):
        Point[i].Distance2B = Point[i].Distance[-1]
    return Point


def get0(O1, O2, C):
    dis1 = space_distance(O1, C)
    dis2 = space_distance(O2, C)
    if dis2 < dis1:
        return O2
    else:
        return O1


def curvePath(A, B, C):
    n1 = (B.X - A.X, B.Y - A.Y, B.Z - A.Z)  ##AB直线向量
    n2 = ((A.Y - B.Y) * (A.Z - C.Z) - (A.Z - B.Z) * (A.Y - C.Y), (A.Z - B.Z) * (A.X - C.X) - (A.X - B.X) * (A.Z - C.Z),
          (A.X - B.X) * (A.Y - C.Y) - (A.Y - B.Y) * (A.X - C.X))  ##ABC平面法向量
    d1 = -(n2[0] * A.X + n2[1] * A.Y + n2[2] * A.Z)
    n3 = (n1[1] * n2[2] - n1[2] * n2[1], n1[2] * n2[0] - n1[0] * n2[2], n1[0] * n2[1] - n1[1] * n2[0])  ##垂直n1,n2向量的直线向量
    sq = math.sqrt(n3[0] * n3[0] + n3[1] * n3[1] + n3[2] * n3[2])
    t1, t2 = 200 / sq, (-200) / sq
    O1 = (B.X + n3[0] * t1, B.Y + n3[1] * t1, B.Z + n3[2] * t1)
    O2 = (B.X + n3[0] * t2, B.Y + n3[1] * t2, B.Z + n3[2] * t2)
    O = get0(O1, O2, (C.X, C.Y, C.Z))
    disCD = math.sqrt(math.pow(space_distance(O, (C.X, C.Y, C.Z)), 2) - 40000.0)
    print("O:", O)
    d2 = O[0] * O[0] + O[1] * O[1] + O[2] * O[2] - C.X * C.X - C.Y * C.Y - C.Z * C.Z - 40000.0 + disCD * disCD
    n4 = (
        (2 * (C.Y - O[1]) * n2[2]) - (2 * (C.Z - O[2]) * n2[1]),
        (2 * (C.Z - O[2]) * n2[0]) - (2 * (C.X - O[0]) * n2[2]),
        (2 * (C.X - O[0]) * n2[1]) - (2 * (C.Y - O[1]) * n2[0]))
    z = (n2[1] * (-d2) - 2 * (C.Y - O[1]) * (-d1)) / (2 * n2[1] * (C.Z - O[2]) - 2 * (C.Y - O[1]) * n2[2])
    y = ((-d1) - n2[2] * z) / n2[1]
    x = 0.0
    func1 = (n4[0] * n4[0] + n4[1] * n4[1] + n4[2] * n4[2],
             -(2 * n4[0] * O[0] - 2 * n4[1] * (y - O[1]) - 2 * n4[2] * (z - O[2])),
             O[0] * O[0] + (y - O[1]) * (y - O[1]) + (z - O[2]) * (z - O[2]) - 40000.0)
    t3, t4 = (-func1[1] + math.sqrt(func1[1] * func1[1] - 4 * func1[0] * func1[2])) / (2 * func1[0]), (
            -func1[1] - math.sqrt(func1[1] * func1[1] - 4 * func1[0] * func1[2])) / (2 * func1[0])
    D1 = (x + n4[0] * t3, y + n4[1] * t3, z + n4[2] * t3)
    D2 = (x + n4[0] * t4, y + n4[1] * t4, z + n4[2] * t4)
    print(D1, D2)
    bd1 = (D1[0] - B.X, D1[1] - B.Y, D1[2] - B.Z)
    bd2 = (D2[0] - B.X, D2[1] - B.Y, D2[2] - B.Z)
    cos1 = (bd1[0] * n1[0] + bd1[1] * n1[1] + bd1[2] * n1[2])/(space_distance((0,0,0),bd1)*space_distance((0,0,0),n1))
    cos2 = (bd2[0] * n1[0] + bd2[1] * n1[1] + bd2[2] * n1[2])/(space_distance((0,0,0),bd2)*space_distance((0,0,0),n1))
    print(cos1,cos2)
    if cos1 > cos2:
        D = D1
        if cos1 < 0:
            l = 2 * math.pi * 200.0 - (2 * 200.0 *math.asin(space_distance(B.XYZ,D)/ 400.0))
        else:
            l = (2 * 200.0 *math.asin(space_distance(B.XYZ,D)/ 400.0))
    else:
        D = D2
        if cos2 < 0:
            l = 2 * math.pi * 200.0 - (2 * 200.0 * math.asin(space_distance(B.XYZ, D) / 400.0))
        else:
            l = (2 * 200.0 * math.asin(space_distance(B.XYZ, D) / 400.0))

    print(l,disCD)
    print(D)
    # print(space_distance(B.XYZ,C.XYZ))
    return [l+disCD,D]


distance = read_text(r"distance1.txt")
p = read_excel('plane1.xlsx', 'data1')
Point = getPoint()
S = showdata(Point[0])
# curvePath(Point[0],Point[303],Point[199])
# end_point = Point[-1]
# end_distance = Point[0].Distance[-1]
cmp = operator.attrgetter('Distance2B', )
Point.sort(key=cmp)



def correction(l, point):
    global S
    if point.Type == 0:
        S.h += distance[S.now_point.Number][point.Number] * l
        S.h_list.append(round(S.h,2))
        S.h = 0
        S.v += distance[S.now_point.Number][point.Number] * l
        S.v_list.append(round(S.v,2))
        S.now_point = point
        S.ans_list.append(S.now_point.Number)
        print(S.now_point.X, S.now_point.Y, S.now_point.Z)
    else:
        S.h += distance[S.now_point.Number][point.Number] * l
        S.h_list.append(round(S.h,2))
        S.v += distance[S.now_point.Number][point.Number] * l
        S.v_list.append(round(S.v,2))
        S.v = 0
        S.now_point = point
        S.ans_list.append(S.now_point.Number)
        print(S.now_point.X, S.now_point.Y, S.now_point.Z)

def A_star(a1, a2, b1, b2, o, l):
    global S
    total_distance = 0
    while S.now_point.Distance2B * l + S.h > o or S.now_point.Distance2B * l + S.v > o:
        OPEN = []
        if S.h == S.v:  ##第一步
            for point in Point:
                ## 水平校正点
                if point.Type == 0 and (S.v + distance[S.now_point.Number][point.Number] * l) <= b1 and (
                        S.h + distance[S.now_point.Number][point.Number] * l) <= b2:
                    OPEN.append(point)
                ##垂直校正点
                elif point.Type == 1 and (S.v + distance[S.now_point.Number][point.Number] * l) <= a1 and (
                        S.h + distance[S.now_point.Number][point.Number] * l) <= a2:
                    OPEN.append(point)
        elif S.h > S.v:
            for point in Point:
                ## 水平校正点
                if point.Type == 0 and (S.v + distance[S.now_point.Number][point.Number] * l) <= b1 and (
                        S.h + distance[S.now_point.Number][point.Number] * l) <= b2:
                    OPEN.append(point)
        else:
            for point in Point:
                ## 垂直校正点
                if point.Type == 1 and (S.v + distance[S.now_point.Number][point.Number] * l) <= a1 and (
                        S.h + distance[S.now_point.Number][point.Number] * l) <= a2:
                    OPEN.append(point)
        min = 100000000000000
        for point in OPEN:
            if point.Distance2B + distance[S.now_point.Number][point.Number] < min:
                cpoint = point
                min = point.Distance2B + distance[S.now_point.Number][point.Number]
        total_distance += distance[S.now_point.Number][cpoint.Number]
        correction(l, cpoint)


    total_distance += S.now_point.Distance2B
    S.h += S.now_point.Distance2B * l
    S.v += S.now_point.Distance2B * l
    S.h_list.append(round(S.h, 2))
    S.v_list.append(round(S.v, 2))
    print(distance[0][-1], total_distance)
    return [S.ans_list, S.h_list, S.v_list]

def greedy(a1, a2, b1, b2, o, l):  # 6个参数
    global S
    total_distance = 0
    while S.now_point.Distance2B * l + S.h > o or S.now_point.Distance2B * l + S.v > o:
        if S.h == S.v:  ##第一步
            for point in Point:
                ## 水平校正点
                if point.Type == 0 and (S.v + distance[S.now_point.Number][point.Number] * l) <= b1 and (
                        S.h + distance[S.now_point.Number][point.Number] * l) <= b2:
                    total_distance += distance[S.now_point.Number][point.Number]
                    correction(l, point)
                    break
                ##垂直校正点
                elif point.Type == 1 and (S.v + distance[S.now_point.Number][point.Number] * l) <= a1 and (
                        S.h + distance[S.now_point.Number][point.Number] * l) <= a2:
                    total_distance += distance[S.now_point.Number][point.Number]
                    correction(l, point)
                    break
        elif S.h > S.v:
            for point in Point:
                ## 水平校正点
                if point.Type == 0 and (S.v + distance[S.now_point.Number][point.Number] * l) <= b1 and (
                        S.h + distance[S.now_point.Number][point.Number] * l) <= b2:
                    total_distance += distance[S.now_point.Number][point.Number]
                    correction(l, point)
                    break
        else:
            for point in Point:
                ## 垂直校正点
                if point.Type == 1 and (S.v + distance[S.now_point.Number][point.Number] * l) <= a1 and (
                        S.h + distance[S.now_point.Number][point.Number] * l) <= a2:
                    total_distance += distance[S.now_point.Number][point.Number]
                    correction(l, point)
                    break
    total_distance += S.now_point.Distance2B
    S.h += S.now_point.Distance2B * l
    S.v += S.now_point.Distance2B * l
    S.h_list.append(round(S.h,2))
    S.v_list.append(round(S.v,2))
    print(distance[0][-1],total_distance)
    return [S.ans_list, S.h_list, S.v_list]


[ans_list, h_list, v_list] = greedy(25, 15, 20, 25, 30, 0.001)
# [ans_list, h_list, v_list] = A_star(25, 15, 20, 25, 30, 0.001)
print(ans_list)
print("垂直误差:",v_list)
print("水平误差:",h_list)
print(np.sum(h_list) + np.sum(v_list))
# for point in Point:
#     if point.Number not in ans_list:
#         print(point.X,point.Y,point.Z)
time_end=time.time()
print('totally cost',time_end-time_start)
# min = 1000000000000000
# for i in distance:
#     for j in i:
#         if j < min and j != 0:
#             min = j
# print(min)
