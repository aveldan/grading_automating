import requests
import os
import filecmp
from dotenv import load_dotenv
import json

# To do
# -- If file struct is already created do not mess with it, maybe introduce a variable to keep note of it.

load_dotenv()

header = {}
header['Authorization'] = os.environ.get("authorization-key")


max_scores = {
    "isItPossible": 15,
    "amountPoliceGets": 15,
    "Insert/Search": 20,
    "Enque/Deque": 20
}

def get_studentIDs():

    req_url = os.environ.get("student-list-url")+os.environ.get("assignment-num")
    response = requests.get(url=req_url,headers=header)

    if response.status_code != 200:
        print("Not a 200 response")
        print(response)
        return None
    
    return response.json()["data"]


def get_studentScore(studentID, studentFullName):

    req_url = os.environ.get("student-submissions-url")+str(studentID)
    response = requests.get(url=req_url,headers=header)

    if response.status_code != 200:
        print("Not a 200 response")
        print(response)
        return None
    
    submissions = response.json()["data"]
    submissions = sorted(submissions, key=lambda x: x['created_at'])
    latest_submission = submissions[len(submissions)-1]

    download_py_file(studentFullName, latest_submission["FilePath"])
    
    
    req_url = os.environ.get("submission-url")+str(studentID)+'/'+str(latest_submission["Id"])
    response = requests.get(url=req_url,headers=header)

    if response.status_code != 200:
        print("Not a 200 response")
        print(response)
        return None
    
    scores = response.json()["data"]["reports"]
    student_scores = []

    for score in scores:
        question_score = {}
        question_score["name"] = score["name"]
        question_score["num_cases"] = score["num_cases"]
        question_score["num_passed"] = score["num_passed"]
        question_score["num_failed"] = score["num_failed"]

        
        if score["num_cases"] != 0:
            question_score["score"] = (max_scores[score["name"]]*score["num_passed"])/score["num_cases"]
        else:
            question_score["score"] = 0

        student_scores.append(question_score)

    return student_scores

def download_py_file(studentFullName, filePath):

    req_url = os.environ.get("download-url")+filePath
    response = requests.get(url=req_url, headers=header)
    
    if response.status_code != 200:
        print("Not a 200 response")
        print(response)
        return None

    filename = ""
    tmp_list = studentFullName.lower().split(' ')
    filename += tmp_list[len(tmp_list)-1]
    for i in range(0,len(tmp_list)-1):
        filename += tmp_list[i]
        
    flptr = open(os.environ.get("working-dir")+filename+'/'+filename+".py", "w")
    flptr.write(response.text)

    flptr.close()

def grade():
    create_file_struct(os.environ.get("working-dir"))

    students = get_studentIDs()
    students_scores = []

    for student in students:
        tmp_dict = {}
        tmp_dict["name"] = student["Fullname"]
        tmp_dict["scores"] = get_studentScore(student["StudentId"], student["Fullname"])
        students_scores.append(tmp_dict)
    
    return students_scores

def change_filenames(path):
    name_dict = {}
    for filename in os.listdir(path):
        str = ""
        cpy_filename = filename[0:len(filename)-4] # Assuming txt file or pdf file

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

def compare_files(student_name):

    tmp_list = student_name.lower().split(' ')
    filename = tmp_list[len(tmp_list)-1]
    for i in range(0, len(tmp_list)-1):
        filename += tmp_list[i]
    
    file1 = os.environ.get("working-dir")+filename+'/'+filename+".py"
    file2 = os.environ.get("working-dir")+filename+'/'+filename+".txt"

    return filecmp.cmp(file1, file2)


if __name__ == "__main__":

    student_scores = grade()
    for i in range(0,len(student_scores)):
        student_scores[i]["same-files"] = compare_files(student_scores[i]["name"])
    
    path = os.environ.get("working-dir")
    path = path[0:len(path)-12]
    
    with open(path+"scores.json", "w") as outfile:
        json.dump(student_scores, outfile, indent=4)