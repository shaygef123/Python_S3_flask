import boto3
from flask import Flask, request, render_template, redirect

app = Flask(__name__)
s3 = boto3.resource('s3')
MyBucket = s3.Bucket('shaygefbucket')

s3Files = []
for obj in MyBucket.objects.all():
    s3Files.append(obj.key)

@app.route('/home', methods=["GET", "POST"])
def home():
    if request.method == "POST":
        if request.form['submit_button'] == "Download_file":
            return redirect('/download')
        elif request.form['submit_button'] == "Upload_file":
            return redirect('/upload')
        elif request.form['submit_button'] == "show_files":
            return redirect('/showFiles')
    return render_template("home.html")

@app.route('/download', methods=["GET", "POST"])
def download():
    if request.method == "POST":
        if request.form['submit_button'] == "Back":
            return redirect('/home')
        if request.form['submit_button'] == "Enter":
            file = request.form['fname']
            c = 0
            for f in s3Files:
                if file == f:
                    c = 1;
            if c == 0:
                return "file not found...."
            else:
                try:
                    MyBucket.download_file(file,file)
                except:
                    return "unable to download..."
            return file + "is downloaded"
    return render_template("download.html")

@app.route('/upload', methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        if request.form['submit_button'] == "Back":
            return redirect('/home')
        if request.form['submit_button'] == "Enter":
            file = request.form['fname']
            c = 0
            for f in s3Files:
                if file == f:
                    c = 1;
            if c == 1:
                return "file already exists. try other name"
            else:
                try:
                    MyBucket.upload_file(file,file)
                except:
                    return "unable to upload..."
            return file + "is uploaded."
    return render_template("upload.html")

@app.route('/showFiles', methods=["GET", "POST"])
def showFiles():
    if request.method == "POST":
        if request.form['submit_button'] == "Back":
            return redirect('/home')
    s3Files = []
    for obj in MyBucket.objects.all():
        s3Files.append(obj.key)
    return render_template("showFiles.html",files=s3Files)

if __name__ == '__main__':
    app.run(debug=True)