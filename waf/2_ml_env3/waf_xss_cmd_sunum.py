import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk
import subprocess
import threading  

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

        # Variable to track the mitmproxy process
        self.mitm_process = None

    def start_mitmproxy(self):
        # Function to start mitmproxy
        ####################################
        mitm_script_path = 'waf_xss_kod_sunum.py'  # Change this to your actual script file
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

    def read_mitmproxy_output(self):
        # Function to read mitmproxy output
        while self.mitm_process.poll() is None:
            line = self.mitm_process.stdout.readline()
            if line:
                # Update the log text in the Tkinter window with HTTP content
                if "request_path_renkli" in line:
                    self.log_text.insert(tk.END, line, "yellow_text")
                else:
                    self.log_text.insert(tk.END, line)
                self.log_text.yview(tk.END)  # Scroll to the end

if __name__ == "__main__":
    root = tk.Tk()
    app = MitmProxyApp(root)

    # Tag configuration to set the background color to yellow
    app.log_text.tag_configure("yellow_text", background="yellow")

    root.mainloop()