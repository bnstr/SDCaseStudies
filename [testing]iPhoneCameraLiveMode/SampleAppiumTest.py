from appium import webdriver
from appium.webdriver.common.mobileby import MobileBy
import unittest

class CameraLiveModeTests(unittest.TestCase):

    def setUp(self):
        desired_caps = {
            'platformName': 'iOS',
            'platformVersion': '16.0',
            'deviceName': 'iPhone Simulator',
            'app': '/path/to/your/app.app',
            'automationName': 'XCUITest'
        }
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

    def test_capture_live_photo(self):
        driver = self.driver

        # Navigate to the camera
        camera_button = driver.find_element(MobileBy.ACCESSIBILITY_ID, 'Camera')
        camera_button.click()

        # Switch to Live mode
        live_mode_button = driver.find_element(MobileBy.ACCESSIBILITY_ID, 'LiveMode')
        live_mode_button.click()

        # Capture a photo
        capture_button = driver.find_element(MobileBy.ACCESSIBILITY_ID, 'Capture')
        capture_button.click()

        # Verify the photo is captured in Live mode
        photo = driver.find_element(MobileBy.ACCESSIBILITY_ID, 'CapturedPhoto')
        self.assertTrue(photo.is_displayed())

        # Additional verification steps as needed

    def tearDown(self):
        self.driver.quit()
