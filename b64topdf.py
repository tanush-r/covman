from flask import *
import base64

app = Flask(__name__)

with open('message.txt','r') as f:
    pdf_data = f.readline()

@app.route('/')
def home():
    data = base64.b64decode(pdf_data)
    response = make_response(data) 
    cd = f"attachment; filename=Main.pdf" 
    response.headers['Content-Disposition'] = cd 
    response.mimetype='application/pdf' 
    return response
    
if __name__ == '__main__':
    app.run(debug=True)