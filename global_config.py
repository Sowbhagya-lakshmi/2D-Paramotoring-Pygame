import multiprocessing
from multiprocessing import Queue
from module.gesture_control import main_avm


speed = 60		# fps
game_duration = 120 # in sec

window_width = 1550
window_height = 800

queue_shared = multiprocessing.Queue()

process_object = multiprocessing.Process(target = main_avm, args = (queue_shared,))
