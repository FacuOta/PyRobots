import sys
import unittest
sys.path.append('../Robot')

from Robot import Robot

class testRobotClass(unittest.TestCase):

    def test_init(self):
        r : Robot = Robot(100, 50)
        self.assertTupleEqual(r.get_position(), (100, 50))
        self.assertIsNotNone(r.motor)
        self.assertIsNotNone(r.scanner)
        self.assertIsNotNone(r.weapon)

    def test_drive(self):
        r = Robot(50, 68)
        r.drive(90, 0)
        self.assertEqual(r.motor.d_direction, 90)
        self.assertEqual(r.motor.d_velocity, 0)
    
    def test_drive_out_of_bounds(self):
        r = Robot(50, 68)
        r.drive(720, 500)
        self.assertEqual(r.motor.d_direction, 720 % 360)
        self.assertEqual(r.motor.d_velocity, 20)

        r.drive(-180, 50)
        self.assertEqual(r.motor.d_direction, 180)
        self.assertEqual(r.motor.d_velocity, 20)

    def test_cannon(self):
        r = Robot(50, 68)
        self.assertTrue(r.is_cannon_ready())

        r.cannon(0, 500)
        self.assertEqual(r.weapon.get_direction(), 0)
        self.assertEqual(r.weapon.get_distance(), 500)

    def test_cannon_out_of_bounds(self):
        r = Robot(50, 68)

        r.cannon(560, 1000)
        self.assertEqual(r.weapon.get_direction(), 560 % 360)
        self.assertEqual(r.weapon.get_distance(), 700)

    
    def test_scanner(self):
        r = Robot(50, 68)

        r.point_scanner(256, -5)
        self.assertEqual(r.scanner.get_direction(), 256)
        self.assertEqual(r.scanner.get_resolution(), 5)

    def test_scanner_out_of_bounds(self):
        r = Robot(50, 68)

        r.point_scanner(900, -15)
        self.assertEqual(r.scanner.get_direction(), 900 % 360)
        self.assertEqual(r.scanner.get_resolution(), 4)

        r.point_scanner(-900, 5)
        self.assertEqual(r.scanner.get_direction(), 180)
        self.assertEqual(r.scanner.get_resolution(), 5)




if __name__ == '__main__':
    unittest.main()
