import sys
import os
import time
import datetime
import shutil
import logging

source = sys.argv[1]
replica = sys.argv[2]
timer=float(sys.argv[3])
log=sys.argv[4]
run = True
logging.basicConfig(filename=log, encoding='utf-8', format='%(asctime)s | %(levelname)s | %(module)s | %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.DEBUG)

#start-functions#

def checkDir(folder):
    if not os.path.exists(folder):
        try:
            os.makedirs(folder)
        except:
            print("Error while creating folder: ", folder)
            

def readFile(path):
    try:
        with open(path, 'rb') as rawdata:
            return rawdata.read()
    except:
        print("Error while reading file: ", path)
    
def writeFile(file, operation):
    try:
        with open(os.path.join(replica,file), 'wb') as fileData:
            fileData.write(readFile(os.path.join(source,file)))
    except:
        print("Error while writing file: ", os.path.join(replica,file))

    logging.info(f"File {operation} - Name: {file}, size: {os.stat(replica + file).st_size} bytes.")

def writeFolder(folder,operation):
    try:
        os.makedirs(os.path.join(replica,folder))
        logging.info(f"Folder {operation} - Name: {folder}, size: {os.stat(replica + folder).st_size} bytes.")
    except:
            print("Error while creating folder: ", os.path.join(replica,folder))
    
def syncFolder():
    print("sync process started...")

    while(run):
        print("\n===========================================================")
        #arrays that allocate the source and replica files and folders.
        sourceFolders = []
        replicaFolders = []
        sourceFiles = []
        replicaFiles = []

        print("\nSource tree:")
        #loop that passes through all the files and folders inside source folder and saves the files and folders as elements in the two arrays.
        for folder in os.walk(source):
            folderPath = os.path.relpath(folder[0], source) + "/"
            print(f" folder:{folderPath}")

            if folderPath not in sourceFolders:
                sourceFolders.append(folderPath)

            for file in os.listdir(folder[0]):
                if not os.path.isdir(os.path.join(folder[0],file)):
                    print(f"    file:{file}")
                    if os.path.join(folderPath,file) not in sourceFiles:
                        sourceFiles.append(os.path.join(folderPath,file))

        print("\nReplica tree:")
        #loop that passes through all the files and folders inside replica and verifies if the file exists inside the source files array, if not removes it.
        for folder in os.walk(replica):
            folderPath = os.path.relpath(folder[0], replica) + "/"
            print(f" folder:{folderPath}")

            if folderPath not in sourceFolders:
                logging.info(f"Folder Deleted - Name: {folderPath}, size: {os.stat(folder[0]).st_size} bytes.")
                shutil.rmtree(folder[0], ignore_errors=True)

            else:
                for file in os.listdir(folder[0]):
                    if not os.path.isdir(os.path.join(folder[0],file)):
                        print(f"    file:{file}")
                
                        if os.path.join(folderPath,file) not in sourceFiles:
                            try:
                                os.remove(os.path.join(replica,folderPath,file))
                                logging.info(f"File Deleted - Name: {file}, size: {os.stat(replica + folderPath + file).st_size} bytes.")
                            except:
                                print("Error while deleting file: ", os.path.join(replica,folderPath,file))

                        else:
                            replicaFiles.append(os.path.join(folderPath,file))
                replicaFolders.append(folderPath)


        #loops that passes through all folders and files and checks if the files dont exist inside replica's arrays and if they are not equal, overwrites if neither is true.
        for folder in sourceFolders:
            if folder not in replicaFolders:
                writeFolder(folder, "Created")

        for file in sourceFiles:
            if file not in replicaFiles:
                writeFile(file, "Created")
            elif readFile(os.path.join(replica,file)) != readFile(os.path.join(source,file)):
                writeFile(file, "Updated")

        #time sleep to delay the while process
        time.sleep(timer)

#end-functions#

if __name__ == "__main__":
    # check source and replica directories.
    try:
        checkDir(source)
        checkDir(replica)

        # creating the log file and writing new log start.
        with open(log, 'w') as logData:
            logData.write(f"\n | NEW LOG STARTED - {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} | \n")
        
        syncFolder()
    except KeyboardInterrupt:
        print("sync process ended...")
        print("app closing...")
        sys.exit()
               

  