from gamepad_mouse.logger import setup_logger
from gamepad_mouse.controller import GamepadMouse


def main():
    logger = setup_logger()
    try:
        controller = GamepadMouse()
        controller.run()
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)


if __name__ == "__main__":
    main()
