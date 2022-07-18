import polling 
import autorun
from time import sleep


autorun.run()

while True:
    polling.main()
    sleep(10)

