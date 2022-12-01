import numpy as np
from scripts.cycle_logic import cycle_logic


if __name__ == "__main__":
    a = np.array([[0,0.9,1/0.63],
                  [1/0.91,0,1.8],
                  [0.61,1/1.81,0]])
    cit = [(0,0),
           (1,2),
           (2,1)]
    print(cycle_logic.calc_cycle_scores(a, cit))