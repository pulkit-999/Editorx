from flask import Flask,render_template,request,flash
from werkzeug.utils import secure_filename
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os
import cv2
from pdf2docx import Converter

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.secret_key='super secret key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
def processImage(filename,operation):
    print(f"The file name is {filename} and the operation is {operation}")
    img=cv2.imread(f"uploads/{filename}")
    if operation =="grayscale":
        imgprocessed=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        newfilename=f"static/{filename}"
        cv2.imwrite(newfilename,imgprocessed)
        return newfilename
    elif operation =="jpg":
        newfilename=f"static/{filename.split('.')[0]}.jpg"
        cv2.imwrite(newfilename,img)
        return newfilename
    elif operation =="pdf":
        newfilename=f"static/{filename.split('.')[0]}.pdf"
        img_height, img_width, _ = img.shape
        page_size = (img_width, img_height)
        c = canvas.Canvas(newfilename, pagesize=page_size)
        c.drawImage(f"uploads/{filename}", 0, 0, width=img_width, height=img_height)
        c.save()
        return newfilename
    # elif operation == "word":
    #     # Convert PDF to Word
    #     pdf_filename = f"static/{filename.split('.')[0]}.pdf"
    #     word_filename = f"static/{filename.split('.')[0]}.docx"
    #     # Check if the PDF file exists
    #     if not os.path.exists(pdf_filename):
    #         return f"Error: PDF file '{pdf_filename}' not found"

    #     try:
    #     # Perform PDF to Word conversion
    #         cv = Converter(pdf_filename)
    #         cv.convert(word_filename, start=0, end=None)
    #         cv.close()
    #         return word_filename
    #     except Exception as e:
    #         return f"Error converting PDF to Word: {e}"
    pass
@app.route('/')
def hello_world():
    return render_template("index.html")
@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/edit',methods=["GET","POST"])
def edit():
    if request.method == 'POST':
        operation=request.form.get("operation")
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return "error"
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return "file not selected"
        if file and allowed_file(file.filename):

            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new =processImage(filename,operation)
            flash(f"your image is successfully processed,click here <a href='/{new}'target='_blank'>here</a>")
            return render_template("index.html")
    return render_template("index.html")
app.run(debug=True,port=5757)