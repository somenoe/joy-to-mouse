import pygame
import pyautogui
import sys
import time
import numpy as np
import logging
from .utils import setup_mouse_settings, get_screen_dimensions
from config import *


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

        self.setup_initial_state()
        self.log_system_info()

    def setup_initial_state(self):
        setup_mouse_settings()
        self.current_sensitivity = MOUSE_SENSITIVITY
        self.current_scroll_sensitivity = SCROLL_SENSITIVITY
        self.is_paused = False
        logging.info("Initial state setup completed")

    def log_system_info(self):
        screen_width, screen_height = get_screen_dimensions()
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
        if self.is_paused and button != PAUSE_BUTTON:
            return

        try:
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
            elif button == PAUSE_BUTTON:
                self.is_paused = not self.is_paused
                logging.info(
                    "Program " + ("paused" if self.is_paused else "resumed"))
        except Exception as e:
            logging.error(f"Button press error: {e}")

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
            try:
                screen_width, screen_height = get_screen_dimensions()
                current_position = np.array(pyautogui.position())

                # Calculate new position
                accelerated_movement = movement_vector * \
                    np.abs(movement_vector) * ACCELERATION
                final_movement = accelerated_movement * self.current_sensitivity * MOUSE_SPEED
                new_position = current_position + final_movement

                # Clamp to screen bounds
                x = max(0, min(new_position[0], screen_width - 1))
                y = max(0, min(new_position[1], screen_height - 1))

                pyautogui.moveTo(x, y)
            except Exception as e:
                logging.error(f"Mouse movement error: {e}", exc_info=True)

    def handle_scrolling(self, scroll_vector):
        try:
            vertical_scroll = scroll_vector[1]
            horizontal_scroll = scroll_vector[0]

            # Clamp scroll values
            max_scroll = 100  # Reasonable maximum
            v_scroll = max(min(int(-vertical_scroll * self.current_scroll_sensitivity * 10),
                               max_scroll), -max_scroll)
            h_scroll = max(min(int(horizontal_scroll * self.current_scroll_sensitivity * 10),
                               max_scroll), -max_scroll)

            if vertical_scroll != 0:
                pyautogui.scroll(v_scroll)
            if horizontal_scroll != 0:
                pyautogui.hscroll(h_scroll)
        except Exception as e:
            logging.error(f"Scrolling error: {e}")

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
        last_event_check = time.time()

        try:
            while True:
                try:
                    # Process events with timeout
                    current_time = time.time()
                    if current_time - last_event_check >= 0.1:  # Check every 100ms
                        pygame.event.pump()
                        last_event_check = current_time

                    for event in pygame.event.get():
                        if event.type == pygame.JOYBUTTONDOWN:
                            self.handle_button_press(event.button)
                        elif event.type == pygame.JOYBUTTONUP:
                            self.handle_button_release(event.button)
                        elif event.type == pygame.JOYDEVICEREMOVED:
                            raise RuntimeError("Controller disconnected")

                    if self.is_paused:
                        time.sleep(0.1)
                        continue

                    # Check if joystick is still connected
                    if not pygame.joystick.get_count():
                        raise RuntimeError("Controller disconnected")

                    l_trigger = self.joystick.get_axis(MOUSE_SENSITIVITY_DOWN)
                    r_trigger = self.joystick.get_axis(MOUSE_SENSITIVITY_UP)

                    if l_trigger > 0.5:
                        self.decrease_sensitivity()
                    elif r_trigger > 0.5:
                        self.increase_sensitivity()

                    movement_vector = self.get_stick_movement_vector(
                        *MOUSE_CONTROL)
                    self.update_mouse_position(movement_vector)

                    scroll_vector = self.get_stick_movement_vector(
                        *SCROLL_CONTROL)
                    self.handle_scrolling(scroll_vector)

                except pygame.error as e:
                    logging.error(f"Pygame error: {e}")
                    if "Controller" in str(e):
                        raise RuntimeError("Controller disconnected")

                time.sleep(0.01)

        except KeyboardInterrupt:
            logging.info("Program terminated by user")
        except RuntimeError as e:
            logging.error(str(e))
        except Exception as e:
            logging.error(f"Unexpected error: {e}", exc_info=True)
        finally:
            pygame.quit()
