from flask import Flask,render_template,request,redirect,url_for,session
import mysql.connector
import base64 

app = Flask(__name__)

# Register custom Jinja2 filter
@app.template_filter('b64encode')
def b64encode_filter(s):
    return base64.b64encode(s).decode('utf-8')

app.secret_key = "super secret key"

mydb = mysql.connector.connect(
    host = "localhost",
    username = "root",
    password = "",
    db = "project"
)


def get_student(filter_by=None):
    if filter_by is not None:
        query = f"SELECT * FROM students WHERE {filter_by}"
    else:
        query = "SELECT * FROM students"
    cursor.execute(query)
    students = cursor.fetchall()
    return students

cursor = mydb.cursor()
mydb.commit()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/admission')
def admission():
    return render_template('admission.html')

# admission form for gathering information

@app.route('/admreport',methods=['GET','POST'])
def admreport():
    if request.method == 'POST':
        admname = request.form['admname']
        admphone = request.form['admphone']
        admemail = request.form['admemail']
        admcourse = request.form['admcourse']
        admaddress = request.form['admaddress']
        tdate = request.form['tdate']

        cursor.execute("INSERT INTO admission (admname,admphone,admemail,admcourse,admaddress,tdate) VALUES (%s,%s,%s,%s,%s,%s)",(admname,admphone,admemail,admcourse,admaddress,tdate))
        mydb.commit()
        return "success"
    else:
        return render_template('admission.html')

@app.route('/adm-view',methods=['GET','POST'])
def adm_view():

    cursor.execute('SELECT * FROM admission')
    adm = cursor.fetchall()

    return render_template('admission-admin.html',adm=adm)
    
@app.route('/faculty')
def faculty():
    cursor.execute('SELECT * FROM staff')
    staff=cursor.fetchall()
    return render_template('faculty.html',staff=staff)

@app.route('/results')
def results():
    return render_template('results.html')

@app.route('/transports')
def transports():
    return render_template('transports.html')

@app.route('/campus')
def campus():
    return render_template('campus.html')

@app.route('/culturals')
def culturals():
    return render_template('culturals.html')

@app.route('/events')
def events():
    return render_template('events.html')

@app.route('/contactus')
def contactus():
    return render_template('contactus.html')

@app.route('/login')
def login():
    return render_template('login-page.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/student-add')
def student_add():
    return render_template('student-add.html')

@app.route('/insert_student',methods=['GET','POST'])
def insert_student():

    if request.method == "POST":

        regno = request.form['stregno']
        name = request.form['stname']
        dept = request.form['stdept']
        batch = request.form['stbatch']
        phone = request.form['stphone']
        dob = request.form['stdob']
        blood = request.form['stblood']

        cursor.execute('INSERT INTO students (stregno,stname,stdept,stbatch,stphone,stdob,stblood) VALUES (%s,%s,%s,%s,%s,%s,%s)',(regno,name,dept,batch,phone,dob,blood))
        mydb.commit()
        return render_template('student-view.html')
    
@app.route('/search')
def search():
    students = get_student()
    return render_template('student-view.html', students=students)


@app.route('/search_form', methods=['GET', 'POST'])
def search_form():
    regno = request.form['stregno']
    filter_by = []
    if regno:
        filter_by.append(f"stregno='{regno}'")
    filter_by = ' AND '.join(filter_by)
    students = get_student(filter_by=filter_by)
    return render_template('student-view.html', students=students)


# staff section
@app.route('/staff-add')
def staff_add():
    return render_template('staff-add.html')

@app.route('/insert_staff',methods=['GET','POST'])
def insert_staff():
    if request.method == 'POST':

        name = request.form['sfname']
        desg = request.form['sfdesg']
        phone = request.form['sfphone']
        photo = request.files['sfphoto'].read()

        cursor.execute('INSERT INTO staff (sfname,sfdesg,sfphone,sfphoto) VALUES (%s,%s,%s,%s)',(name,desg,phone,photo))
        mydb.commit()
        return render_template('staff-add.html')
    
@app.route('/staff-view')
def staff_view():
    cursor.execute('SELECT * FROM staff')
    staff=cursor.fetchall()

    return render_template('staff-view.html',staff=staff)
 
@app.route('/auth',methods=['GET','POST'])
def auth():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            cursor.execute('SELECT * FROM users WHERE username=%s AND password=%s',(username,password))
            user = cursor.fetchone()

            if user:
                session['username'] = user[1]
                return render_template('admin.html')
            else:
                return render_template('login-page.html')
        else:
            return render_template('login-page.html')
        
@app.route('/settings')
def settings():

    cursor.execute('SELECT * FROM users')
    set=cursor.fetchall()
    return render_template('settings.html',set=set)

@app.route('/update_set',methods=['POST'])
def update_set():
        username = request.form['username']
        password = request.form['password']
        cursor.execute('UPDATE users SET username=%s,password=%s',(username,password))
        mydb.commit()
        return render_template('admin.html')

@app.route('/logout')
def logout():
    return render_template('home.html')
            
if __name__ == '__main__':
    app.run(debug=True)
