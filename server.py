from flask import Flask, request, render_template 
app = Flask(__name__) 
@app.route('/', methods=['GET', 'POST']) 
def login(): 
    if request.method == 'POST': 
        username = request.form.get('username') 
        password = request.form.get('password') 
        if username == 'admin' and password == 'letmein': 
            return 'Welcome, admin!' 
        else: 
            return 'Invalid credentials' 
    return render_template('login.html') 

if __name__ == '__main__': 
    app.run(debug=True)