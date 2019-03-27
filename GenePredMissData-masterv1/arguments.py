import sys
import os

EVC = ("EXP","IDA","IPI","IMP","IGI","IEP","HTP","HTP","HDA","HMP",
       "HGI","HEP","IBA","IBD","IKR","IRD","ISS","ISO","ISA","ISM",
       "IGC","RCA","TAS","NAS","IC","ND","IEA","IEA", "*")

def check_stepsize(key, arg):
    text = ""
    if arg.isnumeric():
        arg = int(arg)
    else:
        text = "The argument 'stepsize' or 's' was not numeric."
    return text, arg

def check_evidence(key, arg):
    arg = arg.split(",")
    text = ""
    res = []
    for i in range(len(arg)):
        if arg[i] in EVC:
            res.append(arg)
        else:
            text = "'%s' is not a valid evidence code."%arg[i]
    return text , res

def check_file(key, arg):
    text = ""
    if not os.path.exists(arg):
        text = "The file '%s' does not exist."%arg
    return text, arg

HELP = "HELP"
LETTERS = {"p":"predictor",
          "e":"evaluator",
          "l":"plotter",
          "s":"stepsize",
          "e":"evidence",
          "t":"traindata",
          "g":"traingaf", 
          "T":"testdata",
          "G":"testgaf",
          "h":"help"}
ARGS = {"predictor":{
                    "required":False,
                    "default":"blast",
                    "check":("blast"),
                    "help":"HELP" 
                    },
        "evaluator":{
                    "required":False,
                    "default":"semantic",
                    "check":("semantic"),
                    "help":"HELP" 
                    },
        "plotter":{
                    "required":False,
                    "default":"line",
                    "check":("line"),
                    "help":"HELP" 
                    },
        "stepsize":{
                    "required":False,
                    "default":"5",
                    "check":check_stepsize,
                    "help":"HELP" 
                    },
        "evidence":{
                    "required":False,
                    "default":"*",
                    "check":check_evidence,
                    "help":"HELP" 
                    },
        "traindata":{
                    "required":True,
                    "default":False,
                    "check":check_file,
                    "help":"HELP" 
                    },
        "traingaf":{
                    "required":True,
                    "default":False,
                    "check":check_file,
                    "help":"HELP" 
                    },
        "testdata":{
                    "required":True,
                    "default":False,
                    "check":check_file,
                    "help":"HELP" 
                    },
        "testgaf":{
                    "required":True,
                    "default":False,
                    "check":check_file,
                    "help":"HELP" 
                    },
        "help":{
                    "required":False,
                    "default":False,
                    "check":False,
                    "help":"HELP" 
                    }}
    
def show_help():
    print(HELP)
    print("Arguments:")
    for letter in LETTERS:
        inf = ARGS[LETTERS[letter]]
        print("\t -%s --%s\t%s"%(letter, LETTERS[letter], inf["help"]))


def finish_arg(argstore):
    for arg in ARGS:
        if arg in argstore:
            content = argstore[arg]
            inf = ARGS[arg]
            text = ""
            if inf["check"] != False:
                print("HERE")
                if type(inf["check"]) == tuple:
                    if not content in inf["check"]:
                        print("'%s' not allowed for argument '%s'.\n"%(
                                content, arg) +
                              "Allowed: %s."%", ".join(inf["check"]))
                        exit()
                else:
                    text, arg = inf["check"](arg, content)
                if text != "":
                    print(text)
                    exit()
            argstore[arg] = content
        else:
            if ARGS[arg]["required"]:
                print("Error: Required argument '%s' not given."%arg)
                exit()
            if ARGS[arg]["default"]:
                argstore[arg] = ARGS[arg]["default"]
    return argstore

            

def get_args():
    argstore = {}
    argv = sys.argv
    for i in range(1, len(argv)):
        word = False
        arg = argv[i].lower()
        if arg[0] != "-":
            continue
        if arg[1] != "-":
            if arg[1:] in LETTER:
                arg = LETTER[arg[1:]]
        else:
            arg = arg[2:]
        if arg not in ARGS:
            print("Argument '%s' is not a valid argument."%arg)
        if arg in ARGS:
            if arg == "help":
                show_help()
                exit()
            content = ""
            if len(argv) > i + 1:
                content = argv[i + 1]
            argstore[arg] = content   
    return finish_arg(argstore)
