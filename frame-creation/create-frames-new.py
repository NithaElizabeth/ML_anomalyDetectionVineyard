from flask import Flask, render_template, request
import os
import sys

UPLOAD_FOLDER = '/home/software3d/Documents/Machine Leraning/Grape Detection/Grapes-resized'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def extract_images(file, request):
    date = request.form['date']
    place = request.form['place']
    code = request.form['code']
    left = request.form['left']
    right = request.form['right']
    os.system(
        f"python3 extract-images.py -i {file.filename} -n Abcd -d 12345 -p 9F4E -l 01 -r 02")


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file[]']

        extract_images(file, request)
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        # if file.filename == '':
        #     print('No selected file')
        #     return redirect(request.url)

        # print('This message will be displayed on the screen.')
        # original_stdout = sys.stdout
        # if file and allowed_file(file.filename):
        #     print(file.filename)
        #     with open('filename.txt', 'w') as f:
        #         sys.stdout = f # Change the standard output to the file we created.
        #         print('This message will be written to a file.')
        #         sys.stdout = original_stdout # Reset the standard output to its original value
    return render_template('upload.html')


if __name__ == '__main__':
    app.run(debug=True)
