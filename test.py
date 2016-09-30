import threading
import RPi.GPIO as GPIO
import time



class TestThread(threading.Thread):
    def __init__(self):
        """
	Initialize self. variables
	Start deckel object to check constantly for lid opening
	"""
	threading.Thread.__init__(self)
	self.setDaemon(True)


	GPIO.setmode(GPIO.BCM)

	# Create a dictionary called pins to store the pin number, name, and pin state:
	self.pins = {
	   23 : {'name' : 'Relay1', 'state' : GPIO.LOW, 'count': 0},
	   24 : {'name' : 'Relay2', 'state' : GPIO.LOW, 'count': 0},
	   25 : {'name' : 'Relay3', 'state' : GPIO.LOW, 'count': 0},

	}
		# Create a flag for test state
	self.state = False

		# Set each pin as an output and make it low:
	for pin in self.pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)


    def update(self):
        # read current statea of GPIO pins and update dictionary
        for pin in self.pins:
            self.pins[pin]['state'] = GPIO.input(pin)

    def toggle_pin(self,changePin, action):

	# Convert the pin from the URL into an integer:
	changePin = int(changePin)
	# Get the device name for the pin being changed:
	deviceName = self.pins[changePin]['name']
	# If the action part of the URL is "on," execute the code indented below:
	if action == "on":
	    # Set the pin high:
  	    GPIO.output(changePin, GPIO.HIGH)
	    # Save the status message to be passed into the template:
	    message = "Turned " + deviceName + " on."

	    #Increment cycle count
	    self.pins[changePin]['count'] += 1

	if action == "off":
	    GPIO.output(changePin, GPIO.LOW)
	    message = "Turned " + deviceName + " off."

    def run(self):

        while True:
            if self.state == True:

                for pin in self.pins:
                    self.toggle_pin(pin, 'on')
                    time.sleep(1)
                    self.toggle_pin(pin, 'off')
                    time.sleep(1)
            else:
                pass


	# def write(self,pathfile,data,initial=False):
	# 	"""pass candy tracking data and datetime to the database"""
	# 	with open(pathfile, 'a') as f:
	# 		writer = csv.writer(f)
	# 		writer.writerow(data)
	# 	if initial:
	# 		self.df = pd.DataFrame(columns = data)

	# def log(self):
	# 	print "Open Count:", self.open_count,
	# 	print "Close Count:", self.close_count
	# 	now = datetime.datetime.now()
    #
	# 	data = [now, self.lid_status, self.open_count, self.close_count, self.time_open, self.average_time_open, self.current_weight, self.current_candies,self.consumed,now.date(), now.year, now.month, now.day, now.hour, now.minute, now.second, now.weekday(), now.isocalendar()[1],now.timetuple().tm_yday,self.openings_today]
	# 	self.write(path+filename,data)
	# 	self.df = self.df.append(pd.DataFrame([data],columns=self.header),ignore_index=True)
	# 	# pg.update_weight_plot(path+filename)
    #
	# def get_weight(self):
	# 	"""
	# 	get weight on each sensor, then sum to find total weight of candy in jar
    #
	# 	Returns
	# 	-------
	# 	float
	# 		mass of candy in grams
	# 	"""
	# 	lst = np.zeros(window)
	# 	for i in range(window):
	# 		lst[i] = get_candy_weight()
	# 		time.sleep(delay)
	# 	average = np.average(lst)
	# 	print lst, average
	# 	while abs(average - lst[window-1]) > tolerance:
	# 		lst = np.delete(lst,0)
	# 		lst = np.append(lst, get_candy_weight())
	# 		average = np.average(lst)
	# 		if (average - lst[window-1]) > tolerance:
	# 			time.sleep(delay)
	# 		print lst, average
	# 		if self.lid_opened_event.is_set():
	# 			print 'breaking'
	# 			break
	# 	return average
    #
	# def plot_data(self):
	# 	simple_header = ['daily_avg_o','daily_avg_c','mtbo','mttl','mttf','mttc','open_today','total']
	# 	simple_data = [daily_avg_o(self.df),daily_avg_c(self.df),mtbo(self.df),mttl(self.df),mttf(self.df),mttc(self.df),self.openings_today,self.df.consumed.sum()]
	# 	simple = pd.DataFrame([simple_data],columns=simple_header)
	# 	simple.to_csv(path+'simple.csv')
    #
	# 	weekday_index = ['open_avg_count','open_avg_percent','consume_avg_count','consume_avg_percent']
	# 	a = open_avg_weekday(self.df)
	# 	b = consume_avg_weekday(self.df)
	# 	weekday_data = [a[0],a[1],b[0],b[1]]
	# 	weekday = pd.DataFrame(weekday_data,index=weekday_index)
	# 	weekday.to_csv(path+'weekday.csv')
    #
	# 	hourly_index = ['consume_avg_count','consume_avg_percent']
	# 	c = consume_avg_hour(self.df)
	# 	hourly_data = [c[0],c[1]]
	# 	hourly = pd.DataFrame(hourly_data,index=hourly_index)
	# 	hourly.to_csv(path+'hourly.csv')
    #
	# 	plotz.daily_consumption_percent(path + 'weekday.csv')
	# 	plotz.daily_consumption_absolute(path + 'weekday.csv')
	# 	plotz.hourly_consumption_percent(path + 'hourly.csv')
	# 	plotz.hourly_consumption_absolute(path + 'hourly.csv')
	# 	plotz.weight_over_time(self.df)
    #
	# def run(self):
	# 	"""
	# 	Main data logging loop
    #
	# 	Loops indefinitely, while waiting for open/close lid events from self.deckel
	# 	When open or close event is triggered, logs data to csv, and updates plots
	# 	"""
	# 	# Example of catching deckel's events
	# 	self.close_count = 0
	# 	self.open_count = 0
	# 	self.average_time_open = 0.0
	# 	self.openings_today = 0
	# 	self.start_time = datetime.datetime.now()
	# 	self.current_weight = self.get_weight()
	# 	self.current_candies = self.current_weight / unit_weight
	# 	candies = self.current_candies
	# 	self.consumed = 0.0
	# 	# Load data from previous csv
	# 	self.header = ["datetime","lid_status","open_count","close_count","time_open","average_time_open","weight","candies","consumed",'date','year','month','day','hour','minute','second','weekday','week','dayofyear','open_today']
	# 	try:
	# 		self.df = pd.read_csv(path + filename)
	# 		if len(self.df)>0:
	# 			last_row = self.df.index[-1]
	# 			self.open_count = self.df['open_count'][last_row]
	# 			self.close_count = self.df['close_count'][last_row]
	# 			self.average_time_open = self.df['average_time_open'][last_row]
	# 			self.openings_today = self.df['open_today'][last_row]
	# 	except IOError:
	# 		self.write(path + filename,self.header,initial=True)
    #
	# 	while True:
	# 		self.lid_opened_event.wait()
	# 		if datetime.datetime.now().day == self.start_time.day:
	# 			self.openings_today += 1
	# 		else:
	# 			self.openings_today = 0
	# 		self.open_count+=1
	# 		self.start_time = datetime.datetime.now()
	# 		self.time_open = 0.0
	# 		self.lid_status = 'OPEN'
	# 		self.log()
    #
	# 		self.lid_closed_event.wait()
	# 		self.close_count+=1
	# 		self.time_open = datetime.datetime.now() - self.start_time
	# 		self.time_open = self.time_open.total_seconds()
	# 		print "Time Open:", self.time_open
	# 		self.average_time_open = get_avg_time_open(self.time_open, self.close_count, self.average_time_open)
	# 		self.lid_status = 'CLOSED'
	# 		self.current_weight = self.get_weight()
	# 		self.current_candies = self.current_weight/unit_weight
	# 		diff = self.current_candies - candies
	# 		self.consumed = diff if diff > -1.0 else np.nan
	# 		candies = self.current_candies
	# 		self.log()
    #
	# 		self.plot_data()
