import os
import time
import chardet

source = "source/"
replica = "replica/"
timer = 1
run = True

#start-functions#

def checkDir(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

def readFile(path):
    with open(path, 'rb') as rawdata:
        return rawdata.read()
    
def syncFolder():
    print("sync process started...")


    while(run):
        #arrays that allocate the source and replica files.
        sourceFiles = []
        replicaFiles = []

        print("\nSource:")
        #loop that passes through all the files inside source folder and saves the file as a object.
        for x in os.listdir(source):
            print(" nome:" + x)
            if x not in sourceFiles:
                sourceFiles.append(x)

        print("\nReplica:")
        #loop that passes through all the files inside replica and verifies if the file exists inside the files array, if not removes it.
        for x in os.listdir(replica):
            print(" nome:" + x)

            if x not in sourceFiles:
                os.remove(replica+x)
            elif x not in replicaFiles:
                replicaFiles.append(x)


        #loop that passes through all files objects that checks if the files exist inside "replica" folder and if they are not equal, overwrites if none is true.
        for file in sourceFiles:
            if file not in replicaFiles or readFile(replica + file) != readFile(source + file):
                f = open(replica + file, "wb")
                f.write(readFile(source + file))
                f.close()

                print("\nFile Updated:")
                print(" Name:" + file)

        #time sleep to delay the while process
        time.sleep(timer)

    print("sync process ended...")

#end-functions#

if __name__ == "__main__":
    # check source and replica directories.
    checkDir(source)
    checkDir(replica)
    syncFolder()
               

  