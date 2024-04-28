import rosbag
import matplotlib.pyplot as plt
import numpy as np

# 1. 读取rosbag文件并提取所需数据
bag = rosbag.Bag('./2024-04-26-17-58-06.bag', 'r')
kuavo_arm_traj_data = []
robot_arm_q_v_tau_data = []

kuavo_arm_traj_data_time_stamp=[]
robot_arm_q_v_tau_data_time_stamp=[]

for topic, msg, t in bag.read_messages(topics=['/kuavo_arm_traj', '/robot_arm_q_v_tau']):
    if topic == '/kuavo_arm_traj':
        kuavo_arm_traj_data.append(msg.position)
        kuavo_arm_traj_data_time_stamp.append(msg.header.stamp)
    elif topic == '/robot_arm_q_v_tau':
        # 将弧度转换为角度
        robot_arm_q_v_tau_data.append(np.rad2deg(msg.q))
        robot_arm_q_v_tau_data_time_stamp.append(msg.header.stamp)

bag.close()

# 2. 创建3行5列的图表并进行比较
num_plots = min(len(kuavo_arm_traj_data[0]), len(robot_arm_q_v_tau_data[0]), 15)  # 限制最多只显示15个数据对比
fig, axs = plt.subplots(3, 5, figsize=(20, 12))

for i in range(num_plots):
    kuavo_position = [data[i] for data in kuavo_arm_traj_data]
    robot_q = [data[i] for data in robot_arm_q_v_tau_data]
    row = i // 5
    col = i % 5
    axs[row, col].plot(kuavo_position, label='/kuavo_arm_traj')
    axs[row, col].plot(robot_q, label='/robot_arm_q_v_tau')
    axs[row, col].set_title(f"motor {i+1} state")
    axs[row, col].legend()

plt.tight_layout()
plt.show()
