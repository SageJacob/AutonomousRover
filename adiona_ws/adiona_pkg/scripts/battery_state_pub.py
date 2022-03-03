#!/usr/bin/env python3 

import rclpy # Import the ROS client library for Python
from rclpy.node import Node # Enables the use of rclpy's Node class
from sensor_msgs.msg import BatteryState # Enable use of the sensor_msgs/BatteryState message type
  
class BatteryStatePublisher(Node):
  
# Battery State Publisher Class
   
  def __init__(self):
    """
    Class constructor to set up the node
    """
    
    # Initiate the Node class's constructor and give it a name
    super().__init__('battery_state_pub')
      
    # Create publisher(s)   
    self.publisher_battery_state = self.create_publisher(BatteryState, '/battery_status', 10)
      
    # Time interval in seconds
    timer_period = 5.0
    self.timer = self.create_timer(timer_period, self.get_battery_state)
     
    # Initialize battery level
    self.battery_voltage = 16.0 # Set initial battery voltage
    self.percent_charge_level = 1.0  # Used to monitor percentage out of 100
    self.decrement_factor = 0.99 # Decrement charge by 0.01
      
  def get_battery_state(self):
    """
    Calls self to get battery level every time interval
    """
    msg = BatteryState() # Create a message of this type 
    msg.voltage = self.battery_voltage 
    msg.percentage = self.percent_charge_level
    self.publisher_battery_state.publish(msg) # Publish BatteryState message 
      
    # Decrement the battery state 
    self.battery_voltage = self.battery_voltage * self.decrement_factor
    self.percent_charge_level = self.percent_charge_level * self.decrement_factor
    
def main(args=None):
  
  # Initialize the rclpy library
  rclpy.init(args=args)
  
  # Create the node
  battery_state_pub = BatteryStatePublisher()
  
  # Spin the node until it is done running

  rclpy.spin(battery_state_pub)
  
  # Destroy the node explicitly
  # (optional - otherwise it will be done automatically
  # when the garbage collector destroys the node object)
  battery_state_pub.destroy_node()
  
  # Shutdown the ROS client library for Python
  rclpy.shutdown()
  
if __name__ == '__main__':
  main()