import tkinter as tk
import random
from tkinter import ttk
import customtkinter as ctk
import nltk
from nltk.corpus import wordnet

# Download WordNet if not already downloaded
nltk.download('wordnet')

# Function to get synonyms for a given word and add the synonym to the set
def get_synonyms(word):
    """ Get synonyms for a given word using WordNet """
    synonyms = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name())  
    return synonyms

# Custom fallback descriptions for words that might not have synonyms in WordNet
custom_descriptions = {
    "sonder": "The realization that each passerby has a life as vivid and complex as your own.",
    "oniric": "Related to dreams or the dream state.",
    "petrichor": "The pleasant, earthy scent produced when rain falls on dry soil or ground.",
    "serendipity": "The occurrence of events by chance in a happy or beneficial way.",
    "ephemeral": "Lasting for a very short time.",
    "quixotic": "Extremely idealistic; unrealistic and impractical.",
    "pulchritude": "Physical beauty.",
    "effervescent": "Bubbly, vivacious, or enthusiastic.",
    "panacea": "A solution or remedy for all problems or difficulties."
}

# Function to get a random word of the day
def get_word_of_the_day():
    word_list = [
        "ephemeral", "loquacious", "eloquent", "melancholy", "serendipity", "epiphany", "sonder", "sonorous", "petrichor",
        "surreptitious", "acumen", "incandescent", "nadir", "effervescent", "lagniappe", "ethereal", "inexorable", "lucid", 
        "recalcitrant", "panacea", "quixotic", "limerence", "sagacity", "plethora", "elixir", "languor", "perfidious", "panegyric", 
        "taciturn", "soliloquy", "bombastic", "catharsis", "quintessential", "zeitgeist", "alchemy", "inimitable", "idyllic",  "sumptuous", 
        "magnanimous", "celestial", "pulchritude", "raconteur", "palimpsest", "paradigm",  "verisimilitude", "ubiquitous", "seraphic", "oniric", 
        "tenebrous", "ineffable", "epicurean", "luminous", "eudaimonia", "sapient", "parsimonious"
    ]
    return random.choice(word_list)

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Dumile")

        # Set a fixed window size for compactness
        self.geometry("960x350")  

        # Configuring the grid layout with appropriate weights
        # Column 0 (left) takes 1 unit weight
        self.columnconfigure(0, weight=1, minsize=200)  
        # Column 1 (right) takes 3 units weight
        self.columnconfigure(1, weight=3, minsize=400)  
        self.rowconfigure(0, weight=1)

        # Create input form for adding words
        frame = InputForm(self)
        frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        # Create synonym display form
        frame2 = SynonymForm(self)
        frame2.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

class InputForm(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        # Create entry widget for user input and define width for better alignment
        self.entry = ttk.Entry(self, width=20)  
        self.entry.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

        self.entry.bind("<Return>", self.get_synonym_for_word)

        # Create buttons with fixed widths to prevent expansion
        self.entry_btn = CustomButton(self, text="Find Synonym", command=self.get_synonym_for_word, width=15)
        self.entry_btn.grid(row=0, column=1, padx=5, pady=5)

        self.entry_btn2 = CustomButton(self, text="Clear", command=self.clear_list, width=10)
        self.entry_btn2.grid(row=0, column=2, padx=5, pady=5)

        # Listbox for synonyms, aligned below the input field and set fixed height/width
        self.text_list = tk.Listbox(self, height=5, width=30, selectmode=tk.SINGLE)  
        self.text_list.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)

    def get_synonym_for_word(self, _event=None):
        """ Get a synonym for the entered word and display its synonyms """
        text = self.entry.get().strip()
        if text:
            
            # Clear listbox before adding new results
            self.text_list.delete(0, tk.END)  

            # Get synonyms for the entered word
            synonyms = get_synonyms(text)
            if synonyms:
                # Remove the original word from the synonyms list and insert each synonym as a separate line
                synonyms = [synonym for synonym in synonyms if synonym.lower() != text.lower()]
                
                if synonyms:
                    for synonym in synonyms:
                        self.text_list.insert(tk.END, synonym)   
                else:
                    self.text_list.insert(tk.END, f"No synonyms found except the word itself: '{text}'")
            elif text.lower() in custom_descriptions:
                
                # Display description if no synonyms found but a description is available
                self.text_list.insert(tk.END, f"Description: {custom_descriptions[text.lower()]}")
            else:
                self.text_list.insert(tk.END, f"No synonyms found for '{text}'")

            self.entry.delete(0, tk.END)

    def clear_list(self):
        """ Clear the listbox """
        self.text_list.delete(0, tk.END)

class SynonymForm(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # Word of the Day label (Initially empty)
        self.word_of_the_day_label = ttk.Label(self, text="", font=("Arial", 16), anchor="w")
        self.word_of_the_day_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)

        # Show Synonyms & Change Word button
        self.show_change_btn = CustomButton(self, text="Word of the Day", command=self.show_and_change_word, width=20)
        self.show_change_btn.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)

        # Listbox for synonyms. 5 rows, 30 characters wide
        self.synonym_listbox = tk.Listbox(self, height=5, width=30)  
        self.synonym_listbox.grid(row=4, column=0, sticky="nsew", padx=5, pady=5)

    def show_and_change_word(self):
        """ Show synonyms for the Word of the Day and change to a new word """
        # Change the Word of the Day
        self.word_of_the_day = get_word_of_the_day()
        self.word_of_the_day_label.config(text=f"Word of the Day: {self.word_of_the_day}")

        # Show synonyms for the new Word of the Day and clears previous results
        self.synonym_listbox.delete(0, tk.END)  
        synonyms = get_synonyms(self.word_of_the_day)
        
        if synonyms:
            # Remove the Word of the Day from the list of synonyms
            synonyms = [synonym for synonym in synonyms if synonym.lower() != self.word_of_the_day.lower()]
            self.synonym_listbox.insert(tk.END, f"Synonyms for {self.word_of_the_day}: " + ", ".join(synonyms))
        else:
            self.synonym_listbox.insert(tk.END, f"No synonyms found for {self.word_of_the_day}")

class CustomButton(ctk.CTkButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.default_color = self.cget("fg_color")
          # Red on hover
        self.hover_color = "#FF5733"

        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, event):
        self.configure(fg_color=self.hover_color)

    def on_leave(self, event):
        self.configure(fg_color=self.default_color)

if __name__ == "__main__":
    app = Application()
    app.mainloop()