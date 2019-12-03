import xlrd
import operator
import numpy as np
import time

time_start=time.time()
class point():
    def __init__(self, number, x, y, z, type, pmark, distance):
        self.Number = number
        self.X = x
        self.Y = y
        self.Z = z
        self.Type = type
        self.Pmark = pmark
        self.Distance = distance
class showdata():
    def __init__(self,point):
        self.now_point = point
        self.h = 0
        self.v = 0
        self.ans_list = [0]
        self.h_list = [0]
        self.v_list = [0]

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
        _point = point(int(p[i][0]), round(p[i][1],2), round(p[i][2],2), round(p[i][3],2), p[i][4], int(p[i][5]), distance[i - 2].tolist())
        Point.append(_point)
    for i in range(len(Point)):
        Point[i].Distance2B = Point[i].Distance[-1]
    return Point

distance = read_text(r"distance2.txt")
p = read_excel('plane2.xlsx', 'data2')
Point = getPoint()
S = showdata(Point[0])

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
    while S.now_point.Distance2B * l + S.h> o or S.now_point.Distance2B * l + S.v > o:
        if S.h == S.v:  ##第一步
            for point in Point:
                ## 水平校正点
                if point.Type == 0 and (S.v + distance[S.now_point.Number][point.Number] * l) <= b1 and (
                        S.h + distance[S.now_point.Number][point.Number] * l) <= b2:
                    total_distance += distance[S.now_point.Number][point.Number]
                    correction(l,point)
                    break
                ##垂直校正点
                elif point.Type == 1 and (S.v + distance[S.now_point.Number][point.Number] * l) <= a1 and (
                        S.h + distance[S.now_point.Number][point.Number] * l) <= a2:
                    total_distance += distance[S.now_point.Number][point.Number]
                    correction(l,point)
                    break
        elif S.h > S.v:
            for point in Point:
                ## 水平校正点
                if point.Type == 0 and (S.v + distance[S.now_point.Number][point.Number] * l) <= b1 and (
                        S.h + distance[S.now_point.Number][point.Number] * l) <= b2:
                    total_distance += distance[S.now_point.Number][point.Number]
                    correction(l,point)
                    break
        else:
            for point in Point:
                ## 垂直校正点
                if point.Type == 1 and (S.v + distance[S.now_point.Number][point.Number] * l) <= a1 and (
                        S.h + distance[S.now_point.Number][point.Number] * l) <= a2:
                    total_distance += distance[S.now_point.Number][point.Number]
                    correction(l,point)
                    break
    total_distance += S.now_point.Distance2B
    S.h += S.now_point.Distance2B * l
    S.v += S.now_point.Distance2B * l
    S.h_list.append(round(S.h,2))
    S.v_list.append(round(S.v,2))
    print(distance[0][-1],total_distance)
    return [S.ans_list,S.h_list,S.v_list]

[ans_list,h_list,v_list] = greedy(20,10,15,20,20,0.001)
# # [ans_list,h_list,v_list] = A_star(20,10,15,20,20,0.001)
print(ans_list)
print("垂直误差:",v_list)
print("水平误差:",h_list)
# print(np.sum(h_list)+np.sum(v_list))
# # # for point in Point:
# # #     if point.Number not in ans_list:
# # #         print(point.X,point.Y,point.Z)
# # time_end=time.time()
# # print('totally cost',time_end-time_start)
# min = 1000000000000000
# for i in distance:
#     for j in i:
#         if j < min and j != 0:
#             min = j
# print(min)
