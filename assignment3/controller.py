#convention -> blocks numbered as 1 to n_blocks
#			-> extent range is inclusive
#           -> free space will be allocated starting from the lowest
#			   block number in the extent

class DiskController:
    def __init__(self,block_size,n_blocks):
        elements = [0]*block_size
        block = bytearray(elements)
        self.disk = list([block]*n_blocks)
        self.free_space = [[1,n_blocks]]
        self.disk_map = [] 
    
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

    def locate_block(self,block,extents,n_blocks):
        index = 0
        count = 0
        location = -1
        if(block > n_blocks):
            return location

        while (count<n_blocks):
            ext = extents[index]
            length = ext[1]-ext[0]+1;
            
            if(count+length < block):
                count = count+length
                index = index+1

            else:
                location = ext[0]+block-count-1
                break        
        
        return location

    # return 1 on success, 2 if ID already exists, 3 if invalid ID, 5 if memory exhausted
    def create_disk(self,ID,n_blocks):
        if(ID <= 0):
            return 3

        #search for ID
        index = self.locate_disk(ID)
        if(index != -1):
            return 2    

        #allocate free space and store extents
        blocks = 0;								
        extents = []
        while (blocks!=n_blocks):
            if(len(self.free_space)==0):
                return 5
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

        print(extents)
        #create entry in disk map
        self.disk_map.append([ID,n_blocks,extents])
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
        extents = self.disk_map[index][2]
        for ext in extents:
            self.free_space.append(ext)    

        del self.disk_map[index]
        
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
        extents = self.disk_map[index][2]
        
        #locate block
        location = self.locate_block(block,extents,n_blocks)
        print(location)
        if(location == -1):
            return (4,[],[n_blocks])
        return (1,self.disk[location-1],[])

    #returns (code,msg)
    #code-> 1 on success, 6 if ID not found, 3 if invalid ID, 4 if block number out of range 
    def write_block(self,ID,block,info):
        if(ID<=0):
            return (3,[])
        index = self.locate_disk(ID) 
        if(index == -1): 
            return (6,[])

        n_blocks = self.disk_map[index][1]
        extents = self.disk_map[index][2]
        
        #locate block
        location = self.locate_block(block,extents,n_blocks)
        if(location == -1):
            return (4,[])
        self.disk[location-1] = info   
        return (1,[]) 
        

if __name__ == '__main__':
    disk = DiskController(100,500)        