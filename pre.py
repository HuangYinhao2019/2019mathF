# import xlrd
import math
# import numpy as np
#
# class point():
#     def __init__(self,number,x,y,z,type,pmark):
#         self.Number = number
#         self.X = x
#         self.Y = y
#         self.Z = z
#         self.Type = type
#         self.Pmark = pmark
#
# def read_excel(filename,sheetname):
#     book = xlrd.open_workbook(filename)
#     sheet = book.sheet_by_name(sheetname)
#     array = []
#     rows = sheet.nrows #获取行数
#     for r in range(rows): #读取每一行的数据
#         r_values = sheet.row_values(r)
#         array.append(r_values)
#     return array
#
# p1 = read_excel('plane1.xlsx','data1')
# Point = []
# for i in range(2,len(p1)):
#     _point = point(p1[i][0],p1[i][1],p1[i][2],p1[i][3],p1[i][4],p1[i][5])
#     Point.append(_point)
#
# distance = [[0] * len(Point) for _ in range(len(Point))]
# for i in range(len(Point)):
#     for j in range(len(Point)):
#         distance[i][j] = math.sqrt(math.pow((Point[i].X - Point[j].X),2)+math.pow((Point[i].Y - Point[j].Y),2)+math.pow((Point[i].Z - Point[j].Z),2))
#         distance[i][j] = round(distance[i][j],2)
#         distance[i][j] = str(distance[i][j]) + ' '
#
# print(len(Point))
#
# with open('distance1.txt','w') as f:
#     for i in range(len(distance)):
#         f.writelines(distance[i])
#         f.write('\n')
#
#
#
print(math.acos(0.5))