from CRC8 import CRC8
from packer import Packer
import pickle
import re
marker = '\\'
paths_regexp = re.compile(r'\\?([ _0-9а-яА-Я\w]+[^\\]\w+)?$', re.DOTALL)


class Package:

    def __init__(self, container_filename, messages_file_paths):
        messages_file_names = []
        for path in messages_file_paths:
            name = paths_regexp.search(path).group(1)
            messages_file_names.append(name)
        self.container_filename = container_filename
        with open(container_filename, 'rb') as f:
            self.container = f.read()
        self.offset_bits = int.from_bytes(self.
                                          container[10:14], byteorder='little')
        self.message = Packer.pack(messages_file_names)
        self.messages_file_names = pickle.dumps(messages_file_names)
        self.check_sum = CRC8.get_crc(self.message)\
                             .to_bytes(1, byteorder='little')
        message_size = len(self.message).to_bytes(4, byteorder='little')
        name_size = len(self.messages_file_names).to_bytes(2,
                                                           byteorder='little')
        self.message = marker.encode() + name_size + message_size \
                                       + self.messages_file_names\
                                       + self.message \
                                       + self.check_sum

    @staticmethod
    def __text_to_bits__(byte):
        for b in byte:
            yield bin(ord(b))[2:].zfill(8)

    @staticmethod
    def __bytes_to_bits__(byte):
        for b in byte:
            yield bin(b)[2:].zfill(8)

    def __message_in_bits__(self):
        for bit in self.__bytes_to_bits__(self.message):
            yield bit

    def hide_without_palette(self):
        bmp = open(self.container_filename, 'r+b')
        container = self.container[self.offset_bits:]
        if len(self.message)*8 > len(container):
            raise Exception('Message too big for this file')
        container_bits = self.__bytes_to_bits__(container)
        encrypted = bytearray()
        for message_bits in self.__message_in_bits__():
            for bit in message_bits:
                bits = container_bits.__next__()
                bits = bits[:-1] + bit
                b = (int(bits, 2))
                encrypted.append(b)
        bmp.seek(self.offset_bits)
        bmp.write(encrypted)
        bmp.close()

    def hide_with_palette(self):
        new_offset_bits = self.offset_bits + len(self.message)
        with open(self.container_filename, 'rb') as bmp:
            container = bytearray(bmp.read())
        container[10:14] = new_offset_bits.to_bytes(4, byteorder='little')
        container = container[:self.offset_bits] + self.message \
                                                 + container[self.offset_bits:]
        with open(self.container_filename, 'wb') as bmp:
            bmp.write(container)

    def hide(self):
        if self.offset_bits == 54:
            self.hide_without_palette()
        else:
            self.hide_with_palette()
