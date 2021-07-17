import sys
import os
import multiprocessing

from level_1 import main_level_1
from level_2 import main_level_2
from level_3 import main_level_3

count = 0

id = os.getpid()
print(id)

if __name__ == '__main__':
    multiprocessing.freeze_support()
    count += 1
    print('COUNT: ', count)
    print('EXECUTING~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~`')
    main_level_1.main()
    # print('FINISHED LEVEL 1')
    main_level_2.main()
    main_level_3.main()

    sys.exit()  