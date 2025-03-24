from flask import Flask, render_template, request, jsonify
try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO! This is probably because you need superuser privileges. You can achieve this by using 'sudo' to run your script.")
import atexit
import logging
from flask_cors import CORS

# Configuration du log
logging.basicConfig(level=logging.INFO, format='%(message)s')

# GPIO setup
GPIO_PIN_DIR_GAUCHE = 17
GPIO_PIN_VIT_GAUCHE = 22
GPIO_PIN_DIR_DROITE = 27
GPIO_PIN_VIT_DROITE = 23

GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_PIN_DIR_GAUCHE, GPIO.OUT)
GPIO.setup(GPIO_PIN_VIT_GAUCHE, GPIO.OUT)
GPIO.setup(GPIO_PIN_DIR_DROITE, GPIO.OUT)
GPIO.setup(GPIO_PIN_VIT_DROITE, GPIO.OUT)

# Nettoyage du GPIO ï¿½ la sortie
def cleanup_gpio():
    GPIO.cleanup()

atexit.register(cleanup_gpio)

# Flask setup
app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('js_robotrond_moteurs.html')

@app.route('/moteurs', methods=['GET', 'POST'])
def controler_moteurs():
    logging.info(f"Requête: {request.json}")
    if not request.json:
        return jsonify({'error': 'Invalid input'}), 400

    dirgauche = request.json.get('dirgauche')
    dirdroite = request.json.get('dirdroite')
    vitgauche = request.json.get('vitgauche')
    vitdroite = request.json.get('vitdroite')

    GPIO.output(GPIO_PIN_DIR_GAUCHE, GPIO.HIGH if dirgauche else GPIO.LOW)
    GPIO.output(GPIO_PIN_VIT_GAUCHE, GPIO.HIGH if vitgauche else GPIO.LOW)
    GPIO.output(GPIO_PIN_DIR_DROITE, GPIO.HIGH if dirdroite else GPIO.LOW)
    GPIO.output(GPIO_PIN_VIT_DROITE, GPIO.HIGH if vitdroite else GPIO.LOW)
    logging.info(f"Moteurs DIRG: {dirgauche}, VITG: {vitgauche}, DIRD: {dirdroite}, VITD: {vitdroite}")
    return jsonify({'DirGauche': GPIO.input(GPIO_PIN_DIR_GAUCHE), 'VitGauche': GPIO.input(GPIO_PIN_VIT_GAUCHE), 'DirDroite': GPIO.input(GPIO_PIN_DIR_DROITE), 'VitDroite': GPIO.input(GPIO_PIN_VIT_DROITE)})
@app.route('/status', methods=['GET'])
def status():
    ## send data to client
    stringjson = jsonify({'DirGauche': GPIO.input(GPIO_PIN_DIR_GAUCHE), 'VitGauche': GPIO.input(GPIO_PIN_VIT_GAUCHE), 'DirDroite': GPIO.input(GPIO_PIN_DIR_DROITE), 'VitDroite': GPIO.input(GPIO_PIN_VIT_DROITE)})
    print("test " + str(stringjson))
    return stringjson
@app.route('/stop', methods=['POST'])
def stop():
    ## if stop is called, GPIO is cleaned
    if request.json:    
        GPIO.cleanup()
        return jsonify({'stop': True})
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)