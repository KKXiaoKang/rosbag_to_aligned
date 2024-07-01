# #!/usr/bin/env python

import rosbag
import rospy
import argparse


def main():
    parser = argparse.ArgumentParser(
        description="ROS bag file playback with speedup for a specified time range"
    )
    parser.add_argument(
        "-i", "--input_bag_file", type=str, required=True, help="Input bag file"
    )
    parser.add_argument(
        "-s",
        "--start_time",
        type=float,
        help="Start time in seconds for speedup",
    )
    parser.add_argument(
        "-u",
        "--duration",
        type=float,
        help="Duration in seconds for speedup",
    )
    parser.add_argument(
        "-r", "--play_rate", type=float, required=True, help="Playback speedup rate"
    )
    args = parser.parse_args()
    input_bag_file = args.input_bag_file
    s = args.start_time
    u = args.duration
    play_rate = args.play_rate
    output_bag_file = f"modified_{play_rate}x_{input_bag_file}"
    if not input_bag_file.endswith(".bag"):
        print("输入文件必须是bag文件")
        return
    if play_rate <= 0:
        print("播放速度必须大于0")
        return

    with rosbag.Bag(input_bag_file, "r") as input_bag:
        with rosbag.Bag(output_bag_file, "w") as output_bag:
            start_time = input_bag.get_start_time()
            end_time = input_bag.get_end_time()
            total_duration = rospy.Time.from_sec(end_time - start_time)
            print(f"bag文件的时间范围是 {total_duration.to_sec()} 秒")
            if s is None:
                s = 0
            elif s < 0:
                print("开始时间必须大于等于0")
                return
            if u is None:
                u = int(total_duration.to_sec())
            elif u <= 0:
                print("持续时间必须大于0")
                return
            adjust_rate_start = None
            adjust_rate_end = None
            for topic, msg, t in input_bag.read_messages():
                time_offset = t.to_sec() - start_time
                if s <= time_offset <= s + u:
                    if adjust_rate_start is None:
                        adjust_rate_start = t
                        output_bag.write(topic, msg, t)
                    else:
                        offset = (t - adjust_rate_start) / play_rate
                        new_time = adjust_rate_start + offset
                        output_bag.write(topic, msg, new_time)
                        adjust_rate_end = new_time
                elif time_offset < s:
                    output_bag.write(topic, msg, t)
                elif time_offset > s + u:
                    offset = time_offset - (s + u)
                    new_time = rospy.Time.from_sec(adjust_rate_end.to_sec() + offset)
                    output_bag.write(topic, msg, new_time)

    print(f"倍速 {play_rate} 的bag文件已经保存到 {output_bag_file}")


if __name__ == "__main__":
    main()
