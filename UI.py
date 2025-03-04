import tkinter as tk
from tkinter import ttk, PhotoImage
import threading
import time
import math
import random
import sys
import os

class AssistantFaceUI:
    def __init__(self, assistant=None):
        """Initialize the UI for the voice assistant with a face-like interface"""
        self.assistant = assistant
        self.root = tk.Tk()
        self.root.title("Megatron Assistant")
        self.root.geometry("500x600")
        self.root.configure(bg="#1E1E2E")
        self.root.resizable(False, False)

        try:
            self.root.iconbitmap("assistant_icon.ico")
        except:
            pass

        self.is_speaking = False
        self.is_listening = False
        self.current_emotion = "neutral"
        self.message_text = ""
        self.running = True

        self.setup_ui()
        self.animation_thread = threading.Thread(target=self.animate_ui)
        self.animation_thread.daemon = True
        self.animation_thread.start()

    def setup_ui(self):
        """Configure all UI elements"""
        main_frame = tk.Frame(self.root, bg="#1E1E2E")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Title
        title_label = tk.Label(main_frame, text="MEGATRON", font=("Arial", 24, "bold"), fg="#BB86FC", bg="#1E1E2E")
        title_label.pack(pady=(0, 10))

        # Face canvas with rings and HUD
        self.face_canvas = tk.Canvas(main_frame, width=300, height=300, bg="#121212", highlightthickness=0)
        self.face_canvas.pack(pady=10)

        # Rotating ring dots
        self.ring_dots1 = [self.face_canvas.create_oval(0, 0, 0, 0, fill="#03DAC6") for _ in range(12)]
        self.ring_dots2 = [self.face_canvas.create_oval(0, 0, 0, 0, fill="#BB86FC") for _ in range(16)]

        # HUD elements
        self.face_canvas.create_text(10, 10, text="SYS//MEGATRON:ACTIVE", anchor="nw", fill="#03DAC6", font=("Arial", 8), tags="hud")
        self.face_canvas.create_text(290, 10, text="CONN:SECURE", anchor="ne", fill="#03DAC6", font=("Arial", 8), tags="hud")
        self.face_canvas.create_text(10, 290, text="PING: 12ms", anchor="sw", fill="#03DAC6", font=("Arial", 8), tags="hud")
        self.hud_time = self.face_canvas.create_text(290, 290, text="TIME: 00:00:00", anchor="se", fill="#03DAC6", font=("Arial", 8))

        self.draw_face("neutral")

        # Equalizer canvas
        self.equalizer_canvas = tk.Canvas(main_frame, width=300, height=50, bg="#121212", highlightthickness=0)
        self.equalizer_canvas.pack(pady=5)
        self.equalizer_bars = []
        num_bars = 10
        bar_width = 20
        gap = 5
        total_width = num_bars * (bar_width + gap) - gap
        start_x = (300 - total_width) / 2
        for i in range(num_bars):
            x1 = start_x + i * (bar_width + gap)
            bar = self.equalizer_canvas.create_rectangle(x1, 49, x1 + bar_width, 50, fill="#03DAC6")
            self.equalizer_bars.append(bar)

        # Status frame
        status_frame = tk.Frame(main_frame, bg="#1E1E2E")
        status_frame.pack(fill=tk.X, pady=10)
        self.status_label = tk.Label(status_frame, text="Idle", font=("Arial", 14), fg="#03DAC6", bg="#1E1E2E")
        self.status_label.pack(side=tk.LEFT, padx=5)
        self.status_indicator = tk.Canvas(status_frame, width=20, height=20, bg="#1E1E2E", highlightthickness=0)
        self.status_indicator.pack(side=tk.LEFT)
        self.status_dot = self.status_indicator.create_oval(5, 5, 15, 15, fill="#808080")

        # Message display
        self.message_display = tk.Text(main_frame, height=5, width=40, font=("Arial", 10), bg="#292936", fg="#FFFFFF", wrap=tk.WORD, state=tk.DISABLED)
        self.message_display.pack(pady=10, fill=tk.X)

        # Control buttons
        control_frame = tk.Frame(main_frame, bg="#1E1E2E")
        control_frame.pack(fill=tk.X, pady=10)
        self.mic_button = tk.Button(control_frame, text="🎤", font=("Arial", 16), bg="#BB86FC", fg="#000000", activebackground="#9A67EA", command=self.toggle_listening)
        self.mic_button.pack(side=tk.LEFT, padx=10)
        self.stop_button = tk.Button(control_frame, text="◼", font=("Arial", 16), bg="#CF6679", fg="#000000", activebackground="#B1475E", command=self.stop_assistant)
        self.stop_button.pack(side=tk.LEFT, padx=10)
        self.settings_button = tk.Button(control_frame, text="⚙", font=("Arial", 16), bg="#03DAC6", fg="#000000", activebackground="#00A896", command=self.open_settings)
        self.settings_button.pack(side=tk.RIGHT, padx=10)

    def draw_face(self, emotion="neutral"):
        """Draw the face with specified emotion"""
        self.face_canvas.delete("face")
        self.face_canvas.create_oval(50, 50, 250, 250, outline="#03DAC6", width=2, fill="#292936", tags="face")

        if emotion == "neutral":
            self.face_canvas.create_oval(100, 110, 130, 140, fill="#03DAC6", tags="face")
            self.face_canvas.create_oval(170, 110, 200, 140, fill="#03DAC6", tags="face")
            self.face_canvas.create_line(110, 180, 190, 180, fill="#03DAC6", width=3, tags="face")
        elif emotion == "happy":
            self.face_canvas.create_oval(100, 110, 130, 140, fill="#03DAC6", tags="face")
            self.face_canvas.create_oval(170, 110, 200, 140, fill="#03DAC6", tags="face")
            self.face_canvas.create_arc(90, 140, 210, 210, start=0, extent=-180, outline="#03DAC6", width=3, style="arc", tags="face")
        elif emotion == "thinking":
            self.face_canvas.create_line(95, 125, 135, 125, fill="#03DAC6", width=3, tags="face")
            self.face_canvas.create_line(165, 125, 205, 125, fill="#03DAC6", width=3, tags="face")
            self.face_canvas.create_arc(90, 150, 210, 220, start=30, extent=120, outline="#03DAC6", width=3, style="arc", tags="face")
        elif emotion == "listening":
            self.face_canvas.create_oval(95, 105, 135, 145, fill="#03DAC6", tags="face")
            self.face_canvas.create_oval(165, 105, 205, 145, fill="#03DAC6", tags="face")
            self.face_canvas.create_oval(130, 175, 170, 195, fill="#292936", outline="#03DAC6", width=2, tags="face")
        elif emotion == "speaking":
            self.face_canvas.create_oval(100, 110, 130, 140, fill="#03DAC6", tags="face")
            self.face_canvas.create_oval(170, 110, 200, 140, fill="#03DAC6", tags="face")
            mouth_height = random.randint(5, 20)
            self.face_canvas.create_oval(120, 180 - mouth_height // 2, 180, 180 + mouth_height // 2, fill="#292936", outline="#03DAC6", width=2, tags="face")
        elif emotion == "processing":
            self.face_canvas.create_oval(95, 105, 135, 145, fill="#292936", outline="#03DAC6", width=2, tags="face")
            self.face_canvas.create_oval(165, 105, 205, 145, fill="#292936", outline="#03DAC6", width=2, tags="face")
            angle = time.time() * 3
            pupil_x_offset = math.cos(angle) * 10
            pupil_y_offset = math.sin(angle) * 10
            self.face_canvas.create_oval(115 + pupil_x_offset - 5, 125 + pupil_y_offset - 5, 115 + pupil_x_offset + 5, 125 + pupil_y_offset + 5, fill="#03DAC6", tags="face")
            self.face_canvas.create_oval(185 + pupil_x_offset - 5, 125 + pupil_y_offset - 5, 185 + pupil_x_offset + 5, 125 + pupil_y_offset + 5, fill="#03DAC6", tags="face")
            self.face_canvas.create_line(120, 180, 180, 180, fill="#03DAC6", width=2, tags="face")

        self.current_emotion = emotion

    def update_equalizer(self):
        """Animate equalizer bars when speaking"""
        if self.is_speaking:
            for bar in self.equalizer_bars:
                height = random.randint(10, 50)
                x1, _, x2, _ = self.equalizer_canvas.coords(bar)
                self.equalizer_canvas.coords(bar, x1, 50 - height, x2, 50)
        else:
            for bar in self.equalizer_bars:
                x1, _, x2, _ = self.equalizer_canvas.coords(bar)
                self.equalizer_canvas.coords(bar, x1, 49, x2, 50)

    def animate_ui(self):
        """Handle all UI animations"""
        pulse_size = 0
        pulse_direction = 1
        blink_counter = 0

        while self.running:
            # Status indicator animation
            if self.is_listening:
                self.status_indicator.itemconfig(self.status_dot, fill="#00FF00")
                pulse_size += pulse_direction * 0.1
                if pulse_size > 1 or pulse_size < 0:
                    pulse_direction *= -1
                self.status_indicator.coords(self.status_dot, 5 - pulse_size * 2, 5 - pulse_size * 2, 15 + pulse_size * 2, 15 + pulse_size * 2)
            elif self.is_speaking:
                self.status_indicator.itemconfig(self.status_dot, fill="#03DAC6")
                self.status_indicator.coords(self.status_dot, 5, 5, 15, 15)
                self.draw_face("speaking")
            else:
                self.status_indicator.itemconfig(self.status_dot, fill="#808080")
                self.status_indicator.coords(self.status_dot, 5, 5, 15, 15)

            # Face blinking
            if self.current_emotion == "neutral":
                blink_counter += 1
                if blink_counter >= 50:
                    self.face_canvas.delete("face")
                    self.face_canvas.create_oval(50, 50, 250, 250, outline="#03DAC6", width=2, fill="#292936", tags="face")
                    self.face_canvas.create_line(100, 125, 130, 125, fill="#03DAC6", width=3, tags="face")
                    self.face_canvas.create_line(170, 125, 200, 125, fill="#03DAC6", width=3, tags="face")
                    self.face_canvas.create_line(110, 180, 190, 180, fill="#03DAC6", width=3, tags="face")
                    time.sleep(0.1)
                    self.draw_face("neutral")
                    blink_counter = 0

            # Processing animation
            if self.current_emotion == "processing":
                self.draw_face("processing")

            # Ring animation
            center_x, center_y = 150, 150
            for i, dot in enumerate(self.ring_dots1):
                angle = (time.time() * 2 + i * (360 / 12)) % 360
                x = center_x + 120 * math.cos(math.radians(angle))
                y = center_y + 120 * math.sin(math.radians(angle))
                self.face_canvas.coords(dot, x - 3, y - 3, x + 3, y + 3)
            for i, dot in enumerate(self.ring_dots2):
                angle = (time.time() * -1.5 + i * (360 / 16)) % 360
                x = center_x + 140 * math.cos(math.radians(angle))
                y = center_y + 140 * math.sin(math.radians(angle))
                self.face_canvas.coords(dot, x - 2, y - 2, x + 2, y + 2)

            # Equalizer and HUD updates
            self.update_equalizer()
            current_time = time.strftime("%H:%M:%S")
            self.face_canvas.itemconfig(self.hud_time, text=f"TIME: {current_time}")

            time.sleep(0.1)

    def set_status(self, status, emotion=None):
        """Update status and face emotion"""
        self.status_label.config(text=status)
        if emotion:
            self.draw_face(emotion)
        if status == "Listening":
            self.is_listening = True
            self.is_speaking = False
        elif status == "Speaking":
            self.is_listening = False
            self.is_speaking = True
        elif status == "Processing":
            self.is_listening = False
            self.is_speaking = False
            self.draw_face("processing")
        else:
            self.is_listening = False
            self.is_speaking = False

    def update_message(self, message):
        """Update message display"""
        self.message_text = message
        self.message_display.config(state=tk.NORMAL)
        self.message_display.delete(1.0, tk.END)
        self.message_display.insert(tk.END, message)
        self.message_display.config(state=tk.DISABLED)

    def toggle_listening(self):
        """Toggle listening state"""
        if self.is_listening:
            self.set_status("Idle", "neutral")
            if self.assistant:
                self.assistant.is_listening = False
        else:
            self.set_status("Listening", "listening")
            if self.assistant:
                self.assistant.is_listening = True

    def stop_assistant(self):
        """Stop the assistant"""
        if self.assistant:
            self.assistant.is_listening = False
        self.update_message("Assistant stopped")
        self.set_status("Stopped", "neutral")

    def open_settings(self):
        """Open settings window"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Megatron Settings")
        settings_window.geometry("350x400")
        settings_window.configure(bg="#1E1E2E")
        settings_window.resizable(False, False)

        settings_frame = tk.Frame(settings_window, bg="#1E1E2E")
        settings_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        tk.Label(settings_frame, text="Settings", font=("Arial", 18, "bold"), fg="#BB86FC", bg="#1E1E2E").pack(pady=(0, 20))

        # Voice settings
        voice_frame = tk.LabelFrame(settings_frame, text="Voice Settings", fg="#FFFFFF", bg="#292936")
        voice_frame.pack(fill=tk.X, pady=10, padx=5)
        tk.Label(voice_frame, text="Voice:", fg="#FFFFFF", bg="#292936").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        voice_var = tk.StringVar(value="Female")
        ttk.Combobox(voice_frame, textvariable=voice_var, values=["Male", "Female"], state="readonly").grid(row=0, column=1, padx=10, pady=10, sticky="e")
        tk.Label(voice_frame, text="Speech Rate:", fg="#FFFFFF", bg="#292936").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        speed_var = tk.IntVar(value=180)
        ttk.Scale(voice_frame, from_=100, to=300, variable=speed_var, orient=tk.HORIZONTAL).grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        # Appearance settings
        appearance_frame = tk.LabelFrame(settings_frame, text="Appearance", fg="#FFFFFF", bg="#292936")
        appearance_frame.pack(fill=tk.X, pady=10, padx=5)
        tk.Label(appearance_frame, text="Theme:", fg="#FFFFFF", bg="#292936").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        theme_var = tk.StringVar(value="Dark")
        ttk.Combobox(appearance_frame, textvariable=theme_var, values=["Dark", "Light", "System"], state="readonly").grid(row=0, column=1, padx=10, pady=10, sticky="e")
        tk.Label(appearance_frame, text="Position:", fg="#FFFFFF", bg="#292936").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        position_var = tk.StringVar(value="Center")
        ttk.Combobox(appearance_frame, textvariable=position_var, values=["Center", "Top Right", "Top Left", "Bottom Right", "Bottom Left"], state="readonly").grid(row=1, column=1, padx=10, pady=10, sticky="e")

        # Behavior settings
        behavior_frame = tk.LabelFrame(settings_frame, text="Behavior", fg="#FFFFFF", bg="#292936")
        behavior_frame.pack(fill=tk.X, pady=10, padx=5)
        startup_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(behavior_frame, text="Start with Windows", variable=startup_var).grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky="w")
        ontop_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(behavior_frame, text="Always on top", variable=ontop_var).grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="w")

        tk.Button(settings_frame, text="Save Settings", bg="#BB86FC", fg="#000000", activebackground="#9A67EA", 
                  command=lambda: self.save_settings(voice_var.get(), speed_var.get(), theme_var.get(), position_var.get(), startup_var.get(), ontop_var.get(), settings_window)).pack(pady=20)

    def save_settings(self, voice, speed, theme, position, startup, ontop, window):
        """Apply and save settings"""
        if self.assistant:
            voices = self.assistant.engine.getProperty('voices')
            self.assistant.engine.setProperty('voice', voices[0].id if voice == "Male" else voices[1].id)
            self.assistant.engine.setProperty('rate', speed)

        if theme == "Light":
            self.root.configure(bg="#F5F5F5")

        if position != "Center":
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            window_width, window_height = 500, 600
            if position == "Top Right":
                self.root.geometry(f"{window_width}x{window_height}+{screen_width - window_width - 10}+10")
            elif position == "Top Left":
                self.root.geometry(f"{window_width}x{window_height}+10+10")
            elif position == "Bottom Right":
                self.root.geometry(f"{window_width}x{window_height}+{screen_width - window_width - 10}+{screen_height - window_height - 50}")
            elif position == "Bottom Left":
                self.root.geometry(f"{window_width}x{window_height}+10+{screen_height - window_height - 50}")

        self.root.attributes("-topmost", ontop)
        if startup and self.assistant:
            from voice_assistant import setup_autostart
            setup_autostart()

        window.destroy()
        self.update_message("Settings saved successfully!")

    def run(self):
        """Start the UI"""
        self.root.mainloop()

    def shutdown(self):
        """Clean up and close"""
        self.running = False
        if self.animation_thread and self.animation_thread.is_alive():
            self.animation_thread.join(timeout=1)
        self.root.destroy()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--connect":
        print("This would connect to an existing assistant")
    else:
        ui = AssistantFaceUI()

        def demo_mode():
            time.sleep(1)
            ui.set_status("Idle", "neutral")
            ui.update_message("Hello! I'm Megatron. How can I help you today?")
            time.sleep(3)
            ui.set_status("Listening", "listening")
            ui.update_message("Listening...")
            time.sleep(2)
            ui.set_status("Processing", "processing")
            ui.update_message("Processing your request...")
            time.sleep(2)
            ui.set_status("Speaking", "speaking")
            ui.update_message("I've found the information you're looking for. The weather in New York is currently 72°F with partly cloudy skies.")
            time.sleep(3)
            ui.set_status("Idle", "happy")
            ui.update_message("Is there anything else you would like to know?")
            time.sleep(2)
            ui.set_status("Idle", "neutral")

        demo_thread = threading.Thread(target=demo_mode)
        demo_thread.daemon = True
        demo_thread.start()

        try:
            ui.run()
        except KeyboardInterrupt:
            ui.shutdown()