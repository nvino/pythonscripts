import random
import string
import threading
import os
import sys
import time
import shutil

def randomString(stringLength=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

print("Random String is ", randomString())
print("Random String is ", randomString(8))
print("Random String is ", randomString(8))

def copyfile(pathf,destf):
    pathf = pathf.rstrip()
    destf = destf.rstrip()
    start = time.time()
    lis1 = os.listdir(pathf)
    numcopyfiles = len(lis1)
    print("Number of files to be copied: " + str(numcopyfiles))
    for x in lis1:
        shutil.copy(os.path.join(pathf,x),os.path.join(destf,x))
    end = time.time()
    elapsed = end - start
    totalms = elapsed * 1000
    msperfile = numcopyfiles/totalms
    print ("Total MS for copy: " + str(totalms))
    print ("Millisecond per file for copy : " + str(msperfile))

def delfile(pathf):
    pathf = pathf.rstrip()
    start = time.time()
    lis1 = os.listdir(pathf)
    numdelfiles = len(lis1)
    print("Number of files to be deleted: " + str(numdelfiles))
    for x in lis1:
        os.remove(os.path.join(pathf,x))
    end = time.time()
    elapsed = end - start
    totalms = elapsed * 1000
    msperfile = numdelfiles/totalms
    print ("Total MS for deletion: " + str(totalms))
    print ("Millisecond per file for delete : " + str(msperfile))


def createfile(sizekb, pathf):
    pathf = pathf.rstrip()
    sizebytes = int(sizekb) * 1000
    filename = randomString(8) + "." + randomString(3)
    filename.lstrip()
    filename.rstrip()
   # print("this is " + filename)
    fulname = os.path.join(pathf, filename)
   # print(fulname)
    str1 = '\0'
    with open(fulname, "wb") as out:
        out.seek((sizebytes - 1))
        out.write(str1.encode(encoding='UTF-8'))

optionsfile = sys.argv[1]

file1 = open(optionsfile, 'r') 
Lines = file1.readlines()
for oo in Lines:
    oo.rstrip()
    oo.lstrip()
    print(oo)
    if ("NUMBER" in oo):
        x = oo.split('=')
        numfiles = x[1]
    if ("SIZEKB" in oo):
        x = oo.split('=')
        sizekb = x[1]
    if ("NUMTHREAD" in oo):
        x = oo.split('=')
        numthread = x[1]
    if ("PATH" in oo):
        x = oo.split('=')
        pathf = x[1]
    if ("DEST" in oo):
        x = oo.split('=')
        destf = x[1]

threads = list()
#starting create
start = time.time()
for yy in range(int(numfiles)):
    for index in range(int(numthread)):
        print("starting thread "  + str(index))
        x = threading.Thread(target=createfile, args=(sizekb, pathf))
        threads.append(x)
        x.start()
end = time.time()
elapsed = end - start
totalms = elapsed * 1000
totalfiles = int(numfiles) * int(numthread)
msperfile = totalfiles/totalms

print ("Total Files Created: " + str(totalfiles))
print ("Total MS for creation: " + str(totalms))
print ("Millisecond per file : " + str(msperfile))


#ending create

#start copy
print ("Starting File Copy ")

copyfile(pathf,destf)

#end copy 

#start del main
print ("Starting File Delete on primary path ")

delfile(pathf)

# end del

#start del copy
print ("Starting File Delete on secondary path ")

delfile(destf)

# end del
