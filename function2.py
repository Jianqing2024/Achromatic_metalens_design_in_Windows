import sqlite3
import numpy as np

def hyperbolic_phase(r, wav, f, shift):
    phi = -2 * np.pi / wav * (np.sqrt(r**2 + f**2) - f)+shift
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

def f2(shift0,shift1,shift2):
    R=np.array([0.5e-3])
    f=np.array([3e-3])+shift2

    waveLength=np.array([0.532e-6,0.800e-6])

    conn = sqlite3.connect("structures.db", isolation_level=None)
    cursor = conn.cursor()
    cursor.execute("PRAGMA synchronous = OFF")
    cursor.execute("PRAGMA journal_mode = MEMORY")

    cursor.execute("SELECT DISTINCT baseValue FROM structures ORDER BY baseValue")
    base_values = cursor.fetchall()

    Fit=np.zeros((len(base_values)))
    for dx, (base_val,) in enumerate(base_values):
        query="SELECT * FROM structures WHERE baseValue = ?"
        cursor.execute(query, (base_val,))
        rows=cursor.fetchall()
    
        angle=np.zeros((waveLength.size,len(rows)))
        for idx, row in enumerate(rows):
            angle[0,idx],angle[1,idx]=row[7],row[9]
            
        single=rows[0][2]
        X=create_matrix(R, single)
    
        targetPhi = np.zeros((waveLength.size,X.size))
        shift=[shift0,shift1]
        for idx, wav in enumerate(waveLength):
            targetPhi[idx,:]=wrap_to_pi(hyperbolic_phase(X, wav, f, shift[idx]))
    
        diff=np.zeros((len(rows)))
        Interpolation=np.zeros((X.size))
        for idx, Tphi in enumerate(targetPhi.T):
            for jdx, Ang in enumerate(angle.T):
                diff[jdx]=np.sum(np.abs(Tphi-Ang))

            Interpolation[idx] = diff[np.argmin(diff)]
    
        Fit[dx]=np.sum(Interpolation)
        
    bestFit = np.min(Fit)         # 最小值大小
    bestIdx = np.argmin(Fit)

    conn.close()
    return bestFit,bestIdx