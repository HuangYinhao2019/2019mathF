import xlrd
import operator
import numpy as np
import math
import time
import copy
import random

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
        self.list_pnumber = 0

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
def issuccess(T,p,a1=20, a2=10, b1=15, b2=20, o=20, l=0.001):
    v = 0
    h = 0
    count_p = 0
    for i in range(1,len(T)):
        v += distance[T[i-1]][T[i]] * l
        h += distance[T[i-1]][T[i]] * l
        if (_Point[T[i]].Type == 0 and (v > b1 or h > b2)) or (_Point[T[i]].Type == 1 and(v > a1 or h > a2)):
            # print(round(v,2),round(h,2))
            return T[i]
        elif _Point[T[i]].Type == 0: ##水平
            if _Point[T[i]].Pmark == 1 and p[count_p] == 1:
                h = min(h,5)
            else:
                h = 0
        elif _Point[T[i]].Type == 1:
            if _Point[T[i]].Pmark == 1 and p[count_p] == 1:
                v = min(v,5)
            else:
                v = 0
        if _Point[T[i]].Pmark == 1:
            count_p += 1
    v += _Point[T[-1]].Distance2B * l
    h += _Point[T[-1]].Distance2B * l
    if v > o or h > o:
        # print(round(v, 2), round(h, 2))
        return _Point[-1].Number
    return True

def success_probability(T):
    count_m = 0
    for i in T:
        if _Point[i].Pmark == 1:
            count_m += 1
            print(i)
    pp = 0.0
    for i in range(int(math.pow(2,count_m)+0.2)):
        p = [0] * count_m
        bi = i
        for j in range(count_m):
            if bi % 2 == 1:
                p[j] = 1
            bi = int(bi / 2)
        f = issuccess(T,p)
        #print(p,f,round(math.pow(0.2,np.sum(p)) * math.pow(0.8,count_m-np.sum(p)),5))
        if f == True:
            pp += math.pow(0.2,np.sum(p)) * math.pow(0.8,count_m-np.sum(p))
    print(pp)

distance = read_text(r"distance2.txt")
p = read_excel('plane2.xlsx', 'data2')
Point = getPoint()
S = showdata(Point[0])
cmp = operator.attrgetter('Distance2B', )
_Point = copy.deepcopy(Point)
# Point.sort(key=cmp)

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
        if S.now_point.Pmark == 1:
            S.list_pnumber += 1
        print(S.now_point.X, S.now_point.Y, S.now_point.Z)
    else:
        S.h += distance[S.now_point.Number][point.Number] * l
        S.h_list.append(round(S.h,2))
        S.v += distance[S.now_point.Number][point.Number] * l
        S.v_list.append(round(S.v,2))
        S.v = 0
        S.now_point = point
        S.ans_list.append(S.now_point.Number)
        if S.now_point.Pmark == 1:
            S.list_pnumber += 1
        print(S.now_point.X, S.now_point.Y, S.now_point.Z)
def pro_correction(l, point):
    global S
    if point.Type == 0:
        S.h += distance[S.now_point.Number][point.Number] * l
        S.h_list.append(round(S.h,2))
        S.v += distance[S.now_point.Number][point.Number] * l
        S.v_list.append(round(S.v,2))
        if point.Pmark == 1:
            S.h = min(S.h,5)
        else:
            S.h = 0
        S.now_point = point
        S.ans_list.append(S.now_point.Number)
        print(S.now_point.X, S.now_point.Y, S.now_point.Z)
    else:
        S.h += distance[S.now_point.Number][point.Number] * l
        S.h_list.append(round(S.h,2))
        S.v += distance[S.now_point.Number][point.Number] * l
        S.v_list.append(round(S.v,2))
        if point.Pmark == 1:
            S.v = min(S.v, 5)
        else:
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
        Min = 100000000000000
        for point in OPEN:
            if point.Distance2B + distance[S.now_point.Number][point.Number] < Min:
                cpoint = point
                Min = point.Distance2B + distance[S.now_point.Number][point.Number]
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
def pro_improve(a1, a2, b1, b2, o, l):
    global S
    total_distance = 0
    while S.now_point.Distance2B * l + S.h > o or S.now_point.Distance2B * l + S.v > o:
        OPEN = []
        if True:
            for point in Point:
                ## 水平校正点
                if point.Number not in S.ans_list and point.Type == 0 and (S.v + distance[S.now_point.Number][point.Number] * l) <= b1 and (
                        S.h + distance[S.now_point.Number][point.Number] * l) <= b2:
                    OPEN.append(point)
                ##垂直校正点
                elif point.Number not in S.ans_list and point.Type == 1 and (S.v + distance[S.now_point.Number][point.Number] * l) <= a1 and (
                        S.h + distance[S.now_point.Number][point.Number] * l) <= a2:
                    OPEN.append(point)
        elif S.h > S.v:
            for point in Point:
                ## 水平校正点
                if point.Number not in S.ans_list and point.Type == 0 and (S.v + distance[S.now_point.Number][point.Number] * l) <= b1 and (
                        S.h + distance[S.now_point.Number][point.Number] * l) <= b2:
                    OPEN.append(point)
        else:
            for point in Point:
                ## 垂直校正点
                if point.Number not in S.ans_list and point.Type == 1 and (S.v + distance[S.now_point.Number][point.Number] * l) <= a1 and (
                        S.h + distance[S.now_point.Number][point.Number] * l) <= a2:
                    OPEN.append(point)
        Min = 100000000000000
        if len(S.ans_list) < 7:
            cpoint = Point[a[len(S.ans_list)]]
        else:
            for point in OPEN:
                if point.Distance2B < Min:
                    cpoint = point
                    Min = point.Distance2B

        total_distance += distance[S.now_point.Number][cpoint.Number]
        correction(l, cpoint)

    total_distance += S.now_point.Distance2B
    S.h += S.now_point.Distance2B * l
    S.v += S.now_point.Distance2B * l
    S.h_list.append(round(S.h, 2))
    S.v_list.append(round(S.v, 2))
    print(distance[0][-1], total_distance)
    return [S.ans_list, S.h_list, S.v_list]

a = [0,252,322,100,270,10,89,236,132,53,112,103,250,243,73,82,207,70,211,321,279,301,38,287,99]

# ans_list, h_list, v_list = greedy(20,10,15,20,20,0.001)
# [ans_list, h_list, v_list] = A_star(20,10,15,20,20,0.001)
ans_list, h_list, v_list = pro_improve(20,10,15,20,20,0.001)
print(ans_list)
success_probability(ans_list)
# print("垂直误差:",v_list)
# print("水平误差:",h_list)
# print(np.sum(h_list) + np.sum(v_list))
# # for point in Point:
# #     if point.Number not in ans_list:
# #         print(point.X,point.Y,point.Z)
# time_end=time.time()
# print('totally cost',time_end-time_start)
time_end=time.time()
print('totally cost',time_end-time_start)