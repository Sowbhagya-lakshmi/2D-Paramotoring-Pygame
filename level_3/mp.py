
import multiprocessing

from level_3.module.gesture_control import main_avm

queue_shared = multiprocessing.Queue()

process_object = multiprocessing.Process(target = main_avm, args = (queue_shared,))