import pdb
import csv

global totalBlocks
allocated_blocks = {}

class Inode:
    def __init__(self, iNum,numLinks, numBlocks, p1,p2,p3,p4,p5,
        p6,p7,p8,p9,p10,p11,p12,p13,p14,p15):
        self.inode_number = iNum
        self.ref_list = []
        self.number_of_links = numLinks
        self.number_of_blocks = numBlocks
        self.ptrs = [p1, p2, p3, p4, p5, p6, p7, p8,
        p9, p10, p11, p12, p13, p14, p15]

class Block:
    def __init__(self, bNum):
        self.block_num = bNum
        self.ref_list = []



def update_block(blockNum, inodeNum, indirectBlockNum, entryNum, file):
    if blockNum == 0 or blockNum >= totalBlocks:
        file.write("INVALID BLOCK < " + str(blockNum) + " > IN INODE < " + str(inodeNum) + " >\n") 
    elif blockNum in allocated_blocks:
        allocated_blocks[blockNum].ref_list.append((inodeNum, indirectBlockNum, entryNum))
    else:
        #new block number, so add it
        temp = Block(blockNum)
        allocated_blocks[blockNum] = temp
        allocated_blocks[blockNum].ref_list.append((inodeNum, indirectBlockNum, entryNum))

def check_blocks(inode_map, file):
    for value in inode_map.values():
        #pdb.set_trace()
        if value.number_of_blocks <= 12: #all should be direct blocks
            for i in range(value.number_of_blocks):
                if value.ptrs[i] != 0:
                    update_block(value.ptrs[i], value.inode_number, 0, i, file) #i is entry number, 0-11
        elif value.number_of_blocks > 12: #at least 1 indirect block
            #for i in value.ptrs[12:value.number_of_blocks]: #indirect blocks
            #pdb.set_trace()
            i = value.ptrs[12]
            if i == 0 or i >= totalBlocks:
                file.write("INVALID BLOCK < " + str(i) + " > IN INODE < " + str(value.inode_number) + " >\n")
            else:
                #pdb.set_trace()
                if i in indirect_map.values():
                    val = indirect_map[i]
                    update_block(i, value.iNum, val.block_num, val.entry_num, file)#will make sense once indirect_map is made
                else:
                    file.write("INVALID BLOCK < " + str(i) + " > IN INODE < " + str(value.inode_number) + " >\n")




if __name__ == '__main__':
    #open and read things
    with open('bitmap.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        all_bitmap_list = list(reader)
    with open('super.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        superblock_values = list(reader)
    global totalBlocks
    totalBlocks = int(superblock_values[0][2])
    with open('group.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        group_list = list(reader)
    inode_dictionary = {}
    with open('inode.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            temp = Inode(int(row[0]),int(row[5]), int(row[10]), int(row[11],16), int(row[12],16),int(row[13],16),
            int(row[14],16),int(row[15],16), int(row[16],16),int(row[17],16),int(row[18],16),int(row[19],16),
            int(row[20],16),int(row[21],16),int(row[22],16),int(row[23],16),int(row[24],16),int(row[25],16)) #not very snake..
            inode_dictionary[temp.inode_number] = temp
    indirect_map = {}        
    with open('indirect.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader: #hash map <(block#, entry#),blockPtr>
            indirect_map[(int(row[0],16),int(row[1]))] = int(row[2],16)

    block_bitmap_blocks = []
    inode_bitmap_blocks = []
    #this used to differentiate between inode/blocks in bitmap
    for i in group_list:
        i_num = int(i[4],16)
        b_num = int(i[5],16)
        if not inode_bitmap_blocks: #list is empty
            inode_bitmap_blocks.append(i_num)
        elif inode_bitmap_blocks[-1] != i_num: #only add each block# once
            inode_bitmap_blocks.append(i_num)
        if not block_bitmap_blocks: #list is empty
            block_bitmap_blocks.append(b_num)
        elif block_bitmap_blocks[-1] != b_num: #only add each block# once
            block_bitmap_blocks.append(b_num)
    free_inode_list = []
    free_block_list = []
    #separate entries for free blocks and inodes
    for i in all_bitmap_list:
        num = int(i[0],16)
        if num in block_bitmap_blocks:
            free_block_list.append((num,int(i[1])))
        elif num in inode_bitmap_blocks:
            free_inode_list.append((num,int(i[1])))
 #   pdb.set_trace()
    output = open("lab3b_check.txt", 'w')        
    output.truncate()
    check_blocks(inode_dictionary, output)



