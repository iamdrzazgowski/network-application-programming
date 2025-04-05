import poplib
from email import parser
from email.header import decode_header
import base64
import os

host = "poczta.interia.pl"
port = 995
user = "pas2025inf@interia.pl"
password = "dq4cCRSta4VM&qqN9vesJcVeW*"



def decode_header_value(value):
    decoded_parts = decode_header(value)
    decoded_str = ''
    for part, encoding in decoded_parts:
        if isinstance(part, bytes):
            decoded_str += part.decode(encoding if encoding else 'utf-8')
        else:
            decoded_str += part
    return decoded_str

def save_attachment(part, download_folder='downloads'):
    content_disposition = part.get("Content-Disposition")
    if content_disposition and "attachment" in content_disposition:
        filename = decode_header_value(part.get_filename())

        if not os.path.exists(download_folder):
            os.makedirs(download_folder)

        file_path = os.path.join(download_folder, filename)

        with open(file_path, 'wb') as f:
            f.write(base64.b64decode(part.get_payload()))
            print(f"Załącznik zapisany: {file_path}")

server = poplib.POP3_SSL(host, port)

server.user(user)
server.pass_(password)

messages = server.list()[1]

for message in messages:
    parts = message.decode('utf-8').split()
    if len(parts) == 2:
        message_number = parts[0]

        response = server.retr(message_number)

        message_content = b"\n".join(response[1])

        msg = parser.Parser().parsestr(message_content.decode('utf-8'))

        for part in msg.walk():
            if part.get_content_maintype() == 'multipart':
                continue

            if part.get_content_type().startswith('image'):
                save_attachment(part)

server.quit()
