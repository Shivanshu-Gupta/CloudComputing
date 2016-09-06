from controller import DiskController

class DiskAPI:
    def __init__(self,disk):
        self.disk = disk
        self.error_strings = ["Operation Successful","Disk ID already exists","Invalid ID: Disk ID must be positive","Block number out of range","Memory exhausted","Disk ID not found"]
    
    def CreateDisc(self,ID,blocks):
        rc = self.disk.create_disk(ID,blocks)
        self.print_msg(rc)		
        return
    
    def DeleteDisk(self,ID):
        rc = self.disk.delete_disk(ID)
        self.print_msg(rc)
        return
	
    def read(self,ID,block):
        a = self.disk.read_block(ID,block)
        self.print_msg(a[0])
        return a[1]

    def write(self,ID,block,info):
        a = self.disk.write_block(ID,block,info)
        self.print_msg(a[0])
        return

    def print_msg(self,error):
        print(self.error_strings[error-1])

if __name__ == '__main__':
    disk = DiskController(100,500)
    user = DiskAPI(disk)

    #create 2 disks
    user.CreateDisc(1,300)
    user.CreateDisc(2,100)
    #read operation
    a = user.read(1,200)
    # a = [int(i) for i in a]
    # print(a)
    
    block_update = [1]*100
    block_update = bytearray(block_update)
    user.write(1,200,block_update)
    b = user.read(1,200)
    # b = [int(i) for i in b]
    # print(b)
    user.DeleteDisk(1)
    user.CreateDisc(3,400)
    user.write(3,100,block_update)
    b = user.read(3,100)
    b = [int(i) for i in b]
    print(b)
    user.CreateDisc(4,100)