import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from rclpy.qos import qos_profile_sensor_data

class AutonomousMover(Node):
    def __init__(self):
        super().__init__('autonomous_mover')
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        self.subscription = self.create_subscription(LaserScan, '/scan', self.scan_callback, qos_profile_sensor_data)
        
        self.twist_msg = Twist()
        
        # Flags 
        self.is_turning = False     
        self.turn_direction = 1.0   
        self.turn_counter = 0       
        self.is_finished = False    

    def scan_callback(self, msg):
        # 1. Check if the maze is already completed
        if self.is_finished:
            self.twist_msg.linear.x = 0.0
            self.twist_msg.angular.z = 0.0
            self.publisher_.publish(self.twist_msg)
            return  

        front = msg.ranges[0]
        left = msg.ranges[90]
        right = msg.ranges[270]

        # 2. Turning State
        if self.is_turning:
            self.turn_counter += 1
            
            if self.turn_counter >= 10:
                self.is_turning = False   
                self.turn_counter = 0     
            else:
                self.twist_msg.linear.x = 0.0
                self.twist_msg.angular.z = 0.8 * self.turn_direction

        # 3. Moving Straight State
        else:
            if front < 1.0:
                if left < 1.5 and right < 2:
                    self.get_logger().info('Goal Reached! Stopping the robot.')
                    self.is_finished = True
                    return  
                
                self.is_turning = True
                if left > right:
                    self.turn_direction = 1.0   
                else:
                    self.turn_direction = -1.0  
            else:
                self.twist_msg.linear.x = 0.15
                self.twist_msg.angular.z = 0.0

        self.publisher_.publish(self.twist_msg)

def main(args=None):
    rclpy.init(args=args)
    rclpy.spin(AutonomousMover())
    rclpy.shutdown()

if __name__ == '__main__':
    main()