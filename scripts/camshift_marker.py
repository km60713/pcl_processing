#!/usr/bin/env python
import rospy
from opencv_apps.msg import RotatedRectStamped
from image_view2.msg import ImageMarker2
import sys

class CentroidPublisher:

    def __init__(self):

        self.image_sub = rospy.Subscriber("/camshift/track_box", RotatedRectStamped, self.callback)
        self.camshiftmarker_pub = rospy.Publisher("/camshift_output/image_marker", ImageMarker2, queue_size=10)

    def callback (self, data):
        M = data.rect
        cx = M.center.x
        cy = M.center.y
        wi = M.size.width
        he = M.size.height
        di = max(wi, he)
        # print("-----------------------------------")
        print ("x : %f   y : %f   diameter : %f" %(cx, cy, di))
        camshiftmarker = ImageMarker2()
        camshiftmarker.position.x = cx
        camshiftmarker.position.y = cy
        camshiftmarker.scale = di
        self.camshiftmarker_pub.publish(camshiftmarker)

def main(args):
  cp = CentroidPublisher()
  rospy.init_node('camshiftmarker_publisher', anonymous=True)
  try:
    rospy.spin()
  except LeopardInterrupt:
    print("Shutting down")

if __name__ == '__main__':
    main(sys.argv)
