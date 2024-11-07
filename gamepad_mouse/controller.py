import pygame
import pyautogui
import sys
import time
import numpy as np
import logging
from .utils import setup_mouse_settings, get_screen_dimensions
from config import *


class GamepadMouse:
    """
    A class to control mouse movements and actions using a gamepad/controller.

    This class initializes a gamepad connection and maps controller inputs to mouse
    movements, clicks, and scrolling actions. It handles sensitivity adjustments,
    deadzone compensation, and provides pause functionality.
    """

    def __init__(self) -> None:
        """
        Initialize the GamepadMouse controller.

        Initializes pygame, connects to the first available gamepad, and sets up
        initial state and logging. Exits if no gamepad is detected.

        Raises:
            SystemExit: If no gamepad is detected.
        """
        pygame.init()
        pygame.joystick.init()

        if pygame.joystick.get_count() == 0:
            logging.error("No gamepad detected!")
            sys.exit(1)

        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()
        logging.info(f"Initialized gamepad: {self.joystick.get_name()}")

        self.initialize_state()
        self.log_system_info()

    def initialize_state(self) -> None:
        """
        Initialize the controller's state variables.

        Sets up mouse settings and initializes sensitivity and pause state variables.
        """
        setup_mouse_settings()
        self.current_sensitivity = MOUSE_SENSITIVITY
        self.current_scroll_sensitivity = SCROLL_SENSITIVITY
        self.is_paused = False
        logging.info("Initial state setup completed")

    def log_system_info(self) -> None:
        """Log system information including screen dimensions and initial sensitivity settings."""
        screen_width, screen_height = get_screen_dimensions()
        logging.info(f"Screen dimensions: {screen_width}x{screen_height}")
        logging.info(f"Initial mouse sensitivity: {self.current_sensitivity}")
        logging.info(f"Initial scroll sensitivity: {
                     self.current_scroll_sensitivity}")

    def get_deadzone_adjusted_vector(self, x_axis: int, y_axis: int) -> np.ndarray:
        """
        Apply deadzone adjustment to raw axis inputs.

        Args:
            x_axis: The joystick's x-axis index
            y_axis: The joystick's y-axis index

        Returns:
            np.ndarray: A 2D vector with deadzone-adjusted x and y values
        """
        raw_x = self.joystick.get_axis(x_axis)
        raw_y = self.joystick.get_axis(y_axis)

        deadzone_adjusted_x = 0 if abs(raw_x) < DEADZONE else raw_x
        deadzone_adjusted_y = 0 if abs(raw_y) < DEADZONE else raw_y

        return np.array([deadzone_adjusted_x, deadzone_adjusted_y])

    def process_button_press(self, button: int) -> None:
        """
        Process gamepad button press events.

        Args:
            button: The button index that was pressed

        Handles mouse clicks, sensitivity adjustments, and pause functionality.
        """
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

    def process_button_release(self, button: int) -> None:
        """
        Process gamepad button release events.

        Args:
            button: The button index that was released
        """
        if button == LEFT_CLICK:
            pyautogui.mouseUp(button='left')
        elif button == RIGHT_CLICK:
            pyautogui.mouseUp(button='right')
        elif button == MIDDLE_CLICK:
            pyautogui.mouseUp(button='middle')

    def increase_sensitivity(self) -> None:
        """
        Increase mouse movement sensitivity within defined limits.
        """
        self.current_sensitivity = min(
            self.current_sensitivity * SENSITIVITY_ADJUSTMENT_RATE, MAX_SENSITIVITY)
        logging.info(f"Sensitivity increased to: {self.current_sensitivity}")

    def decrease_sensitivity(self) -> None:
        """
        Decrease mouse movement sensitivity within defined limits.
        """
        self.current_sensitivity = max(
            self.current_sensitivity / SENSITIVITY_ADJUSTMENT_RATE, MIN_SENSITIVITY)
        logging.info(f"Sensitivity decreased to: {self.current_sensitivity}")

    def move_mouse(self, movement_vector: np.ndarray) -> None:
        """
        Move the mouse cursor based on the input vector.

        Args:
            movement_vector: A 2D numpy array containing the movement direction and magnitude

        Applies acceleration and sensitivity, and ensures the cursor stays within screen bounds.
        """
        if not np.array_equal(movement_vector, np.zeros(2)):
            try:
                screen_width, screen_height = get_screen_dimensions()
                current_position = np.array(pyautogui.position())

                accelerated_movement = movement_vector * \
                    np.abs(movement_vector) * ACCELERATION
                final_movement = accelerated_movement * self.current_sensitivity * MOUSE_SPEED
                new_position = current_position + final_movement

                x = max(0, min(new_position[0], screen_width - 1))
                y = max(0, min(new_position[1], screen_height - 1))

                pyautogui.moveTo(x, y)
            except Exception as e:
                logging.error(f"Mouse movement error: {e}", exc_info=True)

    def process_scrolling(self, scroll_vector: np.ndarray) -> None:
        """
        Process scrolling input from the gamepad.

        Args:
            scroll_vector: A 2D numpy array containing horizontal and vertical scroll values
        """
        try:
            vertical_scroll = scroll_vector[1]
            horizontal_scroll = scroll_vector[0]

            v_scroll = max(min(int(-vertical_scroll * self.current_scroll_sensitivity * 10),
                               MAX_SCROLL_VALUE), -MAX_SCROLL_VALUE)
            h_scroll = max(min(int(horizontal_scroll * self.current_scroll_sensitivity * 10),
                               MAX_SCROLL_VALUE), -MAX_SCROLL_VALUE)

            if vertical_scroll != 0:
                pyautogui.scroll(v_scroll)
            if horizontal_scroll != 0:
                pyautogui.hscroll(h_scroll)
        except Exception as e:
            logging.error(f"Scrolling error: {e}")

    def increase_scroll_sensitivity(self) -> None:
        """
        Increase scrolling sensitivity within defined limits.
        """
        self.current_scroll_sensitivity = min(
            self.current_scroll_sensitivity * SCROLL_SENSITIVITY_ADJUSTMENT_RATE,
            MAX_SCROLL_SENSITIVITY
        )
        logging.info(f"Scroll sensitivity increased to: {
                     self.current_scroll_sensitivity}")

    def decrease_scroll_sensitivity(self) -> None:
        """
        Decrease scrolling sensitivity within defined limits.
        """
        self.current_scroll_sensitivity = max(
            self.current_scroll_sensitivity / SCROLL_SENSITIVITY_ADJUSTMENT_RATE,
            MIN_SCROLL_SENSITIVITY
        )
        logging.info(f"Scroll sensitivity decreased to: {
                     self.current_scroll_sensitivity}")

    def run(self) -> None:
        """
        Start the main control loop for the gamepad mouse control.

        Continuously processes gamepad inputs and converts them to mouse actions.
        Handles controller disconnection and program termination.

        Raises:
            RuntimeError: If the controller is disconnected
            KeyboardInterrupt: If the program is terminated by the user
        """
        logging.info("Starting gamepad mouse control")
        last_event_check = time.time()

        try:
            while True:
                try:
                    current_time = time.time()
                    if current_time - last_event_check >= EVENT_CHECK_INTERVAL:
                        pygame.event.pump()
                        last_event_check = current_time

                    for event in pygame.event.get():
                        if event.type == pygame.JOYBUTTONDOWN:
                            self.process_button_press(event.button)
                        elif event.type == pygame.JOYBUTTONUP:
                            self.process_button_release(event.button)
                        elif event.type == pygame.JOYDEVICEREMOVED:
                            raise RuntimeError("Controller disconnected")

                    if self.is_paused:
                        time.sleep(0.1)
                        continue

                    if not pygame.joystick.get_count():
                        raise RuntimeError("Controller disconnected")

                    l_trigger = self.joystick.get_axis(MOUSE_SENSITIVITY_DOWN)
                    r_trigger = self.joystick.get_axis(MOUSE_SENSITIVITY_UP)

                    if l_trigger > 0.5:
                        self.decrease_sensitivity()
                    elif r_trigger > 0.5:
                        self.increase_sensitivity()

                    movement_vector = self.get_deadzone_adjusted_vector(
                        *MOUSE_CONTROL)
                    self.move_mouse(movement_vector)

                    scroll_vector = self.get_deadzone_adjusted_vector(
                        *SCROLL_CONTROL)
                    self.process_scrolling(scroll_vector)

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
