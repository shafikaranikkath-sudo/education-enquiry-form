from flask import Flask, render_template, request, redirect, send_from_directory
from fpdf import FPDF
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'data'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    data = request.form.to_dict()
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for key, value in data.items():
        pdf.cell(200, 10, txt=f"{key}: {value}", ln=True)
    filename = f"{data.get('name', 'candidate')}_info.pdf".replace(" ", "_")
    pdf_path = os.path.join(UPLOAD_FOLDER, filename)
    pdf.output(pdf_path)
    return redirect(f'/candidate/{filename}')

@app.route('/candidate/<filename>')
def candidate(filename):
    return render_template('candidate_info.html', filename=filename)

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
