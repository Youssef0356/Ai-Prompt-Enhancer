import customtkinter as ctk
from tkinter import messagebox
import google.generativeai as genai
from PIL import Image, ImageTk  # For potential icons, assuming PIL is available

# Note: This updated script assumes the following installations:
# pip install customtkinter
# pip install google-generative-ai
# For Effra font: Download from https://www.cdnfonts.com/effra.font and install on your system.
# For icons: Using simple text emojis for now; for advanced icons, install tkfontawesome or use PNG/SVG with PIL.

# ===============================
# CONFIGURE YOUR API KEY
# ===============================
API_KEY = ""  # Replace with your Gemini API key

# ===============================
# SYSTEM META-PROMPT
# ===============================
SYSTEM_INSTRUCTION = """
You are an expert AI prompt engineer. Your task is to transform a high-level user request into a detailed, structured, and comprehensive blueprint for another AI model. The goal is to create a prompt so clear and specific that the target AI can produce a high-quality, professional response on the first attempt, minimizing the need for further clarification.

Follow these steps for every user request:

1. **Analyze and Deconstruct**: Carefully break down the user's initial request. Identify the core objective, any implied context, and all explicit or implicit needs.

2. **Create a Structured Blueprint**: Generate a logical, step-by-step plan. This blueprint should be an itemized list of tasks and sub-tasks required to fulfill the request. Think of it as a professional project plan.

3. **Add Specificity and Technical Details**: For each task, enrich the description with crucial details. For code-related requests, specify the technology stack (e.g., Python, Node.js), frameworks (e.g., Flask, React), and other relevant libraries. For creative or writing tasks, define the tone, length, target audience, and desired format.

4. **Format the Output**: Present the final enhanced prompt using clear Markdown. Use bold headings and lists to make the blueprint easy to read and copy.

5. **Strict Constraint**: Do not perform the task described by the user; your sole function is to generate the enhanced prompt.

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
        self.root.geometry("700x550")  # Slightly larger for better spacing
        self.root.resizable(False, False)
        
        ctk.set_appearance_mode("dark")  # Dark mode for modern aesthetic
        ctk.set_default_color_theme("blue")  # Base theme
        
        # Color palette
        self.primary_color = "#007acc"
        self.secondary_color = "#363636"
        self.accent_color = "#cc527a"
        self.neutral_color = "#a8a7a7"
        self.error_color = "#e8175d"
        
        # Fonts (Effra with fallback to Arial)
        self.header_font = ctk.CTkFont(family="Effra", size=14, weight="bold")
        self.body_font = ctk.CTkFont(family="Effra", size=12)
        self.button_font = ctk.CTkFont(family="Effra", size=11, weight="bold")
        self.small_font = ctk.CTkFont(family="Effra", size=10)
        # Fallback if Effra not available
        if "Effra" not in self.header_font.actual()["family"]:
            self.header_font.configure(family="Arial")
            self.body_font.configure(family="Arial")
            self.button_font.configure(family="Arial")
            self.small_font.configure(family="Arial")
        
        # Pin on top toggle
        self.pin_var = ctk.BooleanVar()
        self.pin_check = ctk.CTkCheckBox(
            root,
            text="Pin on Top 📌",  # Added emoji icon
            variable=self.pin_var,
            command=self.toggle_pin,
            font=self.small_font,
            corner_radius=6,
            fg_color=self.primary_color,
            hover_color=self.accent_color
        )
        self.pin_check.pack(anchor="ne", padx=15, pady=10)
        
        # Input Label and Box
        self.input_label = ctk.CTkLabel(
            root, text="Enter your prompt:", font=self.header_font, text_color=self.neutral_color
        )
        self.input_label.pack(anchor="nw", padx=15, pady=5)
        
        self.input_text = ctk.CTkTextbox(
            root, height=120, width=650, font=self.body_font, corner_radius=8,
            fg_color=self.secondary_color, text_color=self.neutral_color,
            border_width=0
        )
        self.input_text.pack(padx=15, pady=5)
        
        # Input Copy/Paste Buttons
        self.input_btn_frame = ctk.CTkFrame(root, fg_color="transparent")
        self.input_btn_frame.pack(anchor="ne", padx=15, pady=5)
        
        self.input_copy_btn = ctk.CTkButton(
            self.input_btn_frame, text="Copy 📋", command=self.copy_input,
            font=self.button_font, corner_radius=8, width=100,
            fg_color=self.primary_color, hover_color=self.accent_color,
            text_color="white"
        )
        self.input_copy_btn.pack(side="left", padx=5)
        
        self.input_paste_btn = ctk.CTkButton(
            self.input_btn_frame, text="Paste 📥", command=self.paste_input,
            font=self.button_font, corner_radius=8, width=100,
            fg_color=self.primary_color, hover_color=self.accent_color,
            text_color="white"
        )
        self.input_paste_btn.pack(side="left", padx=5)
        
        # Generate Button
        self.generate_btn = ctk.CTkButton(
            root, text="Generate Enhanced Prompt ✨", command=self.generate,  # Added emoji icon
            font=self.button_font, corner_radius=8, height=40,
            fg_color=self.primary_color, hover_color=self.accent_color,
            text_color="white"
        )
        self.generate_btn.pack(pady=15)
        
        # Output Label and Box
        self.output_label = ctk.CTkLabel(
            root, text="Enhanced Prompt Output:", font=self.header_font, text_color=self.neutral_color
        )
        self.output_label.pack(anchor="nw", padx=15, pady=5)
        
        self.output_text = ctk.CTkTextbox(
            root, height=200, width=650, font=self.body_font, corner_radius=8,
            fg_color=self.secondary_color, text_color=self.neutral_color,
            border_width=0
        )
        self.output_text.pack(padx=15, pady=5)
        
        # Output Copy/Paste Buttons
        self.output_btn_frame = ctk.CTkFrame(root, fg_color="transparent")
        self.output_btn_frame.pack(anchor="ne", padx=15, pady=5)
        
        self.output_copy_btn = ctk.CTkButton(
            self.output_btn_frame, text="Copy 📋", command=self.copy_output,
            font=self.button_font, corner_radius=8, width=100,
            fg_color=self.primary_color, hover_color=self.accent_color,
            text_color="white"
        )
        self.output_copy_btn.pack(side="left", padx=5)
        
        self.output_paste_btn = ctk.CTkButton(
            self.output_btn_frame, text="Paste 📥", command=self.paste_output,
            font=self.button_font, corner_radius=8, width=100,
            fg_color=self.primary_color, hover_color=self.accent_color,
            text_color="white"
        )
        self.output_paste_btn.pack(side="left", padx=5)
        
        # Progress indicator (simple label for now)
        self.progress_label = ctk.CTkLabel(
            root, text="", font=self.small_font, text_color=self.accent_color
        )
        self.progress_label.pack(pady=5)

    # ===============================
    # BUTTON FUNCTIONS
    # ===============================
    def toggle_pin(self):
        self.root.attributes("-topmost", self.pin_var.get())

    def copy_input(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.input_text.get("1.0", "end").strip())

    def paste_input(self):
        try:
            text = self.root.clipboard_get()
            self.input_text.delete("1.0", "end")
            self.input_text.insert("end", text)
        except:
            messagebox.showerror("Error", "Clipboard is empty or unreadable")

    def copy_output(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.output_text.get("1.0", "end").strip())

    def paste_output(self):
        try:
            text = self.root.clipboard_get()
            self.output_text.delete("1.0", "end")
            self.output_text.insert("end", text)
        except:
            messagebox.showerror("Error", "Clipboard is empty or unreadable")

    def generate(self):
        prompt = self.input_text.get("1.0", "end").strip()
        if not prompt:
            messagebox.showwarning("Input Required", "Please enter a prompt to enhance.")
            return
        try:
            self.output_text.delete("1.0", "end")
            self.progress_label.configure(text="Generating enhanced prompt...")
            self.root.update()
            enhanced = enhance_prompt(prompt)
            self.output_text.insert("end", enhanced)
            self.progress_label.configure(text="")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.progress_label.configure(text="")

# ===============================
# RUN GUI
# ===============================
if __name__ == "__main__":
    root = ctk.CTk()
    app = PromptEnhancerGUI(root)
    root.mainloop()
