import matplotlib.pyplot as plt
import numpy as np

# 每个Sprint的任务清单和每天已完成的任务量或工作小时数
# 以下是示例数据，您需要替换它们为您自己的数据
sprint1_tasks = [7, 7, 7, 3, 3, 1, 0]
sprint1_days = np.arange(len(sprint1_tasks))

sprint2_tasks = [5, 5, 4, 4, 4, 4, 2, 2, 2, 2, 2, 2, 0]
sprint2_days = np.arange(len(sprint2_tasks))

sprint3_tasks = [4, 4, 4, 4, 3, 0]
sprint3_days = np.arange(len(sprint3_tasks))

sprint4_tasks = [3, 3, 3, 3, 3, 1, 0, 0, 0, 0, 0]
sprint4_days = np.arange(len(sprint4_tasks))

# 绘制燃尽图
fig, ax = plt.subplots()
ax.plot(sprint1_days, sprint1_tasks, label='Sprint 1')
ax.plot(sprint2_days, sprint2_tasks, label='Sprint 2')
ax.plot(sprint3_days, sprint3_tasks, label='Sprint 3')
ax.plot(sprint4_days, sprint4_tasks, label='Sprint 4')

# 添加标题和标签
ax.set_title('Sprint Burn-Down Chart')
ax.set_xlabel('Days')
ax.set_ylabel('Tasks Remaining')

# 添加图例
ax.legend()

plt.show()
