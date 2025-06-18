from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'any-secret-key-you-like'  # Needed to store session

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        num_subjects = int(request.form.get('num_subjects', 1))
        criteria = float(request.form.get('criteria', 75))
        session['num_subjects'] = num_subjects
        session['criteria'] = criteria
        return redirect(url_for('form'))
    return render_template("index.html")

@app.route('/form', methods=['GET', 'POST'])
def form():
    num_subjects = session.get('num_subjects', 1)
    return render_template("form.html", num_subjects=num_subjects)

@app.route('/calculate', methods=['POST'])
def calculate():
    criteria = session.get('criteria', 75)
    num_subjects = session.get('num_subjects', 1)

    subjects = []
    for i in range(1, num_subjects + 1):
        name = request.form.get(f'subject{i}')
        attended = int(request.form.get(f'attended{i}', 0))
        total = int(request.form.get(f'total{i}', 1))
        percent = round((attended / total) * 100, 2) if total > 0 else 0
        subjects.append({
            'name': name,
            'attended': attended,
            'total': total,
            'percent': percent
        })

    return render_template("result.html", results=subjects, criteria=criteria)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
