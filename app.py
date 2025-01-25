from flask import Flask, render_template, request, jsonify
import pyttsx3
import datetime
import wikipediaapi
import webbrowser
import re

# Initialize Flask app
app = Flask(__name__)

# Initialize Text-to-Speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

# Speak function
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

# Wish the user based on time
def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        return "Good Morning!"
    elif hour >= 12 and hour < 18:
        return "Good Afternoon!"
    else:
        return "Good Evening!"

# Flask Routes
@app.route('/')
def index():
    greeting = wishMe()
    return render_template('index.html', greeting=greeting)

@app.route('/process', methods=['POST'])
def process_command():
    data = request.json
    query = data.get('query', '').lower()
    response = ""

    try:
        if re.search(r'\b(wikipedia|wiki)\b', query):
            response = "Searching Wikipedia..."
            speak(response)
            query = re.sub(r'\b(wikipedia|wiki)\b', "", query).strip()
            wiki = wikipediaapi.Wikipedia('en')
            page = wiki.page(query)
            if page.exists():
                results = page.summary[:500]
                response = f"According to Wikipedia: {results}"
            else:
                response = "Sorry, no results found on Wikipedia."
        elif re.search(r'\b(open|launch)\s(youtube|google)\b', query):
            if 'youtube' in query:
                webbrowser.open("https://youtube.com")
                response = "Opening YouTube..."
            elif 'google' in query:
                webbrowser.open("https://google.com")
                response = "Opening Google..."
        elif re.search(r'\b(time|clock)\b', query):
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            response = f"The time is {strTime}."
        else:
            response = "I'm sorry, I can't process that command yet."
    except Exception as e:
        response = f"An error occurred: {str(e)}"

    speak(response)
    return jsonify({'response': response})

if __name__ == "__main__":
    app.run(debug=True)
