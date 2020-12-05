from unittest.mock import patch, Mock
from unittest import mock, main, TestCase
import Receive
import Requests
import Send
import base64
import datetime
from freezegun import freeze_time

class TestPrivateMessaging(TestCase):
    
    @patch('builtins.print')
    @freeze_time("2020-12-04")
    def test_receive(self, mock_print):
        # Input
        message = "hello"
        sender = "bob"
        recipient = "alice"

        contacts = {'bob': {
            'public_key': b'-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAoNd3g3mkIOmsKHfzAEDs\n34oqVz71+ZhbyyQ4wfkKjWHCbz9js7iXt5uerTLso+CivkxRE4cx3stUWFtIc9Jq\nlAiOrkPjuOZrW1qvTUI/g4EuNpBIN1UKrQTjnInVLLXD8ko5fgu38xlPMhOU2Owi\nSo6EXskByHFQVuktQxmVIdGvLf8r5sBAImtdsROxR/owjiZ4mGz7yLiOKwV9Hik4\ndQMpkHduCH5H6P0kki1B2+3pnIP3vdAXoSvfxUcL9xkb8+KpX/idwrB06hftBO9i\n6MmknI5RFwquirF1bxnuEMByWTsywvg50qCyaM+TsgMtucUkwCnkDvSL7vk5IJe7\nQwIDAQAB\n-----END PUBLIC KEY-----',
            'aes_key': b'/\x9ei\xa0\xa9\xeclp;r[\xea\xad\x99\x009',
            'hmac_key': b'\x1ca\x93\xe5\x94?\xe4C\xa2N\xa4\xe1\xe5:\xceB'}}

        # Expected
        timestamp = '1607040000.0'
        enc_msg = b'\xbf\xebdMr\x9f\xdb\x94\\\x86A\xf4\xaa\x99n\xb1'
        iv = b'mVw\xc1\x93\x04Q\xb3?%\x1e\x87\x86\xd2`\xe2'
        tag = b'msf7Rb8Mia3oB9k9DAVCdDKi9MA/G1zlgGLFN4+mxIc='
        enc_msg_b64 = base64.b64encode(enc_msg)
        iv_b64 = base64.b64encode(iv)

        request = Requests.direct_message(sender, recipient, str(enc_msg_b64), str(iv_b64), timestamp, str(tag))
        parsed_request = Requests.parse_request(request)

        # Actual test
        Receive.receive_direct(parsed_request.data, contacts, dict())
        mock_print.assert_called_with(sender + ": " + message)

    @freeze_time("2020-12-04")
    def test_receive_bad_tag(self):
        # Input
        message = "hello"
        sender = "bob"
        recipient = "alice"

        contacts = {'bob': {
            'public_key': b'-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAoNd3g3mkIOmsKHfzAEDs\n34oqVz71+ZhbyyQ4wfkKjWHCbz9js7iXt5uerTLso+CivkxRE4cx3stUWFtIc9Jq\nlAiOrkPjuOZrW1qvTUI/g4EuNpBIN1UKrQTjnInVLLXD8ko5fgu38xlPMhOU2Owi\nSo6EXskByHFQVuktQxmVIdGvLf8r5sBAImtdsROxR/owjiZ4mGz7yLiOKwV9Hik4\ndQMpkHduCH5H6P0kki1B2+3pnIP3vdAXoSvfxUcL9xkb8+KpX/idwrB06hftBO9i\n6MmknI5RFwquirF1bxnuEMByWTsywvg50qCyaM+TsgMtucUkwCnkDvSL7vk5IJe7\nQwIDAQAB\n-----END PUBLIC KEY-----',
            'aes_key': b'/\x9ei\xa0\xa9\xeclp;r[\xea\xad\x99\x009',
            'hmac_key': b'\x1ca\x93\xe5\x94?\xe4C\xa2N\xa4\xe1\xe5:\xceB'}}

        # Expected
        timestamp = '1607040000.0'
        enc_msg = b'\xbf\xebdMr\x9f\xdb\x94\\\x86A\xf4\xaa\x99n\xb1'
        iv = b'mVw\xc1\x93\x04Q\xb3?%\x1e\x87\x86\xd2`\xe2'
        tag = ""
        enc_msg_b64 = base64.b64encode(enc_msg)
        iv_b64 = base64.b64encode(iv)

        request = Requests.direct_message(sender, recipient, str(enc_msg_b64), str(iv_b64), timestamp, str(tag))
        parsed_request = Requests.parse_request(request)

        # Actual test
        with self.assertRaises(Exception) as context:
            Receive.receive_direct(parsed_request.data, contacts, timestamp)

    @patch('Crypto_Functions.aes_encrypt')
    @patch('Crypto_Functions.hmac')
    @freeze_time("2020-12-04")
    def test_send(self, mock_hmac, mock_aes_encrypt):
        # Input
        message = "hello"
        sender = "bob"
        recipient = "alice"

        contacts = {'bob': {
            'public_key': b'-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAoNd3g3mkIOmsKHfzAEDs\n34oqVz71+ZhbyyQ4wfkKjWHCbz9js7iXt5uerTLso+CivkxRE4cx3stUWFtIc9Jq\nlAiOrkPjuOZrW1qvTUI/g4EuNpBIN1UKrQTjnInVLLXD8ko5fgu38xlPMhOU2Owi\nSo6EXskByHFQVuktQxmVIdGvLf8r5sBAImtdsROxR/owjiZ4mGz7yLiOKwV9Hik4\ndQMpkHduCH5H6P0kki1B2+3pnIP3vdAXoSvfxUcL9xkb8+KpX/idwrB06hftBO9i\n6MmknI5RFwquirF1bxnuEMByWTsywvg50qCyaM+TsgMtucUkwCnkDvSL7vk5IJe7\nQwIDAQAB\n-----END PUBLIC KEY-----',
            'aes_key': b'/\x9ei\xa0\xa9\xeclp;r[\xea\xad\x99\x009',
            'hmac_key': b'\x1ca\x93\xe5\x94?\xe4C\xa2N\xa4\xe1\xe5:\xceB'},

                    'alice': {
                        'public_key': b'-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAoNd3g3mkIOmsKHfzAEDs\n34oqVz71+ZhbyyQ4wfkKjWHCbz9js7iXt5uerTLso+CivkxRE4cx3stUWFtIc9Jq\nlAiOrkPjuOZrW1qvTUI/g4EuNpBIN1UKrQTjnInVLLXD8ko5fgu38xlPMhOU2Owi\nSo6EXskByHFQVuktQxmVIdGvLf8r5sBAImtdsROxR/owjiZ4mGz7yLiOKwV9Hik4\ndQMpkHduCH5H6P0kki1B2+3pnIP3vdAXoSvfxUcL9xkb8+KpX/idwrB06hftBO9i\n6MmknI5RFwquirF1bxnuEMByWTsywvg50qCyaM+TsgMtucUkwCnkDvSL7vk5IJe7\nQwIDAQAB\n-----END PUBLIC KEY-----',
                        'aes_key': b'/\x9ei\xa0\xa9\xeclp;r[\xea\xad\x99\x009',
                        'hmac_key': b'\x1ca\x93\xe5\x94?\xe4C\xa2N\xa4\xe1\xe5:\xceB'}
                    }

        # Mocks
        timestamp = '1607040000.0'
        mock_socket = Mock(send=Mock())
        enc_msg = b'\xbf\xebdMr\x9f\xdb\x94\\\x86A\xf4\xaa\x99n\xb1'
        iv = b'mVw\xc1\x93\x04Q\xb3?%\x1e\x87\x86\xd2`\xe2'
        mock_aes_encrypt.return_value = (enc_msg, iv)
        tag = b'msf7Rb8Mia3oB9k9DAVCdDKi9MA/G1zlgGLFN4+mxIc='
        mock_hmac.return_value = tag

        # Expected
        enc_msg_b64 = base64.b64encode(enc_msg) 
        iv_b64 = base64.b64encode(iv)
        request = Requests.direct_message(sender, recipient, str(enc_msg_b64), str(iv_b64), timestamp, str(tag))

        # Actual test
        Send.send_direct(sender, recipient, contacts, str(enc_msg_b64), mock_socket)
        mock_socket.send.assert_called_with(request)

if __name__ == '__main__':
    main()