import math
def cosTwoVec(A, B):
    _cos = (A[0] * B[0] + A[1] * B[1] + A[2] * B[2]) / (
            math.sqrt(A[0] * A[0] + A[1] * A[1] + A[2] * A[2]) * math.sqrt(B[0] * B[0] + B[1] * B[1] + B[2] * B[2]))
    return _cos
def NorVec(A,B,C):
    n2 = [(A[1] - B[1]) * (A[2] - C[2]) - (A[2] - B[2]) * (A[1]- C[1]), (A[2] - B[2]) * (A[0] - C[0]) - (A[0] - B[0]) * (A[2] - C[2]),
          (A[0] - B[0]) * (A[1] - C[1]) - (A[1] - B[1]) * (A[0] - C[0])]
    return n2
def space_distance(A, B):
    return math.sqrt(math.pow(A[0] - B[0], 2) + math.pow(A[1] - B[1], 2) + math.pow(A[2] - B[2], 2))
def getO(A,B,C):
    n1 = (B[0] - A[0], B[1] - A[1], B[2] - A[2])  ##AB直线向量
    n2 = [(A[1] - B[1]) * (A[2] - C[2]) - (A[2] - B[2]) * (A[1] - C[1]),
          (A[2] - B[2]) * (A[0] - C[0]) - (A[0] - B[0]) * (A[2] - C[2]),
          (A[0] - B[0]) * (A[1] - C[1]) - (A[1] - B[1]) * (A[0] - C[0])]  ##ABC平面法向量
    n3 = (n1[1] * n2[2] - n1[2] * n2[1], n1[2] * n2[0] - n1[0] * n2[2], n1[0] * n2[1] - n1[1] * n2[0])  ##垂直n1,n2向量的直线向量
    sq = math.sqrt(n3[0] * n3[0] + n3[1] * n3[1] + n3[2] * n3[2])
    t1, t2 = 200 / sq, (-200) / sq
    O1 = (B[0] + n3[0] * t1, B[1] + n3[1] * t1, B[2] + n3[2] * t1)
    O2 = (B[0] + n3[0] * t2, B[1] + n3[1] * t2, B[2] + n3[2] * t2)
    dis1 = space_distance(O1, C)
    dis2 = space_distance(O2, C)
    if dis2 < dis1:
        return O2
    else:
        return O1
def MiddlePoint(S, M, T, E, R=200, m=100):  ##S=A M=B E=C T=D O=0 R=200,m20

    norvec=NorVec(S,M,E)
    O=getO(S,M,E)
    a=norvec[0]
    b=norvec[1]
    c=norvec[2]
    # print(norvec[0])
    midpoint = []
    T0_XO = [T[0] - O[0], T[1] - O[1], T[2] - O[2]]
    OM=[M[0]-O[0],M[1]-O[1],M[2]-O[2]]
    # 平面法向量
    i = c * T0_XO[1] - b * T0_XO[2]
    j = a * T0_XO[2] - c * T0_XO[0]
    k = b * T0_XO[0] - a * T0_XO[1]
    # print(cosTwoVec(OM, T0_XO))
    xita = math.acos(cosTwoVec(OM, T0_XO))
    _index = 1
    while _index < m:

        f_xita = math.cos((_index * xita) / m)
        _xi = 0
        g_xita = f_xita * R * math.sqrt(T0_XO[0] * T0_XO[0] + T0_XO[1] * T0_XO[1] + T0_XO[2] * T0_XO[2]) + O[0] * \
                 T0_XO[
                     0] + O[1] * T0_XO[1] + O[2] * T0_XO[2]
        _zi = (b * g_xita - (T0_XO[1] * (a * S[0] + b * S[1] + c * S[2]))) / (b * T0_XO[2] - c * T0_XO[1])
        _yi = (a * S[0] + b * S[1] + c * S[2] - c * _zi) / b

        A = i * i + j * j + k * k
        B = 2 * ((-1) * i * O[0] + j * _yi - j * O[1] + k * _zi - k * O[2])
        C = O[0] * O[0] + _yi * _yi - 2 * O[1] * _yi + O[1] * O[1] + _zi * _zi - 2 * O[2] * _zi + O[2] * O[
            2] - R * R

        delta = B * B - 4 * A * C

        _t1 = ((-1) * B + math.sqrt(delta)) / (2 * A)
        _t2 = ((-1) * B - math.sqrt(delta)) / (2 * A)

        X1 = i * _t1
        Y1 = j * _t1 + _yi
        Z1 = k * _t1 + _zi

        xpoint1 = [X1, Y1, Z1]

        X2 = i * _t2
        Y2 = j * _t2 + _yi
        Z2 = k * _t2 + _zi
        xpoint2 = [X2, Y2, Z2]

        SM = [M[0] - S[0], M[1] - S[1], M[2] - S[2]]
        MxPoitn1 = [xpoint1[0] - M[0], xpoint1[1] - M[1], xpoint1[2] - M[2]]
        MxPoitn2 = [xpoint2[0] - M[0], xpoint2[1] - M[1], xpoint2[2] - M[2]]

        # print(cosTwoVec(SM, MxPoitn1))
        # print(cosTwoVec(SM, MxPoitn2))
        if cosTwoVec(SM, MxPoitn1) > cosTwoVec(SM, MxPoitn2):
            midpoint.append(xpoint1)
        else:
            midpoint.append(xpoint2)
        _index += 1
    # print(midpoint)
    return midpoint