#!/usr/bin/env python3
"""Local desktop chat client. No shell execution or external Python dependencies."""
import json
import queue
import threading
import tkinter as tk
from tkinter import scrolledtext
import urllib.request

URL = "http://127.0.0.1:11434/api/chat"

def request_reply(model, messages):
    data = json.dumps({"model": model, "messages": messages, "stream": False}).encode()
    req = urllib.request.Request(URL, data=data, headers={"Content-Type": "application/json"})
    # Ignore HTTP_PROXY/HTTPS_PROXY even if the user's environment sets them.
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    with opener.open(req, timeout=300) as response:
        reply = json.load(response)["message"]["content"]
    if not isinstance(reply, str):
        raise ValueError("The model returned a non-text response")
    return reply

class App:
    def __init__(self, root):
        self.root = root
        self.events = queue.Queue()
        self.messages = []
        self.conversation_model = None
        root.title("LANTERN AI • Local Intelligence")
        root.geometry("920x680")
        root.configure(bg="#101827")
        tk.Label(root, text="LANTERN / AI LINUX", bg="#101827", fg="#48e0d2", font=("Sans", 24, "bold")).pack(pady=18)
        tk.Label(root, text="Local chat • Your prompts stay on this computer • No command execution", bg="#101827", fg="white").pack()
        row = tk.Frame(root, bg="#101827")
        row.pack(pady=10)
        tk.Label(row, text="Installed Ollama model:", bg="#101827", fg="white").pack(side="left")
        self.model = tk.Entry(row, width=30)
        self.model.insert(0, "qwen2.5:1.5b")
        self.model.pack(side="left", padx=8)
        self.log = scrolledtext.ScrolledText(root, wrap="word", bg="#18243a", fg="#edf6ff", font=("Sans", 12), state="disabled")
        self.log.pack(fill="both", expand=True, padx=20)
        self.entry = tk.Entry(root, font=("Sans", 13))
        self.entry.pack(fill="x", padx=20, pady=10)
        self.entry.bind("<Return>", lambda event: self.send())
        self.button = tk.Button(root, text="Send", command=self.send)
        self.button.pack(pady=(0, 12))
        self.add("LANTERN", "Install Ollama and download a model using the README setup steps, then type here. Chat history is kept in memory only.")
        root.after(100, self.poll)

    def add(self, who, text):
        self.log.configure(state="normal")
        self.log.insert("end", f"{who}: {text}\n\n")
        self.log.configure(state="disabled")
        self.log.see("end")

    def send(self):
        text = self.entry.get().strip()
        model = self.model.get().strip()
        if not text or not model or str(self.button["state"]) == "disabled":
            return
        self.entry.delete(0, "end")
        self.add("You", text)
        self.button.configure(state="disabled")
        if model != self.conversation_model:
            self.messages = []
            self.conversation_model = model
        pending = self.messages + [{"role": "user", "content": text}]
        def work():
            try:
                reply = request_reply(model, pending)
                self.events.put((True, pending, reply))
            except Exception as exc:
                self.events.put((False, pending, f"Could not reach the local model: {exc}. Check that Ollama is running and the model is downloaded."))
        threading.Thread(target=work, daemon=True).start()

    def poll(self):
        try:
            ok, pending, reply = self.events.get_nowait()
            if ok:
                self.messages = pending + [{"role": "assistant", "content": reply}]
            self.add("LANTERN" if ok else "Setup", reply)
            self.button.configure(state="normal")
        except queue.Empty:
            pass
        self.root.after(100, self.poll)

if __name__ == "__main__":
    App(tk.Tk()).root.mainloop()
