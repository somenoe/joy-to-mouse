from typing import Tuple
import numpy as np
import pyautogui


def setup_mouse_settings(failsafe: bool = False, pause: float = 0.01) -> None:
    """Configure PyAutoGUI settings for mouse control."""
    pyautogui.FAILSAFE = failsafe
    pyautogui.PAUSE = pause


def get_screen_dimensions() -> Tuple[int, int]:
    """Get the current screen dimensions."""
    return pyautogui.size()


def calculate_movement(
    movement_vector: np.ndarray,
    sensitivity: float,
    acceleration: float,
    speed: float
) -> np.ndarray:
    """
    Calculate the final movement vector based on input and parameters.

    Args:
        movement_vector: Raw input vector from controller
        sensitivity: Current mouse sensitivity
        acceleration: Acceleration multiplier
        speed: Base movement speed

    Returns:
        Calculated movement vector
    """
    if not np.array_equal(movement_vector, np.zeros(2)):
        accelerated_movement = movement_vector * \
            np.abs(movement_vector) * acceleration
        return accelerated_movement * sensitivity * speed
    return np.zeros(2)
