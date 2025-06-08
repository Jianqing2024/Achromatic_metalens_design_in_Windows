from MetaSet import advancedStructure as ad
from MetaSet import structSet as ss

meta = ad.MetaEngine()
ad.fishnetset(meta.fdtd, "SiO2 (Glass) - Palik", 5e-6, 5e-6, 6e-6, 5e-6)
meta.fdtd.save("aaa.fsp")