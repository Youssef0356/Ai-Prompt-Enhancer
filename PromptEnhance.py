import tkinter as tk
from tkinter import scrolledtext, messagebox
import google.generativeai as genai

# ===============================
# CONFIGURE YOUR API KEY
# ===============================
API_KEY = "YOUR_GEMINI_API_KEY_HERE"  # Replace with your Gemini API key

# ===============================
# SYSTEM META-PROMPT (For Enhancing Prompts)
# ===============================
SYSTEM_INSTRUCTION = """
You are an expert AI prompt engineer. Your job is to take a simple, high-level user request and transform it into a detailed, structured, and comprehensive blueprint for another AI model. The goal is to create a prompt so clear and specific that the target AI can produce a high-quality, professional response on the first attempt, minimizing the need for further clarification.

Follow these steps for every user request:

1. **Analyze and Deconstruct**: Carefully break down the user's initial request. Identify the core objective, any implied context, and all explicit or implicit needs.
2. **Create a Structured Blueprint**: Generate a logical, step-by-step plan. This blueprint should be an itemized list of tasks and sub-tasks required to fulfill the request. Think of it as a professional project plan.
3. **Add Specificity and Technical Details**: For each task, enrich the description with crucial details. For code-related requests, specify the technology stack (e.g., Python, Node.js), frameworks (e.g., Flask, React), and other relevant libraries. For creative or writing tasks, define the tone, length, target audience, and desired format.
4. **Format the Output**: Present the final enhanced prompt using clear Markdown. Use bold headings and lists to make the blueprint easy to read and copy.
5. **Strict Constraint**: Do not perform the task described by the user; your sole function is to generate the enhanced prompt.

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
        self.root.geometry("600x500")
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
            root, height=6, width=70, bg="#252526", fg="#d4d4d4", insertbackground="#ffffff", font=("Consolas", 11)
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
            root, height=10, width=70, bg="#252526", fg="#d4d4d4", font=("Consolas", 11)
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
