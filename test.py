from pynput import keyboard
import threading

class KeyHandler:
    def __init__(self):
        self.default_function = self.default_function
        self.key_functions = {
            '1': self.default_function,
            '2': self.function_2,
            '3': self.function_3,
            # Add more key-function mappings here
        }
        self.current_function = self.default_function

    def on_press(self, key):
        try:
            if key.char in self.key_functions:
                self.current_function = self.key_functions[key.char]
                print(f"Running function for key '{key.char}'")
                self.current_function()  # Execute the corresponding function
        except AttributeError:
            pass

    def default_function(self):
        print("Default function")

    def function_2(self):
        print("Function 2")

    def function_3(self):
        print("Function 3")

    def run(self):
        listener = keyboard.Listener(on_press=self.on_press)
        listener.start()

        while True:
            # You can add your own logic here to resume the flow of another program

            # Sleep for a short duration to avoid excessive CPU usage
            # Adjust the sleep duration as needed
            threading.Event().wait(0.1)

# Create an instance of the KeyHandler class
key_handler = KeyHandler()

# Create a thread for running the key handler
key_handler_thread = threading.Thread(target=key_handler.run)
key_handler_thread.daemon = True  # Set the thread as a daemon to allow the main program to exit

# Start the key handler thread
key_handler_thread.start()


