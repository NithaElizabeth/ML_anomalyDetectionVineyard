import argparse as ap
import shutil
import pickle
import cv2
import os

parser = ap.ArgumentParser(description="Extracts images from a video")

parser.add_argument("--input", "-i",   required=True,  help="The location of the input video file")
parser.add_argument("--output", "-o", help="The output directory")
parser.add_argument("--date", "-d",  required=True,  help="The date when the video was taken")
parser.add_argument("--name", "-n",  required=True,  help="Name of the customer")
parser.add_argument("--parcel", "-p",  required=True,  help="The Parcel Number")
parser.add_argument("--left", "-l",  required=True,  help="Left Rank ID")
parser.add_argument("--right", "-r",  required=True,  help="Right Rank ID")
args = parser.parse_args()

dirName = str(args.date) + "_" + str(args.name) + "_" + str(args.parcel) + "_" + str(args.right) + "_" + str(args.left)
filePrefix = dirName + "/" + dirName + "_CanonEOS_img-"

frameSkip = 25
i = 0
start = 29483  
print("start=" + str(start))

# with open('last_num.pickle','rb') as f:
#    start = pickle.load(f)
#    print("start=" + str(start))

if not os.path.exists(dirName):
    os.mkdir(dirName)
    print("Successfully created the directory: " + dirName)
else:
    option = input('[INFO] Directory already exists. Remove directory? y/n: ')
    if option == 'y':
        shutil.rmtree(dirName)
        os.mkdir(dirName)
    if option == 'n':
        pass

logFileName = dirName + "/log.txt"

k = input('Press any key to begin:')

with open(logFileName, "w") as f:
    f.write("Location of video: " + str(args.input))
f.close()

print("Directory Name: " + dirName)
print("File Prefix:    " + filePrefix)

cap = cv2.VideoCapture(str(args.input))

while True:
    i += 1
    ret, frame = cap.read()
    frame = cv2.resize(frame, (1280, 720))

    if (i % frameSkip) == 0:
        start += 1
        fileName = filePrefix + str(start) + ".jpg"
        cv2.imshow(filePrefix, frame)
        cv2.imwrite(fileName, frame)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

print("Last number: {}".format(start))
f = open('last_num.pickle', 'wb')
pickle.dump(start, f)
f.close()

cap.release()
cv2.destroyAllWindows()
