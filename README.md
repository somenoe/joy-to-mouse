# GamePad Mouse Controller

A Python application that allows you to use your game controller as a mouse input device.

## Features

- Use left analog stick for mouse movement
- Use right analog stick for scrolling (vertical and horizontal)
- Controller buttons for mouse clicks
- Adjustable mouse sensitivity with shoulder buttons (LB/RB)
- Adjustable scroll sensitivity using triggers (L2/R2)
- Support for multiple controller types (Xbox, PlayStation, and generic controllers)
- Smooth cursor movement with adjustable acceleration
- Comprehensive logging system
- Easy-to-customize control mappings

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

### Default Control Mappings

#### Button Controls

| Action          | Xbox Controller | PlayStation Controller |
|-----------------|-----------------|------------------------|
| Left Click      | A Button        | X Button               |
| Right Click     | B Button        | Circle Button          |
| Middle Click    | X Button        | Square Button          |
| Speed Up        | RB              | R1                     |
| Speed Down      | LB              | L1                     |
| Exit Program    | Start           | Options                |

#### Analog Controls

| Action                   | Control                |
|--------------------------|------------------------|
| Mouse Movement           | Left Analog Stick      |
| Scrolling                | Right Analog Stick     |
| Decrease Scroll Speed    | L2 Trigger             |
| Increase Scroll Speed    | R2 Trigger             |

## Configuration

You can customize the controls and settings by editing `config.py`. The configuration is organized into several sections:

### Button Mappings

```python
# Xbox Controller Button Constants
BUTTON_A = 0
BUTTON_B = 1
BUTTON_X = 2
# ... etc

# Button Action Mappings
LEFT_CLICK = BUTTON_A
RIGHT_CLICK = BUTTON_B
MIDDLE_CLICK = BUTTON_X
```

### Analog Stick and Trigger Mappings

```python
# Stick Action Mappings
MOUSE_CONTROL = (LEFT_ANALOG_X, LEFT_ANALOG_Y)
SCROLL_CONTROL = (RIGHT_ANALOG_X, RIGHT_ANALOG_Y)
SCROLL_SENSITIVITY_DOWN = TRIGGER_L2
SCROLL_SENSITIVITY_UP = TRIGGER_R2
```

### Mouse Settings

```python
MOUSE_SPEED = 20.0
MOUSE_SENSITIVITY = 2.0
MIN_SENSITIVITY = 0.5
MAX_SENSITIVITY = 5.0
DEADZONE = 0.1
ACCELERATION = 1.2
```

### Scroll Settings

```python
SCROLL_SENSITIVITY = 2
SCROLL_SENSITIVITY_ADJUSTMENT_RATE = 1.2
MIN_SCROLL_SENSITIVITY = 0.5
MAX_SCROLL_SENSITIVITY = 5.0
```

## Features

### Logging

The application creates detailed logs in the `logs` directory, including:

- Mouse movement tracking
- Sensitivity changes
- Error reporting
- System information

### Dynamic Sensitivity

- Real-time mouse sensitivity adjustment using shoulder buttons
- Real-time scroll sensitivity adjustment using triggers
- Built-in minimum and maximum sensitivity limits
- Smooth acceleration for precise control

## Troubleshooting

1. **Controller not detected**:
   - Ensure your controller is properly connected
   - Try reconnecting the controller
   - Check if pygame recognizes your controller
   - Verify controller drivers are installed

2. **Cursor movement issues**:
   - Adjust `MOUSE_SENSITIVITY` and `MOUSE_SPEED` in config.py
   - Try adjusting `DEADZONE` if there's unwanted drift
   - Modify `ACCELERATION` for different movement feels

3. **Scrolling issues**:
   - Adjust `SCROLL_SENSITIVITY` in config.py
   - Verify right analog stick functionality
   - Check trigger axis mappings for your controller
   - Review logs for any reported issues

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to the pygame community for the controller support
- PyAutoGUI team for mouse control functionality
- NumPy team for mathematical operations
