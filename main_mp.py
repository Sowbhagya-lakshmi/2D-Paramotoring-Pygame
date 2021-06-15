import multiprocessing
import time
from global_config import num_of_lives

import main 
import AVM 
from AVM import main_avm
from main import main_game

    # creating processes
def main_multiprocessing(num_of_lives):
    #x_pos_avm, y_pos_avm = main_avm()
    p1 = multiprocessing.Process(target=main_avm, args=())
    p2 = multiprocessing.Process(target=main_game, args=())
  
    # starting process 1
    p1.start() 
    print("Started")

    time.sleep(5)

    # starting process 2
    p2.start()
  

    # wait until process 2 is finished
    p2.join()

    # wait until process 1 is finished
    p1.join()



if __name__ == "__main__":
    
    main_multiprocessing(num_of_lives)
    