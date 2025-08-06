from flask import Flask, render_template, request, redirect, url_for, session, abort

app = Flask(__name__)
app.secret_key = ' '

# ==== QUESTIONS ====
questions = [
    {
        "text": "Which of these situations would stress you out the most?",
        "options": [
            {"text": "Being underestimated despite your potential", "house": "slytherin"},
            {"text": "Being forced to follow rules you don’t agree with", "house": "gryffindor"},
            {"text": "Being isolated with no one to rely on", "house": "hufflepuff"},
            {"text": "Being told to stop asking questions", "house": "ravenclaw"},
        ]
    },
    {
        "text": "You’re given a day with no responsibilities. What do you do?",
        "options": [
            {"text": "Dive into a project you've been planning", "house": "slytherin"},
            {"text": "Go on an unplanned adventure", "house": "gryffindor"},
            {"text": "Spend time catching up with loved ones", "house": "hufflepuff"},
            {"text": "Get lost in reading or exploring new ideas", "house": "ravenclaw"},
        ]
    },
    {
        "text": "Which quote hits you the hardest?",
        "options": [
            {"text": "“Without loyalty, you have nothing.”", "house": "hufflepuff"},
            {"text": "“The mind is not a vessel to be filled but a fire to be kindled.”", "house": "ravenclaw"},
            {"text": "“Fortune favors the bold.”", "house": "gryffindor"},
            {"text": "“Power is taken, never given.”", "house": "slytherin"},
        ]
    },
    {
        "text": "A new rule is introduced at school that you strongly disagree with. You…",
        "options": [
            {"text": "Gather support and challenge it openly", "house": "gryffindor"},
            {"text": "Analyze the reasoning behind it before acting", "house": "ravenclaw"},
            {"text": "Adapt, but quietly work around it if needed", "house": "slytherin"},
            {"text": "Talk it over with others and find a peaceful solution", "house": "hufflepuff"},
        ]
    },
    {
        "text": "How do you react when someone questions your beliefs?",
        "options": [
            {"text": "I explain my views calmly and listen in return", "house": "hufflepuff"},
            {"text": "I debate them logically and confidently", "house": "ravenclaw"},
            {"text": "I take it as a challenge and defend my stance", "house": "gryffindor"},
            {"text": "I stay composed but make sure I come out on top", "house": "slytherin"},
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
# ==== ROUTES ====
@app.route("/")
def home():
    session.clear()    
    return render_template("index.html")

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
    
        # Initialize score + answers in session if not exist
    if 'scores' not in session:
        session['scores'] = {
            'gryffindor': 0,
            'ravenclaw': 0,
            'hufflepuff': 0,
            'slytherin': 0
        }

    if 'answers' not in session:
        session['answers'] = {}

    # Save answer and update score
    session['answers'][str(qid)] = selected_house
    scores = session['scores']
    scores[selected_house] += 1
    session['scores'] = scores

    next_qid = qid + 1
    if next_qid >= len(questions):
        winner = max(scores, key=scores.get)
        session['quiz_completed'] = True
        return redirect(url_for('result', house=winner))
    else:
        return redirect(url_for('question', qid=next_qid))

@app.route("/result/<house>")
def result(house):
    if not session.get('quiz_completed'):
        abort(403)
    session.clear()
    return render_template("result.html", house=house, houses=houses)

if __name__ == '__main__':
    app.run(debug=True)