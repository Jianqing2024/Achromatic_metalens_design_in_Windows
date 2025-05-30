import numpy as np
import sqlite3
import os

base_dir = os.getcwd()
DB_PATH = os.path.join(base_dir, "data", "Main.db")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute('SELECT baseValue=0 FROM BaseParameter')
count = cursor.fetchone()[0]


r = 80e-6
single = 0.4e-6
lambda0 = 0.8e-6
lambda1 = 0.7e-6

f = 60e-6

N = int(2 * r / single)
x = np.linspace(-r, r, N)

ftx0 = -(2 * np.pi) / lambda0 * (np.sqrt(x**2 + f**2) - f)
ftx0 = np.mod(ftx0, 2 * np.pi)  # wrapTo2Pi

ftx1 = -(2 * np.pi) / lambda1 * (np.sqrt(x**2 + f**2) - f)
ftx1 = np.mod(ftx1, 2 * np.pi)  # wrapTo2Pi

phase=[0,0]
for i in range(N):
    phase[0]=ftx0[i]
    phase[1]=ftx1[i]