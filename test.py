import multiprocessing
from tqdm import tqdm
import time

def worker(pos, iterations):
    """
    子进程任务函数，包含一个带有独立进度条的循环
    pos: 进度条的位置（行号）
    iterations: 总迭代次数
    """
    for _ in tqdm(range(iterations), position=pos, desc=f'进程 {pos}', leave=False):
        # 模拟任务处理
        time.sleep(0.1)

if __name__ == '__main__':
    num_processes = 4  # 进程数量
    iterations = 50    # 每个进程的迭代次数

    processes = []
    for i in range(num_processes):
        p = multiprocessing.Process(target=worker, args=(i, iterations))
        processes.append(p)

    # 启动所有进程
    for p in processes:
        p.start()

    # 等待所有进程完成
    for p in processes:
        p.join()

    print("所有进程已完成！")