from MetaSet import advancedStructure as ad
import numpy as np

r = 240e-6
single = 1.2e-6
U = np.int64(r/single*2)
x = np.linspace(-(r-0.5*single), (r-0.5*single), U)
y = np.linspace(-(r-0.5*single), (r-0.5*single), U)