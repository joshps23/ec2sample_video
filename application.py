from flask import Flask, render_template, Response,jsonify,request,session
import random
import datetime
from flask_wtf import FlaskForm
from werkzeug.utils import secure_filename
from wtforms.validators import InputRequired,NumberRange
import os
import base64
import cv2


# YOLO_Video is the python file which contains the code for our object detection model
#Video Detection is the Function which performs Object Detection on Input Video
from YOLO_Video import video_detection

from wtforms import FileField, SubmitField
application = Flask(__name__)
app=application
app.config['SECRET_KEY'] = 'anewflaskapp'
app.config['UPLOAD_FOLDER'] = 'static/files'

class UploadFileForm(FlaskForm):
  file = FileField("File",validators=[InputRequired()])
  submit = SubmitField("Run")

def generate_frames(path_x = ''):
    yolo_output = video_detection(path_x)
    for detection_ in yolo_output:
        ref,buffer=cv2.imencode('.jpg',detection_)

        frame=buffer.tobytes()
        yield (b'--frame\\r\\n'
                    b'Content-Type: image/jpeg\\r\\n\\r\\n' + frame +b'\\r\\n')

def generate_frames_web(path_x):
    yolo_output = video_detection(path_x)
    for detection_ in yolo_output:
        
        ref,buffer=cv2.imencode('.jpg',detection_)

        frame=buffer.tobytes()
        yield (b'--frame\\r\\n'
                    b'Content-Type: image/jpeg\\r\\n\\r\\n' + frame +b'\\r\\n')

# @app.route('/')
# def hello_world():
#   session.clear()
#   random_number = random.randint(1, 100)
#   current_year = datetime.datetime.now().year
#   return render_template("index.html", num=random_number, yr=current_year)

@app.route('/')
def hello_world2():
  return render_template("indexvideo.html")
#     return """
#     <!DOCTYPE html>
#     <html lang="en">
#     <head>
#         <meta charset="UTF-8">
#         <title>Title</title>
#     </head>
#     <body>
#     <video id="video" width="640" height="480" autoplay></video>
#     <button id="snap">Snap Photo</button>
#     <canvas id="canvas" width="640" height="480"></canvas>
#     </body>
#     <script>

#     var video = document.getElementById('video');
#     if(navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
#         navigator.mediaDevices.getUserMedia({ video: true }).then(function(stream) {
#             //video.src = window.URL.createObjectURL(stream);
#             video.srcObject = stream;
#             video.play();
#         });
#     }

#     var canvas = document.getElementById('canvas');
#     var context = canvas.getContext('2d');
#     var video = document.getElementById('video');

#     // Trigger photo take
#     document.getElementById("snap").addEventListener("click", function() {
#         context.drawImage(video, 0, 0, 640, 480);
#     var request = new XMLHttpRequest();
#     request.open('POST', '/submit?image=' + video.toString('base64'), true);
#     request.send();
#     });



# </script>
# </html>
#     """

@app.route('/cam')
def cam():
      return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Title</title>
    </head>
    <body>
    <video id="video" width="640" height="480" autoplay></video>
    <button id="snap">Snap Photo</button>
    <canvas id="canvas" width="640" height="480"></canvas>
    </body>
    <script>

    var video = document.getElementById('video');
    if(navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({ video: true }).then(function(stream) {
            //video.src = window.URL.createObjectURL(stream);
            video.srcObject = stream;
            video.play();
        });
    }

    var canvas = document.getElementById('canvas');
    var context = canvas.getContext('2d');
    var video = document.getElementById('video');

    // Trigger photo take
    document.getElementById("snap").addEventListener("click", function() {
        context.drawImage(video, 0, 0, 640, 480);
    var request = new XMLHttpRequest();
    request.open('POST', '/submit?image=' + video.toString('base64'), true);
    request.send();
    });



</script>
</html>
    """

@app.route('/submit',methods=['POST'])
def submit():
    image = request.args.get('image')

    print(type(image))
    return ""

@app.route('/anotherpage')
def get_another_page():
  return render_template("anotherpage.html")

@app.route('/videoanalysis', methods=['GET','POST'])
def get_video_analysis():
  form = UploadFileForm()
  if form.validate_on_submit():
      # Our uploaded video file path is saved here
      file = form.file.data
      file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'],
                              secure_filename(file.filename)))  # Then save the file
      # Use session storage to save video file path
      session['video_path'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'],
                                            secure_filename(file.filename))
  return render_template("videoanalysis.html", form=form)

@app.route('/video')
def video():
    #return Response(generate_frames(path_x='static/files/bikes.mp4'), mimetype='multipart/x-mixed-replace; boundary=frame')
    return Response(generate_frames(path_x = session.get('video_path', None)),mimetype='multipart/x-mixed-replace; boundary=frame')

# To display the Output Video on Webcam page
@app.route("/webcam", methods=['GET','POST'])

def webcam():
    session.clear()
    return render_template('ui.html')


@app.route('/webapp')
def webapp():
    #return Response(generate_frames(path_x = session.get('video_path', None),conf_=round(float(session.get('conf_', None))/100,2)),mimetype='multipart/x-mixed-replace; boundary=frame')
    return Response(generate_frames_web(path_x=1), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
  app.run(host="0.0.0.0",port=80)