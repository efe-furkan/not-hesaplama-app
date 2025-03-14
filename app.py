from flask import Flask, render_template, request, session

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Session için gizli anahtar

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Kullanıcıdan gelen notları al
        session['grammar_scores'] = [request.form[f'grammar{i}'] for i in range(1, 6)]
        session['writing_scores'] = [request.form[f'writing{i}'] for i in range(1, 6)]
        session['speaking_scores'] = [request.form[f'speaking{i}'] for i in range(1, 6)]
        
        # Notları float'a çevir
        grammar_scores = list(map(float, session['grammar_scores']))
        writing_scores = list(map(float, session['writing_scores']))
        speaking_scores = list(map(float, session['speaking_scores']))
        
        # Ders saat ağırlıkları
        grammar_weight = 8
        writing_weight = 8
        speaking_weight = 6
        total_weight = grammar_weight + writing_weight + speaking_weight  # 8 + 8 + 6 = 22

        # Vize ortalamaları
        grammar_avg = sum(grammar_scores[:4]) / 4
        writing_avg = sum(writing_scores[:4]) / 4
        speaking_avg = sum(speaking_scores[:4]) / 4

        # Final notları
        grammar_final = grammar_scores[4]
        writing_final = writing_scores[4]
        speaking_final = speaking_scores[4]

        # **Ağırlıklı Vize Ortalaması**
        vize_avg = (
            (grammar_avg * grammar_weight) +
            (writing_avg * writing_weight) +
            (speaking_avg * speaking_weight)
        ) / total_weight

        # **Ağırlıklı Final Ortalaması**
        final_avg = (
            (grammar_final * grammar_weight) +
            (writing_final * writing_weight) +
            (speaking_final * speaking_weight)
        ) / total_weight

        # **Ağırlıklı Yıl Sonu Notu**
        year_end_grade = (vize_avg * 0.4) + (final_avg * 0.6)

        # Başarı durumu ve neden belirleme
        status = "Geçti"
        status_color = "green"
        reason = "-"
        reason_color = "blue"
        final_display = "normal"

        # Geçme kriterleri
        if vize_avg < 40:
            status = "Kaldı"
            status_color = "red"
            reason = "Vizeler Ham Ortalaması 40'ın altında olduğu için final sınavına giriş hakkı yok."
            final_display = "dash"
        elif final_avg < 50:
            status = "Kaldı"
            status_color = "red"
            reason = "Final notunun ham ortalaması 50'in altında olduğu için yetersiz."
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
                              year_end_grade=year_end_grade,
                              status=status, 
                              status_color=status_color,
                              reason=reason,
                              reason_color=reason_color,
                              final_display=final_display)

    return render_template('index.html', session=session)

if __name__ == '__main__':
    app.run(debug=True)