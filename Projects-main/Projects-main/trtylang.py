import speech_recognition as sr
import pyttsx3
import datetime
import re
import webbrowser
import threading
import tkinter as tk
import random

from math_operations import (
    add, sub, multiply, divide,
    find_sqrt, cube_root, power, square, cube,
    fact,
    sin_value, sinh_value,
    cos_value, cosh_value,
    tan_value, tanh_value,
    log,
    symbolic_integral
)

recognizer = sr.Recognizer()
engine = pyttsx3.init()
engine.setProperty('voice', engine.getProperty('voices')[-1].id)
engine.setProperty('rate', engine.getProperty('rate') - 62)

root = tk.Tk()
root.title("TKAA Voice Assistant")
root.geometry("720x480")
root.configure(bg="#0d0d0f")

FONT_TITLE = ("Segoe UI", 14, "bold")
FONT_TEXT = ("Consolas", 12)
COLOR_BG = "#0d0d0f"
COLOR_TEXT = "#e0e0e0"
COLOR_INPUT = "#1b1b2f"
COLOR_BUTTON = "#26263a"
COLOR_HIGHLIGHT = "#7d5fff" 

main_frame = tk.Frame(root, bg=COLOR_BG, padx=25, pady=25)
main_frame.pack(fill="both", expand=True)

title_label = tk.Label(
    main_frame,
    text="🪐  TKAA Voice Assistant",
    font=("Segoe UI Semibold", 20, "bold"),
    fg=COLOR_HIGHLIGHT,
    bg=COLOR_BG
)
title_label.pack(pady=(0, 20))


user_frame = tk.LabelFrame(
    main_frame,
    text="🎙️ You said",
    font=FONT_TITLE,
    fg=COLOR_HIGHLIGHT,
    bg=COLOR_BG,
    labelanchor="nw",
    bd=2,
    relief="groove"
)
user_frame.pack(fill="x", pady=(0, 10))

command_text = tk.Text(
    user_frame, height=2, font=FONT_TEXT,
    bg=COLOR_INPUT, fg=COLOR_TEXT,
    insertbackground=COLOR_HIGHLIGHT,
    bd=0, wrap="word", padx=10, pady=8
)
command_text.pack(fill="x", padx=5, pady=5)

response_frame = tk.LabelFrame(
    main_frame,
    text="💬 Assistant Response",
    font=FONT_TITLE,
    fg=COLOR_HIGHLIGHT,
    bg=COLOR_BG,
    labelanchor="nw",
    bd=2,
    relief="groove"
)
response_frame.pack(fill="x", pady=(0, 20))

response_text = tk.Text(
    response_frame, height=4, font=FONT_TEXT,
    bg=COLOR_INPUT, fg=COLOR_TEXT,
    insertbackground=COLOR_HIGHLIGHT,
    bd=0, wrap="word", padx=10, pady=8
)
response_text.pack(fill="x", padx=5, pady=5)

listen_button = tk.Button(
    main_frame,
    text="🎤 Tap to Speak",
    font=("Segoe UI Semibold", 14),
    bg=COLOR_BUTTON, fg=COLOR_TEXT,
    activebackground=COLOR_HIGHLIGHT,
    activeforeground="#fff",
    padx=20, pady=10,
    relief="flat",
    bd=0,
    cursor="hand2"
)
listen_button.pack(pady=(10, 0))

def on_enter(e):
    listen_button.configure(bg=COLOR_HIGHLIGHT, fg="#fff")
def on_leave(e):
    listen_button.configure(bg=COLOR_BUTTON, fg=COLOR_TEXT)

listen_button.bind("<Enter>", on_enter)
listen_button.bind("<Leave>", on_leave)

for widget in [user_frame, response_frame]:
    widget.configure(highlightbackground="#2f2f4f", highlightcolor="#2f2f4f", highlightthickness=1)

