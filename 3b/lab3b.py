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
        p9, p10, p11, p12]

class Block:
    def __init__(bNum):
        self.block_num = bnum
        self.ref_list = []

def update_block(blockNum, inodeNum, indirectBlockNum, entryNum):
    if blockNum == 0 or blockNum >= totalBlocks:
        pass#invalid block error
    elif blockNum in allocated_blocks:
        allocated_blocks[blockNum].ref_list.add(inodeNum, indirectBlockNum, entryNum)
    else:
        #new block number, so add it
        allocated_blocks.add(blockNum)
        allocated_blocks[blockNum].ref_list.add(inodeNum, indirectBlockNum, entryNum)

def check_blocks(inode_map):
    pass#numBlocks = 
    



if __name__ == '__main__':
    #open and read things
    with open('bitmap.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        all_bitmap_list = list(reader)
    with open('super.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        superblock_values = list(reader)
    global totalBlocks
    totalBlocks = superblock_values[0][2]
    with open('group.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        group_list = list(reader)
    inode_dictionary = {}
    with open('inode.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            temp = Inode(row[0],row[5], row[10], row[11], row[12],row[13],
            row[14],row[15], row[16],row[17],row[18],row[19],
            row[20],row[21],row[22],row[23],row[24],row[25]) #not very snake..
            inode_dictionary[temp.inode_number] = temp

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




