from planning_creator_multi_obj import *
from figure_builder import *

if __name__ == "__main__":
    X,Y,Z = surface_pareto()
    plot_3D(X,Y,Z)