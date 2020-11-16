from unittest.mock import patch, Mock
from unittest import mock, main, TestCase

import Receive
import Requests
import Send
import base64

class TestPrivateMessaging(TestCase):
    @patch('builtins.print')
    def test_receive(self, mock_print):
        # Input
        message = "hello"
        sender = "bob"
        recipient = "alice"

        contacts = {'bob': {'public_key': b'-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAoNd3g3mkIOmsKHfzAEDs\n34oqVz71+ZhbyyQ4wfkKjWHCbz9js7iXt5uerTLso+CivkxRE4cx3stUWFtIc9Jq\nlAiOrkPjuOZrW1qvTUI/g4EuNpBIN1UKrQTjnInVLLXD8ko5fgu38xlPMhOU2Owi\nSo6EXskByHFQVuktQxmVIdGvLf8r5sBAImtdsROxR/owjiZ4mGz7yLiOKwV9Hik4\ndQMpkHduCH5H6P0kki1B2+3pnIP3vdAXoSvfxUcL9xkb8+KpX/idwrB06hftBO9i\n6MmknI5RFwquirF1bxnuEMByWTsywvg50qCyaM+TsgMtucUkwCnkDvSL7vk5IJe7\nQwIDAQAB\n-----END PUBLIC KEY-----', 'aes_key': b'/\x9ei\xa0\xa9\xeclp;r[\xea\xad\x99\x009', 'hmac_key': b'\x1ca\x93\xe5\x94?\xe4C\xa2N\xa4\xe1\xe5:\xceB'}}

        # Expected
        enc_msg = b'q>\x1f\x9b\xab1\xf7]\x8a\x12\x0c\xd5\x91&\xc6\xef'
        iv = b'\xcb\xca\xa0U[\xf4\x15\xa8\x1fY\xf3\xc98v\xd0\xf0'
        tag = '6745d330f6b9ca03c972f617d322b733aa67ecd8a81ab5cc310c658b017dd9fd'
        enc_msg_b64 = base64.b64encode(enc_msg)
        iv_b64 = base64.b64encode(iv)

        request = Requests.direct_message(sender, recipient, str(enc_msg_b64), str(iv_b64), tag)
        parsed_request = Requests.parse_request(request)
        
        # Actual test
        Receive.receive_direct(parsed_request.data, contacts)
        mock_print.assert_called_with(sender + ": " + message)

    def test_receive_bad_tag(self):
        # Input
        message = "hello"
        sender = "bob"
        recipient = "alice"

        contacts = {'bob': {'public_key': b'-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAoNd3g3mkIOmsKHfzAEDs\n34oqVz71+ZhbyyQ4wfkKjWHCbz9js7iXt5uerTLso+CivkxRE4cx3stUWFtIc9Jq\nlAiOrkPjuOZrW1qvTUI/g4EuNpBIN1UKrQTjnInVLLXD8ko5fgu38xlPMhOU2Owi\nSo6EXskByHFQVuktQxmVIdGvLf8r5sBAImtdsROxR/owjiZ4mGz7yLiOKwV9Hik4\ndQMpkHduCH5H6P0kki1B2+3pnIP3vdAXoSvfxUcL9xkb8+KpX/idwrB06hftBO9i\n6MmknI5RFwquirF1bxnuEMByWTsywvg50qCyaM+TsgMtucUkwCnkDvSL7vk5IJe7\nQwIDAQAB\n-----END PUBLIC KEY-----', 'aes_key': b'/\x9ei\xa0\xa9\xeclp;r[\xea\xad\x99\x009', 'hmac_key': b'\x1ca\x93\xe5\x94?\xe4C\xa2N\xa4\xe1\xe5:\xceB'}}

        # Expected
        enc_msg = b"\x06\xef\xd2\xf5\xa6\x93\xed']\x81\xc4\xfb\x84K\xbe\xe0"
        iv = b'\xa4\xd58\xee\x8fu\x937y\xb6\xfd\x13\xf8\xe8j@'
        tag = ""
        enc_msg_b64 = base64.b64encode(enc_msg)
        iv_b64 = base64.b64encode(iv)

        request = Requests.direct_message(sender, recipient, str(enc_msg_b64), str(iv_b64), tag)
        parsed_request = Requests.parse_request(request)
        parsed_request = Requests.parse_request(request)
        
        # Actual test
        with self.assertRaises(Exception) as context:
            Receive.receive_direct(parsed_request.data, contacts)

    @patch('Crypto_Functions.aes_encrypt')
    @patch('Crypto_Functions.hmac')
    def test_send(self, mock_hmac, mock_aes_encrypt):
        # Input
        message = "hello"
        sender = "bob"
        recipient = "alice"

        contacts = {'bob': {'public_key': b'-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAoNd3g3mkIOmsKHfzAEDs\n34oqVz71+ZhbyyQ4wfkKjWHCbz9js7iXt5uerTLso+CivkxRE4cx3stUWFtIc9Jq\nlAiOrkPjuOZrW1qvTUI/g4EuNpBIN1UKrQTjnInVLLXD8ko5fgu38xlPMhOU2Owi\nSo6EXskByHFQVuktQxmVIdGvLf8r5sBAImtdsROxR/owjiZ4mGz7yLiOKwV9Hik4\ndQMpkHduCH5H6P0kki1B2+3pnIP3vdAXoSvfxUcL9xkb8+KpX/idwrB06hftBO9i\n6MmknI5RFwquirF1bxnuEMByWTsywvg50qCyaM+TsgMtucUkwCnkDvSL7vk5IJe7\nQwIDAQAB\n-----END PUBLIC KEY-----', 'aes_key': b'/\x9ei\xa0\xa9\xeclp;r[\xea\xad\x99\x009', 'hmac_key': b'\x1ca\x93\xe5\x94?\xe4C\xa2N\xa4\xe1\xe5:\xceB'}, 

        'alice': {'public_key': b'-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAoNd3g3mkIOmsKHfzAEDs\n34oqVz71+ZhbyyQ4wfkKjWHCbz9js7iXt5uerTLso+CivkxRE4cx3stUWFtIc9Jq\nlAiOrkPjuOZrW1qvTUI/g4EuNpBIN1UKrQTjnInVLLXD8ko5fgu38xlPMhOU2Owi\nSo6EXskByHFQVuktQxmVIdGvLf8r5sBAImtdsROxR/owjiZ4mGz7yLiOKwV9Hik4\ndQMpkHduCH5H6P0kki1B2+3pnIP3vdAXoSvfxUcL9xkb8+KpX/idwrB06hftBO9i\n6MmknI5RFwquirF1bxnuEMByWTsywvg50qCyaM+TsgMtucUkwCnkDvSL7vk5IJe7\nQwIDAQAB\n-----END PUBLIC KEY-----', 'aes_key': b'/\x9ei\xa0\xa9\xeclp;r[\xea\xad\x99\x009', 'hmac_key': b'\x1ca\x93\xe5\x94?\xe4C\xa2N\xa4\xe1\xe5:\xceB'}
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
        request = Requests.direct_message(sender, recipient, str(enc_msg_b64), str(iv_b64), tag)
        
        # Actual test
        Send.send_direct(sender, recipient, contacts, str(enc_msg_b64), mock_socket)
        mock_socket.send.assert_called_with(request)

main()