def speak(text):
    try:
        print(text.encode('ascii', 'ignore').decode())
    except:
        print(text)
    engine.say(text)
    engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio)
        command = command.replace("√", "square root")
        try:
            print("You said:", command.encode('ascii', 'ignore').decode())
        except:
            print("You said:", command)
        return command.lower()
    except sr.UnknownValueError:
        return "Sorry, I didn't catch that."
    except sr.RequestError:
        return "Connection error with the speech service."

def extract_numbers(command):
    return list(map(str, re.findall(r"[-+]?\d*\.?\d+", command)))

def handle_command(command):
    if "time" in command:
        return datetime.datetime.now().strftime("The current time is %H:%M %p")
    elif "open google" in command:
        webbrowser.open("https://www.google.com")
        return "Opening Google"
    elif "open youtube" in command:
        webbrowser.open("https://www.youtube.com")
        return "Opening YouTube"
    elif "search for" in command:
        query = command.replace("search for", "").strip()
        webbrowser.open(f"https://www.google.com/search?q={query}")
        return f"Searching Google for {query}"
    elif "play" in command or "youtube" in command:
        query = command.replace("play", "").replace("on youtube", "").strip()
        webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
        return f"Playing {query} on YouTube"
    elif "wikipedia" in command:
        topic = command.replace("wikipedia", "").strip()
        webbrowser.open(f"https://en.wikipedia.org/wiki/{topic.replace(' ', '_')}")
        return f"Opening Wikipedia page for {topic}"
    elif "open facebook" in command:
        webbrowser.open("https://www.facebook.com")
        return "Opening Facebook"
    elif "open twitter" in command or "open x" in command:
        webbrowser.open("https://x.com")
        return "Opening X (Twitter)"
    elif "open gmail" in command:
        webbrowser.open("https://mail.google.com")
        return "Opening Gmail"
    elif "open reddit" in command:
        webbrowser.open("https://www.reddit.com")
        return "Opening Reddit"
    elif "open spotify" in command:
        webbrowser.open("https://open.spotify.com")
        return "Opening Spotify"
    elif "open github" in command:
        webbrowser.open("https://github.com")
        return "Opening GitHub"
    elif "look up" in command:
        query = command.replace("look up", "").strip()
        webbrowser.open(f"https://duckduckgo.com/?q={query}")
        return f"Looking up {query}"
    elif "open news" in command:
        webbrowser.open("https://news.google.com")
        return "Opening latest news"
    elif "weather" in command:
        webbrowser.open("https://www.google.com/search?q=weather")
        return "Opening current weather"
    elif "define" in command:
        word = command.replace("define", "").strip()
        webbrowser.open(f"https://www.google.com/search?q=define+{word}")
        return f"Searching definition of {word}"
    elif "open wikipedia" in command:
        webbrowser.open("https://www.wikipedia.org")
        return "Opening Wikipedia"
    elif "open quizlet" in command:
        webbrowser.open("https://quizlet.com")
        return "Opening Quizlet"
    elif "open khan academy" in command:
        webbrowser.open("https://www.khanacademy.org")
        return "Opening Khan Academy"
    elif "open messenger" in command:
        webbrowser.open("https://www.messenger.com")
        return "Opening Messenger"
    elif "open instagram" in command:
        webbrowser.open("https://www.instagram.com")
        return "Opening Instagram"
    elif "open tiktok" in command:
        webbrowser.open("https://www.tiktok.com")
        return "Opening TikTok"
    elif "hello" in command or "hi" in command:
        return "Hey there! How are you today?"
    elif "good morning" in command:
        return "Good morning! Let's make today productive."
    elif "good night" in command:
        return "Good night! Sweet dreams and rest well."
    elif "open google classroom" in command:
        webbrowser.open("https://classroom.google.com")
        return "Opening Google Classroom"
    elif "translate" in command:
        phrase = command.replace("translate", "").strip()
        webbrowser.open(f"https://translate.google.com/?sl=auto&tl=en&text={phrase}")
        return f"Translating {phrase}"
    elif "map" in command or "direction" in command:
        location = command.replace("map", "").replace("direction", "").strip()
        webbrowser.open(f"https://www.google.com/maps/search/{location}")
        return f"Showing map for {location}"
    elif "how are you" in command:
        responses = [
            "I’m feeling electric today ⚡",
            "Doing great — just waiting for your next command!",
            "I’m fine, but my circuits could use some coffee.",
        ]
        return random.choice(responses)
    elif "tell me a joke" in command:
        jokes = [
            "Why do programmers hate nature? Too many bugs.",
            "I told my computer I needed a break — it said no problem, it’ll go to sleep.",
            "Why did the function stop calling the variable? Because it had constant arguments."
        ]
        return random.choice(jokes)
    elif "motivate me" in command or "inspire me" in command:
        quotes = [
            "Every expert was once a beginner. Keep going!",
            "You don’t have to be perfect — just consistent.",
            "Small steps every day add up to big results.",
            "Courage doesn’t always roar. Sometimes it whispers, 'I’ll try again tomorrow.'"
        ]
        return random.choice(quotes)
    elif "percentage of" in command:
        nums = extract_numbers(command)
        if len(nums) >= 2:
            base = float(nums[1])
            percent = float(nums[0])
            return f"{percent}% of {base} is {base * (percent / 100)}"
        return "Please say it like 'what is 20 percent of 150'"

    elif "temperature" in command:
        webbrowser.open("https://www.google.com/search?q=temperature")
        return "Checking current temperature"

    elif "integrate" in command or "integral of" in command:
        return symbolic_integral(command)
    elif any(op in command for op in ["+", "sum", "add"]):
        return f"Total is: {add(extract_numbers(command))}"
    elif any(op in command for op in ["minus", "subtract", "substract"]):
        return f"Result is: {sub(extract_numbers(command))}"
    elif any(op in command for op in ["multiply", "product"]):
        return f"Product is: {multiply(extract_numbers(command))}"
    elif any(op in command for op in ["divide by", "division"]):
        return f"Result is: {divide(extract_numbers(command))}"
    elif "square root" in command:
        return f"Square root is: {find_sqrt(extract_numbers(command))}"
    elif "cube root" in command:
        return f"Cube root is: {cube_root(extract_numbers(command))}"
    elif "square" in command:
        return f"Square is: {square(extract_numbers(command))}"
    elif "cube of" in command or "cube" in command:
        return f"Cube is: {cube(extract_numbers(command))}"
    elif "power" in command or "is to the power" in command:
        return f"Result is: {power(extract_numbers(command))}"
    elif "factorial" in command:
        return f"Factorial is: {fact(extract_numbers(command))}"
    elif "sine of" in command:
        return f"Sine value is: {sin_value(extract_numbers(command))}"
    elif "cos of" in command:
        return f"Cos value is: {cos_value(extract_numbers(command))}"
    elif "tan of" in command:
        return f"Tan value is: {tan_value(extract_numbers(command))}"
    elif "hyperbolic sine" in command:
        return f"Hyperbolic sine is: {sinh_value(extract_numbers(command))}"
    elif "hyperbolic cos" in command:
        return f"Hyperbolic cos is: {cosh_value(extract_numbers(command))}"
    elif "hyperbolic tan" in command:
        return f"Hyperbolic tan is: {tanh_value(extract_numbers(command))}"
    elif "log of" in command:
        nums = extract_numbers(command)
        if len(nums) >= 2:
            return f"Log of {nums[0]} base {nums[1]} is: {log(nums)}"
        else:
            return "Please provide both number and base for logarithm."
    elif "stop" in command or "exit" in command:
        root.quit()
        return "Goodbye!"
    else:
        return "Sorry, I don't know that command yet."

def update_gui(command, response):
    command_text.delete("1.0", tk.END)
    command_text.insert(tk.END, command)
    response_text.delete("1.0", tk.END)
    response_text.insert(tk.END, response)

def threaded_listen():
    def run():
        command = listen()
        response = handle_command(command)
        update_gui(command, response)
        speak(response)
    threading.Thread(target=run).start()

# Bind button to threaded listener
listen_button.config(command=threaded_listen)

# ==== 🚀 Start Assistant ====
speak("Hello, I am Tres, your voice assistant. How can I help you?")
root.mainloop()
        