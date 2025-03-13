import gymnasium as gym
import numpy as np
import pygame
from math import sin, cos, pi

ENABLE_WIND = False
WIND_POWER = 15.0
TURBULENCE_POWER = 0.0
GRAVITY = -10.0
RENDER_MODE = 'human'
#RENDER_MODE = None #seleccione esta opção para não visualizar o ambiente (testes mais rápidos)
EPISODES = 1000

env = gym.make("LunarLander-v3", render_mode =RENDER_MODE, 
    continuous=True, gravity=GRAVITY, 
    enable_wind=ENABLE_WIND, wind_power=WIND_POWER, 
    turbulence_power=TURBULENCE_POWER)


def check_successful_landing(observation):
    x = observation[0]
    vy = observation[3]
    ori = observation[4]
    contact_left = observation[6]
    contact_right = observation[7]

    legs_touching = contact_left == 1 and contact_right == 1

    on_landing_pad = abs(x) <= 0.2

    stable_velocity = vy > -0.2
    stable_orientation = abs(ori) < np.deg2rad(20)
    stable = stable_velocity and stable_orientation
 
    if legs_touching and on_landing_pad and stable:
        print("✅ Aterragem bem sucedida!")
        return True

    print("⚠️ Aterragem falhada!")        
    return False
        
def simulate(steps=4000,seed=None, policy = None):    
    observ, _ = env.reset(seed=seed)
    for step in range(steps):
        action = policy(observ)

        observ, _, term, trunc, _ = env.step(action)

        if term or trunc:
            break

    success = check_successful_landing(observ)
    return step, success



#Perceptions
##TODO: Defina as suas perceções aqui

posX = lambda var: var[0]
posY = lambda var: var[1]
velX = lambda var: var[2]
velY = lambda var: var[3]
orientation = lambda var: var[4]
velocAngular = lambda var: var[5]
left_leg_touching = lambda var: var[6]
right_leg_touching = lambda var: var[7]


#Actions
##TODO: Defina as suas ações aqui



act = dict(
    up = np.array([1,0]),
    left = np.array([0,-1]),
    right = np.array([0,1])
)


def moveUp(action,mod):
    action += np.array([1, mod])
    # action += act['up']*mod
    
def turn(action,mod):
    action += act["left"]*mod


def reactive_agent(observation):
    action = np.array([0.0, 0.0])
    
    x = posX(observation)
    y = posY(observation)
    vx = velX(observation)
    vy = velY(observation)
    ori = orientation(observation)
    velAng = velocAngular(observation)
    left_leg = left_leg_touching(observation)
    right_leg = right_leg_touching(observation)

    # Salvador's test #
    # if y < 0.11 and abs(vx) > 0.27:
    #     turn(action, -1.13*cos(ori)*vx)
    #     return action

    
    if y < 0.11 and abs(x) > 0.22:
        moveUp(action,-2.4*x*0.72*sin(ori)*vy +ori+velAng)
        #turn(action,1.2*x)
        return action
    
    
    if left_leg and right_leg and abs(vx) > 0.25:
        return action
    
    # if abs(x) < 0.05:
    #     moveUp(action,-0.01*sin(ori)*vy +ori+velAng)
    #     return action
    
    # If falling too fast, go up
    if vy < -.27:
        
        moveUp(action, -0.75*sin(ori)*vy +ori+velAng)
        return action
    
    # # If ship is too low outside flags, go up
    # if y < .3 and (x < .25 or x > .25):
    #     moveUp(action, ori+velAng)
    #     return action
    
    # Turning too fast, turn the other way
    if abs(velAng) > 0.4:
        turn(action, -1.25*velAng*(1-0.1*x))
        return action
    
    # Going X too fast, turn
    if abs(vx) > 0.275:
        #moveUp(action,(1-x)*-sin(ori)*vy)
        turn(action, 1.02*(1-0.13*x)*1.15*vx)
        return action
    
    
    # if y < .2 and x > .2:
    #     moveUp(action, ori)
    #     return action
    
    """
    # Is left, turn right
    if x < -.2 and ori > 0 and vx < 0.5:
        turn(action, -.7)
        return action
    """
    # Balance
    # if x < -.2 and ori < -.1 and velAng < .1:# and vx > .5:
    #     turn(action, .7)
    #     return action
    """
    # Is right, turn left
    if x > .2 and ori < 0 and vx > -0.5:
        turn(action, .7)
        return action
    """
    # Balance
    # if x > .2 and ori > .1 and velAng > -.1:# and vx < -.5:
    #     turn(action, -.7)
    #     return action
    
    # Between flags
    # Correct orientation
    # if ori < 0 and velAng < 0.1 :
    #     turn(action,  -.5)
    #     return action
    
    # if ori > 0 and velAng > -.1:
    #     turn(action, .5)
    #     return action
    
    # if vx > 0 and ori <= 0:
    #     turn(action, -1)
    #     return action
    
    # if vx < 0 and ori >= 0:
    #     turn(action, 1)
    #     return action




    return action
    
    
def keyboard_agent(observation):
    action = [0,0] 
    keys = pygame.key.get_pressed()
    
    print('observação:',observation)

    if keys[pygame.K_UP]:  
        action =+ np.array([1,0])
    if keys[pygame.K_LEFT]:  
        action =+ np.array( [0,-1])
    if keys[pygame.K_RIGHT]: 
        action =+ np.array([0,1])

    return action
    

success = 0.0
steps = 0.0
for i in range(EPISODES):
    st, su = simulate(steps=1000000, policy=reactive_agent)

    if su:
        steps += st
    success += su
    
    if su>0:
        print('Média de passos das aterragens bem sucedidas:', steps/success*100)
    print('Taxa de sucesso:', success/(i+1)*100)
    
