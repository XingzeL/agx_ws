#!/usr/bin/env python3
# coding=UTF-8
import rospy
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Float32  

def scan_callback(scan_msg, distance_publisher):
    scan_data = scan_msg.ranges
    angle_min = scan_msg.angle_min
    angle_max = scan_msg.angle_max
    angle_increment = scan_msg.angle_increment

    # 前方方向の角度範囲を指定
    start_index = int((-0.436332 - angle_min) / angle_increment)
    end_index = int((0.436332 - angle_min) / angle_increment)

    # 前方方向の距離を取得し、無効な値（例：0）をフィルタリング
    forward_distances = [distance for distance in scan_data[start_index:end_index + 1] if distance > 0.1]

    # 最小の距離を求める
    if forward_distances:
        min_distance = min(forward_distances)
    else:
        min_distance = float('inf')

    # 結果を表示とトピックへの発行
    if min_distance != float('inf'):
        # rospy.loginfo("最小の距離: %f メートル", min_distance)
        distance_publisher.publish(min_distance)  # 距離をトピックに発行
    else:
        # rospy.loginfo("有効な距離データがありません")
        distance_publisher.publish(float('inf'))  # 無限大を発行

def main():
    rospy.init_node('scan_reader', anonymous=True)
    distance_publisher = rospy.Publisher('/front_obstacle_distance', Float32, queue_size=10)  # 追加: Publisherを設定
    rospy.Subscriber('/scan', LaserScan, lambda msg: scan_callback(msg, distance_publisher))
    rospy.loginfo("計測開始")
    rospy.spin()
    rospy.loginfo("計測終了")

if __name__ == '__main__':
    main()
