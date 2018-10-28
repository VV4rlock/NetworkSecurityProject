
import pymysql as mysql
import hashlib
import re

import struct
import umsgpack
from gmpy2 import mpz, isqrt, invert, to_binary,from_binary,powmod
from gmpy2 import random_state, mpz_urandomb

from Crypto.Cipher import ARC4
from big_number_generator import CryptoObject

import socket

DEFAULT_SERVER_IP='127.0.0.1'
DEFAULT_SERVER_PORT=8888
SOCKET_TIMEOUT=5
SESS_KEY_LENGTH=16

KEY_LENGTH=512


crypto=CryptoObject()

def pack_message(msg):
    return umsgpack.dumps(msg)

def unpack_message(packed_msg):
    return umsgpack.loads(packed_msg)

class InputOverflowException(Exception):
    pass


class InputUnderflowException(Exception):
    pass


class Category_exist_exception(Exception):
    pass

class User_exist_exception(Exception):
    pass

class ServerAPI:

    def __init__(self,ip=DEFAULT_SERVER_IP,port=DEFAULT_SERVER_PORT):
        self.ip=ip
        self.port=port
        self.KEY=None
        self.login=None

    def signup(self,login,password):
        data = {'cmd': "signup", 'args': [login,password]}
        return self._socket_communication(data)

    def get_account_by_id(self,id):
        data = {'cmd': "get_account_by_id", 'args': [id]}
        return self._socket_communication(data)

    def change_pass(self,login,old_pass,new_pass):
        data = {'cmd': "change_pass", 'args': [login, old_pass, new_pass]}
        return self._socket_communication(data)

    def auth(self,login,password):
        fd = socket.create_connection((self.ip, self.port), timeout=SOCKET_TIMEOUT)
        self.generate_key(fd)

        sess_key=self._read_message(fd)

        md5 = hashlib.md5()
        md5.update(password.encode())
        pass_hash=md5.hexdigest()

        md5 = hashlib.md5()
        md5.update(pass_hash.encode()+sess_key)
        hash=md5.hexdigest()
        data=[login,hash]
        self._send_message(fd,pack_message(data))
        self.login=login
        return unpack_message(self._read_message(fd))


    def send_str(self,str):
        data={'cmd':"send_str", 'args':[str]}
        return self._socket_communication(data)


    def _read_message(self,s, max_input_length=4196):
        received_buffer = s.recv(8)
        # print('recv:',received_buffer)
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


    def _send_message(self,s, message):
        send_buffer = struct.pack('<Q', len(message)) + message
        s.sendall(send_buffer)


    def generate_key(self,fd):
        self._send_message(fd, b"GENERATE_KEY")
        b = crypto.gen_big_prime(KEY_LENGTH)
        data4key = self._read_message(fd)
        data4key = unpack_message(data4key)
        g, p, A = from_binary(data4key['g']), from_binary(data4key['p']), from_binary(data4key['A'])
        B = powmod(g, b, p)
        self._send_message(fd, pack_message(to_binary(B)))
        KEY = powmod(A, b, p)
        KEY = to_binary(KEY)
        self.KEY=KEY

    def _socket_communication(self,obj):
        fd = socket.create_connection((self.ip, self.port), timeout=SOCKET_TIMEOUT)
        self._send_message(fd, b"COMMUNICATION")
        self._send_message(fd, pack_message([self.login]))
        rc4 = ARC4.new(self.KEY)
        data2send = pack_message(obj)
        encpypted=rc4.encrypt(data2send)

        self._send_message(fd, encpypted)
        recv_encrypted_data = self._read_message(fd)

        recv_decpypted_data=rc4.decrypt(recv_encrypted_data)

        return unpack_message(recv_decpypted_data)
