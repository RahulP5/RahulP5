# data = {"lat": 73.098765432}
# s = str(data["lat"])
# print(s[0:5])
#
# value = -0.234674465
# print(format(value, '.4f')


import evdev
from time import sleep

JOY = 0

LEVEL = 1
DEAD_SWITCH = 0

on_off = 0
event_trigger_flag = False
ptz_event_trigger = False

left_throtle = 0
right_throtle = 0

old_left_throtle_val = 0
old_right_throtle_val = 0

is_joystick_connected_flag = False

def connect():
    global JOY, is_joystick_connected_flag
    # Find the device
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    for device in devices:
        print(device)
        if "Gamepad" in device.name:
            JOY = evdev.InputDevice(device.path)
            print("joydevise added")
            is_joystick_connected_flag = False
            break


while True:
    try:
        # Continuously get joystick events
        for event in JOY.read_loop():
            # print(evdev.categorize(event))
            if event.type == evdev.ecodes.EV_ABS and on_off == 1 and DEAD_SWITCH == 1:
                if event.type == evdev.ecodes.EV_ABS:
                    if event.code == evdev.ecodes.ABS_Y:
                        y = JOY.absinfo(event.code)
                        left_throtle = y.value
                        if left_throtle > 1000 or left_throtle < -1000:
                            pass
                        else:
                            left_throtle = 0
                        # print("Y axis: ", y.value)
                        event_trigger_flag = True

                if event.type == evdev.ecodes.EV_ABS and on_off == 1 and DEAD_SWITCH == 1:
                    if event.code == evdev.ecodes.ABS_RX:
                        x = JOY.absinfo(event.code)
                        right_throtle = x.value
                        if right_throtle > 1000 or right_throtle < -1000:
                            pass
                        else:
                            right_throtle = 0
                        # print("x axis: ", x.value)
                        event_trigger_flag = True

            if event.type == evdev.ecodes.EV_KEY:
                event_state = evdev.categorize(event).keystate
                if event_state == evdev.KeyEvent.key_down:    # Button press event
                    if evdev.categorize(event).scancode == 308 and LEVEL < 4:   # 308 = Y Button pressed
                        if on_off == 1:
                            LEVEL += 1
                            event_trigger_flag = True
                        else:
                            pass

                    elif evdev.categorize(event).scancode == 304 and LEVEL > 1:  # 304 = A Button pressed
                        if on_off == 1:
                            LEVEL -= 1
                            event_trigger_flag = True
                        else:
                            pass

                    if evdev.categorize(event).scancode == 310:  # 310 = LB button pressed
                        if on_off == 1:
                            DEAD_SWITCH = 1
                            event_trigger_flag = True
                        else:
                            pass

                    if evdev.categorize(event).scancode == 314:  # Back button
                        on_off = 1
                        print("interlock engage")

                    if evdev.categorize(event).scancode == 315:  # start button
                        on_off = 0
                        print("interlock release")

                    # print("Button: ", evdev.categorize(event).scancode, "State: Down")

                if event_state == evdev.KeyEvent.key_up:  # Button release event
                    # print("Button: ", evdev.categorize(event).scancode, "State: Up")
                    if evdev.categorize(event).scancode == 310:    # 310 = LB button release
                        DEAD_SWITCH = 0
                        left_throtle = 0
                        right_throtle = 0

                        if on_off == 1:
                            print("Dead switch release")

                    else:
                        pass
            if event_trigger_flag and (old_left_throtle_val != left_throtle or old_right_throtle_val != right_throtle):
                print(f"level = {LEVEL}, left joy = {left_throtle}, right joy = {right_throtle}")
                old_right_throtle_val = right_throtle
                old_left_throtle_val = left_throtle

    except:
        print("joy disconnected")
        if not is_joystick_connected_flag:
            print("joydevise removed")
            is_joystick_connected_flag = True
        connect()
        sleep(1)
