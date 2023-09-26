import requests
import os
import filecmp

authorization_val = 'Secret auth key'

def get_my_students(ass_num):
    
    students_info_url = "The url"
    req_url = students_info_url + str(ass_num)
    head_dict = {}
    head_dict['Authorization'] = authorization_val
    response = requests.get(url=req_url,headers=head_dict)

    if response.status_code != 200:
        print("Not a 200 response")
        print(response)
        return None
    
    return response.json()["data"]

def get_the_latest_submission(std_id, ass_num):
    submissions_list_url = "The url"+str(ass_num)+"conti url"+str(std_id)
    head_dict = {}
    head_dict['Authorization'] = authorization_val
    response = requests.get(url=submissions_list_url, headers=head_dict)

    if response.status_code != 200:
        print("Not a 200 response")
        print(response)
        return None
    
    submissions = response.json()["data"]
    submissions = sorted(submissions, key=lambda x: x['created_at'])
    latest_submission = submissions[len(submissions)-1]

    return latest_submission

def download_py(std_id, path, filename, ass_num):
    
    latest_submission = get_the_latest_submission(std_id, ass_num)
    
    file_download_url = "The url"+latest_submission["FilePath"]
    head_dict = {}
    head_dict['Authorization'] = authorization_val
    response = requests.get(url=file_download_url, headers=head_dict)
    
    if response.status_code != 200:
        print("Not a 200 response")
        print(response)
        return None

    flptr = open(path+filename+'/'+filename+".py", "w")
    flptr.write(response.text)

    flptr.close()

    return latest_submission

def get_py_files(ass_num, path):
    std_list = get_my_students(ass_num=ass_num)
    
    if std_list == None:
        return
    
    std_dict = {}
    for student in std_list:
        tmp_string = ""
        tmp_list = student["Fullname"].lower().split(' ')
        tmp_string += tmp_list[len(tmp_list)-1]
        for i in range(0,len(tmp_list)-1):
            tmp_string += tmp_list[i]
        std_dict[student["StudentId"]] = tmp_string

    last_subs = {}
    for key, elem in std_dict.items():
        last = download_py(key,path,elem,ass_num)
        if last == None:
            return None
        
        last_subs[elem] = last

    return last_subs    


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

def compare(path, std_dict):
    
    same_or_not = {}

    for key in std_dict.keys():
        file1 = path+key+'/'+key+".py"
        file2 = path+key+'/'+key+".txt"
        same_or_not[key] = filecmp.cmp(file1, file2)
    
    # Now use this filecmp to create a csv file for same files or not
    return same_or_not

if __name__ == "__main__":
    #For testing
    
    create_file_struct("path/to/the/all/submission/files/")