from flask import Flask, request
import os
import qrcode
from relatorio.templates.opendocument import Template

import tempfile
import time
import win32api 
import win32print

app = Flask(__name__)

@app.route('/')
def my_api():
  return { "message": "My API." }, 200

@app.route('/print-label', methods=['POST'])
def print_label():
    if request.method == 'POST':
        try:
            info = {}
            info = request.get_json()
            print_placard(info)
            return {"message": "success"}, 201
        except:
            return {"message": "error"}, 400

def generate_qr_code(qr_input: str):
    with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmpfile:
        qr = qrcode.make(qr_input)
        qr.save(tmpfile, qr.format, quality=100)
        time.sleep(1)
        return tmpfile.name

def print_placard(info):

    printerName = 'Honeywell PC42t plus (203 dpi)'

    info['my_qr'] = (open(generate_qr_code(info['job_id']), 'rb'), 'image/png')

    template_path = os.path.dirname(os.path.abspath(__file__))
    template_file = r'template_qr.odt'

    filepath = os.path.join(template_path, template_file)
    print(filepath)

    template_qr = Template(source='', filepath=filepath)

    with tempfile.NamedTemporaryFile(delete=False, suffix='.odt') as tmpfile:
        output = template_qr.generate(o=info).render().getvalue()
        tmpfile.write(output)  # /tmp in GNU/Linux,  %temp% in Windows        
        time.sleep(2)
        print(f'Printing: {tmpfile.name}')
        win32print.SetDefaultPrinterW(printerName)
        win32api.ShellExecute(0, 'print', tmpfile.name, f'/d:"{win32print.GetDefaultPrinter()}"', '.', 0)

if  __name__ == "__main__":
    app.run(debug=True)