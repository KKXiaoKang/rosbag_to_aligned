## 下采样数据显示
* new_plot_show_data.py 原始显示数据
* new_plot_hz_down_sampling 将数据进行采样后对齐显示
* aligned_data_to_show.py 时间戳对齐，没办法保证百分比可以对齐

## 调整 ROSBAG 速率工具

1. 使用方法

```shell
python3 adjust_rosbag_playrate.py [-h] -i INPUT_BAG_FILE -s START_TIME -u DURATION -r PLAY_RATE

ROS bag file playback with speedup for a specified time range

options:
  -h, --help            show this help message and exit
  -i INPUT_BAG_FILE, --input_bag_file   输入 bag 文件路径
  -s START_TIME, --start_time           开始时间，单位为秒
  -u DURATION, --duration DURATION      播放时长，单位为秒
  -r PLAY_RATE, --play_rate PLAY_RATE   播放速率
```

2. 示例

**原文件**, 时长为 21.8s
```shell
$ rosbag info input.bag              
path:        input.bag
version:     2.0
duration:    21.8s
```

**加快速率**, 将 `input.bag` 文件的 `0s` 到 `10s` 的时间段，以 `2.0` 倍速播放，经过计算新时间应为 `16.8s`，通过 `rosbag info` 查看新文件的时长与预期一致

```shell
$ python3 src/kuavo_remote_control_launch/utils/adjust_rosbag_playrate.py -i input.bag -s 0 -u 10 -r 2
倍速 2.0 的bag文件已经保存到 modified_2.0x_input.bag

$ rosbag info modified_2.0x_input.bag 
path:        modified_2.0x_input.bag
version:     2.0
duration:    16.8s
```

**减慢速率**, 将 `input.bag` 文件的 `0s` 到 `20s` 的时间段，以 `0.5` 倍速播放，经过计算新时间应为 `41.8s`，通过 `rosbag info` 查看新文件的时长与预期一致

```shell
$ python3 src/kuavo_remote_control_launch/utils/adjust_rosbag_playrate.py -i input.bag -s 0 -u 20 -r 0.5
倍速 0.5 的bag文件已经保存到 modified_0.5x_input.bag

$ rosbag info modified_0.5x_input.bag
path:        modified_0.5x_input.bag
version:     2.0
duration:    41.8s
```

3. 注意事项

- 请确保输入的文件是 `ROS` 的 `bag` 文件
- 开始时间加上播放时长可以大于文件的总时长，这样默认调整到文件的最后一帧
- `r` 参数不能小于 `0`
- `s` 默认为 `0`
- `u` 默认为文件的总时长