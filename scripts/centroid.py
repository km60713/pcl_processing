#!/usr/bin/env python
import rospy
from opencv_apps.msg import MomentArrayStamped
from image_view2.msg import ImageMarker2
import sys

class CentroidPublisher:

    def __init__(self):

        self.image_sub = rospy.Subscriber("/opencv_centroid/moments", MomentArrayStamped, self.callback)
        self.centroid_pub = rospy.Publisher("/centroid_image/image_marker", ImageMarker2, queue_size=10)

    def callback (self, data):
        M = data.moments[0]
        cx = int(M.m10/M.m00)
        cy = int(M.m01/M.m00)
        # print("-----------------------------------")
        print ("cx : {%d}   cy : %d " %(cx, cy))
        centroid = ImageMarker2()
        centroid.position.x = cx
        centroid.position.y = cy
        self.centroid_pub.publish(centroid)

def main(args):
  cp = CentroidPublisher()
  rospy.init_node('centroid_publisher', anonymous=True)
  try:
    rospy.spin()
  except LeopardInterrupt:
    print("Shutting down")

if __name__ == '__main__':
    main(sys.argv)
