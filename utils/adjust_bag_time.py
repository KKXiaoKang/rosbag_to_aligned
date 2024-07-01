#!/usr/bin/env python
import rospy
import rosbag
import argparse
from datetime import datetime


def parse_args():
    parser = argparse.ArgumentParser(description="Adjust rosbag message time")
    parser.add_argument("bags", nargs="+", type=str, help="Bag files to process")
    return parser.parse_args()


def adjust_bag_message_time(bag_files):
    with rosbag.Bag(bag_files[0], "r") as first_bag:
        f_end_time = first_bag.get_end_time()
        formatted_time = datetime.fromtimestamp(first_bag.get_start_time()).strftime(
            "%Y-%m-%d-%H-%M-%S"
        )
        new_bag_filename = f"new_{formatted_time}.bag"

    previous_end_time = f_end_time

    with rosbag.Bag(new_bag_filename, "w") as outbag:
        for i, bag_file in enumerate(bag_files):
            with rosbag.Bag(bag_file, "r") as current_bag:
                if i == 0:
                    for topic, msg, t in current_bag.read_messages():
                        outbag.write(topic, msg, t)
                else:
                    current_start_time = current_bag.get_start_time()
                    offset = rospy.Time.from_sec(
                        previous_end_time + 0.01
                    ) - rospy.Time.from_sec(current_start_time)
                    for topic, msg, t in current_bag.read_messages():
                        t += offset
                        outbag.write(topic, msg, t)
                    previous_end_time = current_bag.get_end_time() + offset.to_sec()


if __name__ == "__main__":
    args = parse_args()
    bag_files = args.bags
    adjust_bag_message_time(bag_files)
