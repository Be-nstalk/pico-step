from machine import Pin
from utime import sleep
# from utime import ticks?
sleep(0.1) # Wait for USB to become ready

DEBUG = False

def dprint(string):
  if DEBUG == True: print(string)

STEPS_PER_REVOLUTION = 200

MAGIC_FLOAT = float(360/STEPS_PER_REVOLUTION)

travel_degs = 90

SLEEPVAL = 0.01

# u = 343.2 / 1000 / 1000

# trigger = Pin(27, Pin.OUT)
# echo = Pin(26, Pin.IN)

pins = [
  Pin(2, Pin.OUT), # DIR
  Pin(3, Pin.OUT), # STEP
]

SWITCH_DOWN = Pin(4, Pin.IN, Pin.PULL_UP)
SWITCH_UP = Pin(5, Pin.IN, Pin.PULL_UP)

BWD = [
  [1,0],
  [0,1],
  [0,0], # CLEAR THE PIN OUTPUT!!!!!!!!!!! works as it looks for a change?
]

FWD = [
  [1,1],
  [0,0],
]

def STEPS_FROM_DEGS(degrees):
  return int(degrees / MAGIC_FLOAT)

def step(step_array):
  for step in step_array:
      for i in range(len(pins)):
        pins[i].value(step[i])
        sleep(SLEEPVAL)

stepcount = 0
target = 0

def dprint_switch():
  dprint(f"SWITCH_UP = {SWITCH_UP.value()} | SWITCH_DOWN = {SWITCH_DOWN.value()} stepcount = {stepcount} | target = {target}")
  sleep(0.001)


dprint("check")

# def ultra():
#   trigger.low()
  
#   sleep_us(2)
#   trigger.high()
#   sleep_us(5)
#   trigger.low()

#   while echo.value() == 0:
#     signaloff = ticks_us()

#   while echo.value() == 1:
#     signalon = ticks_us()

#   timepassed = (signalon - signaloff)

#   distance = (timepassed * u) / 2

#   global distance_ticks = ticks_us()

#   dprint(f"measured distance: {distance}m")
#   return distance


dprint("check")


# def stepcount_check():
  # if abs(stepcount) == STEPS_PER_REVOLUTION / 2: stepcount = abs(stepcount)
  # reset stepcount at full revolution
  # if abs(stepcount) >= 200 and abs(stepcount) % STEPS_PER_REVOLUTION == 0: stepcount = 0


print("initialised (open)")

# error = False

# try: distance = ultra()
# except: print("ultrasonic error")

while True:
  dprint_switch()

  # current_ticks = ticks_us()

  # if current_ticks - distance_ticks >= 1000000:
  #   distance = ultra()

  # if distance < 4:
  #   target = 10
  #   # indicator light -> red, flashing

  if SWITCH_DOWN.value() == 0 and SWITCH_UP.value() == 1:
    target = 0
    # indicator light -> green
  elif SWITCH_DOWN.value() == 1 and SWITCH_UP.value() == 0:
    target = STEPS_FROM_DEGS(travel_degs)
    # indicator light -> red
  # elif SWITCH_DOWN.value() == 1 and SWITCH_UP.value() == 1: continue
  else: continue
    # print("switch error")
    # print(SWITCH_DOWN.value(), SWITCH_UP.value())
    # error = True
    # if stepcount == target: break

  # if error == True:
  #   # error light -> on
  #   continue

  # stepcount_check()

  if stepcount == target:

    sleep(SLEEPVAL)
  
  elif stepcount > target:
    step(BWD)
    dprint("stepped bwd")
    stepcount -= 1
    if stepcount == target and target == 0: print("open")

  elif stepcount < target:
    # if distance >= 4: target = 10
    step(FWD)
    dprint("stepped fwd")
    stepcount += 1
    if stepcount == target and target >= 45: print("closed")

  
  sleep(SLEEPVAL)


 
 
