# import rosbag
# import matplotlib.pyplot as plt
# import numpy as np

# # 读取rosbag文件并提取所需数据
# bag = rosbag.Bag('./2024-04-25-17-22-45.bag', 'r')
# kuavo_arm_traj_data = []
# robot_arm_q_v_tau_data = []

# kuavo_arm_traj_data_time_stamp = []
# robot_arm_q_v_tau_data_time_stamp = []

# for topic, msg, t in bag.read_messages(topics=['/kuavo_arm_traj', '/robot_arm_q_v_tau']):
#     if topic == '/kuavo_arm_traj':
#         kuavo_arm_traj_data.append(msg.position)
#         kuavo_arm_traj_data_time_stamp.append(msg.header.stamp)
#     elif topic == '/robot_arm_q_v_tau':
#         # 将弧度转换为角度
#         robot_arm_q_v_tau_data.append(np.rad2deg(msg.q))
#         robot_arm_q_v_tau_data_time_stamp.append(msg.header.stamp)

# bag.close()

# # 根据时间戳对齐数据
# aligned_robot_arm_q_v_tau_data = []
# aligned_kuavo_arm_traj_data = []

# for stamp in kuavo_arm_traj_data_time_stamp:
#     stamp_sec = stamp.to_sec()
#     idx = np.argmin(np.abs(np.array([t.to_sec() for t in robot_arm_q_v_tau_data_time_stamp]) - stamp_sec))
#     aligned_robot_arm_q_v_tau_data.append(robot_arm_q_v_tau_data[idx])
#     aligned_kuavo_arm_traj_data.append(kuavo_arm_traj_data[kuavo_arm_traj_data_time_stamp.index(stamp)])

# # 下采样
# num_plots = min(len(aligned_kuavo_arm_traj_data[0]), len(aligned_robot_arm_q_v_tau_data[0]), 15)  # 限制最多只显示15个数据对比
# sampled_robot_arm_q_v_tau_data = []
# sampled_kuavo_arm_traj_data = []

# for i in range(0, len(aligned_robot_arm_q_v_tau_data), len(aligned_robot_arm_q_v_tau_data) // num_plots):
#     sampled_robot_arm_q_v_tau_data.append(aligned_robot_arm_q_v_tau_data[i])
#     sampled_kuavo_arm_traj_data.append(aligned_kuavo_arm_traj_data[i])

# # 更新图表
# fig, axs = plt.subplots(3, 5, figsize=(20, 12))

# for i in range(num_plots):
#     kuavo_position = sampled_kuavo_arm_traj_data[i]
#     robot_q = sampled_robot_arm_q_v_tau_data[i]
#     row = i // 5
#     col = i % 5
#     axs[row, col].plot(kuavo_position, label='/kuavo_arm_traj')
#     axs[row, col].plot(robot_q, label='/robot_arm_q_v_tau')
#     axs[row, col].set_title(f"motor {i+1} state")
#     axs[row, col].legend()

# plt.tight_layout()
# plt.show()