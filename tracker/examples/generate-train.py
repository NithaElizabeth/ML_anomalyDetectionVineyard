import os
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--input', '-i', type=str,  help='')
args = parser.parse_args()

os.chdir(args.input)

folders = os.listdir()

for folder in folders:
    output_file = folder + '/train.txt'
    image_files = []
    print('Writing to: ' + output_file)

    for filename in os.listdir(folder):
        if filename.endswith(".jpg") or filename.endswith(".JPG"):
            image_files.append(filename)

    with open(output_file, "w") as outfile:
        for image in image_files:
            outfile.write(image)
            outfile.write("\n")
        outfile.close()
#os.chdir("..")
