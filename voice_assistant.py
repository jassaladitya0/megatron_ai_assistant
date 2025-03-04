import speech_recognition as sr
import pyttsx3
import webbrowser
import subprocess
import datetime
import os
import random
import pyautogui
import json
import requests
import wikipedia
import time
import re
import threading
from bs4 import BeautifulSoup

class VoiceAssistant:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.mic = sr.Microphone()
        self.engine = pyttsx3.init()
        self.name = "Megatron"
        self.user_name = "User"
        self.is_listening = True
        self.initialize_voice()
        
    def initialize_voice(self):
        """Set up voice properties"""
        voices = self.engine.getProperty('voices')
        # Select a voice - usually index 0 is male, 1 is female
        self.engine.setProperty('voice', voices[0].id)  # Female voice
        self.engine.setProperty('rate', 180)  # Speech rate
        self.engine.setProperty('volume', 1.0)  # Volume (0.0 to 1.0)
        
        
    def speak(self, text):
        """Convert text to speech"""
        print(f"{self.name}: {text}")
        self.engine.say(text)
        self.engine.runAndWait()
        
    def listen(self):
        """Listen for user voice input with timeout"""
        with self.mic as source:
            print("Listening...")
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            try:
                # Wait for speech with a timeout
                audio = self.recognizer.listen(source, timeout=5)
            except sr.WaitTimeoutError:
                # No speech detected within timeout period
                return ""
            
        try:
            print("Recognizing...")
            query = self.recognizer.recognize_google(audio)
            print(f"{self.user_name}: {query}")
            return query.lower()
        except sr.UnknownValueError:
            # This occurs when speech was detected but not recognized
            return "$$SILENCE$$"  # Special marker for silence/unrecognized speech
        except sr.RequestError:
            self.speak("Sorry, my speech service is down.")
            return "$$ERROR$$"  # Special marker for service errors
            
    def greet(self):
        """Greet the user based on time of day"""
        hour = datetime.datetime.now().hour
        
        if 0 <= hour < 12:
            greeting = "Good morning!"
        elif 12 <= hour < 18:
            greeting = "Good afternoon!"
        else:
            greeting = "Good evening!"
            
        self.speak(f"{greeting} I am {self.name}, your virtual assistant created by Megatron team. How can I help you today?")
        
    def open_website(self, site_name):
        """Open specified website"""
        sites = {
            "google": "https://www.google.com",
            "youtube": "https://www.youtube.com",
            "facebook": "https://www.facebook.com",
            "instagram": "https://www.instagram.com",
            "telegram": "https://web.telegram.org",
            "flipkart": "https://www.flipkart.com",
            "amazon": "https://www.amazon.com",
            "whatsapp": "https://web.whatsapp.com",
            "linkedin": "https://www.linkedin.com",
            "github": "https://www.github.com",
            "wikipedia": "https://www.wikipedia.org"
           
                }
        
        if site_name in sites:
            self.speak(f"Opening {site_name}")
            webbrowser.open(sites[site_name])
        else:
            self.speak(f"I don't have {site_name} in my database, but I'll try to open it")
            webbrowser.open(f"https://www.{site_name}.com")
            
    def open_app(self, app_name):
        """Open applications on the device"""
        windows_apps = {
            "chrome": "chrome.exe",
            "edge": "msedge.exe",
            "microsoft edge": "msedge.exe",
            "notepad": "notepad.exe",
            "calculator": "calc.exe",
            "paint": "mspaint.exe",
            "file explorer": "explorer.exe",
            "word": "winword.exe",
            "excel": "excel.exe",
            "powerpoint": "powerpnt.exe"
        }
        
        try:
            if app_name in windows_apps:
                self.speak(f"Opening {app_name}")
                subprocess.Popen(windows_apps[app_name])
            else:
                self.speak(f"Trying to open {app_name}")
                os.system(f"start {app_name}")
        except Exception as e:
            self.speak(f"Sorry, I couldn't open {app_name}. {str(e)}")
            
    def search_google(self, query):
        """Search on Google"""
        self.speak(f"Searching for {query} on Google")
        webbrowser.open(f"https://www.google.com/search?q={query}")
        
    def search_youtube(self, query):
        """Search on YouTube"""
        self.speak(f"Searching for {query} on YouTube")
        webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
        
    def play_song(self, song_name):
        """Play a song on YouTube"""
        self.speak(f"Playing {song_name} on YouTube")
        webbrowser.open(f"https://www.youtube.com/results?search_query={song_name}")
        time.sleep(2)  # Wait for page to load
        pyautogui.press('tab')
        pyautogui.press('enter')  # Click on first video
        
    def get_time(self):
        """Tell the current time"""
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        self.speak(f"The current time is {current_time}")
        
    def get_date(self):
        """Tell the current date"""
        current_date = datetime.datetime.now().strftime("%B %d, %Y")
        self.speak(f"Today is {current_date}")
        
    def set_alarm(self, time_str):
        """Set an alarm"""
        # Simple implementation - in a real app you'd need a background thread
        self.speak(f"Setting alarm for {time_str}")
        # Extract hour and minute from the time string
        match = re.search(r'(\d+):*(\d*)\s*(am|pm)*', time_str.lower())
        if match:
            hour = int(match.group(1))
            minute = int(match.group(2)) if match.group(2) else 0
            meridiem = match.group(3)
            
            if meridiem == "pm" and hour < 12:
                hour += 12
            elif meridiem == "am" and hour == 12:
                hour = 0
                
            self.speak(f"Alarm set for {hour}:{minute:02d}")
            # In a real app, you would set up a timer here
        else:
            self.speak("Sorry, I couldn't understand the time format")
        
    def set_reminder(self, reminder_text):
        """Set a reminder"""
        # Simple implementation - in a real app you'd need persistent storage
        self.speak(f"I'll remind you to {reminder_text}")
        # In a real app, you would save this reminder to a file or database
        
    def take_screenshot(self):
        """Take a screenshot"""
        screenshot_path = os.path.join(os.path.expanduser("~"), "Pictures", f"screenshot_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
        self.speak("Taking screenshot")
        pyautogui.screenshot(screenshot_path)
        self.speak("Screenshot saved to Pictures folder")
        
    def adjust_volume(self, up=True):
        """Adjust system volume"""
        for _ in range(5):  # Adjust by pressing key 5 times
            if up:
                pyautogui.press('volumeup')
            else:
                pyautogui.press('volumedown')
        
        status = "up" if up else "down"
        self.speak(f"Volume turned {status}")
        
    def mute_unmute(self):
        """Mute or unmute the system"""
        pyautogui.press('volumemute')
        self.speak("Volume toggled")
        
    def adjust_brightness(self, up=True):
        """Adjust screen brightness - Note: This is system specific and may not work on all computers"""
        if up:
            self.speak("Increasing brightness")
            # This is a Windows-specific approach, might need different implementation for other OS
            try:
                os.system("powershell (Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,10)")
            except:
                self.speak("Sorry, I couldn't adjust the brightness")
        else:
            self.speak("Decreasing brightness")
            try:
                os.system("powershell (Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,-10)")
            except:
                self.speak("Sorry, I couldn't adjust the brightness")
                
    def search_wikipedia(self, query):
        """Search information on Wikipedia"""
        self.speak(f"Searching Wikipedia for {query}")
        try:
            results = wikipedia.summary(query, sentences=2)
            self.speak("According to Wikipedia")
            self.speak(results)
        except Exception as e:
            self.speak("Sorry, I couldn't find that on Wikipedia")
            self.search_google(query)
            
    def get_recipe(self, food_name):
        """Get recipe for a specific food"""
        self.speak(f"Looking for recipes for {food_name}")
        webbrowser.open(f"https://www.google.com/search?q=recipe+for+{food_name}")
        
    def search_movies(self, movie_name, platform="google"):
        """Search for movies on specified platform"""
        if platform.lower() == "youtube":
            self.speak(f"Searching for {movie_name} on YouTube")
            webbrowser.open(f"https://www.youtube.com/results?search_query={movie_name}+movie")
        else:
            self.speak(f"Searching for {movie_name} movie")
            webbrowser.open(f"https://www.google.com/search?q={movie_name}+movie")
            
    def download_app(self, app_name):
        """Open Microsoft Store to download an app"""
        self.speak(f"Opening Microsoft Store to download {app_name}")
        os.system(f"start ms-windows-store://search/?query={app_name}")
        
    def scroll_screen(self, direction="down"):
        """Scroll the screen up or down"""
        if direction.lower() == "up":
            pyautogui.scroll(300)  # Positive value scrolls up
            self.speak("Scrolling up")
        else:
            pyautogui.scroll(-300)  # Negative value scrolls down
            self.speak("Scrolling down")
            
    def write_text(self, text):
        """Type text on the screen"""
        self.speak(f"Writing: {text}")
        pyautogui.write(text)
        
    def answer_question(self, question):
        """Answer questions by searching Google and extracting information"""
        self.speak("Let me find that information for you")
        
        try:
            # Search Google
            search_url = f"https://www.google.com/search?q={question}"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            
            response = requests.get(search_url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Try to get a featured snippet
            featured_snippet = soup.find('div', class_='kp-header')
            if featured_snippet:
                answer = featured_snippet.get_text()
                self.speak(answer)
                return
                
            # Try to extract from knowledge panel
            knowledge_panel = soup.find('div', class_='kno-rdesc')
            if knowledge_panel:
                answer = knowledge_panel.get_text()
                self.speak(answer)
                return
                
            # Fall back to Wikipedia
            try:
                results = wikipedia.summary(question, sentences=2)
                self.speak("According to Wikipedia")
                self.speak(results)
                return
            except:
                pass
                
            # If all else fails
            self.speak("I found some results online, opening Google for you.")
            webbrowser.open(search_url)
            
        except Exception as e:
            self.speak(f"Sorry, I couldn't find an answer. Opening a web search for you.")
            webbrowser.open(f"https://www.google.com/search?q={question}")
    
    def process_command(self, command):
        """Process user commands"""
        
        try:
            # Greeting commands
            if "hello" in command or "hi" in command:
                responses = ["Hello there!", "Hi! How can I help?", "Hey! Nice to hear from you!"]
                self.speak(random.choice(responses))
                return
                
            # Assistant identity
            elif "who are you" in command:
                self.speak(f"I am {self.name}, a virtual AI assistant created by Megatron team to help you with various tasks.")
                return
                
            elif "who made you" in command:
                self.speak("I was made by the Megatron team.")
                return
                
            elif "how are you" in command:
                responses = ["I'm doing well, thank you for asking!", "I'm fine, how are you?", "All systems operational and ready to assist you!"]
                self.speak(random.choice(responses))
                return
                
            # Open website commands
            elif "open google" in command:
                self.open_website("google")
            elif "open youtube" in command:
                self.open_website("youtube")
            elif "open facebook" in command:
                self.open_website("facebook")
            elif "open instagram" in command:
                self.open_website("instagram")
            elif "open telegram" in command:
                self.open_website("telegram")
            elif "open flipkart" in command:
                self.open_website("flipkart")
            elif "open amazon" in command:
                self.open_website("amazon")
            elif "open whatsapp" in command:
                self.open_website("whatsapp")
            elif "open linkedin" in command:
                self.open_website("linkedin")
            elif "open github" in command:
                self.open_website("github")
                
            # Open application commands
            elif "open chrome" in command:
                self.open_app("chrome")
            elif "open edge" in command or "open microsoft edge" in command:
                self.open_app("microsoft edge")
            elif "open notepad" in command:
                self.open_app("notepad")
            elif "open calculator" in command:
                self.open_app("calculator")
            elif "open" in command and "app" in command:
                app_name = command.replace("open", "").replace("app", "").strip()
                self.open_app(app_name)
                
            # Search commands
            elif "search" in command and "google" in command:
                query = command.replace("search", "").replace("on google", "").replace("google", "").strip()
                self.search_google(query)
            elif "search" in command and "youtube" in command:
                query = command.replace("search", "").replace("on youtube", "").replace("youtube", "").strip()
                self.search_youtube(query)
            elif "search" in command and "wikipedia" in command:
                query = command.replace("search", "").replace("on wikipedia", "").replace("wikipedia", "").strip()
                self.search_wikipedia(query)
            elif "play song" in command or "play music" in command:
                song_name = command.replace("play song", "").replace("play music", "").strip()
                self.play_song(song_name)
                
            # System control commands
            elif "volume up" in command:
                self.adjust_volume(up=True)
            elif "volume down" in command:
                self.adjust_volume(up=False)
            elif "mute" in command:
                self.mute_unmute()
            elif "unmute" in command:
                self.mute_unmute()
            elif "brightness up" in command:
                self.adjust_brightness(up=True)
            elif "brightness down" in command:
                self.adjust_brightness(up=False)
            elif "take screenshot" in command:
                self.take_screenshot()
            elif "scroll down" in command:
                self.scroll_screen("down")
            elif "scroll up" in command:
                self.scroll_screen("up")
                
            # Time and date commands
            elif "what time" in command or "current time" in command:
                self.get_time()
            elif "what date" in command or "current date" in command or "today's date" in command:
                self.get_date()
            elif "set alarm" in command:
                time_str = command.replace("set alarm", "").replace("for", "").replace("at", "").strip()
                self.set_alarm(time_str)
            elif "set reminder" in command or "remind me" in command:
                reminder_text = command.replace("set reminder", "").replace("remind me", "").replace("to", "", 1).strip()
                self.set_reminder(reminder_text)
                
            # Recipe commands
            elif "recipe" in command:
                food_name = command.replace("recipe", "").replace("of", "").replace("for", "").strip()
                self.get_recipe(food_name)
                
            # Movie search commands
            elif "search movie" in command:
                if "on youtube" in command:
                    movie_name = command.replace("search movie", "").replace("on youtube", "").strip()
                    self.search_movies(movie_name, "youtube")
                else:
                    movie_name = command.replace("search movie", "").replace("on chrome", "").strip()
                    self.search_movies(movie_name)
                    
            # App download commands
            elif "download app" in command:
                app_name = command.replace("download app", "").replace("from microsoft store", "").strip()
                self.download_app(app_name)
                
            # Text writing commands
            elif "write" in command and "text" in command:
                text = command.replace("write", "").replace("text", "").strip()
                self.write_text(text)
                
            # General question answering
            else:
                self.answer_question(command)
        except Exception as e:
            self.speak("Sorry, I am not able to process this command.")
            print(f"Error processing command: {str(e)}")
    
    def run(self):
        """Main method to run the assistant"""
        self.greet()
        
        while self.is_listening:
            command = self.listen()
            
            if command == "$$SILENCE$$":
                # User was silent or speech wasn't recognized
                continue
            elif command == "$$ERROR$$":
                # Error with speech recognition service
                continue
            elif command == "":
                # Timeout occurred, just continue listening
                continue
            elif "exit" in command or "quit" in command or "goodbye" in command or "bye" in command:
                self.speak("Goodbye! Have a nice day!")
                self.is_listening = False
            else:
                self.process_command(command)
                
    def run_background(self):
        """Run the assistant in a background thread"""
        thread = threading.Thread(target=self.run)
        thread.daemon = True  # Make thread a daemon so it exits when main program exits
        thread.start()
        return thread
    
    
# Create a class for the background service
class AssistantService:
    def __init__(self):
        self.assistant = VoiceAssistant()
        self.thread = None
        
    def start(self):
        """Start the assistant as a background service"""
        print("Starting Megatron Assistant in background mode...")
        self.thread = self.assistant.run_background()
        
    def stop(self):
        """Stop the assistant service"""
        if self.thread and self.thread.is_alive():
            self.assistant.is_listening = False
            self.thread.join(timeout=1)
            print("Megatron Assistant has been stopped.")
            
    def restart(self):
        """Restart the assistant service"""
        self.stop()
        self.assistant = VoiceAssistant()
        self.start()


# Add code to register as a Windows service or auto-start application
def setup_autostart():
    """Set up the assistant to start automatically with Windows"""
    try:
        # Get the path to the current script
        script_path = os.path.abspath(__file__)
        
        # Create a shortcut in the startup folder
        startup_folder = os.path.join(os.environ["APPDATA"], 
                                     r"Microsoft\Windows\Start Menu\Programs\Startup")
        shortcut_path = os.path.join(startup_folder, "MegatronAssistant.lnk")
        
        # Windows-specific approach using PowerShell
        cmd = f"""
        $WshShell = New-Object -ComObject WScript.Shell
        $Shortcut = $WshShell.CreateShortcut("{shortcut_path}")
        $Shortcut.TargetPath = "pythonw.exe"
        $Shortcut.Arguments = "{script_path}"
        $Shortcut.WorkingDirectory = "{os.path.dirname(script_path)}"
        $Shortcut.Description = "Megatron AI Assistant"
        $Shortcut.Save()
        """
        
        # Execute the PowerShell command
        subprocess.run(["powershell", "-Command", cmd], check=True)
        
        print(f"Autostart configured. The assistant will start with Windows.")
        return True
    except Exception as e:
        print(f"Failed to set up autostart: {str(e)}")
        return False


if __name__ == "__main__":
    # Check if this should run as a background service
    import sys
    
    # If the script is run with --setup-autostart argument
    if len(sys.argv) > 1 and sys.argv[1] == "--setup-autostart":
        setup_autostart()
        sys.exit(0)
    
    # If the script is run with --service argument or called by pythonw.exe
    if len(sys.argv) > 1 and sys.argv[1] == "--service" or "pythonw" in sys.executable:
        # Run as background service
        service = AssistantService()
        service.start()
        
        # Keep the main thread alive
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            service.stop()
    else:
        # Run normally in console
        print("Starting Megatron Assistant...")
        assistant = VoiceAssistant()
        assistant.run()