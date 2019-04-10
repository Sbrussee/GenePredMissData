import sys
import os

EVC = ("EXP","IDA","IPI","IMP","IGI","IEP","HTP","HTP","HDA","HMP",
       "HGI","HEP","IBA","IBD","IKR","IRD","ISS","ISO","ISA","ISM",
       "IGC","RCA","TAS","NAS","IC","ND","IEA","IEA")

DOMAINS = ("C", "F", "P")

EVAL = ('f-score', 'precision')

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
            res.append(arg[i])
        else:
            text = "'%s' is not a valid evidence code."%arg[i]
    return text , res

def check_file(key, arg):
    text = ""
    if not os.path.exists(arg):
        text = "The file '%s' does not exist."%arg
    return text, arg

def check_domain(key, arg):
    text = ""
    res = []
    domains = arg.split(",")
    if arg == "*":
        res = DOMAINS
    else:
        for domain in domains:
            if domain in DOMAINS:
                res.append(domain)
            else:
                text = "Domain '%s' is not valid."%domain
                break
    return text, res

def check_repeats(key, arg):
    text = ""
    if not arg.isnumeric():
        text = "Repeat input '%s' is not numeric."%arg
    else:
        arg = int(arg)
        if arg > 100 or arg < 0:
            text = "Repeat input has to be a number between 100 and 0."
    return text, arg

def check_threads(key, arg):
    text = ""
    if arg.isnumeric():
        arg = int(arg)
        if arg < 1:
            text = "Threads has to be higher than 0."
    else:
        text = "Threads has to be a number."
    return text, arg

def check_evaluator(key, arg):
    arg = arg.split(",")
    text = ""
    res = []
    for i in range(len(arg)):
        if arg[i] in EVAL:
            res.append(arg[i])
        else:
            text = "'%s' is not a valid evaluator."%arg[i]
    return text , res

HELP = "====GOA_PREDICTION FRAMEWORK====\n"\
       "Tests different GO-prediction algorithms "\
       "by removing values incrementally from the "\
       "input dataset."
LETTERS = {"p":"predictor",
           "e":"evaluator",
           "l":"plotter",
           "s":"stepsize",
           "E":"evidence",
           "t":"traindata",
           "g":"traingaf", 
           "T":"testdata",
           "G":"testgaf",
           "d":"domain",
           "r":"repeats",
           "n":"threads",
           "f":"nogofix",
           "h":"help"}
ARGS = {"predictor":{
                    "required":False,
                    "default":"blast",
                    "check":check_file,
                    "help":"What predictor to use. Can be one of: 'blast'. " 
                    },
        "evaluator":{
                    "required":False,
                    "default":["f-score"],
                    "check":check_evaluator,
                    "help":"What evaluator to use. Can be one of: 'f-score', 'precision'." 
                    },
        "plotter":{
                    "required":False,
                    "default":"line",
                    "check":("line"),
                    "help":"What plotter to use. Can be one of: 'line'." 
                    },
        "stepsize":{
                    "required":False,
                    "default":"5",
                    "check":check_stepsize,
                    "help":"Percentage decrease of dataset sample per round. Should be a number from 0 to 100." 
                    },
        "evidence":{
                    "required":False,
                    "default":"*",
                    "check":check_evidence,
                    "help":"Evidence codes to use. Should be multiple seperated by comma without spaces or * for all." 
                    },
        "traindata":{
                    "required":True,
                    "default":False,
                    "check":check_file,
                    "help":"Filename of traindata." 
                    },
        "traingaf":{
                    "required":True,
                    "default":False,
                    "check":check_file,
                    "help":"Filename of traingaf." 
                    },
        "testdata":{
                    "required":True,
                    "default":False,
                    "check":check_file,
                    "help":"Filename of testdata."  
                    },
        "testgaf":{
                    "required":True,
                    "default":False,
                    "check":check_file,
                    "help":"Filename of testgaf." 
                    },
        "domain":{
                    "required":False,
                    "default":"*",
                    "check":check_domain,
                    "help":"Domains to use. Should be multiple seperated by comma without spaces or * for all." 
                    },
        "repeats":{
                    "required":False,
                    "default":1,
                    "check":check_repeats,
                    "help":"Amount of repeats per step. Should be a positive number." 
                    },
        "threads":{
                    "required":False,
                    "default":"*",
                    "check":check_threads,
                    "help":"Amount of processing threads to use. Should be a positive number." 
                    },
        "nogofix":{
                    "required":False,
                    "default":"",
                    "check":None,
                    "help":"Skip GO-TREE completing the GO terms." 
                    },
        "help":{
                    "required":False,
                    "default":False,
                    "check":False,
                    "help":"Display this help." 
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
                if type(inf["check"]) == tuple:
                    if not content in inf["check"]:
                        print("'%s' not allowed for argument '%s'.\n"%(
                                content, arg) +
                              "Allowed: %s."%", ".join(inf["check"]))
                        exit()
                elif inf["check"] != None:
                    text, content = inf["check"](arg, content)
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
        arg = argv[i]
        if arg[0] != "-":
            continue
        if arg[1] != "-":
            if arg[1:] in LETTERS:
                arg = LETTERS[arg[1:]]
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
