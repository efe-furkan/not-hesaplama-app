from flask import Flask, render_template, request, session

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Session için gizli anahtar

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get all five quiz scores for each course
        session['grammar_scores'] = [request.form[f'grammar{i}'] for i in range(1, 6)]
        session['writing_scores'] = [request.form[f'writing{i}'] for i in range(1, 6)]
        session['speaking_scores'] = [request.form[f'speaking{i}'] for i in range(1, 6)]
        
        # Convert strings to floats
        grammar_scores = list(map(float, session['grammar_scores']))
        writing_scores = list(map(float, session['writing_scores']))
        speaking_scores = list(map(float, session['speaking_scores']))
        
        # Calculate averages for each course (first 4 scores are midterms, 5th is final)
        grammar_avg = sum(grammar_scores[:4]) / 4
        writing_avg = sum(writing_scores[:4]) / 4
        speaking_avg = sum(speaking_scores[:4]) / 4
        
        # The 5th score is the final
        grammar_final = grammar_scores[4]
        writing_final = writing_scores[4]
        speaking_final = speaking_scores[4]
        
        # Calculate weighted midterm average (all midterms, not including finals)
        vize_avg = (sum(grammar_scores[:4]) + sum(writing_scores[:4]) + sum(speaking_scores[:4])) / 12
        
        # Calculate final exam average
        final_avg = (grammar_final + writing_final + speaking_final) / 3
        
        # Calculate combined averages for each course with their respective finals
        grammar_final_avg = (grammar_avg + grammar_final) / 2
        writing_final_avg = (writing_avg + writing_final) / 2
        speaking_final_avg = (speaking_avg + speaking_final) / 2
        
        # Calculate year-end grade
        year_end_grade = (vize_avg * 0.4) + (final_avg * 0.6)
        
        # Determine status and reason
        status = "Geçti"
        status_color = "green"
        reason = "-"
        reason_color = "blue"
        
        # Final notları için varsayılan durum
        final_display = "normal"
        
        # Check failure conditions
        if vize_avg < 40:
            status = "Kaldı"
            status_color = "red"
            reason = "Vizeler Ham Ortalaması 40'ın altında olduğu için final sınavına giriş hakkı yok."
            final_display = "dash"  # Final notları için tire gösterimi
        elif final_avg < 50:
            status = "Kaldı"
            status_color = "red"
            reason = "Final notunun ham ortalaması 50'ın altında olduğu için yetersiz."
        elif year_end_grade < 60:
            status = "Kaldı"
            status_color = "red"
            reason = "Yıl sonu notu 60'ın altında olduğu için yetersiz."

        return render_template('result.html', 
                              grammar_avg=grammar_avg, 
                              writing_avg=writing_avg, 
                              speaking_avg=speaking_avg,
                              grammar_final=grammar_final,
                              writing_final=writing_final,
                              speaking_final=speaking_final,
                              vize_avg=vize_avg,
                              final_avg=final_avg,
                              grammar_final_avg=grammar_final_avg,
                              writing_final_avg=writing_final_avg,
                              speaking_final_avg=speaking_final_avg,
                              year_end_grade=year_end_grade,
                              status=status, 
                              status_color=status_color,
                              reason=reason,
                              reason_color=reason_color,
                              final_display=final_display)

    return render_template('index.html', session=session)

if __name__ == '__main__':
    app.run(debug=True)