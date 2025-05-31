import subprocess
import os 

from datetime import datetime

from dotenv import load_dotenv

load_dotenv()

fileName = input("Name of csv file")

pathName = os.getenv("pathName")
outputPath = os.getenv("outputPath")


with open(fileName, 'r', encoding="utf-8-sig") as file:
    for line in file.readlines():

        videoDetails = line.split(",")

        titleOfVideoFile = pathName + "\\" + videoDetails[0]
        timeStart: str = videoDetails[1]
        timeEnd: str = videoDetails[2]
        titleOfOutputFile = videoDetails[3].strip()
        titleOfOutputFile = outputPath + "\\" + titleOfOutputFile.removesuffix("\n")

        timeStart = timeStart.strip()
        timeEnd = timeEnd.strip()
        titleOfVideoFile = titleOfVideoFile.strip()
        titleOfOutputFile = titleOfOutputFile.strip()

        timeStart = datetime.strptime(timeStart, "%H:%M:%S")
        timeEnd = datetime.strptime(timeEnd, "%H:%M:%S")

        timeDifference = timeEnd - timeStart        

        commandString = f"ffmpeg -ss {videoDetails[1].strip()} -i {titleOfVideoFile} -t {timeDifference.seconds} -c:v libx264 -preset slow -c:a copy {titleOfOutputFile}"

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