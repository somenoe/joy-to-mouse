import numpy as np
import pyautogui


def setup_mouse_settings(failsafe=False, pause=0.01):
    pyautogui.FAILSAFE = failsafe
    pyautogui.PAUSE = pause


def get_screen_dimensions():
    return pyautogui.size()


def calculate_movement(movement_vector, sensitivity, acceleration, speed):
    if not np.array_equal(movement_vector, np.zeros(2)):
        accelerated_movement = movement_vector * \
            np.abs(movement_vector) * acceleration
        return accelerated_movement * sensitivity * speed
    return np.zeros(2)
