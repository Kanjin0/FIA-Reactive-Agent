import gymnasium as gym
import numpy as np
import pygame
from math import sin, cos, pi

ENABLE_WIND = False
WIND_POWER = 15.0
TURBULENCE_POWER = 0.0
GRAVITY = -10.0
RENDER_MODE = 'human'
RENDER_MODE = None #seleccione esta opção para não visualizar o ambiente (testes mais rápidos)
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


# Perceptions #

def getPerceptions(x, y, vx, vy, ori, velAng, left_leg, right_leg):
    return {
        "leftTouching"  : left_leg,
        "rightTouching" : right_leg,
        "isLow"         : y < 0.11,
        "isFar"         : abs(x) > 0.18 + y*0.75,
        "isLeft"        : x < 0,
        "isFarRight"    : x > 0.33,
        "inCenter"      : abs(x) < .2,
        "leaningRight"  : ori < -0.25,
        "leaningLeft"   : ori > 0.25,
        "fallingFast"   : vy < -0.25,
        "turningFast"   : abs(velAng) > 0.4,
        "sidewaysFast"  : abs(vx) > 0.275
    }


# Actions #

# Turn main motor on with given power
def moveUp(action,mod):
    action += np.array([mod, 0])
    # action += np.array([1, mod])
    
# Turn on secondary motor with given power
# A positive value will turn on left motor
# A negative value will turn on right motor
def turn(action,mod):
    action += np.array([0, mod])


def reactive_agent(observation):
    action = np.array([0.0, 0.0])
    
    x = observation[0]
    y = observation[1]
    vx = observation[2]
    vy = observation[3]
    ori = observation[4]
    velAng = observation[5]
    left_leg = observation[6]
    right_leg = observation[7]

    perc = getPerceptions(x, y, vx, vy, ori, velAng, left_leg, right_leg)
    

    # If both legs are touching the ground
    # & not going sideways too fast:
    #   do nothing
    if perc["leftTouching"] and perc["rightTouching"] and perc["inCenter"]:
        return action

    if perc["inCenter"] and perc["isLow"]:
        moveUp(action, (.05 - np.min(vy, 0)) / np.cos(ori))
        turn(action, -20 *(np.arcsin((x + vx)/np.hypot(x+vx, 10-y)) - ori - velAng))
        return action

    if perc["inCenter"]:
        moveUp(action, (.0 - np.min(vy, 0)) / np.cos(ori))
        turn(action, -20 *(np.arcsin((x + vx)/np.hypot(x+vx, 10-y)) - ori - velAng))
        return action
    
    if perc["isLow"]:
        moveUp(action, (.25 - np.min(vy, 0)) / np.cos(ori))
        turn(action, -100 *(np.arcsin((x + vx)/np.hypot(x+vx, 10-y)) - 0.5*(ori + velAng)))
        return action
    
    if perc["isLeft"]:
        moveUp(action, (.1 - np.min(vy, 0)) / np.cos(ori))
        turn(action, -100 *(np.arcsin((x + vx + .2)/np.hypot(x+vx+.2, 10-y)) - 0.5*(ori + velAng)))
        return action
    
    if True:
        moveUp(action, (.1 - np.min(vy, 0)) / np.cos(ori))
        turn(action, -100 *(np.arcsin((x + vx - .2)/np.hypot(x+vx-.2, 10-y)) - 0.5*(ori + velAng)))
        return action

    
    
    # # If ship is too low and outside flag's range:
    # #   turn in flags' direction
    # #   while keeping its balance
    # if perc["isLow"] and perc["isFar"]:
    #     moveUp(action, 1)
    #     turn(action, -2.4*x*0.72*sin(ori)*vy +ori+velAng)
    #     # moveUp(action, -2.4*x*0.72*sin(ori)*vy +ori+velAng)
    #     return action
    
    # # If ship is falling too fast:
    # #   go up while maintaining balance
    # if perc["fallingFast"]:
    #     moveUp(action, 1)
    #     turn(action, -0.75*sin(ori)*vy +ori+velAng)
    #     # moveUp(action, -0.75*sin(ori)*vy +ori+velAng)
    #     return action
    
    # # If ship is turning too fast:
    # #   turn the other way
    # if perc["turningFast"]:
    #     turn(action, 1.25*velAng*(1-0.1*x))
    #     return action
    
    # # If ship is moving sideways too fast:
    # #   turn opposite direction
    # if perc["sidewaysFast"]:
    #     #move(up, action)
    #     #turn(action,(1-x)*-sin(ori)*vy)
    #     turn(action, -1.02*(1-0.13*x)*1.15*vx)
    #     return action
    
    # # If ship is too low
    # # &  ( is far right and facing right
    # #    | is far left and facing left
    # #    ):
    # #   turn oposite direction
    # if not perc["isLow"] and ((perc["isFarRight"] and perc["leaningLeft"]) or (perc["isFarLeft"] and perc["leaningRight"])):
    #     turn(action, 2.1*0.75*sin(ori)*vy -ori-velAng)
    #     return action
    
    
    
    # Failed Tests #

    # if y < 0.11 and abs(vx) > 0.27:
    #     turn(action, -1.13*cos(ori)*vx)
    #     return action
    
    # if abs(x) < 0.05:
    #     moveUp(action, 1)
    #     turn(action,-0.01*sin(ori)*vy +ori+velAng)
    #     return action
    
    # # If ship is too low outside flags, go up
    # if y < .3 and (x < .25 or x > .25):
    #     move(up, action)
    #     turn(action, ori+velAng)
    #     return action
    
    # if y < .2 and x > .2:
    #     move(up, action)
    #     turn(action, ori)
    #     return action
    
    # # Is left, turn right
    # if x < -.2 and ori > 0 and vx < 0.5:
    #     turn(action, -.7)
    #     return action
    
    # Balance
    # if x < -.2 and ori < -.1 and velAng < .1:# and vx > .5:
    #     turn(action, .7)
    #     return action
    
    # # Is right, turn left
    # if x > .2 and ori < 0 and vx > -0.5:
    #     turn(action, .7)
    #     return action
    
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
    
