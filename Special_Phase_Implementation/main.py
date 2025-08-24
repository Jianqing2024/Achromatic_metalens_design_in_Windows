from Data_quality_evaluation import main as Dm
from Data_quality_evaluation import General_function as Dg
from scipy.io import savemat
import os

def Parameter_Export():
    best = Dm.Preliminary_numerical_evaluation(48)
    COM = Dg.Command(best)

    current_dir = os.getcwd()
    save_path = os.path.join(current_dir, "Special_Phase_Implementation", 'ParameterData.mat')

    savemat(save_path, {
    'r': COM.r,
    'single': COM.single,
    })