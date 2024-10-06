from flask import Flask, render_template, request, redirect, url_for, session, flash
from model import db, User  # Your model import

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management

# Database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///game.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Create tables
with app.app_context():
    db.create_all()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check if user exists
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['user_id'] = user.id  # Store user ID in session
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password!')

    return render_template('login.html')

    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        # Check if the username or email is already taken
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash('Username or Email already exists!')
            return redirect(url_for('signup'))

        # Create new user
        new_user = User(id=username, username=username, password=password, email=email)
        db.session.add(new_user)
        db.session.commit()
        flash('Signup successful! Please login.')
        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/dashboard')
def dashboard():
    # Assuming you have the user ID stored in session
    user_id = session.get('user_id')
    user = User.query.get(user_id)  # Fetch the user from the database

    if user:
        return render_template('dashboard.html', user=user)  # Pass user object to the template
    else:
        return redirect(url_for('login'))  # Redirect if user is not logged in



@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)  # Remove the username from the session
    flash('You have been logged out successfully.')  # Optional flash message
    return redirect(url_for('login'))  # Redirect to the login page

@app.route('/challenge1')
def challenge1():
    return render_template('challenge1.html')

@app.route('/challenge2')
def challenge2():
    return render_template('challenge2.html')

@app.route('/challenge3')
def challenge3():
    return render_template('challenge3.html')

@app.route('/challenge4')
def challenge4():
    return render_template('challenge4.html')

@app.route('/challenge5')
def challenge5():
    return render_template('challenge5.html')

expected_output = "Hello, World!"  # Example output


    
@app.route('/submit_code', methods=['POST'])
def submit_code():
    user_code = request.form['code']
    # Example input/output for the challenge
    expected_output = "Hello, World!"

    # Capture the output of the user's code
    try:
        # WARNING: Using exec is dangerous, be cautious with untrusted inputs
        exec_globals = {}
        exec(user_code, exec_globals)
        result = exec_globals.get('output', None)  # Assume user's code prints or assigns to 'output'
        
        # Check if the output matches expected
        if result == expected_output:
            return "Congratulations! Your code worked correctly."
        else:
            return "Oops! The code output is incorrect."
    except Exception as e:
        return f"Error: {str(e)}"



challenges = {
    1: {
        1: "Write a Python function to reverse a string.",
        2: "Write a Python function to check if a number is prime.",
        3: "Write a Python program to find the factorial of a number.",
        4: "Write a Python program to print the Fibonacci sequence.",
        5: "Write a Python function to check if a string is a palindrome."
    },
    2: {
        1: "Merge two sorted lists.",
        2: "Sort a list of dictionaries by a key.",
        3: "Calculate the nth Fibonacci number recursively.",
        4: "Find the GCD of two numbers.",
        5: "Solve the Tower of Hanoi problem."
    },
    3: {
        1: "Solve a Sudoku puzzle.",
        2: "Find the shortest path in a graph using Dijkstra's algorithm.",
        3: "Implement a binary search tree.",
        4: "Solve the knapsack problem using dynamic programming.",
        5: "Implement the A* search algorithm."
    }
}

@app.route('/level/<int:level>/stage/<int:stage>')
def show_challenge(level, stage):
    try:
        challenge_question = challenges.get(level, {}).get(stage)
        print(f"Fetched Question: {challenge_question}")  # Print the question to the console
        if not challenge_question:
            return "Challenge not found!", 404
    except KeyError:
        return "Invalid Level or Stage!", 404

    return render_template('challenge1.html', level=level, stage=stage, question=challenge_question)





user_progress = {}  # Dictionary to hold user progress

@app.route('/update_progress', methods=['POST'])
def update_progress():
    username = request.form['username']
    level = request.form['level']
    stage = request.form['stage']
    
    if username not in user_progress:
        user_progress[username] = {}
    
    if level not in user_progress[username]:
        user_progress[username][level] = []
    
    user_progress[username][level].append(stage)
    return "Progress updated!"


if __name__ == '__main__':
    app.run(debug=True)
    
