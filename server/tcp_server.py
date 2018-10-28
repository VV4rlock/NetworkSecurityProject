import asyncio


import struct
import umsgpack
from gmpy2 import mpz, isqrt, invert, to_binary,from_binary,powmod
from gmpy2 import random_state, mpz_urandomb
import binascii

from Crypto.Cipher import ARC4

from server.db_manager import DbManager
from server.big_number_generator import CryptoObject


KEY=b"a"*50

KEY_LENGTH=1024
HOST, PORT = "localhost", 8888
SESS_KEY_LENGTH=16

crypto=CryptoObject()
G, P = crypto.get_public_g_p(KEY_LENGTH)


print("G,P was generated")

def str_handler(s):
    return "Hello,{}".format(s)


db=DbManager()
funcs={
    "auth" : db.auth,
    "change_pass" : db.change_pass,
    "get_account_by_id" : db.get_account_by_id,
    "signup" : db.signup,
    "send_str":str_handler,

}

def pack_message(msg):
    return umsgpack.dumps(msg)

def unpack_message(packed_msg):
    return umsgpack.loads(packed_msg)

class InputOverflowException(Exception):
    pass

class InputUnderflowException(Exception):
    pass

import socketserver

def read_message(s, max_input_length=4196):
    received_buffer = s.recv(8)
    #print('recv:',received_buffer)
    if len(received_buffer) < 8:
        raise InputUnderflowException('Failed to receive data: the received length is less than 8 bytes long')
    to_receive = struct.unpack('<Q', received_buffer[0:8])[0]
    if to_receive > max_input_length:
        raise InputOverflowException('Failed to receive data: requested to accept too much data')
    received_buffer = b''

    while len(received_buffer) < to_receive:
        data = s.recv(to_receive - len(received_buffer))
        if len(data) == 0:
            raise InputUnderflowException('Failed to receive data: the pipe must have been broken')
        received_buffer += data
        if len(received_buffer) > max_input_length:
            raise InputOverflowException('Failed to receive data: accepted too much data')

    return received_buffer


def send_message(s, message):
    send_buffer = struct.pack('<Q', len(message)) + message
    s.sendall(send_buffer)


a=crypto.gen_big_prime(KEY_LENGTH)
class MyTCPHandler(socketserver.BaseRequestHandler):


    def handle(self):
        # self.request is the TCP socket connected to the client
        # generate key
        global a

        command=read_message(self.request)
        if command==b"GENERATE_KEY":
            data4key={'g':to_binary(G),'p':to_binary(P),'A':to_binary(powmod(G,a,P))}
            send_message(self.request,pack_message(data4key))
            data4key=read_message(self.request)
            KEY=powmod(from_binary(unpack_message(data4key)),a,P)
            print("key created: ", KEY)
            KEY = to_binary(KEY)

            sess_key=to_binary(crypto.get_random_bytes(SESS_KEY_LENGTH))
            send_message(self.request, sess_key)

            data=unpack_message(read_message(self.request))
            account=db.auth(data[0],data[1],sess_key)
            send_message(self.request,pack_message(account))
            if account is not None:
                db.set_sesskey(account[1],binascii.b2a_hex(KEY).decode())

            a = crypto.gen_big_prime(KEY_LENGTH)
            print("<bin key>",KEY)
        elif command==b"COMMUNICATION":
            login=unpack_message(read_message(self.request))[0]
            KEY = db.get_sesskey(login)
            if KEY is None:
                print("No Sess Key")
                self.request.close()
                return
            KEY=binascii.a2b_hex(KEY)
            print("<key from db>",KEY)
            rc4 = ARC4.new(KEY)
            data = read_message(self.request)
            decrypted=rc4.decrypt(data)
            d=unpack_message(decrypted)

            if 'cmd' in d and 'args' in d:
                #print(d['args'])
                res=funcs[d['cmd']](*d['args'])
                data2recv=pack_message(res)
                encrypted_res=rc4.encrypt(data2recv)
                send_message(self.request, encrypted_res)
            else:
                data2recv = pack_message(b"null")
                encrypted_res = rc4.encrypt(data2recv)
                send_message(self.request, encrypted_res)
            self.request.close()




    # Create the server, binding to localhost on port 9999
print("Server was started of {}".format((HOST,PORT)))
with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
    server.serve_forever()