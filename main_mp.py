import multiprocessing
import time

import main 
import AVM 
# from main import main_game
# from AVM import main_avm
# #import AVM
if __name__ == "__main__":
    # creating processes
    p1 = multiprocessing.Process(target=AVM.main_avm, args=())
    p2 = multiprocessing.Process(target=main.main_game, args=())
  
    # starting process 1
    p1.start() 

    time.sleep(10)

    # starting process 2
    p2.start()
  
    
    # wait until process 2 is finished
    p2.join()

    # wait until process 1 is finished
    p1.join()
  
    # both processes finished
    print("Done!")