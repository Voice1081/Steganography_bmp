from CRC8 import CRC8
from packer import Packer
import pickle
marker = '\\'


class Unpacking:

    def __init__(self, container_filename):
        self.container_filename = container_filename
        with open(container_filename, 'rb') as f:
            self.container = f.read()
        self.offset_bits = int.from_bytes(self.container[10:14],
                                          byteorder='little')

    @staticmethod
    def __bytes_to_bits__(byte):
        for b in byte:
            yield bin(b)[2:].zfill(8)

    def verify_check_sum(self, message, end):
        new_check_sum = CRC8.get_crc(message)
        check_sum = ''
        for byte in self.__bytes_to_bits__(self.container[end:end + 8]):
            check_sum += byte[-1]
        return new_check_sum == int(check_sum, 2)

    def decrypt_char(self, container):
        message_bits = ''
        for container_bits in self.__bytes_to_bits__(container):
            message_bits += container_bits[-1]
            if len(message_bits) == 8:
                char = chr(int(message_bits, 2))
                yield char
                message_bits = ''

    def bits_to_bytes(self, container):
        message_bits = ''
        for container_bits in self.__bytes_to_bits__(container):
            message_bits += container_bits[-1]
            if len(message_bits) == 8:
                byte = int(message_bits, 2)
                yield byte
                message_bits = ''

    def extract_without_palette(self):
        container = self.container[self.offset_bits:]

        for b in self.decrypt_char(container[0:8]):
            if b != marker:
                raise Exception('File has no message')
        decrypted = bytearray()
        message_filename_size = bytearray()
        message_size = bytearray()
        message_filename = bytearray()

        for b in self.bits_to_bytes(container[8:24]):
            message_filename_size.append(b)
        message_filename_size = int.from_bytes(message_filename_size,
                                               byteorder='little') * 8

        for b in self.bits_to_bytes(container[24:56]):
            message_size.append(b)
        message_size = int.from_bytes(message_size, byteorder='little') * 8

        for b in self.bits_to_bytes(container[56:56 + message_filename_size]):
            message_filename.append(b)

        for b in self.bits_to_bytes(container[56 + message_filename_size:56
                                                 + message_filename_size
                                                 + message_size]):
            decrypted.append(b)

        if not self.verify_check_sum(decrypted, 56 + message_filename_size
                                                   + message_size
                                                   + self.offset_bits):
            raise Exception('File was changed')
        return Packer.unpack(decrypted, message_filename)

    def extract_with_palette(self):
        start_index = 54
        while chr(self.container[start_index]) != marker \
                and start_index < len(self.container):
            start_index += 1
        if start_index == len(self.container) - 1:
            raise Exception('File has no message')

        message = self.container[start_index:self.offset_bits]
        message_filename_size = int.from_bytes(message[1:3],
                                               byteorder='little')
        message_size = int.from_bytes(message[3:7], byteorder='little')
        message_filename = message[7:7+message_filename_size]
        msg = message[7+message_filename_size:7+message_filename_size
                                               + message_size]
        if CRC8.get_crc(msg) != self.container[self.offset_bits - 1]:
            raise Exception('File was changed')
        return Packer.unpack(msg, message_filename)

    def extract(self):
        if self.offset_bits == 54:
            return self.extract_without_palette()
        else:
            return self.extract_with_palette()

    def extract_names(self):
        if self.offset_bits == 54:
            message_filename_size = bytearray()
            message_filename = bytearray()
            for b in self.decrypt_char(self.container[54:62]):
                if b != marker:
                    raise Exception('File has no message')
            for b in self.bits_to_bytes(self.container[62:78]):
                message_filename_size.append(b)
            message_filename_size = int.from_bytes(message_filename_size,
                                                   byteorder='little') * 8
            for b in self.bits_to_bytes(self.container[110:
                                                       110
                                                       + message_filename_size]
                                        ):
                message_filename.append(b)
        else:
            start_index = 54
            while chr(self.container[start_index]) != marker \
                    and start_index < len(self.container):
                start_index += 1
            if start_index == len(self.container) - 1:
                raise Exception('File has no message')
            message = self.container[start_index:offset_bits]
            message_filename_size = int.from_bytes(message[1:3],
                                                   byteorder='little')
            message_filename = message[7:7 + message_filename_size]
        return pickle.loads(message_filename)
