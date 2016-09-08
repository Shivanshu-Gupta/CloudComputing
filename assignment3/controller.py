import random

#convention -> blocks numbered as 1 to n_blocks
#			-> extent range is inclusive
#           -> free space will be allocated starting from the lowest
#			   block number in the extent
#           -> index for a disk in disk_map and backup will always be same

class DiskController:
    def __init__(self,block_size,n_blocks):
        elements = [0]*block_size
        block = bytearray(elements)
        self.disk = list([block]*n_blocks)
        self.free_space = [[1,n_blocks]]
        self.disk_map = []
        self.backup = []
        self.bad_blocks = [] 
    
    #returns index of disk in disk_map given ID; -1 if ID not present 
    def locate_disk(self,ID):
        #search for ID
        index = -1
        if(ID<=0):
            return index
        length = len(self.disk_map)
        for it in range(0,length):
            if(self.disk_map[it][0] == ID):
                index = it
                break

        return index

    #returns block number in the main disk
    def locate_block(self,block,extents,n_blocks):
        index = 0
        count = 0
        location = -1
        if(block > n_blocks):
            return (location,-1)

        while (count<n_blocks):
            ext = extents[index]
            length = ext[1]-ext[0]+1;
            
            if(count+length < block):
                count = count+length
                index = index+1

            else:
                location = ext[0]+block-count-1
                break        
        
        return (location,index)

    #returns list of extents and return code 
    def find_extents(self,n_blocks):
        blocks = 0								
        extents = []
        while (blocks!=n_blocks):
            if(len(self.free_space)==0):
                return (5,[])
            ext = self.free_space.pop()
            length = ext[1]-ext[0]+1;
            
            #add ext to extents
            if(blocks+length <= n_blocks):
                blocks = blocks+length
                extents.append(ext)

            #split the ext and add to extents
            else:
                ext1 = [ext[0],ext[0]+n_blocks-blocks-1]
                ext2 = [ext[0]+n_blocks-blocks,ext[1]]
                extents.append(ext1)
                self.free_space.append(ext2)
                blocks = n_blocks

        return (1,extents)        

    # return 1 on success, 2 if ID already exists, 3 if invalid ID, 5 if memory exhausted
    def create_disk(self,ID,n_blocks):
        if(ID <= 0):
            return 3

        #search for ID
        index = self.locate_disk(ID)
        if(index != -1):
            return 2    

        #allocate free space and store extents    
        extents1 = self.find_extents(n_blocks)
        
        #reliable storage
        extents2 = self.find_extents(n_blocks) 
        
        if(extents1[0] == 5 or extents2[0] == 5):
            return 5
        print(extents1[1])
        print(extents2[1])

        #create entry in disk map
        self.disk_map.append([ID,n_blocks,extents1[1]])
        #create entry in backup
        self.backup.append([ID,n_blocks,extents2[1]])
        return 1

    # return 1 on success, 6 if ID not found, 3 if invalid ID 
    def delete_disk(self,ID):
        #delete entry in disk map and free the corresponding space
        if(ID <= 0):
            return 3

        #search for ID
        index = self.locate_disk(ID)
        if(index == -1):
            return 6
        print(index)
        extents1 = self.disk_map[index][2]
        for ext in extents1:
            self.free_space.append(ext)    
        
        extents2 = self.backup[index][2]
        for ext in extents2:
            self.free_space.append(ext)
        
        del self.disk_map[index]
        del self.backup[index]
        
        return 1
    
    #returns (code,content,msg)
    #code-> 1 on success, 6 if ID not found, 3 if invalid ID, 4 if block number out of range 
    def read_block(self,ID,block):
        if(ID<=0):
            return (3,[],[])
        index = self.locate_disk(ID) 
        if(index == -1): 
            return (6,[],[])

        n_blocks = self.disk_map[index][1]
        extents1 = self.disk_map[index][2]

        #locate block in disk_map
        location1 = self.locate_block(block,extents1,n_blocks)
        if(location1[0] == -1):
            return (4,[],[n_blocks])
        print(location1)

        #simulate read error
        r = random.randint(1,100)
        if(r< 10):
            print("Read error")
            #read error; read from second copy; mark block as bad; create another copy
            extents2 = self.backup[index][2]
            
            #locate block in disk_map
            location2 = self.locate_block(block,extents2,n_blocks)
            
            #create another copy
            ext = self.find_extents(1)[1]
            if(ext == []):
                return (5,[],[])
            self.disk[ext[0][0]-1] = self.disk[location2[0]-1]
            
            #update extent in disk map
            pos = location1[1]
            ext_target = extents1[pos]
            if(ext_target[0] == ext_target[1]):
                extents1[pos] = ext[0]
            else:
                #handle corner case of split here                    
                if(location1[0] == ext_target[0]):
                    ext_1 = ext[0]
                    ext_2 = [location1[0]+1,ext_target[1]]
                    del extents1[pos]
                    extents1.insert(pos,ext_1)
                    extents1.insert(pos+1,ext_2)
                elif(location1[0] == ext_target[1]):
                    ext_1 = [ext_target[0],location1[0]-1]
                    ext_2 = ext[0]
                    del extents1[pos]
                    extents1.insert(pos,ext_1)
                    extents1.insert(pos+1,ext_2)
                else:        
                    ext_1 = [ext_target[0],location1[0]-1]
                    ext_2 = ext[0]
                    ext_3 = [location1[0]+1,ext_target[1]]
                    del extents1[pos]
                    extents1.insert(pos,ext_1)
                    extents1.insert(pos+1,ext_2)
                    extents1.insert(pos+2,ext_3)
                  
            #mark block as bad
            self.bad_blocks.append(location1[0])
            print(extents1)
            return (1,self.disk[location2[0]-1],[])  

        else:
            return (1,self.disk[location1[0]-1],[])

    #returns (code,msg)
    #code-> 1 on success, 6 if ID not found, 3 if invalid ID, 4 if block number out of range 
    def write_block(self,ID,block,info):
        if(ID<=0):
            return (3,[])
        index = self.locate_disk(ID) 
        if(index == -1): 
            return (6,[])

        n_blocks = self.disk_map[index][1]
        extents1 = self.disk_map[index][2]
        extents2 = self.backup[index][2]
        #locate blocks
        location1 = self.locate_block(block,extents1,n_blocks)
        location2 = self.locate_block(block,extents2,n_blocks)
        if(location1[0] == -1 or location2[0] == -1):
            return (4,[])
        self.disk[location1[0]-1] = info
        self.disk[location2[0]-1] = info   
        return (1,[]) 
        

if __name__ == '__main__':
    disk = DiskController(100,500)        