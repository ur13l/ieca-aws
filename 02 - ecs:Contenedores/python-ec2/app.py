
from flask import Flask, render_template, request, redirect, url_for
import boto3

app = Flask(__name__)
ec2 = boto3.resource('ec2')
                    

@app.route('/')
def index():
    instances = ec2.instances.all() 
    return render_template('index.html', instances=instances)

@app.route('/action', methods=['POST'])
def action():
    instance_id = request.form.get('id')
    action = request.form.get('action')
    
    instance = ec2.Instance(instance_id)
    
    if action == 'Detener':
        instance.stop()
    elif action == 'Iniciar':
        instance.start()
 
    return redirect(url_for('index'))
        
