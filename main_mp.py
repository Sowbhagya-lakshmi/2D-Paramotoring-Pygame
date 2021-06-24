import multiprocessing
import time

from AVM import main_avm

process_object = multiprocessing.Process(target = main_avm)

# if __name__ == "__main__":
#     process_object = multiprocessing.Process(target = main_avm)
#     process_object.start()