from app import app
from flask import request, session, render_template

@app.route('/hangman')
def ttt():
    if "secret" in session:   #Retrieve game state from session, if it exists
        secret = session["secret"]
        guesses = session["guesses"]
    else:  #This must be a new game
        secret = "python"  #This plays with the same word
                           #Perhaps pick a word at random?
        guesses = [ ]
    
    if "reset" in request.args:
        secret = "python"  #This plays with the same word
                           #Perhaps pick a word at random?
        guesses = [ ]
        
    if "guess" in request.args:
        guess = request.args["guess"]
        guesses.append(guess)
        
    #Let's compute how many of the guesses were incorrect
    incorrect = 0
    for letter in guesses:
        if letter not in secret:
            incorrect += 1
    
    #Compute hint for user        
    hint = ""
    for letter in secret:
        if letter in guesses:
            hint += letter
        else:
            hint += "-"

    if hint == secret:
        done = True
    else:
        done = False
            
    #Save data back to the session object
    session["secret"] = secret
    session["guesses"] = guesses
    
    return render_template('hangman.html', incorrects=incorrect,\
                           hint=hint, done=done, guesses=guesses)
      
@app.route('/')
def index():
    return "Hello. check out /ttt , dawg"

app.secret_key = '324iu234oiu124iu214io12u42i214iou12'