import speech_recognition as sr
import pyttsx3
import threading
import time
import sys
import os

# Import the main assistant and UI
from voice_assistant import VoiceAssistant
from UI import AssistantFaceUI

class IntegratedAssistant(VoiceAssistant):
    def __init__(self):
        """Initialize the assistant with UI integration"""
        super().__init__()
        self.ui = AssistantFaceUI(self)
        self.ui_thread = None
        
    def speak(self, text):
        """Override speak method to update UI"""
        print(f"{self.name}: {text}")
        # Update UI before speaking
        if hasattr(self, 'ui'):
            self.ui.set_status("Speaking", "speaking")
            self.ui.update_message(text)
        
        # Speak the text
        self.engine.say(text)
        self.engine.runAndWait()
        
        # Return to idle state
        if hasattr(self, 'ui'):
            self.ui.set_status("Idle", "neutral")
    
    def listen(self):
        """Override listen method to update UI"""
        if hasattr(self, 'ui'):
            self.ui.set_status("Listening", "listening")
            self.ui.update_message("Listening...")
            
        with self.mic as source:
            print("Listening...")
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            try:
                # Wait for speech with a timeout
                audio = self.recognizer.listen(source, timeout=5)
            except sr.WaitTimeoutError:
                # No speech detected within timeout period
                if hasattr(self, 'ui'):
                    self.ui.set_status("Idle", "neutral")
                return ""
            
        try:
            if hasattr(self, 'ui'):
                self.ui.set_status("Processing", "processing")
                self.ui.update_message("Processing your command...")
                
            print("Recognizing...")
            query = self.recognizer.recognize_google(audio)
            print(f"{self.user_name}: {query}")
            
            # Update UI with recognized text
            if hasattr(self, 'ui'):
                self.ui.update_message(f"You said: {query}")
                
            return query.lower()
        except sr.UnknownValueError:
            # This occurs when speech was detected but not recognized
            if hasattr(self, 'ui'):
                self.ui.set_status("Idle", "thinking")
                self.ui.update_message("I didn't catch that. Could you try again?")
            return "$$SILENCE$$"  # Special marker for silence/unrecognized speech
        except sr.RequestError:
            if hasattr(self, 'ui'):
                self.ui.set_status("Idle", "neutral")
                self.ui.update_message("Sorry, my speech service is down.")
            self.speak("Sorry, my speech service is down.")
            return "$$ERROR$$"  # Special marker for service errors
    
    def process_command(self, command):
        """Override process_command to update UI state"""
        try:
            # Update UI state
            if hasattr(self, 'ui'):
                self.ui.set_status("Processing", "processing")
            
            # Call the parent method to process the command
            super().process_command(command)
            
        except Exception as e:
            if hasattr(self, 'ui'):
                self.ui.set_status("Idle", "thinking")
                self.ui.update_message(f"Sorry, I encountered an error: {str(e)}")
            self.speak("Sorry, I am not able to process this command.")
            print(f"Error processing command: {str(e)}")
    
    def run_with_ui(self):
        """Run the assistant with UI"""
        # Start UI in main thread
        self.ui_thread = threading.Thread(target=self.run)
        self.ui_thread.daemon = True
        self.ui_thread.start()
        
        # Run UI in main thread
        self.ui.run()
    
    def shutdown(self):
        """Shutdown the assistant and UI"""
        self.is_listening = False
        if self.ui_thread and self.ui_thread.is_alive():
            self.ui_thread.join(timeout=1)
        if hasattr(self, 'ui'):
            self.ui.shutdown()


def main():
    """Main function to run the integrated assistant"""
    print("Starting Megatron Assistant with UI...")
    
    # Parse command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "--setup-autostart":
            from voice_assistant import setup_autostart
            setup_autostart()
            sys.exit(0)
        elif sys.argv[1] == "--service":
            # Run as background service
            assistant = IntegratedAssistant()
            assistant.run_with_ui()
    else:
        # Run normally
        assistant = IntegratedAssistant()
        try:
            assistant.run_with_ui()
        except KeyboardInterrupt:
            assistant.shutdown()
            
            
if __name__ == "__main__":
    main()
