import os
from controller import DiskController

class DiskApi:
    def __init__(self,disk_controller):
        self.disk_controller = disk_controller

    def read(self,block):
        a = self.disk.read_block(block)
        return a

    def write(self,block,info):
        success = self.disk.write_block(block,info)
        if(success):
            print("Write to block successful")
        else:
            print("Write failed: Invalid block number")		

if __name__ == '__main__':
    disk = DiskController()
    location = disk.locate_block(100)
    print(location) 
    user = DiskApi(disk)
    a = user.read(400)
    a = [int(i) for i in a]
    print(a)
    block_update = [1]*100
    block_update = bytearray(block_update)
    user.write(400,block_update)
    b = user.read(400)
    b = [int(i) for i in b]
    print(b)

    c = user.read(100)
    c = [int(i) for i in c]
    print(c)