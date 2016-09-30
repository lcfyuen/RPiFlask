
import RPi.GPIO as GPIO
from flask_script import Manager, Server
from flask_bootstrap import Bootstrap
from flask import Flask, render_template, request


app = Flask(__name__)
#server = Server(host='0.0.0.0', port= 5000)
manager = Manager(app)
manager.add_command("runserver", Server(host='0.0.0.0', port=5000))
boostrap = Bootstrap(app)


GPIO.setmode(GPIO.BCM)

# Create a dictionary called pins to store the pin number, name, and pin state:
pins = {
   23 : {'name' : 'Relay1', 'state' : GPIO.LOW, 'count': 0},
   24 : {'name' : 'Relay2', 'state' : GPIO.LOW, 'count': 0},
   25 : {'name' : 'Relay3', 'state' : GPIO.LOW, 'count': 0},

   }

# Set each pin as an output and make it low:
for pin in pins:
   GPIO.setup(pin, GPIO.OUT)
   GPIO.output(pin, GPIO.LOW)

@app.route("/")
def main():
   # For each pin, read the pin state and store it in the pins dictionary:
   for pin in pins:
      pins[pin]['state'] = GPIO.input(pin)
   # Put the pin dictionary into the template data dictionary:
   templateData = {
      'pins' : pins
      }
   # Pass the template data into the template main.html and return it to the user
   return render_template('index.html', **templateData)

# The function below is executed when someone requests a URL with the pin number and action in it:
@app.route("/<changePin>/<action>")
def action(changePin, action):
   # Convert the pin from the URL into an integer:
   changePin = int(changePin)
   # Get the device name for the pin being changed:
   deviceName = pins[changePin]['name']
   # If the action part of the URL is "on," execute the code indented below:
   if action == "on":
      # Set the pin high:
      GPIO.output(changePin, GPIO.HIGH)
      # Save the status message to be passed into the template:
      message = "Turned " + deviceName + " on."

      #Increment cycle count
      pins[changePin]['count'] += 1

   if action == "off":
      GPIO.output(changePin, GPIO.LOW)
      message = "Turned " + deviceName + " off."

   # For each pin, read the pin state and store it in the pins dictionary:
   for pin in pins:
      pins[pin]['state'] = GPIO.input(pin)

   # Along with the pin dictionary, put the message into the template data dictionary:
   templateData = {
      'pins' : pins
   }

   return render_template('index.html', **templateData)

if __name__ == "__main__":
   
   manager.run()
