import pygame
import pyautogui
import sys
import time
import numpy as np
import logging
import os
from datetime import datetime
from config import *

os.makedirs('logs', exist_ok=True)

log_filename = f'logs/mouse_movement_{
    datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_filename),
        logging.StreamHandler()
    ]
)


class GamepadMouse:
    def __init__(self):
        pygame.init()
        pygame.joystick.init()

        if pygame.joystick.get_count() == 0:
            logging.error("No gamepad detected!")
            sys.exit(1)

        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()
        logging.info(f"Initialized gamepad: {self.joystick.get_name()}")

        self.setup_mouse_settings()
        self.current_scroll_sensitivity = SCROLL_SENSITIVITY
        self.log_system_info()

    def setup_mouse_settings(self):
        pyautogui.FAILSAFE = False
        pyautogui.PAUSE = 0.01
        self.current_sensitivity = MOUSE_SENSITIVITY

    def log_system_info(self):
        screen_width, screen_height = pyautogui.size()
        logging.info(f"Screen dimensions: {screen_width}x{screen_height}")
        logging.info(f"Initial mouse sensitivity: {self.current_sensitivity}")
        logging.info(f"Initial scroll sensitivity: {
                     self.current_scroll_sensitivity}")

    def get_stick_movement_vector(self, x_axis, y_axis):
        raw_x = self.joystick.get_axis(x_axis)
        raw_y = self.joystick.get_axis(y_axis)

        deadzone_adjusted_x = 0 if abs(raw_x) < DEADZONE else raw_x
        deadzone_adjusted_y = 0 if abs(raw_y) < DEADZONE else raw_y

        return np.array([deadzone_adjusted_x, deadzone_adjusted_y])

    def handle_button_press(self, button):
        if button == LEFT_CLICK:
            pyautogui.mouseDown(button='left')
            logging.debug("Left mouse button pressed")
        elif button == RIGHT_CLICK:
            pyautogui.mouseDown(button='right')
            logging.debug("Right mouse button pressed")
        elif button == MIDDLE_CLICK:
            pyautogui.mouseDown(button='middle')
            logging.debug("Middle mouse button pressed")
        elif button == SCROLL_SPEED_UP:
            self.increase_scroll_sensitivity()
        elif button == SCROLL_SPEED_DOWN:
            self.decrease_scroll_sensitivity()
        elif button == EXIT_BUTTON:
            logging.info("Exit button pressed")
            return True
        return False

    def handle_button_release(self, button):
        if button == LEFT_CLICK:
            pyautogui.mouseUp(button='left')
        elif button == RIGHT_CLICK:
            pyautogui.mouseUp(button='right')
        elif button == MIDDLE_CLICK:
            pyautogui.mouseUp(button='middle')

    def increase_sensitivity(self):
        self.current_sensitivity = min(
            self.current_sensitivity * SENSITIVITY_ADJUSTMENT_RATE, MAX_SENSITIVITY)
        logging.info(f"Sensitivity increased to: {self.current_sensitivity}")

    def decrease_sensitivity(self):
        self.current_sensitivity = max(
            self.current_sensitivity / SENSITIVITY_ADJUSTMENT_RATE, MIN_SENSITIVITY)
        logging.info(f"Sensitivity decreased to: {self.current_sensitivity}")

    def update_mouse_position(self, movement_vector):
        if not np.array_equal(movement_vector, np.zeros(2)):
            accelerated_movement = movement_vector * \
                np.abs(movement_vector) * ACCELERATION
            final_movement = accelerated_movement * self.current_sensitivity * MOUSE_SPEED

            try:
                current_position = np.array(pyautogui.position())
                new_position = current_position + final_movement
                pyautogui.moveTo(new_position[0], new_position[1])
            except pyautogui.FailSafeException:
                logging.warning("Failsafe triggered - cursor in corner")
            except Exception as e:
                logging.error(f"Error moving cursor: {e}", exc_info=True)

    def handle_scrolling(self, scroll_vector):
        vertical_scroll = scroll_vector[1]
        horizontal_scroll = scroll_vector[0]

        if vertical_scroll != 0:
            pyautogui.scroll(
                int(-vertical_scroll * self.current_scroll_sensitivity * 10))
        if horizontal_scroll != 0:
            pyautogui.hscroll(
                int(horizontal_scroll * self.current_scroll_sensitivity * 10))

    def increase_scroll_sensitivity(self):
        self.current_scroll_sensitivity = min(
            self.current_scroll_sensitivity * SCROLL_SENSITIVITY_ADJUSTMENT_RATE,
            MAX_SCROLL_SENSITIVITY
        )
        logging.info(f"Scroll sensitivity increased to: {
                     self.current_scroll_sensitivity}")

    def decrease_scroll_sensitivity(self):
        self.current_scroll_sensitivity = max(
            self.current_scroll_sensitivity / SCROLL_SENSITIVITY_ADJUSTMENT_RATE,
            MIN_SCROLL_SENSITIVITY
        )
        logging.info(f"Scroll sensitivity decreased to: {
                     self.current_scroll_sensitivity}")

    def run(self):
        logging.info("Starting gamepad mouse control")
        try:
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.JOYBUTTONDOWN:
                        should_exit = self.handle_button_press(event.button)
                        if should_exit:
                            return
                    elif event.type == pygame.JOYBUTTONUP:
                        self.handle_button_release(event.button)

                # Handle triggers for mouse sensitivity (changed from scroll sensitivity)
                l_trigger = self.joystick.get_axis(MOUSE_SENSITIVITY_DOWN)
                r_trigger = self.joystick.get_axis(MOUSE_SENSITIVITY_UP)

                if l_trigger > 0.5:
                    self.decrease_sensitivity()
                elif r_trigger > 0.5:
                    self.increase_sensitivity()

                movement_vector = self.get_stick_movement_vector(
                    *MOUSE_CONTROL)
                self.update_mouse_position(movement_vector)

                scroll_vector = self.get_stick_movement_vector(*SCROLL_CONTROL)
                self.handle_scrolling(scroll_vector)

                time.sleep(0.01)

        except KeyboardInterrupt:
            logging.info("Program terminated by user")
        except Exception as e:
            logging.error(f"Unexpected error: {e}", exc_info=True)
        finally:
            pygame.quit()


if __name__ == "__main__":
    try:
        controller = GamepadMouse()
        controller.run()
    except Exception as e:
        logging.error(f"Fatal error: {e}", exc_info=True)
