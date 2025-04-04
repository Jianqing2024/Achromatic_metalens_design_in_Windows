import sqlite3
import numpy as np
import optuna

def hyperbolic_phase(r, wav, f):
    phi = -2 * np.pi / wav * (np.sqrt(r**2 + f**2) - f)
    return phi
def create_matrix(R, single):
    num_elements = int(R // single)
    if R % single != 0:
        num_elements += 1
    matrix = np.arange(0.5*single, num_elements * single, single)
    if matrix[-1] > R:
        matrix = matrix[matrix <= R]
    return matrix
def wrap_to_pi(angles):
    return (angles + np.pi) % (2 * np.pi) - np.pi

R=np.array([0.5e-3])
f=np.array([3e-3])

conn = sqlite3.connect("structures.db")
cursor = conn.cursor()

cursor.execute("SELECT DISTINCT baseValue FROM structures ORDER BY baseValue")
base_values = cursor.fetchall()

for (base_val,) in base_values:
    query="SELECT * FROM structures WHERE baseValue = ?"
    cursor.execute(query, (base_val,))
    rows=cursor.fetchall()
    single=rows[0][2]
    x=create_matrix(R, single)
    phi=hyperbolic_phase(x, np.array([0.532e-6]), f)
    phi=wrap_to_pi(phi)
    print(phi)
    for row in rows:
        print("++++++")



































conn.close()