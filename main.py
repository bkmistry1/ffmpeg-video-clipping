import subprocess
import os 
import glob
import asyncio

from pathlib import Path

from datetime import datetime

from dotenv import load_dotenv

load_dotenv()

rootPath = os.getenv("rootPath")


# set the current working directory

cwd = Path(rootPath)

# traverse through all directories looking for clips.csv files
csvFilesOnly = "clips.csv"



async def main():    

    while(1):
        print("running")
        allCsvFiles = list(cwd.rglob(csvFilesOnly))

        # read csv file and check if it fits in the four headers
        # nameOfFile,startTime,endTime,nameOfClip

        for csvFile in allCsvFiles:
            # print(csvFile.parent)
            # print(csvFile.name)

            parentDirectory = csvFile.parent

            with open(csvFile, 'r', encoding="utf-8-sig") as file:
                for line in file.readlines():

                    videoDetails = line.split(",")

                    if(len(videoDetails) == 4):

                        titleOfVideoFile = parentDirectory / videoDetails[0]
                        timeStart: str = videoDetails[1]
                        timeEnd: str = videoDetails[2]
                        titleOfOutputFile = videoDetails[3].strip()
                        titleOfOutputFile = titleOfOutputFile.strip("\n")
                        titleOfOutputFile = parentDirectory / titleOfOutputFile
                        
                        titleOfVideoFile = str(titleOfVideoFile).replace(" ", "%20")
                        titleOfOutputFile = str(titleOfOutputFile).replace(" ", "%20")
                        print(titleOfVideoFile)
                        print(titleOfOutputFile)

                        timeStart = timeStart.strip()
                        timeEnd = timeEnd.strip()

                        timeStartDateTime = datetime.strptime(timeStart, "%H:%M:%S")
                        timeEndDateTime = datetime.strptime(timeEnd, "%H:%M:%S")

                        timeDifference = timeEndDateTime - timeStartDateTime

                        # print(timeStart)
                        # print(timeEnd)
                        # print(timeDifference)

                        # begin creating the clips  

                        commandString = f"ffmpeg -n -ss {timeStart} -i {titleOfVideoFile} -t {timeDifference.seconds} -c:v libx264 -preset slow -c:a aac {titleOfOutputFile}"
                        # [
                        #     'ffmpeg',
                        #     '-y',
                        #     '-ss', '0:04:00',
                        #     '-i', '\\\\mistrysharenas.localdomain\\Church\\Next Gen\\Next Gen Peace Cup\\2025-11-23\\MainCam\\C0007.MP4',
                        #     '-t', '12',
                        #     '-c:v', 'libx264',
                        #     '-preset', 'slow',
                        #     '-c:a', 'aac',
                        #     '-b:a', '192k',
                        #     '\\\\mistrysharenas.localdomain\\Church\\Next Gen\\Next Gen Peace Cup\\2025-11-23\\MainCam\\oop.mp4'
                        # ]
                        tmpCommand = commandString.split(" ")

                        print(commandString)

                        command = []
                        for item in tmpCommand:
                            tmpItem = item
                            if ("%20" in item):
                                tmpItem = item.replace("%20", " ")

                            command.append(tmpItem)


                        print(command)

                        p = subprocess.Popen(command, stdin=subprocess.PIPE)
                        p.wait()
        
            newCsvFileName = csvFile.parent / f"done-{csvFile.name}"
            # os.replace(csvFile, newCsvFileName)
            # print(f"Renamed {csvFile} -> {newCsvFileName}")

            try:
                os.replace(csvFile, newCsvFileName)   # or os.rename
                print(f"Renamed {csvFile} -> {newCsvFileName}")
            except FileNotFoundError as e:
                print(f"File not found: {e}")
            except PermissionError as e:
                print(f"Permission denied (file may be locked): {e}")
            except OSError as e:
                print(f"OS error during rename: {e}")


        await asyncio.sleep(5)

asyncio.run(main())