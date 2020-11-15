from unittest.mock import patch, Mock
from unittest import mock, main, TestCase

import Receive
import Requests
import Send
import base64

class TestGroupMessaging(TestCase):
    @patch('builtins.print')
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
        enc_msg = b"\x06\xef\xd2\xf5\xa6\x93\xed']\x81\xc4\xfb\x84K\xbe\xe0"
        iv = b'\xa4\xd58\xee\x8fu\x937y\xb6\xfd\x13\xf8\xe8j@'
        tag = "22c28febe02f33793d80696e88b50ba188c3f0aafc76f4e1ea0b094be80b50d2"
        enc_msg_b64 = base64.b64encode(enc_msg)
        iv_b64 = base64.b64encode(iv)

        request = Requests.group_message(sender, ",".join(group_members), group_name, str(enc_msg_b64), str(iv_b64), tag)
        parsed_request = Requests.parse_request(request)
        
        # Actual test
        Receive.receive_group(parsed_request.data, groups)
        mock_print.assert_called_with(sender + " to " + group_name + ": " + message)

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
        enc_msg = b"\x06\xef\xd2\xf5\xa6\x93\xed']\x81\xc4\xfb\x84K\xbe\xe0"
        iv = b'\xa4\xd58\xee\x8fu\x937y\xb6\xfd\x13\xf8\xe8j@'
        tag = ""
        enc_msg_b64 = base64.b64encode(enc_msg)
        iv_b64 = base64.b64encode(iv)

        request = Requests.group_message(sender, ",".join(group_members), group_name, str(enc_msg_b64), str(iv_b64), tag)
        parsed_request = Requests.parse_request(request)
        
        # Actual test
        with self.assertRaises(Exception) as context:
            Receive.receive_group(parsed_request.data, groups)

    @patch('Crypto_Functions.aes_encrypt')
    @patch('Crypto_Functions.hmac')
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

        # Mocks
        mock_socket = Mock(send=Mock())
        enc_msg = b"\xfd\xbdL\xb0\xb6!x%\xd2\x01]\xf2\x9a^vM"
        iv = b"\x8a\x8eP\x9aU7;\xe8\xb8,M\xb7\xa5\x97\x14\xc3"
        mock_aes_encrypt.return_value = (enc_msg, iv)
        tag = "c5c8e2d7baad57b7819bc6748bcd14cf91dc9ad5e0731fa8c26f95959ebbce01"
        mock_hmac.return_value = tag

        # Expected
        enc_msg_b64 = base64.b64encode(enc_msg)
        iv_b64 = base64.b64encode(iv)
        request = Requests.group_message(sender, ",".join(group_members), group_name, str(enc_msg_b64), str(iv_b64), tag)
        
        # Actual test
        Send.send_group_message(message, sender, group_name, mock_socket, group_members, groups)
        mock_socket.send.assert_called_with(request)

main()