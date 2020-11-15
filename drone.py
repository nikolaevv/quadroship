import rospy
from clover import srv
from std_srvs.srv import Trigger

rospy.init_node('flight')

get_telemetry = rospy.ServiceProxy('get_telemetry', srv.GetTelemetry)
navigate = rospy.ServiceProxy('navigate', srv.Navigate)
navigate_global = rospy.ServiceProxy('navigate_global', srv.NavigateGlobal)
set_position = rospy.ServiceProxy('set_position', srv.SetPosition)
set_velocity = rospy.ServiceProxy('set_velocity', srv.SetVelocity)
set_attitude = rospy.ServiceProxy('set_attitude', srv.SetAttitude)
set_rates = rospy.ServiceProxy('set_rates', srv.SetRates)
land = rospy.ServiceProxy('land', Trigger)

def land_wait():
    land()
    while get_telemetry().armed:
        rospy.sleep(0.2)

def fly(lat, lon):
    navigate(x = 0, y = 0, z = 3, speed = 5, frame_id = 'body', auto_arm = True)
    # Взлёт на 1.5 м вверх
    navigate_global(lat = lat, lon = lon, z = 0, speed = 11.11, frame_id = 'body')
    # Полёт по координатам
    land_wait()
    # Приземление