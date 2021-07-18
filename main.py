import sys
import multiprocessing

from level_1 import main_level_1
from level_2 import main_level_2
from level_3 import main_level_3

def main():
    """
    Runs all 3 levels of the game
    """
    volume_button_on_status = main_level_1.main()
    main_level_2.main(volume_button_on_status)
    main_level_3.main(volume_button_on_status)


if __name__ == '__main__':
    multiprocessing.freeze_support()
    main()
    sys.exit()  