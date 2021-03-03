from numpy import sqrt, array, linspace, zeros, concatenate
from matplotlib.pyplot import subplot, figure
from scipy.integrate import odeint


# set parameters
T = 1.8 #time headway
delta_exp = 4
L = 5
a_accel = 0.7
b_decel = 3
v0 = 28 #desired speed in m/s
s0 = 2.0 #desired gap m
circ = 1000 #circumference of loop
#number of cars
ncars = 50

#Vblock = v0/2

#Xblock = 5000. # front bumper of stopped car

# set initial conditions
xinit = linspace(0,circ,ncars,endpoint=False)
vinit = zeros(ncars)

# pack i.c.
X0 = concatenate([xinit, vinit])

def rate_func( t, V ):
    # RATE_FUNC: IDM Car model
    # Model a car approaching a solid wall
    
    # unpack
    x = V[:ncars] # position
    v = V[ncars:] # velocity
    
    dv = zeros(ncars)
    
    for i in range(ncars):

        # Compute acceleration from IDM
        #Lead Car
        if i == 0:
    
            Vblock = v[-1] 
            Xblock = x[-1] - x[i]

            
            s = (Xblock + Vblock*t) - L# distance to car ahead
            delta_v = v[i] - v[-1]  # approach speed to car ahead
        
            sStar = s0 + v[i]*T + (v[i]*delta_v)/(2*sqrt(a_accel*b_decel))
            
            a_idm = a_accel*(1-(v[i]/v0)**delta_exp-(sStar/s)**2)
            #print(a_idm)
            
        else:
            delta_v = v[i] - v[i-1]
            sStar = s0 + v[i]*T + (v[i]*delta_v)/(2*sqrt(a_accel*b_decel))
            Vblock = v[i-1] - v[i]
            Xblock = x[i-1] - x[i]

            s = (Xblock + Vblock*t) - L
                
            a_idm = a_accel*(1-(v[i]/v0)**delta_exp-(sStar/s)**2)
            #print(a_idm)
        dv[i] = a_idm
        
    # compute derivatives
    dx = v
    
    # pack rate array
    rate = concatenate([dx, dv])
    return rate

# set the time interval for solving
Tstart = 0
Tend = 1500

# Form Time array
time = linspace(Tstart,Tend,400) # 400 steps for nice plot


X = odeint(rate_func, X0, time, tfirst=True) 


# unpack the results. In the output array, variables are columns, times are rows
pos = X[:,:ncars]
vel = X[:,ncars:]

#graphing -------------

#plot(time, pos)
#plot(time, vel)


fig=figure()

ax1 = subplot()
ax1.plot(time,pos,'b')
ax1.set_xlabel('time (s)')
ax1.set_ylabel('distance (m)', color='b')
ax1.tick_params('y', colors='b')

ax2=ax1.twinx()
ax2.plot(time,vel,'r')
ax2.set_ylabel('velocity (m/s)', color='r')
ax2.tick_params('y', colors='r')

fig.tight_layout()


































