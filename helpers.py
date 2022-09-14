from flask import render_template

def apology(message, code):
    """Render message as an apology to user."""
    return render_template("apology.html", code=code, message=message)
