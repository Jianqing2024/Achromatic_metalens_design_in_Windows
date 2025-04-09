import matlab.engine

eng = matlab.engine.start_matlab()
x = eng.sqrt(36.0)
a=6
print(x)