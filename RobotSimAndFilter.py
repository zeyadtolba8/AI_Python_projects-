
import random
import numpy as np

from models import TransitionModel,ObservationModel,StateModel

#
# Add your Robot Simulator here
#
class RobotSim:
    def __init__(self, starting_state, tm):
        self._curr_State = starting_state
        self._tm = tm 
        
        
    def NewRoboPose(self):
        new_pose = np.random.choice(self._tm.get_num_of_states(), p= self._tm.get_T()[self._curr_State])
        self._curr_State = new_pose
        return new_pose

    def sensor(self, sm, om):
        o_matrix = om.get_o_matrix(self._curr_State//4)

        Ls = []
        Ls2 = []

        for index, value in enumerate(o_matrix[::4]):
            if value == 0.05:
                Ls.append(index)
            elif value == 0.025:
                Ls2.append(index)

        prob = random.random()

        if prob <= 0.1:
            return sm.state_to_reading(self._curr_State)
        elif prob <= (0.1 + (0.05 * len(Ls))):
            return random.choice(Ls)
        elif prob <= (0.1 + (0.05 * len(Ls)) + (0.025 * len(Ls2))):
            return random.choice(Ls2)
        return None

#
# Add your Filtering approach here (or within the Localiser, that is your choice!)
#
class HMMFilter:
    def __init__(self, tm):
        self._tm = tm 
        
    def calc_fvec(self, o_matrix, fVec):
        fVec = o_matrix @ self._tm.get_T_transp() @ fVec
        alpha = 1 / np.sum(fVec)
        fVec =  alpha * fVec
        return fVec



        
        
        
