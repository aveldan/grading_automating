import os

def change_filenames(path):
    name_dict = {}
    for filename in os.listdir(path):
        str = ""
        cpy_filename = filename[0:len(filename)-4]

        i = 0
        while i<len(cpy_filename) and cpy_filename[i] != '_':
            str += cpy_filename[i]
            i += 1

        str += filename[len(filename)-4:]
        name_dict[filename] = str
    
    for key, elem in name_dict.items():
        src = path+key
        dst = path+elem
        os.rename(src,dst)

def create_file_struct(path):
    
    change_filenames(path)

    submission_dict = {}
    for filename in os.listdir(path):
        dir_name = filename[0:len(filename)-4]

        if dir_name in submission_dict.keys():
            submission_dict[dir_name].append(filename)
        else:
            submission_dict[dir_name] = [filename]

    for key, elem in submission_dict.items():
        if not os.path.isdir(path+key):
            os.mkdir(path+key)

        for fl in elem:
            src = path+fl
            dst = path+key+'/'+fl
            os.rename(src,dst)


if __name__ == "__main__":
    #For testing
    
    create_file_struct("path/to/the/all/submission/files/")