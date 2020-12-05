from unittest.mock import patch, Mock
from unittest import mock, main, TestCase
import Receive
import Requests
import Send
import base64
import datetime
from freezegun import freeze_time


class TestGroupMessaging(TestCase):

    @patch('builtins.print')
    @freeze_time("2020-12-04")
    def test_receive(self, mock_print):
        # Input
        message = "hello"
        sender = "alice"
        group_name = "test"
        group_members = ["alice", "bob", "mark"]
        groups = {
            "test": {
                "aes_key": b'e\xcfO\xdc&\x8d\x87\xe0q\xf7\x1a\xeas\x05\x98\x0b',
                "hmac_key": b'\x89\x07\xadl\xa7bS\xbe\xf3\xb7\xc8\xb9\xbe\x95\xb6\xc9'
            }
        }

        # Expected
        timestamp = '1607040000.0'
        enc_msg = b'\x96\xeet\xef\xd8\xffD\xf9\xc4\xdb^\xd2\xbc\xf3\xa4k'
        iv = b'\x81\xc0\xd4\xa7\x06\x91\xdb\xea$\x99\xba\xdf\xae\xc1Q\xf1'
        tag = b'aY2BArPfzsEnjqd4m0UlKkFIIP7ExD5nLxR2GWJLHUg='
        enc_msg_b64 = base64.b64encode(enc_msg)
        iv_b64 = base64.b64encode(iv)

        request = Requests.group_message(sender, ",".join(group_members), group_name, str(enc_msg_b64), str(iv_b64), timestamp, str(tag))
        parsed_request = Requests.parse_request(request)

        # Actual test
        Receive.receive_group(parsed_request.data, groups, dict())
        mock_print.assert_called_with(sender + " to " + group_name + ": " + message)

    @freeze_time("2020-12-04")
    def test_receive_bad_tag(self):
        # Input
        message = "hello"
        sender = "alice"
        group_name = "test"
        group_members = ["alice", "bob", "mark"]
        groups = {
            "test": {
                "aes_key": b'e\xcfO\xdc&\x8d\x87\xe0q\xf7\x1a\xeas\x05\x98\x0b',
                "hmac_key": b'\x89\x07\xadl\xa7bS\xbe\xf3\xb7\xc8\xb9\xbe\x95\xb6\xc9'
            }
        }

        # Expected
        timestamp = '1607040000.0'
        enc_msg = b'\x96\xeet\xef\xd8\xffD\xf9\xc4\xdb^\xd2\xbc\xf3\xa4k'
        iv = b'\xa4\xd58\xee\x8fu\x937y\xb6\xfd\x13\xf8\xe8j@'
        tag = ""
        enc_msg_b64 = base64.b64encode(enc_msg)
        iv_b64 = base64.b64encode(iv)

        request = Requests.group_message(sender, ",".join(group_members), group_name, str(enc_msg_b64), str(iv_b64), timestamp, str(tag))
        parsed_request = Requests.parse_request(request)

        # Actual test
        with self.assertRaises(Exception) as context:
            Receive.receive_group(parsed_request.data, groups, dict())

    @freeze_time("2020-12-04")
    def test_receive_bad_iv(self):
        # Input
        message = "hello"
        sender = "alice"
        group_name = "test"
        group_members = ["alice", "bob", "mark"]
        groups = {
            "test": {
                "aes_key": b'e\xcfO\xdc&\x8d\x87\xe0q\xf7\x1a\xeas\x05\x98\x0b',
                "hmac_key": b'\x89\x07\xadl\xa7bS\xbe\xf3\xb7\xc8\xb9\xbe\x95\xb6\xc9'
            }
        }

        # Expected
        timestamp = '1607040000.0'
        enc_msg = b'\x96\xeet\xef\xd8\xffD\xf9\xc4\xdb^\xd2\xbc\xf3\xa4k'
        iv = b''
        tag = b'aY2BArPfzsEnjqd4m0UlKkFIIP7ExD5nLxR2GWJLHUg='
        enc_msg_b64 = base64.b64encode(enc_msg)
        iv_b64 = base64.b64encode(iv)

        request = Requests.group_message(sender, ",".join(group_members), group_name, str(enc_msg_b64), str(iv_b64), timestamp, str(tag))
        parsed_request = Requests.parse_request(request)

        # Actual test
        with self.assertRaises(Exception):
            Receive.receive_group(parsed_request.data, groups, dict())

    @freeze_time("2020-12-04")
    def test_receive_bad_enc_msg(self):
        # Input
        message = "hello"
        sender = "alice"
        group_name = "test"
        group_members = ["alice", "bob", "mark"]
        groups = {
            "test": {
                "aes_key": b'e\xcfO\xdc&\x8d\x87\xe0q\xf7\x1a\xeas\x05\x98\x0b',
                "hmac_key": b'\x89\x07\xadl\xa7bS\xbe\xf3\xb7\xc8\xb9\xbe\x95\xb6\xc9'
            }
        }

        # Expected
        timestamp = '1607040000.0'
        enc_msg = b""
        iv = b'\x81\xc0\xd4\xa7\x06\x91\xdb\xea$\x99\xba\xdf\xae\xc1Q\xf1'
        tag = b'aY2BArPfzsEnjqd4m0UlKkFIIP7ExD5nLxR2GWJLHUg='
        enc_msg_b64 = base64.b64encode(enc_msg)
        iv_b64 = base64.b64encode(iv)

        request = Requests.group_message(sender, ",".join(group_members), group_name, str(enc_msg_b64), str(iv_b64), timestamp, str(tag))
        parsed_request = Requests.parse_request(request)

        # Actual test
        with self.assertRaises(Exception) as context:
            Receive.receive_group(parsed_request.data, groups, dict())

    @patch('Crypto_Functions.aes_encrypt')
    @patch('Crypto_Functions.hmac')
    @freeze_time("2020-12-04")
    def test_send(self, mock_hmac, mock_aes_encrypt):
        # Input
        message = "hello"
        sender = "alice"
        group_name = "test"
        group_members = ["alice", "bob", "mark"]
        groups = {
            "test": {
                "aes_key": b'e\xcfO\xdc&\x8d\x87\xe0q\xf7\x1a\xeas\x05\x98\x0b',
                "hmac_key": b'\x89\x07\xadl\xa7bS\xbe\xf3\xb7\xc8\xb9\xbe\x95\xb6\xc9'
            }
        }

        # Mock
        mock_socket = Mock(send=Mock())
        enc_msg = b'\x96\xeet\xef\xd8\xffD\xf9\xc4\xdb^\xd2\xbc\xf3\xa4k'
        iv = b'\x81\xc0\xd4\xa7\x06\x91\xdb\xea$\x99\xba\xdf\xae\xc1Q\xf1'
        mock_aes_encrypt.return_value = (enc_msg, iv)
        tag = b'aY2BArPfzsEnjqd4m0UlKkFIIP7ExD5nLxR2GWJLHUg='
        mock_hmac.return_value = tag

        # Expected
        timestamp = '1607040000.0'
        enc_msg_b64 = base64.b64encode(enc_msg)
        iv_b64 = base64.b64encode(iv)
        request = Requests.group_message(sender, ",".join(group_members), group_name, str(enc_msg_b64), str(iv_b64), timestamp, str(tag))

        # Actual test
        Send.send_group_message(message, sender, group_name, mock_socket, group_members, groups)
        mock_socket.send.assert_called_with(request)


if __name__ == '__main__':
    main()