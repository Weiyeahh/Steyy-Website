
import os
from flask import Flask, flash, render_template, request, redirect
from werkzeug.utils import secure_filename
from main import botres

responselist=""


UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt',"jpg","png","gif"}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000
app.config['SECRET_KEY'] = '12345'

@app.route('/')
def my_form():
    
    return render_template('my-form.html')

@app.route('/', methods=['POST','GET'])
def my_form_post():
    name = request.form['chatbotname']
    personality = request.form['p1']
    personality_2 = request.form['p2']
    personality_3 = request.form['p3']
    relationship=request.form['relationship']
    with open('datafile/userinfo.txt', 'w',encoding="UTF8") as f:
        f.write(f"{name}\n{personality}\n{personality_2}\n{personality_3}\n{relationship}")
    return redirect('/chathistory')



@app.route('/chathistory')
def decision():
    return render_template("chathistory.html", upload_file = upload_file(), home = home())


    
# def change_page():
#     if request.method == 'POST': 
#         redirect('/upload')
#         return 'you\'re being redirected'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# @app.route('/chat', methods=['GET', 'POST'])
# def chat():
#     return render_template('chat-form.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part',category="success")
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file',category="success")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename("trainning")
            file.save("datafile/trainning.txt")
            return redirect("/hi")
    return render_template('file-uploader.html', filename = 'file')

@app.route('/userprofile', methods=['GET', 'POST'])
def upload_userprofile():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part',category="success")
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file',category="success")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename("userprofile")
            file.save("static/userprofile.jpg")
            return redirect("/botprofile")
    return render_template('userprofileupload.html', filename = 'file')

@app.route('/botprofile', methods=['GET', 'POST'])
def upload_botprofile():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part',category="success")
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file',category="success")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename("userprofile")
            file.save("static/botprofile.jpg")
            return redirect("/index")
    return render_template('botprofile.html', filename = 'file')


@app.route("/index",methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/get",methods=["GET"])

def get_bot_response():
    f = open("datafile/userinfo.txt", "r")
    name=f.readline().strip("\n")
    personality1=f.readline().strip("\n")
    personality2=f.readline().strip("\n")
    personality3=f.readline().strip("\n")
    relationship=f.readline().strip("\n")
    prompttext=f"The following is a conversation with an AI {relationship}. The AI {relationship} is very {personality1}, {personality2}, and {personality3}. The AI's name is {name}. Only generate the conversation for the AI.\n\n\nHuman: Hello, who are you?\nAI: I am AI, I will always be there for you."
    if os.path.isfile(f"datafile/trainning.txt")==True:
        f=open("datafile/trainning.txt", "r",encoding="UTF8")
        extratraining=list(f)
        trainingstr=""
        for items in extratraining:
            trainingstr+=items
        trainingprompt=trainingstr.split("\n")
        cleantrainingprompt=[]
        for items in trainingprompt:
            firstDelPos=items.find("[") # get the position of [
            secondDelPos=items.find("]") # get the position of ]
            newitem = items.replace(items[firstDelPos:secondDelPos+2],"")
            cleantrainingprompt.append(f'\n{newitem}')
        for items in cleantrainingprompt:
            if "\u200eimage omitted" or "Messages and calls are end-to-end encrypted." or "https" or "Missed voice call" in items:
                cleantrainingprompt.remove(items)
        # print(cleantrainingprompt)
        trainingstr=""
        for items in cleantrainingprompt:
            if cleantrainingprompt.index(items)<=300:
                items=items.replace(name,"AI")
                items=items.replace("Weiye:","Human:")
                trainingstr+=items
            else:
                break
        # print(cleanprompt)
        prompttext+=trainingstr
    userText = request.args.get('msg')
    response=botres(prompttext,userText,responselist).replace("AI",name)
    return(f"{response}")

@app.route('/usercase')
def my_usercase():
    
    return render_template('usercase.html')

@app.route('/contact')
def my_contact():
    
    return render_template('contactus.html')
@app.route('/sitemap')
def my_sitemap():
    
    return render_template('sitemap.html')
if __name__=="__main__":
    app.run()
