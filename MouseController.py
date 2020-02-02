from pynput.mouse import Button, Controller
import time

mouse = Controller()

# Read pointer position
print('The current pointer position is {0}'.format(
    mouse.position))

# Set pointer position
mouse.position = (1000, 500)
print('Now we have moved it to {0}'.format(
    mouse.position))

time.sleep(1)

# Move pointer relative to current position
mouse.move(500, -100)
print('Now we have moved it to {0}'.format(
    mouse.position))

# Press and release
mouse.press(Button.left)
mouse.release(Button.left)

# Double click; this is different from pressing and releasing
# twice on Mac OSX
mouse.click(Button.left, 2)
mouse.release(Button.left)

time.sleep(1)

mouse.click(Button.left, 1)

time.sleep(1)

mouse.press(Button.right)
mouse.release(Button.right)

time.sleep(1)

mouse.move(10, 10)
mouse.click(Button.left, 1)


# Scroll two steps down
mouse.scroll(0, 2)
