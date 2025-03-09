from flask import Flask, render_template, request, session

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Session için gizli anahtar

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session['grammar_scores'] = [request.form[f'grammar{i}'] for i in range(1, 5)]
        session['writing_scores'] = [request.form[f'writing{i}'] for i in range(1, 5)]
        session['speaking_scores'] = [request.form[f'speaking{i}'] for i in range(1, 5)]
        session['final_score'] = request.form['final']

        grammar_scores = list(map(float, session['grammar_scores']))
        writing_scores = list(map(float, session['writing_scores']))
        speaking_scores = list(map(float, session['speaking_scores']))
        final_score = float(session['final_score'])

        grammar_avg = sum(grammar_scores) / len(grammar_scores)
        writing_avg = sum(writing_scores) / len(writing_scores)
        speaking_avg = sum(speaking_scores) / len(speaking_scores)

        vize_avg = (grammar_avg * 8 + writing_avg * 8 + speaking_avg * 6) / 22
        overall_avg = (final_score * 0.6) + (vize_avg * 0.4)

        if final_score < 50 or vize_avg < 40:
            status = "Kaldı"
            status_color = "red"
        elif overall_avg >= 60:
            status = "Geçti"
            status_color = "green"
        else:
            status = "Kaldı"
            status_color = "red"

        return render_template('result.html', grammar_avg=grammar_avg, writing_avg=writing_avg, speaking_avg=speaking_avg, overall_avg=overall_avg, status=status, status_color=status_color)

    return render_template('index.html', session=session)

if __name__ == '__main__':
    app.run(debug=True)
