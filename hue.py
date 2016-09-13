#!/usr/bin/python
import colorsys
import multiprocessing
import queue

import phue

HUE_IP = "192.168.1.38"

aaa = [1, 2, 3]

BRIGHTNESS = 0
ONNESS = True
bedlights = [1, 3]
halllights = [2]
bl = bedlights
hl = halllights
h1 = 0.0
h2 = 0.2
h3 = 0.4
h4 = 0.6
h5 = 0.8
h6 = 1.0


def brightness_up(increment):
    return {"bri_inc": increment}


def bu(increment):
    return brightness_up(increment)


offness = {"on": False}
onness = {"on": True}

hue_bridge = phue.Bridge(HUE_IP)


def set_across_lights(lights, actions):
    for light in lights:
        hue_bridge.set_light(light, actions)


def sal(lights, actions):
    set_across_lights(lights, actions)


def salb(actions):
    set_across_lights(bedlights, actions)


def combine_commands(commands):
    combined_command = commands[0]
    for command in commands[1:]:
        combined_command.update(command)
    return combined_command


def command_from_rgb(r, g, b):
    hue_val, sat, val = colorsys.rgb_to_hsv(r, g, b)
    hue_val = int(65536 * hue_val)
    sat = int(255 * sat)
    val = int(255 * val)
    return {"hue": hue_val, "sat": sat, "bri": val}


def car(r, g, b):
    return command_from_rgb(r, g, b)


hue_bridge.connect()


def cc(coms):
    return combine_commands(coms)


def timed(com, transition_time):
    return combine_commands([com, {"transitiontime": transition_time}])


def salc(r, g, b):
    salb(car(r, g, b))


def hu(amount):
    return {"hue_inc": amount}


def su(amount):
    return {"sat_inc": amount}


def sfull(ls, r, g, b, bright, ctime=None):
    hue_dict = car(r, g, b)
    hue_dict["bri"] = bright
    if ctime is not None:
        hue_dict["transitiontime"] = ctime
    sal(ls, hue_dict)


def shue(r, g, b):
    foo = car(r, g, b)
    del (foo["bri"])
    return foo


def hxs(rgbstr):
    bit1 = (int(rgbstr[1:3], 16) * 1.0) / 715.0
    bit2 = (int(rgbstr[3:5], 16) * 1.0) / 715.0
    bit3 = (int(rgbstr[5:7], 16) * 1.0) / 715.0
    print(bit1, bit2, bit3)
    return car(bit1, bit2, bit3)


def rgb(r, g, b):
    bit1 = (r * 1.0) / 715.0
    bit2 = (g * 1.0) / 715.0
    bit3 = (b * 1.0) / 715.0
    return car(bit1, bit2, bit3)


def hue(r, g, b):
    foo = shue(r, g, b)
    del (foo["sat"])
    return foo


def pod():
    sal(aaa, su(-254))


hue_bridge.get_api()


def get_light_status():
    for num, light in enumerate(hue_bridge.lights):
        print(str(num + 1) + " " + str(light.hue) + "," + str(light.saturation))


soft_orange = (10922, 200)
soft_yellow = (16922, 200)
striking_blue = (47492, 214)
striking_fuschia = (54492, 214)
trippy = [striking_blue, striking_fuschia]
bal = [4, 5]

sunset = [soft_orange, soft_yellow]


def hs(huesat):
    hue_val, sat = huesat
    return {"hue": hue_val, "sat": sat}


def apply_color_list(light_list, color_list):
    for num in range(len(light_list)):
        sal([light_list[num]], hs(color_list[num]))


def acs(light_list, color_list):
    apply_color_list(light_list, color_list)


queued_actions = multiprocessing.Queue()


def cycle_lightset(task_queue: multiprocessing.Queue, light_set, speed):
    received_quit = False
    while not received_quit:
        try:
            sal(light_set, timed(hu(100 * speed), 10))
            print("CYCLING AT " + str(speed))
            signal = task_queue.get(timeout=1)
            if signal == "stop":
                received_quit = True
        except queue.Empty:
            pass


def start_cycling(light_set, speed):
    p = multiprocessing.Process(target=cycle_lightset(queued_actions, light_set, speed))
    p.start()
    print("STARTED")
    return p


get_light_status()
if __name__ == '__main__':
    multiprocessing.freeze_support()
    print("GOT SUPPORT")
    start_cycling(bl, 30)
    print("STARTING")
multiprocessing.freeze_support()
