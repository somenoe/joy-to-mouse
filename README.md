# Joy-to-Mouse Controller

A Python application that allows you to use your game controller as a mouse input device.

## Features

- Use left analog stick for mouse movement
- Use right analog stick for scrolling (vertical and horizontal)
- Controller buttons for mouse clicks (A/B/X for left/right/middle)
- Adjustable scroll sensitivity with shoulder buttons (LB/RB)
- Adjustable mouse sensitivity using triggers (L2/R2)
- Pause functionality with Start button
- Smooth cursor movement with configurable:
  - Deadzone
  - Acceleration
  - Min/max sensitivity ranges
- Comprehensive logging system with:
  - Timestamped log files
  - Debug and error tracking
  - System info logging
- Easy-to-customize control mappings via config.py

## Requirements

- Python 3.7+ (3.12+ recommended 😆)
- [pygame](https://www.pygame.org/)
- [pyautogui](https://pyautogui.readthedocs.io/)
- [numpy](https://numpy.org/)

## Installation

1. Clone this repository:

    ```bash
    git clone https://github.com/somenoe/joy-to-mouse
    cd joy-to-mouse
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

### Control Mappings

#### Button Controls

| Action          | Xbox Controller | PlayStation Controller |
|-----------------|-----------------|------------------------|
| Left Click      | A Button        | X Button               |
| Right Click     | B Button        | Circle Button          |
| Middle Click    | X Button        | Square Button          |
| Speed Up        | RB              | R1                     |
| Speed Down      | LB              | L1                     |
| Pause Program   | Start           | Options                |

#### Analog Controls

| Action                   | Control                |
|--------------------------|------------------------|
| Mouse Movement           | Left Analog Stick      |
| Scrolling                | Right Analog Stick     |
| Decrease Scroll Speed    | L2 Trigger             |
| Increase Scroll Speed    | R2 Trigger             |

### Configuration

You can customize the controls and settings by editing `config.py`.

## Troubleshooting

1. **Controller not detected**:
   - Ensure your controller is properly connected
   - Try reconnecting the controller
   - Check if pygame recognizes your controller
   - Verify controller drivers are installed
   - Check logs in `logs/` directory for initialization errors

2. **Cursor movement issues**:
   - Adjust `MOUSE_SENSITIVITY` (default: 3.0) and `MOUSE_SPEED` (default: 20.0) in config.py
   - Try adjusting `DEADZONE` (default: 0.1) if there's unwanted drift
   - Modify `ACCELERATION` (default: 1.2) for different movement feels
   - Use L2/R2 triggers to dynamically adjust sensitivity between 0.5 and 7.0

3. **Scrolling issues**:
   - Adjust `SCROLL_SENSITIVITY` (default: 3) in config.py
   - Use LB/RB buttons to dynamically adjust scroll speed between 0.5 and 7.0
   - Verify right analog stick functionality
   - Check trigger axis mappings for your controller
   - Review logs in `logs/` directory for any reported issues

4. **Program freezing/unresponsive**:
   - Press Start/Options button to toggle pause state
   - Check logs for any error messages
   - Ensure CPU usage isn't too high during operation
   - Verify controller is still connected

## Acknowledgments

- Thanks to the [pygame](https://www.pygame.org) community for the controller support
- [PyAutoGUI](https://pyautogui.readthedocs.io) team for mouse control functionality
- [NumPy](https://numpy.org) team for mathematical operations

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
