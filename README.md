# GamePad Mouse Controller

A Python application that allows you to use your game controller as a mouse input device.

## Features

- Use left analog stick for mouse movement
- Use right analog stick for scrolling (vertical and horizontal)
- Controller buttons for mouse clicks
- Adjustable mouse sensitivity with upper and lower limits
- Support for multiple controller types (Xbox, PlayStation, and generic controllers)
- Smooth cursor movement with adjustable acceleration
- Comprehensive logging system
- Easy-to-customize button mappings

## Requirements

- Python 3.7+
- pygame
- pyautogui
- numpy

## Installation

1. Clone this repository:

    ```bash
    git clone https://github.com/yourusername/gamepad-mouse
    cd gamepad-mouse
    ```

2. Install the required dependencies:

    ```bash
    pip install pygame pyautogui numpy
    ```

## Usage

1. Connect your game controller to your computer
2. Run the application:

```bash
python main.py
```

### Default Controls

| Action           | Xbox Controller                  | PlayStation Controller        |
|-----------------|----------------------------------|------------------------------|
| Move Cursor     | Left Analog Stick                | Left Analog Stick           |
| Scroll Up/Down  | Right Analog Stick (Up/Down)     | Right Analog Stick (Up/Down)|
| Scroll Left/Right| Right Analog Stick (Left/Right)  | Right Analog Stick (Left/Right)|
| Left Click      | A Button (0)                     | X Button (0)                |
| Right Click     | B Button (1)                     | Circle Button (1)           |
| Middle Click    | X Button (2)                     | Square Button (2)           |
| Increase Speed  | RB (5)                           | R1 (5)                      |
| Decrease Speed  | LB (4)                           | L1 (4)                      |
| Exit            | Start Button (7)                 | Options Button (7)          |

## Configuration

You can customize the controller settings by editing `config.py`:

```python
# Mouse Settings
MOUSE_SENSITIVITY = 2.0
MOUSE_SPEED = 20.0
MIN_SENSITIVITY = 0.2
MAX_SENSITIVITY = 3.0
SCROLL_SENSITIVITY = 0.8
DEADZONE = 0.1
ACCELERATION = 1.2
```

## Features

### Logging

The application creates detailed logs in the `logs` directory, including:

- Mouse movement tracking
- Sensitivity changes
- Error reporting
- System information

### Dynamic Sensitivity

- Adjustable sensitivity during runtime using shoulder buttons
- Built-in minimum and maximum sensitivity limits
- Smooth acceleration for precise control

## Troubleshooting

1. **Controller not detected**:
   - Make sure your controller is properly connected
   - Try reconnecting the controller
   - Check if pygame recognizes your controller

2. **Cursor movement issues**:
   - Adjust MOUSE_SENSITIVITY and MOUSE_SPEED in `config.py`
   - Check the DEADZONE settings
   - Verify ACCELERATION value for smoother movement

3. **Scrolling issues**:
   - Adjust SCROLL_SENSITIVITY in `config.py`
   - Make sure the right analog stick is functioning properly
   - Check the logs for any reported issues

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to the `pygame` and `pyautogui` library developers
- Special thanks to `numpy` for vector calculations
