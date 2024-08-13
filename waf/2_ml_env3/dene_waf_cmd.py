import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk
import subprocess
import threading  
import pandas as pd
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from sklearn.metrics import precision_score, recall_score, f1_score,accuracy_score
import csv
class MitmProxyApp:
	def __init__(self, master):
		self.master = master
		self.master.title("MitmProxy App")

		# Create a main frame to hold the widgets
		self.main_frame = tk.Frame(master)
		self.main_frame.pack(fill="both", expand=True)

		# Scrollable text widget for displaying logs
		self.log_text = scrolledtext.ScrolledText(self.main_frame, wrap=tk.WORD, width=80, height=20)
		self.log_text.pack(fill="both", expand=True, pady=10)

		# Create a button frame to hold the buttons
		self.button_frame = tk.Frame(self.main_frame)
		self.button_frame.pack(fill="x", pady=10)

		# Start button to run mitmproxy script
		self.start_button = ttk.Button(self.button_frame, text="Start MitmProxy", command=self.start_mitmproxy)
		self.start_button.pack(side=tk.LEFT, padx=5)

		# Stop button to stop mitmproxy process
		self.stop_button = ttk.Button(self.button_frame, text="Stop MitmProxy", command=self.stop_mitmproxy, state=tk.DISABLED)
		self.stop_button.pack(side=tk.LEFT, padx=5)

		# Text box to display blocked requests
		self.blocked_text = tk.Text(self.button_frame, width=40, height=5)
		self.blocked_text.pack(side=tk.LEFT, padx=5)
		self.blocked_text.tag_configure("yellow_text", background="yellow")

		# Variable to track the mitmproxy process
		self.mitm_process = None

		# Variables to track the number of total and blocked requests
		self.total_requests = 0
		self.blocked_requests = 0
		self.good_requests = 0

	def start_mitmproxy(self):
		# Function to start mitmproxy
		mitm_script_path = 'dene_waf_kod.py'  # Change this to your actual script file
		command = ['mitmdump', '-s', mitm_script_path]

		try:
			# Run mitmdump command and capture the process
			self.mitm_process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

			# Disable the start button and enable the stop button
			self.start_button["state"] = tk.DISABLED
			self.stop_button["state"] = tk.NORMAL

			# Read the output in a separate thread
			self.read_output_thread = threading.Thread(target=self.read_mitmproxy_output)
			self.read_output_thread.start()
		except subprocess.CalledProcessError as e:
			# Handle any errors that occur
			self.log_text.insert(tk.END, f"Error running mitmproxy: {e}\n")

	def stop_mitmproxy(self):
		# Function to stop mitmproxy process
		if self.mitm_process and self.mitm_process.poll() is None:
			self.mitm_process.terminate()  # Terminate the mitmproxy process

		# Enable the start button and disable the stop button
		self.start_button["state"] = tk.NORMAL
		self.stop_button["state"] = tk.DISABLED

		# Display the total and blocked request counts
		self.log_text.insert(tk.END, f"Total requests: {self.total_requests}\n")
		self.log_text.insert(tk.END, f"Blocked requests: {self.blocked_requests}\n")
		self.log_text.insert(tk.END, f"Total good requests: {self.good_requests}\n")

		# Run the accuracy calculation code
		df = pd.read_csv('all_bad_good_0_1_real.csv')
		y_pred = df['pred']
		y_test = df['real']
		accuracy = accuracy_score(y_test, y_pred)

		# Create a new TextBox to display the accuracy value
		self.accuracy_text = tk.Text(self.button_frame, width=20, height=1)
		self.accuracy_text.pack(side=tk.LEFT, padx=5)
		self.accuracy_text.insert(tk.END, f"Accuracy: {accuracy:.3f}")

 

	'''def read_mitmproxy_output(self):
		# Function to read mitmproxy output
		while self.mitm_process.poll() is None:
			line = self.mitm_process.stdout.readline()
			if line:
				# Update the log text in the Tkinter window with HTTP content
				if "request_path_renkli" in line:
					self.blocked_text.insert(tk.END, line)
					self.blocked_requests += 1
				else:
					self.log_text.insert(tk.END, line)
				self.log_text.yview(tk.END)	 # Scroll to the end
				self.total_requests += 1'''				
	'''def read_mitmproxy_output(self):
		# Function to read mitmproxy output
		while self.mitm_process.poll() is None:
			line = self.mitm_process.stdout.readline()
			if line:
				# Update the log text in the Tkinter window with HTTP content
				if "request_path_renkli" in line:
					self.blocked_text.insert(tk.END, line, "yellow_text")
					self.blocked_requests += 1
				else:
					self.log_text.insert(tk.END, line)
				self.log_text.yview(tk.END)	 # Scroll to the end
				self.total_requests += 1'''
	
	'''def read_mitmproxy_output(self):
		# Function to read mitmproxy output
		while self.mitm_process.poll() is None:
			line = self.mitm_process.stdout.readline()
			if line:
				# Update the log text in the Tkinter window with HTTP content
				if "request_path_renkli" in line:
					self.log_text.insert(tk.END, line, "yellow_text")
					self.blocked_requests += 1
				else:
					self.log_text.insert(tk.END, line)
				self.log_text.yview(tk.END)	 # Scroll to the end
				self.total_requests += 1'''
	
	def read_mitmproxy_output(self):
		# Function to read mitmproxy output
		while self.mitm_process.poll() is None:
			line = self.mitm_process.stdout.readline()
			if line:
				# Update the log text in the Tkinter window with HTTP content
				if "request_path_renkli" in line:
					self.log_text.insert(tk.END, line, "yellow_text")
					self.blocked_text.insert(tk.END, line)	# Add to blocked_text widget
					self.blocked_requests += 1
				else:
					self.log_text.insert(tk.END, line)
					self.good_requests += 1
				self.log_text.yview(tk.END)	 # Scroll to the end
				self.total_requests += 1
				
	'''def read_mitmproxy_output(self):
		# Function to read mitmproxy output
		while self.mitm_process.poll() is None:
			line = self.mitm_process.stdout.readline()
			if line:
				# Update the log text in the Tkinter window with HTTP content
				if "request_path_renkli" in line:
					self.log_text.insert(tk.END, line, "yellow_text")
					self.blocked_text.insert(tk.END, line)	# Add to blocked_text widget
					if "demo.testfire.net" in line:
						self.blocked_requests += 1
				else:
					self.log_text.insert(tk.END, line)
				self.log_text.yview(tk.END)	 # Scroll to the end
				if "demo.testfire.net" in line:
					self.total_requests += 1'''
if __name__ == "__main__":
	root = tk.Tk()
	app = MitmProxyApp(root)

	# Tag configuration to set the background color to yellow
	app.log_text.tag_configure("yellow_text", background="yellow")

	root.mainloop()