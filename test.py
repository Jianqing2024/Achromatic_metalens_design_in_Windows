import numpy as np

def wrap_to_pi(angles):
    """
    将角度包装到 [-π, π] 区间，输入为一维 numpy 数组
    """
    return (angles + np.pi) % (2 * np.pi) - np.pi

angles = np.array([0, np.pi, 2*np.pi, -3*np.pi, 3*np.pi])
wrapped = wrap_to_pi(angles)

print(wrapped)
# 输出: [ 0.         -3.14159265  0.         3.14159265 -3.14159265]
