from flask import Flask, render_template, redirect, request, flash, session
from surveys import satisfaction_survey

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a secure key

responses = []


@app.route('/')
def home():
    return render_template('start.html', survey_title=satisfaction_survey.title,
                           instructions=satisfaction_survey.instructions)


@app.route('/questions/<int:qid>')
def show_question(qid):
    if qid != len(responses):
        flash("Invalid question access. Please answer the questions in order.")
        return redirect(f'/questions/{len(responses)}')
    if qid >= len(satisfaction_survey.questions):
        return redirect('/complete')

    question = satisfaction_survey.questions[qid]
    return render_template('question.html', question_num=qid, question=question)


@app.route('/answer', methods=['POST'])
def handle_answer():
    choice = request.form['answer']
    responses.append(choice)

    if len(responses) < len(satisfaction_survey.questions):
        return redirect(f'/questions/{len(responses)}')
    else:
        return redirect('/complete')


@app.route('/complete')
def complete():
    return render_template('complete.html')


if __name__ == '__main__':
    app.run(debug=True)
