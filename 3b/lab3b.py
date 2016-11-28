import csv


if __name__ == '__main__':
    with open('bitmap.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        all_bitmap_list = list(reader)
    with open('super.csv', 'r') as csvfile:
    	reader = csv.reader(csvfile)
    	superblock_values = list(reader)
    free_inode_list = []
    free_block_list = []
    #print(free_inode_list[0][len(free_inode_list[0]) - 1])
    for i in all_bitmap_list:
    	if i[0].endswith("1") or i[0].endswith("3"):
    		free_block_list.append((int(i[0],16),int(i[1])))
    	if i[0].endswith("2") or i[0].endswith("4"):
    		free_inode_list.append((int(i[0],16),int(i[1])))


