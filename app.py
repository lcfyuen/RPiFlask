
from flask_script import Manager, Server
from flask_bootstrap import Bootstrap
from flask import Flask, render_template, request

from test import TestThread

app = Flask(__name__)
#server = Server(host='0.0.0.0', port= 5000)
manager = Manager(app)
manager.add_command("runserver", Server(host='0.0.0.0', port=5000))
boostrap = Bootstrap(app)

test = TestThread()


@app.route("/")
def main():
   # For each pin, read the pin state and store it in the pins dictionary:
   test.update()

   # Put the pin dictionary into the template data dictionary:
   templateData = {
      'pins' : test.pins,
      'test_state' : test.state
      }
   # Pass the template data into the template main.html and return it to the user
   return render_template('index.html', **templateData)

# The function below is executed when someone requests a URL with the pin number and action in it:
@app.route("/<changePin>/<action>")
def action(changePin, action):
   test.toggle_pin(changePin,action)

   # For each pin, read the pin state and store it in the pins dictionary:
   test.update()

   # Along with the pin dictionary, put the message into the template data dictionary:
   templateData = {
      'pins' : test.pins,
      'test_state' : test.state

   }

   return render_template('index.html', **templateData)

@app.route("/run")
def run():

   # For each pin, read the pin state and store it in the pins dictionary:
   test.update()

   test.state = True

   if test.running == True:
      test.resume()
   else:
      test.start()

   # Put the pin dictionary into the template data dictionary:
   templateData = {
      'pins' : test.pins,
      'test_state' : test.state
      }
   # Pass the template data into the template main.html and return it to the user
   return render_template('index.html', **templateData)


@app.route("/stop")
def stop():
  # For each pin, read the pin state and store it in the pins dictionary:
   test.update()

   test.state = False
   test.wait()

   # Put the pin dictionary into the template data dictionary:
   templateData = {
      'pins' : test.pins,
      'test_state' : test.state
      }
   # Pass the template data into the template main.html and return it to the user
   return render_template('index.html', **templateData)



if __name__ == "__main__":
   
   manager.run()