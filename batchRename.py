import shutil
import sys
import glob
import os

'''
Returns a dict mapping input file name to output file name such that
    dict[input_name] = output_name
'''
def get_mappings(mappingsFile):
    mapping = {}
    with open(mappingsFile) as data:
        for line in data:
            key, value = line.split(',')
            mapping[key] = value.strip()
    return mapping

'''
References
    https://stackoverflow.com/questions/123198/how-do-i-copy-a-file-in-python
''' 
def main():
    #Handle incorrect input
    if(len(sys.argv) < 4):
        print('Please provide the input folder, outpug folder, and renaming mappings file')
        print('For example: python batchResize.py in/folder/ out/folder/ mappings.csv')
        exit()

    #Collect input
    inDir = sys.argv[1]
    outDir = sys.argv[2]
    mappingsFile = sys.argv[3]

    #Get file names (base names only)
    os.chdir(inDir)
    file_names = glob.glob('*')
    os.chdir('..')

    #Copy images to outDir with their new names
    mappings = get_mappings(mappingsFile)
    for file_name in file_names:
        shutil.copyfile(os.path.join(inDir, file_name), os.path.join(outDir, mappings[file_name]))

main()