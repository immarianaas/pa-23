import os
import json
import glob
import subprocess

def interpret(obj):
   pass
    
def interpretBytecode(byteArray, stack = 0, memory = 0):
    byteObj = byteArray.pop()
    match byteObj["opr"]:
        case "load":
            pass
        case "new":
            pass
        case "dup":
            pass 
        case "put":
            pass
        case "invoke":
            pass
        case "binary":
            match byteObj["operant"]:
                case "add":
                    pass
    if(byteArray.lengh > 0):
        interpretBytecode(byteArray, stack, memory)
    else :
        return "something"



def interpretProjDir(proj_directory: str):
    for file in glob.iglob(proj_directory + "/**/*.class", recursive=True):
        new_filename = "." + file.split('.')[1] + ".json"
        # ret = subprocess.run(["jvm2json", "-s", file, "-t", new_filename ])

        f = open( new_filename )
        data: json = json.load(f)
        f.close()
        interpret(data)



