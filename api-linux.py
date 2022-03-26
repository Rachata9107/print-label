from flask import Flask, request
from relatorio.templates.opendocument import Template

import os
import subprocess
import qrcode
import time
import tempfile
import cups

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

def print_placard(info={}):

    # info['job_id'] = '1850002208'
    # info['part_no'] = '10004426'
    # info['part_name'] = 'BCu-P'
    # info['qty'] = '520'
    # info['mc_from'] = 'Bending'
    # info['mc_to'] = 'Packing'
    # info['datetime'] = '2022/03/07'
    
    info['my_qr'] = (open(generate_qr_code(info['job_id']), 'rb'), 'image/png')

    template_path = os.path.dirname(os.path.abspath(__file__))
    template_file = r'template_qr.odt'

    filepath = os.path.join(template_path, template_file)
    print(filepath)

    template_qr = Template(source='', filepath=filepath)

    with tempfile.NamedTemporaryFile(delete=False, suffix='.odt') as tmpfile:
        output = template_qr.generate(o=info).render().getvalue()
        tmpfile.write(output)
        convertPdf = ['libreoffice', '--headless', '--convert-to', 'pdf', tmpfile.name, '--outdir', 'files']
        subprocess.call(convertPdf)
        time.sleep(1)

        printerName = 'Honeywell_PC42tp-203-FP'
        fileName = 'files' + tmpfile.name[4:-3] + 'pdf'

        conn = cups.Connection()
        #printers = conn.getPrinters()
        conn.printFile(printerName, fileName, " ", {})

if __name__ == "__main__":
    app.run(debug=True)
    #print_placard()
