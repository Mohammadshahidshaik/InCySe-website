from comms.Mapper import Mapper
import time 
mpr_p1 = Mapper("P3")

values, status, exeption = mpr_p1.AllGather(modelLocal=None)
print(values)
    # time.sleep(1)