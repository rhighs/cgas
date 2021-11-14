from ..cloudygram_api_server.controllers import UserController
from ..cloudygram_api_server.models import UserModels
from pyramid import testing
import unittest

PHONE_NUMBER_TEST = "+393421323295"

class UserControllerTest(unittest.TestCase):
    def setUp(self):
        request = testing.DummyRequest()
        request.matchdict.update({ "phone_number": PHONE_NUMBER_TEST })
        self.config = testing.setUp(request=request)
        self.user_controller = UserController(request)

    def tearDown(self):
        testing.tearDown()

    def test_user_info_status(self):
        response = self.user_controller.user_info_req()
        self.assertTrue(response.status_code == 200)

    def test_is_authorized(self):
        response = self.user_controller.is_authorized_req()
        expected = UserModels.success("User is authorized")
        self.assertDictEqual(response.json_body, expected)

    def test_download_profile_photo(self):
        pass

    def test_contacts(self):
        pass

    def test_logout(self):
        pass

    def test_session_valid(self):
        pass

