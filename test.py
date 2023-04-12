from models import *
import random

Rows = 8
Cols = 8
SM = StateModel(Rows, Cols)
My_robo = Localizer(SM)

steps = 100
senses = 0

filter_estimateItRight = 0
Sensor_guessItRight = 0
RandomRobo_guessItRight = 0

filter_error = 0
Sensor_error = 0
RandomRobo_error = 0


for i in range(steps):
        ret, tsX, tsY, _, srX, srY, _, _, error, _ = My_robo.update()
        rrX = random.randint(0, Rows)
        rrY = random.randint(0, Cols)
        SE = My_robo.Calc_manhattanDistance([tsX, tsY], [srX, srY])
        RE = My_robo.Calc_manhattanDistance([tsX, tsY], [rrX, rrY])

       
        # filtering
        if error == 0:
            filter_estimateItRight += 1
        filter_error += error

        # sensor readings only
        if ret:
            senses += 1
            if SE == 0:
                Sensor_guessItRight += 1
            else:    
               Sensor_error += SE

        # random movement
        if  RE == 0:
            RandomRobo_guessItRight += 1
        else:    
            RandomRobo_error += RE
   
print("Rows:", Rows)
print("Columns:", Cols)
print("Number of steps:", steps)

print("Correct filtering guesses =", filter_estimateItRight)
print("Correct sensor guesses =", Sensor_guessItRight)
print("Correct RandomRobo  guesses:", RandomRobo_guessItRight)

print("Filtering success rate: {}%".format(filter_estimateItRight/steps * 100))
print("Sensing success rate: {}%".format(Sensor_guessItRight/steps * 100))
print("RandomRobo success rate: {}%".format(RandomRobo_guessItRight/steps * 100))

print("Avg filtering error:", filter_error / steps)
print("Avg sensor  error:", (Sensor_error / senses) if senses != 0 else "Inf")
print("Avg RandomRobo error:", RandomRobo_error / steps)