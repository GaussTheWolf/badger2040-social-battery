import badger2040
import badger_os

WIDTH = badger2040.WIDTH
HEIGHT = badger2040.HEIGHT

# Arbitrary values tbh
BATTERY_START_W = int(WIDTH*0.25)
BATTERY_START_H = int(HEIGHT*0.4)
BATTERY_WIDTH = int(WIDTH*0.5)
BATTERY_HEIGHT = int(HEIGHT*0.4)

def draw_battery():
    display.set_thickness(1)
    # Draw white background
    display.set_pen(15)
    display.clear()
    display.rectangle(0, 0, WIDTH, HEIGHT)

    # Draw battery rectangle
    display.set_pen(0)
    display.rectangle(BATTERY_START_W, BATTERY_START_H, BATTERY_WIDTH, BATTERY_HEIGHT)

    # Draw tip of battery
    display.set_pen(0)
    display.rectangle(BATTERY_START_W + BATTERY_WIDTH, BATTERY_START_H + int(BATTERY_HEIGHT*0.3), 7, int(BATTERY_HEIGHT*0.4))

    # Hollow out battery
    display.set_pen(15)
    display.rectangle(BATTERY_START_W+6, BATTERY_START_H+6, BATTERY_WIDTH-12, BATTERY_HEIGHT-12)

    # Draw text
    display.set_pen(0)
    display.set_font("sans")
    display.text("Social battery rn", int(WIDTH*0.05), int(HEIGHT*0.2), WIDTH, 1)

    # Draw levels
    display.set_pen(0)
    for i in range(0, state["level"]):
        display.rectangle(BATTERY_START_W+12 + i*25, BATTERY_START_H+12, 20, BATTERY_HEIGHT-24)

    display.update()


# ----------------
# Main starts here
# ----------------

changed = True
state = {
    # Level is from 1 to 5
    "level": 5
}
badger_os.state_load("battery", state)

display = badger2040.Badger2040()
display.led(128)
display.set_update_speed(badger2040.UPDATE_NORMAL)
display.set_thickness(2)

while True:
    # Don't go to sleep while we're doing stuff
    display.keepalive()

    if display.pressed(badger2040.BUTTON_DOWN):
        if state["level"] > 1:
            state["level"] -= 1
            changed = True

    if display.pressed(badger2040.BUTTON_UP):
        if state["level"] < 5:
            state["level"] += 1
            changed = True

    if changed:
        draw_battery()
        badger_os.state_save("battery", state)
        changed = False

    # Go to sleep if on battery
    display.halt()
