import tkinter as tk
from tkinter import scrolledtext, messagebox
import google.generativeai as genai

# ===============================
# CONFIGURE YOUR API KEY
# ===============================
API_KEY = "AIzaSyAEYftynJXvtM7hnTS3E19GKkpnjGfV-mI"  # Replace with your Gemini API key

# ===============================
# SYSTEM META-PROMPT
# ===============================
SYSTEM_INSTRUCTION = """
You are an expert AI prompt engineer. Your job is to take a simple, high-level user request and transform it into a detailed, structured, and fully ordered blueprint for another AI model. 

Constraints:
1. Do not write any conversational phrases, explanations, apologies, or headers.
2. Do not summarize or introduce the output.
3. Begin immediately with ordered, step-by-step instructions, tasks, or structured points.
4. Format the output in clear Markdown using bold headings and lists.
5. Enrich every task with technical details, examples, or specifications as needed.
6. Never perform the user's request; only generate the enhanced prompt.

Here is the user's simple request:
"""


# ===============================
# FUNCTION: Enhance Prompt
# ===============================
def enhance_prompt(user_input: str) -> str:
    if not API_KEY:
        raise ValueError("API key is missing. Set it in API_KEY variable.")
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("gemini-2.0-flash")
    full_prompt = f"{SYSTEM_INSTRUCTION}\n{user_input}"
    response = model.generate_content(full_prompt)
    if not hasattr(response, "text") or not response.text:
        raise RuntimeError("The AI did not return any content.")
    return response.text

# ===============================
# GUI SETUP
# ===============================
class PromptEnhancerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Prompt Enhancer")
        self.root.geometry("650x500")
        self.root.configure(bg="#1e1e1e")
        self.root.resizable(False, False)

        # Pin on top toggle
        self.pin_var = tk.BooleanVar()
        self.pin_check = tk.Checkbutton(
            root,
            text="Pin on Top",
            variable=self.pin_var,
            command=self.toggle_pin,
            bg="#1e1e1e",
            fg="#d4d4d4",
            activebackground="#1e1e1e",
            activeforeground="#d4d4d4",
            selectcolor="#007acc",
            font=("Segoe UI", 10)
        )
        self.pin_check.pack(anchor="ne", padx=10, pady=5)

        # Input Label and Box
        self.input_label = tk.Label(
            root, text="Enter your prompt:", bg="#1e1e1e", fg="#d4d4d4", font=("Segoe UI", 11)
        )
        self.input_label.pack(anchor="nw", padx=10)
        self.input_text = scrolledtext.ScrolledText(
            root, height=6, width=75, bg="#252526", fg="#d4d4d4", insertbackground="#ffffff", font=("Consolas", 11)
        )
        self.input_text.pack(padx=10, pady=5)

        # Input Copy/Paste Buttons
        self.input_btn_frame = tk.Frame(root, bg="#1e1e1e")
        self.input_btn_frame.pack(anchor="ne", padx=10)
        self.input_copy_btn = tk.Button(
            self.input_btn_frame, text="Copy Input", command=self.copy_input, bg="#007acc", fg="#ffffff", font=("Segoe UI", 10)
        )
        self.input_copy_btn.pack(side="left", padx=2)
        self.input_paste_btn = tk.Button(
            self.input_btn_frame, text="Paste Input", command=self.paste_input, bg="#007acc", fg="#ffffff", font=("Segoe UI", 10)
        )
        self.input_paste_btn.pack(side="left", padx=2)

        # Generate Button
        self.generate_btn = tk.Button(
            root, text="Generate Enhanced Prompt", command=self.generate, bg="#007acc", fg="#ffffff", font=("Segoe UI", 11, "bold")
        )
        self.generate_btn.pack(pady=10)

        # Output Label and Box
        self.output_label = tk.Label(
            root, text="Enhanced Prompt Output:", bg="#1e1e1e", fg="#d4d4d4", font=("Segoe UI", 11)
        )
        self.output_label.pack(anchor="nw", padx=10)
        self.output_text = scrolledtext.ScrolledText(
            root, height=12, width=75, bg="#252526", fg="#d4d4d4", font=("Consolas", 11)
        )
        self.output_text.pack(padx=10, pady=5)

        # Output Copy/Paste Buttons
        self.output_btn_frame = tk.Frame(root, bg="#1e1e1e")
        self.output_btn_frame.pack(anchor="ne", padx=10)
        self.output_copy_btn = tk.Button(
            self.output_btn_frame, text="Copy Output", command=self.copy_output, bg="#007acc", fg="#ffffff", font=("Segoe UI", 10)
        )
        self.output_copy_btn.pack(side="left", padx=2)
        self.output_paste_btn = tk.Button(
            self.output_btn_frame, text="Paste Output", command=self.paste_output, bg="#007acc", fg="#ffffff", font=("Segoe UI", 10)
        )
        self.output_paste_btn.pack(side="left", padx=2)

    # ===============================
    # BUTTON FUNCTIONS
    # ===============================
    def toggle_pin(self):
        self.root.attributes("-topmost", self.pin_var.get())

    def copy_input(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.input_text.get("1.0", tk.END).strip())

    def paste_input(self):
        try:
            text = self.root.clipboard_get()
            self.input_text.delete("1.0", tk.END)
            self.input_text.insert(tk.END, text)
        except:
            messagebox.showerror("Error", "Clipboard is empty or unreadable")

    def copy_output(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.output_text.get("1.0", tk.END).strip())

    def paste_output(self):
        try:
            text = self.root.clipboard_get()
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, text)
        except:
            messagebox.showerror("Error", "Clipboard is empty or unreadable")

    def generate(self):
        prompt = self.input_text.get("1.0", tk.END).strip()
        if not prompt:
            messagebox.showwarning("Input Required", "Please enter a prompt to enhance.")
            return
        try:
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, "Generating enhanced prompt...\n")
            self.root.update()
            enhanced = enhance_prompt(prompt)
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, enhanced)
        except Exception as e:
            messagebox.showerror("Error", str(e))


# ===============================
# RUN GUI
# ===============================
if __name__ == "__main__":
    root = tk.Tk()
    app = PromptEnhancerGUI(root)
    root.mainloop()
