# 2019年华为数学建模国赛研究生竞赛F题
该代码为2019年华为数学建模研究生竞赛F题代码。
## 题目大意
该题是无人机航迹规划问题，是一个经典的路径优化问题，给定出发点和目的地，在含有一定约束条件的情况下，以路径长度以及最少校正点为优化目标求出最优路径。

### 约束
(1)飞行器在空间飞行过程中需要实时定位，其定位误差包括垂直误差和水平误差。飞行器每飞行1m，垂直误差和水平误差将各增加δ个专用单位，以下简称单位。到达终点时垂直误差和水平误差均应小于𝜃个单位，并且为简化问题，假设当垂直误差和水平误差均小于𝜃个单位时，飞行器仍能够按照规划路径飞行。

(2)飞行器在飞行过程中需要对定位误差进行校正。飞行区域中存在一些安全位置（称之为校正点） 可用于误差校正，当飞行器到达校正点即能够根据该位置的误差校正类型进行误差校正。校正垂直和水平误差的位置可根据地形在航迹规划前确定（如图1为某条航迹的示意图, 黄色的点为水平误差校正点，蓝色的点为垂直误差校正点，出发点为A点，目的地为B点，黑色曲线代表一条航迹）。可校正的飞行区域分布位置依赖于地形，无统一规律。若垂直误差、水平误差都能得到及时校正，则飞行器可以按照预定航线飞行，通过若干个校正点进行误差校正后最终到达目的地。

![](https://github.com/HuangYinhao2019/2019mathF/raw/master/image/sample.png) 

(3)在出发地A点，飞行器的垂直和水平误差均为0。

(4)飞行器在垂直误差校正点进行垂直误差校正后，其垂直误差将变为 0，水平误差保持不变。

(5)飞行器在水平误差校正点进行水平误差校正后，其水平误差将变为 0，垂直误差保持不变。

(6)当飞行器的垂直误差不大于α<sub>1</sub>个单位，水平误差不大于α<sub>2</sub>个单位时才能进行垂直误差校正。

(7)当飞行器的垂直误差不大于β<sub>1</sub>个单位，水平误差不大于β<sub>2</sub>个单位时才能进行水平误差校正。

(8)飞行器在转弯时受到结构和控制系统的限制，无法完成即时转弯(飞行器前进方向无法突然改变)，假设飞行器的最小转弯半径为200m。

## 问题
问题1. 针对附件1和附件2中的数据分别规划满足条件(1)~(7)时飞行器的航迹，并且综合考虑以下优化目标：

（A）航迹长度尽可能小；

（B）经过校正区域进行校正的次数尽可能少。




问题2. 针对附件1和附件2中的数据(参数与第一问相同)分别规划满足条件(1)~(8)时飞行器的航迹，并且综合考虑以下优化目标：

（A）航迹长度尽可能小；

（B）经过校正区域进行校正的次数尽可能少。

问题3.飞行器的飞行环境可能随时间动态变化，虽然校正点在飞行前已经确定，但飞行器在部分校正点进行误差校正时存在无法达到理想校正的情况(即将某个误差精确校正为0)，例如天气等不可控因素导致飞行器到达校正点也无法进行理想的误差校正。现假设飞行器在部分校正点(附件1和附件2中F列标记为“1”的数据)能够成功将某个误差校正为0的概率是80%，如果校正失败，则校正后的剩余误差为 min(error，5)个单位(其中error为校正前误差,min为取小函数),并且假设飞行器到达该校正点时即可知道在该点处是否能够校正成功，但不论校正成功与否，均不能改变规划路径。请针对此情况重新规划问题1所要求的航迹，并要求成功到达终点的概率尽可能大。

## 思路
三题的思路基本都是以A*算法为基础，第一题我们考虑两个误差，对于较大的误差我们进行优先校正，即下一个校正点去当前误差较大的误差类型的误差校正点。

对于优化目标(A)航迹长度尽可能小，在满足约束条件的基础上，选择校正点的标准是，根据校正点与当前所在点与目标点B的直线的距离最短。
对于优化目标(B)经过校正区域进行校正的次数尽可能少，选择校正点的标准是，根据校正点与当前所在点的距离尽可能远。

对于问题二新加入的约束，需要根据数学方程求出最优轨迹(从问题1两点确定路径变为三点确定一条路径)，其余思路与第一题基本相同。

对于问题三新加入的约束，作最坏考虑，假设在问题校正点校正必定失败，以此作为约束使飞行器尽可能选择没有问题的校正点。

对于多个优化目标同时优化，可以考虑用加权法。

工程中，q1q2q3分别表示三个问题,plane1和plane2表示题目给出的两个不同的实验环境。