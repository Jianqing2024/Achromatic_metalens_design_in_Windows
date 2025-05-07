import numpy as np

# 示例布尔矩阵
bool_matrix = np.array([
    [1, 0, 1],
    [1, 0, 1],
    [0, 1, 1]
], dtype=bool)

def Task_directory_generation(bool_matrix):
    rows, cols = bool_matrix.shape
    neighbors_dict = {}

    # 遍历所有为 False 的位置
    for i in range(rows):
        for j in range(cols):
            if not bool_matrix[i, j]:
                neighbors = []

                # 遍历邻域（从 i-1 到 i+1，j-1 到 j+1）
                for di in [-1, 0, 1]:
                    for dj in [-1, 0, 1]:
                        ni, nj = i + di, j + dj

                        # 排除自己
                        if di == 0 and dj == 0:
                            continue

                        # 边界检查
                        if 0 <= ni < rows and 0 <= nj < cols:
                            if bool_matrix[ni, nj]:  # 只要非0的
                                neighbors.append((ni, nj))

                # 如果有非零邻居，则记录
                if neighbors:
                    neighbors_dict[(i, j)] = neighbors
    return neighbors_dict
neighbors_dict=Task_directory_generation(bool_matrix)
# 输出结果
for key, value in neighbors_dict.items():
    print(f"{key}: {value}")
