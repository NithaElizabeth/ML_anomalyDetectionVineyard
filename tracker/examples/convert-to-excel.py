import os.path
import openpyxl

excel_path = "Dataset-Properties.xlsx"

wb = openpyxl.load_workbook(filename+)
sheet = wb.active

with open('train.txt', 'r') as f:
    lines = f.readlines()

    for line in lines:
        img_name = line[line.rfind('/')+1:]
        sheet['B' + str(count)] = img_name
        sheet['C' + str(count)] = line
        sheet['D' + str(count)] = "JPEG"

        count += 1

f.close()
wb.save(excel_path)   # TODO : Encode with name of video
