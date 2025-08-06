from flask import Flask, render_template, request, redirect, url_for, session


app = Flask(__name__)

app.secret_key = '1234'

Gryffindor = Ravenclaw = Hufflepuff = Slytherin = 0
scores = {
    'gryffindor':0,
    'ravenclaw':0,
    'hufflepuff':0,
    'slytherin':0,
}

@app.route("/")
def home():
    return render_template("index.html")

# ==== QUESTIONS ====
questions = [
    {
        "text": "What do you value most?",
        "options": [
            {"text": "Bravery", "house": "gryffindor"},
            {"text": "Intelligence", "house": "ravenclaw"},
            {"text": "Loyalty", "house": "hufflepuff"},
            {"text": "Ambition", "house": "slytherin"},
        ]
    },
    {
        "text": "What would you do if a friend was being bullied?",
        "options": [
            {"text": "Step in and defend them, no matter what", "house": "gryffindor"},
            {"text": "Think of a clever way to stop it", "house": "ravenclaw"},
            {"text": "Stand by them and report it if needed", "house": "hufflepuff"},
            {"text": "Use the situation to show who's really in control", "house": "slytherin"},
        ]
    },
    {
        "text": "Pick a magical pet to take to Hogwarts:",
        "options": [
            {"text": "Lion", "house": "gryffindor"},
            {"text": "Owl", "house": "ravenclaw"},
            {"text": "Badger", "house": "hufflepuff"},
            {"text": "Snake", "house": "slytherin"},
        ]
    },
    {
        "text": "What’s your ideal weekend?",
        "options": [
            {"text": "Going on an adventure with friends", "house": "gryffindor"},
            {"text": "Reading or learning something new", "house": "ravenclaw"},
            {"text": "Spending time helping family or friends", "house": "hufflepuff"},
            {"text": "Working on your goals or side hustle", "house": "slytherin"},
        ]
    },
    {
        "text": "You find a mysterious book in the library. You…",
        "options": [
            {"text": "Open it immediately and see what happens", "house": "gryffindor"},
            {"text": "Research its origin before touching it", "house": "ravenclaw"},
            {"text": "Ask a professor or friend if it's safe", "house": "hufflepuff"},
            {"text": "Keep it to yourself — knowledge is power", "house": "slytherin"},
        ]
    },
]

# ==== HOUSES ====
houses = {
    "gryffindor": {
        "name": 'Gryffindor',
        "quote": (
            "You might belong in Gryffindor,\n"
            "Where dwell the brave at heart,\n"
            "Their daring, nerve and chivalry\n"
            "Set Gryffindors apart."
        ),
        "mascot": "Lion",
        "colors": "Red & Gold",
        "traits": ["Bravery", "Courage", "Daring", "Determination"],
        "notable": ["Harry Potter", "Hermione Granger", "Ron Weasley"],
        "logo": "/static/img/gryffindor.png"
    },
    "ravenclaw": {
        "name": 'Ravenclaw',
        "quote": (
            "Or yet in wise old Ravenclaw,\n"
            "If you've a ready mind,\n"
            "Where those of wit and learning,\n"
            "Will always find their kind."
        ),
        "mascot": "Eagle",
        "colors": "Blue & Bronze",
        "traits": ["Intelligence", "Wisdom", "Creativity", "Individuality"],
        "notable": ["Luna Lovegood", "Cho Chang", "Filius Flitwick"],
        "logo": "/static/img/ravenclaw.png"
    },
    "hufflepuff": {
        "name": 'Hufflepuff',
        "quote": (
            "You might belong in Hufflepuff,\n"
            "Where they are just and loyal,\n"
            "Those patient Hufflepuffs are true\n"
            "And unafraid of toil."
        ),
        "mascot": "Badger",
        "colors": "Yellow & Black",
        "traits": ["Loyalty", "Patience", "Fairness", "Hard Work"],
        "notable": ["Cedric Diggory", "Nymphadora Tonks", "Newt Scamander"],
        "logo": "/static/img/hufflepuff.png"
    },
    "slytherin": {
        "name": 'Slytherin',
        "quote": (
            "Or perhaps in Slytherin,\n"
            "You'll make your real friends,\n"
            "Those cunning folk use any means\n"
            "To achieve their ends."
        ),
        "mascot": "Snake",
        "colors": "Green & Silver",
        "traits": ["Ambition", "Cunning", "Leadership", "Resourcefulness"],
        "notable": ["Severus Snape", "Draco Malfoy", "Tom Riddle"],
        "logo": "/static/img/slytherin.png"
    }
}



@app.route("/question/<int:qid>")
def question(qid):
    if qid < 0 or qid >= len(questions):
        return "Quiz finished or invalid question"

    q = questions[qid]
    return render_template("question.html", question=q, qid=qid)


@app.route("/answer/<int:qid>", methods=["POST"])
def answer(qid):
    selected_house = request.form.get('answer')
    if not selected_house:
        # no option selected, redirect back to same question
        return redirect(url_for('question', qid=qid))
    
    # Save user's answers in session
    if 'answers' not in session:
        session['answers'] = {}
    session['answers'][str(qid)] = selected_house
    scores[selected_house] += 1
    
    next_qid = qid + 1
    if next_qid >= len(questions):
        winner = max(scores, key=scores.get)
        return redirect(url_for('result', house=winner))
    else:
        return redirect(url_for('question', qid=next_qid))


    # ==== HOUSE ROUTES ====

@app.route("/result/<house>")
def result(house):
    return render_template("result.html", house=house, houses=houses)


if __name__ == '__main__':
    app.run(debug=True)