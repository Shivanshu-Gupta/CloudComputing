import os
#convention-> blocks numbered as 1 to 500
class DiskController:
    def __init__(self):
        elements = [0]*100
        block = bytearray(elements)
        self.A = list([block]*200)
        self.B = list([block]*300)

    def locate_block(self,block):
        #block in disc A
        if(block<=200 and block>=0):
            location = (0,block-1)
        #block in disc B	
        elif(block>200 and block<=500):
            location = (1,block-200-1)
        #invalid block ID
        else:
            location = (-1,0)
        return location
					
    def read_block(self,block):
        location = self.locate_block(block)
        if(location[0] == 0):
            return self.A[location[1] ]
        elif(location[0] == 1):
            return self.B[location[1] ]
        else:
            return []		

    def write_block(self,block,info):
        location = self.locate_block(block)
        if(location[0] == 0):
            self.A[location[1] ] = info
            success = 1
        elif(location[0] == 1):
            self.B[location[1] ] = info
            success = 1
        else:
            success = 0
        return success	
							

if __name__ == '__main__':
    disk = DiskController()
    location = disk.locate_block(100)
    print(location)							