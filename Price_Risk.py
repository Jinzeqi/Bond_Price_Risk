'''
Calculate duration for bonds
'''
import math
from datetime import datetime as dt

def calc_bond_n(d1,d2):
    if(d1.day >= d2.day):
        n_month = (d1.year - d2.year) * 12 + d1.month - d2.month
    else:
        n_month = (d1.year - d2.year) * 12 + d1.month - d2.month - 1
    return(int(n_month / 6))

def calc_bond_price(n,y,c,m):
    price = 0
    for i in range(1,n+1):
        price += c * m / math.pow((1 + y), i)
    price +=  m / math.pow((1 + y),n)
    return(price)
    
def calc_bond_duration_y(n,y,c,m):
    dur = 0
    for i in range(2,n+2):
        dur += (-(i - 1) * c * m) / math.pow((1 + y/2),i)
    dur += -1 * n * m / math.pow((1 + y/2),n+1)
    price = calc_bond_price(n,y/2,c,m)
    result = dur / price
    return(result/2)

def calc_bond_duration_p(n,c,m,p):
    from scipy import optimize as opti
    y = opti.fsolve(lambda x:calc_bond_price(n,x,c,m)-p,0.02)
    return(calc_bond_duration_y(n,2 * y,c,m))
    
def calc_bond_pvbp_y(n,y,c,m):
    p1 = calc_bond_price(n,y/2,c,m)
    p2 = calc_bond_price(n,(y+0.0001)/2,c,m)
    return([p1-p2,(p1-p2)/p1])
    
def calc_bond_pvbp_p(n,c,m,p):
    from scipy import optimize as opti
    y = opti.fsolve(lambda x:calc_bond_price(n,x,c,m)-p,0.02)    
    p2 = calc_bond_price(n,y+0.0001/2,c,m)
    return([p-p2,(p-p2)/p])

def calc_bond_conv_y(n,y,c,m):
    con = 0
    for i in range(1,n+1):
        con += (i * (i + 1) * c * m) / math.pow((1 + y/2),i+2) 
    con += n * (n + 1) * m / math.pow((1 + y/2),n+2)
    price = calc_bond_price(n,y/2,c,m)
    result = con / price
    return(result / 4)

def calc_bond_conv_p(n,c,m,p):
    from scipy import optimize as opti
    y = opti.fsolve(lambda x:calc_bond_price(n,x,c,m)-p,0.02)
    return(calc_bond_conv_y(n,y*2,c,m))
    
# test0
dur = calc_bond_duration_y(50,0.045,4.5,100)
pvbp = calc_bond_pvbp_y(50,0.045,4.5,100)

# test1
n1 = calc_bond_n(dt(2031,11,1),dt(2017,8,16))
c1 = 0.08 / 2
m1 = 100
p1 = 125.93
dur1 = calc_bond_duration_p(n1,c1,m1,p1)
pvbp1 = calc_bond_pvbp_p(n1,c1,m1,p1)
con1 = calc_bond_conv_p(n1,c1,m1,p1)
# test2
n2 = calc_bond_n(dt(2053,7,1),dt(2017,8,16))
c2 = 0.0483 / 2
m2 = 100
p2 = 102.42
dur2 = calc_bond_duration_p(n2,c2,m2,p2)
pvbp2 = calc_bond_pvbp_p(n2,c2,m2,p2)
con2 = calc_bond_conv_p(n2,c2,m2,p2)
# test3
n3 = calc_bond_n(dt(2021,2,25),dt(2017,8,16))
c3 = 0.02875 / 2
m3 = 100
p3 = 101.6
dur3 = calc_bond_duration_p(n3,c3,m3,p3)
pvbp3 = calc_bond_pvbp_p(n3,c3,m3,p3)
con3 = calc_bond_conv_p(n3,c3,m3,p3)
#test4
n4 = calc_bond_n(dt(2037,4,1),dt(2017,8,16))
c4 = 0.074 / 2
m4 = 100
p4 = 75.7
dur4 = calc_bond_duration_p(n4,c4,m4,p4)
pvbp4 = calc_bond_pvbp_p(n4,c4,m4,p4)
con4 = calc_bond_conv_p(n4,c4,m4,p4)

# #test4
n = calc_bond_n(dt(2025,8,7),dt(2015,8,4))
c = 0.03 / 2
m = 100
p = 99.615

def calc_bond_pvbp_y(n,y,c,m):
    p1 = calc_bond_price(n,y/2,c,m)
    p2 = calc_bond_price(n,(y+0.0001)/2,c,m)
    return([p1-p2,(p1-p2)/p1])
from scipy import optimize as opti
y = opti.fsolve(lambda x:calc_bond_price(n,x,c,m)-p,0.02)


# all
dur = [dur1,dur3,dur2,dur4]
pvbp = [pvbp1,pvbp2,pvbp3,pvbp4]
con = [con1,con2,con3,con4]

# liability case
lia_dur =  calc_bond_duration_p(11,0,17183033,8820262)
bond1_dur = calc_bond_duration_p(11,0.125/2,100,100)
bond2_dur = calc_bond_duration_p(16,0.10125/2,100,88.20262)

# solve the equations for Barbell and Bullet
import numpy as np
a = np.mat('4.52,16.611;23.4,389.7')
b = np.mat('-8.033,-74.8').T
r = np.linalg.solve(a,b)
print(r)
p = r[0] * 102.5954 + r[1] * 102.7802