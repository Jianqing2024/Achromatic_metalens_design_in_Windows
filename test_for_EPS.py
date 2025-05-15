from Exhaustive_parameter_sweep import main
from time import time

if __name__ == "__main__":
    t1=time()
    main.main_for_EPS_Initialization()
    t2=time()
    print(f"{t2-t1}")
    #main.main_for_EPS_Resume()