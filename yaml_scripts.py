import yaml

in_out = {'input': [], 'output':-1}


# import sys
# sys.path.insert(0, '/home/vav/Documents/TA-CSCI-B-505/scripts')

# from yaml_script import populateOutput

# if __name__ == "__main__":
#     populateOutput(minimum_balls,"minimum_balls","test-cases")

def read_one_block_of_yaml_data(filename):
    with open(f'{filename}.yaml','r') as f:
        output = yaml.safe_load(f)
    return output

def addThis(func, funcName, fileName, input):
    file_dict = read_one_block_of_yaml_data(fileName)
    cp = in_out
    cp["input"] = input
    cp["output"] = func(*input)

    idx = 0
    for i in range(0,len(file_dict["unitArgs"])):
        tmp = file_dict["unitArgs"][i]
        if tmp["func"] == funcName:
            idx = i
            break
    

    file_dict["unitArgs"][idx]["explicit"].append(cp)
    with open(f'{fileName}.yaml', 'w') as file:
        yaml.dump(file_dict,file,sort_keys=False)

def populateOutput(func, funcName, fileName):
    # given function and input it will populate output
    file_dict = read_one_block_of_yaml_data(fileName)
    for i in range(0,len(file_dict["unitArgs"])):
        if file_dict["unitArgs"][i]["func"] == funcName:
            expli = file_dict["unitArgs"][i]["explicit"]
            for test_case in expli:
                inp = test_case["input"]
                out = func(*inp)
                test_case["output"] = out
                # print(test_case["input"])
            
            file_dict["unitArgs"][i]["excplicit"] = expli
    
    with open(f'{fileName}.yaml', 'w') as file:
        yaml.dump(file_dict,file,sort_keys=False)

# if __name__ == "__main__":
    # for tsting