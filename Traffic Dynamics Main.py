from numpy import sqrt, array, linspace, zeros, concatenate
from random import randint  
from matplotlib.pyplot import figure, subplot
from scipy.integrate import odeint

#Traffic dynamics for a set of cars in a linear line.

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
        if t >= 500:
            v0 = 1
        else:
            v0 = 28
        
        if i == 0:
            
            Vblock = v_a    
            Xblock = x_a0 - x[i]

            #if t > 50: 
            #    Vblock = 0
                
            s = (Xblock + Vblock*t) - L# distance to car ahead
            delta_v = abs(v[i] - v_a)  # approach speed to car ahead
        
            sStar = s0 + v[i]*T + (v[i]*delta_v)/(2*sqrt(a_accel*b_decel))
            
            a_idm = a_accel*(1-(v[i]/v0)**delta_exp-(sStar/s)**2)
            #print(a_idm)
         
           
        else:
            delta_v = abs(v[i] - v[i-1])
            sStar = s0 + v[i]*T + (v[i]*delta_v)/(2*sqrt(a_accel*b_decel))
            Vblock = v[i] - v[i-1] #diff of velocity
            Xblock = x[i] - x[i-1] #diff of position

            s = (Xblock + Vblock*t) - L
                
            a_idm = a_accel*(1-(v[i]/v0)**delta_exp-(sStar/s)**2)
            #print(a_idm)
        dv[i] = a_idm
        
    # compute derivatives
    dx = v
    
    # pack rate array
    rate = concatenate([dx, dv])
    return rate


# set parameters
T = 1.8 #time headway
delta_exp = 4
L = 5
a_accel = 0.3
b_decel = 3
v0 = 28 #desired speed in m/s
s0 = 2.0 #desired gap m

#Lead Car
x_a0 = 2000
v_a = v0/2

#number of cars
ncars = 10


# set initial conditions
xinit = array([0, -10, -20, -30, -40, -50, -60, -70, -80, -90])
vinit = zeros(ncars)

#for i in range(len(xinit)):
#    xinit[i] = xinit[i] + randint(0,75)



#xinit = xinit * 10
#vinit = (vinit + 1) * v_a

#Main
# pack i.c.
X0 = concatenate([xinit, vinit])

# set the time interval for solving
Tstart = 0
Tend = 600

# Form Time array
time = linspace(Tstart,Tend,400) # 400 steps for nice plot

X = odeint(rate_func, X0, time, tfirst=True) 

# unpack the results. In the output array, variables are columns, times are rows
pos = X[:,:ncars]
vel = X[:,ncars:]

#graphing -------------
fig=figure()

ax1 = subplot()
ax1.plot(time,pos)
ax1.set_xlabel('time (s)')
ax1.set_ylabel('distance (m)', color='b')
ax1.tick_params('y', colors='b')

ax2=ax1.twinx()
ax2.plot(time,vel, 'r')
ax2.set_ylabel('velocity (m/s)', color='r')
ax2.tick_params('y', colors='r')

fig.tight_layout()


































