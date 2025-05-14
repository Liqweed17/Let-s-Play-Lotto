import tkinter as tk
from tkinter import font as tkfont
import random
from collections import Counter
import itertools

class LotteryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Discrete 6/45 Lottery")
        self.root.geometry("320x640")
        self.root.configure(bg="#1B0E3B")
        
        # Create main container
        self.main_frame = tk.Frame(root, bg="#1B0E3B")
        self.main_frame.pack(fill="both", expand=True)
        
        # Top bar with signal icons
        self.top_bar = tk.Frame(self.main_frame, bg="#1B0E3B")
        self.top_bar.pack(fill="x", padx=20, pady=10)
        
        self.signal_icons = tk.Frame(self.top_bar, bg="#1B0E3B")
        self.signal_icons.pack(side="right")
        
        # Title
        self.title_label = tk.Label(self.main_frame, text="Lottery", fg="white", bg="#1B0E3B", 
                                  font=("Montserrat", 18, "bold"))
        self.title_label.pack(pady=10)
        
        # Winning numbers container
        self.numbers_frame = tk.Frame(self.main_frame, bg="#4B2D82")
        self.numbers_frame.pack(padx=20, pady=10, fill="x")
        
        self.winning_label = tk.Label(self.numbers_frame, text="Winning Numbers", fg="white", 
                                     bg="#4B2D82", font=("Montserrat", 12, "bold"))
        self.winning_label.pack(pady=10)
        
        self.numbers_display = tk.Frame(self.numbers_frame, bg="#4B2D82")
        self.numbers_display.pack(pady=10)
        
        # Frequency analysis label
        self.freq_label = tk.Label(self.main_frame, text="", fg="white", bg="#1B0E3B",
                                  font=("Montserrat", 10), wraplength=280, justify="left")
        self.freq_label.pack(pady=10)
        
        # Number grid
        self.grid_frame = tk.Frame(self.numbers_frame, bg="#4B2D82")
        self.grid_frame.pack(pady=10)
        
        self.number_labels = []  # Store references to number grid labels
        self.create_number_grid()
        
        # Generate button
        self.generate_btn = tk.Button(self.main_frame, text="Generate Lucky Numbers", 
                                     command=self.generate_numbers, bg="#FF004F", fg="white", 
                                     font=("Montserrat", 12, "bold"), bd=0, padx=20, pady=10)
        self.generate_btn.pack(pady=20)
        
        # Generate initial numbers
        self.generate_numbers()
    
    def create_number_grid(self):
        # Create number grid (1-45)
        for i in range(7):
            for j in range(7):
                num = i * 7 + j + 1
                if num <= 45:
                    label = tk.Label(self.grid_frame, text=str(num), width=3, height=1, 
                                     bg="#3B2A7A", fg="white", font=("Montserrat", 10, "bold"))
                    label.grid(row=i, column=j, padx=2, pady=2)
                    self.number_labels.append(label)
    
    def generate_numbers(self):
        # 1. Create list of all possible combinations (LUCKY NUMBERS)
        numbers = list(range(1, 46))
        all_combinations = list(itertools.combinations(numbers, 6))
        
        # 2. Pick randomly at least 1000 combinations
        selected = random.sample(all_combinations, min(1000, len(all_combinations)))
        
        # 3. Count frequencies for each number
        all_numbers = [num for combo in selected for num in combo]
        frequency = Counter(all_numbers)
        
        # 4. Pick top 6 with highest frequency
        top_6 = frequency.most_common(6)
        winning_numbers = [num for num, count in top_6]
        
        # Update display in circles
        for widget in self.numbers_display.winfo_children():
            widget.destroy()
        
        colors = ["#FFA500", "#FFB800", "#FFB800", "#FFB800", "#FFB800", "#FF004F"]
        for i, num in enumerate(winning_numbers):
            circle = tk.Canvas(self.numbers_display, width=32, height=32, bg="#4B2D82", 
                             highlightthickness=0)
            circle.create_oval(0, 0, 32, 32, fill=colors[i])
            circle.create_text(16, 16, text=str(num), fill="white", 
                              font=("Montserrat", 12, "bold"))
            circle.grid(row=0, column=i, padx=5)
        
        # Highlight numbers in the grid
        for label in self.number_labels:
            label_num = int(label.cget("text"))
            if label_num in winning_numbers:
                label.configure(bg="#FFB800", fg="black")
            else:
                label.configure(bg="#3B2A7A", fg="white")
        
        # Update frequency analysis text
        freq_text = "Frequency Analysis:\n"
        for num, count in top_6:
            freq_text += f"Number {num}: Appeared {count} times\n"
        self.freq_label.config(text=freq_text)
        
        # Print sample output (for submission)
        print("Sample Output:")
        print("Top 6 Most Frequent Numbers:")
        for num, count in top_6:
            print(f"Number {num}: {count} occurrences")

if __name__ == "__main__":
    root = tk.Tk()
    app = LotteryApp(root)
    root.mainloop()