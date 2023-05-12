import matplotlib.pyplot as plt
import datetime as dt
import pandas as pd

# 创建任务数据框
tasks = ['Task 1', 'Task 2', 'Task 3', 'Task 4', 'Task 5', 'Task 6', 'Task 7', 'Task 8', 'Task 9', 'Task 10', 'Task 11', 'Task 12', 'Task 13', 'Task 14', 'Task 15', 'Task 16', 'Task 17', 'Task 18', 'Task 19']
start_dates = ['2023-03-01', '2023-03-04', '2023-03-08', '2023-03-12', '2023-03-10', '2023-03-15', '2023-03-20', '2023-03-23', '2023-03-27', '2023-03-30', '2023-04-03', '2023-04-08', '2023-04-12', '2023-04-17', '2023-04-20', '2023-04-24', '2023-04-27', '2023-05-01', '2023-05-05']
end_dates = ['2023-03-10', '2023-03-13', '2023-03-18', '2023-03-20', '2023-03-15', '2023-03-22', '2023-03-25', '2023-03-31', '2023-04-04', '2023-04-06', '2023-04-11', '2023-04-16', '2023-04-19', '2023-04-23', '2023-04-25', '2023-04-28', '2023-05-02', '2023-05-06', '2023-05-09']
durations = [10, 9, 11, 9, 6, 8, 5, 8, 7, 3, 8, 7, 4, 6, 5, 4, 5, 4, 3]
df = pd.DataFrame({
    'Task': tasks,
    'Start': start_dates,
    'End': end_dates,
    'Duration': durations
})

# 按照开始日期排序任务
df = df.sort_values(by='Start')

# 创建甘特图数据框
gantt = pd.DataFrame({
    'Task': df['Task'],
    'Start': pd.to_datetime(df['Start']),
    'End': pd.to_datetime(df['End']),
    'Duration': df['Duration'],
    'Complete': [0 for i in range(19)]
})

# 创建画布和坐标轴
fig, ax = plt.subplots(figsize=(12, 8))

# 隐藏顶部和右侧的坐标轴
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# 设置Y轴刻度
ax.set_yticks([i+0.5 for i in range(19)])
ax.set_yticklabels(gantt['Task'])

# 设置X轴范围
start_date = gantt['Start'].min() - dt.timedelta(days=1)
end_date = gantt['End'].max() + dt.timedelta(days=1)
ax.set_xlim(start_date, end_date)

# 设置图形样式
bar_height = 0.3
bar_space = 0.1
colors = ['#4CAF50', '#2196F3', '#FFC107', '#FF5722', '#9C27B0', '#00BCD4', '#F44336', '#673AB7', '#FF9800', '#795548', '#8BC34A', '#03A9F4', '#E91E63', '#9E9E9E', '#CDDC39', '#607D8B', '#FFEB3B', '#9FA8DA', '#FF5722']

# 添加任务条
for i, task in enumerate(gantt['Task']):
    start = gantt['Start'][i]
    duration = gantt['Duration'][i]
    end = gantt['End'][i]
    color = colors[i % len(colors)]
    y = i + 1
    ax.barh(y=y-bar_height/2, width=duration, height=bar_height, left=start, color=color, alpha=0.8)
    # ax.text(start, y-bar_height/2-bar_space, task, ha='left', va='center', color='white', fontsize=10)
    # ax.text(end, y-bar_height/2-bar_space, end.strftime('%Y-%m-%d'), ha='right', va='center', color='black', fontsize=10)

# 添加任务完成度
for i, comp in enumerate(gantt['Complete']):
    if comp > 0:
        y = i + 1
        ax.text(end_date, y-bar_height/2-bar_space, f'{comp:.0%}', ha='center', va='center', color='white', fontsize=10)

# 添加任务持续时间
for i, dur in enumerate(gantt['Duration']):
    y = i + 1
    ax.text(start_date, y-bar_height/2-bar_space, f'{dur} days', ha='left', va='center', fontsize=10)

# 添加标题和网格线
ax.set_title('Gantt Chart')
ax.grid(axis='y')

# 显示图形
plt.show()
