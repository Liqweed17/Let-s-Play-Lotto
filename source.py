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
        
        # main container
        self.main_frame = tk.Frame(root, bg="#1B0E3B")
        self.main_frame.pack(fill="both", expand=True)
        self.top_bar = tk.Frame(self.main_frame, bg="#1B0E3B")
        self.top_bar.pack(fill="x", padx=20, pady=10)
        
        self.signal_icons = tk.Frame(self.top_bar, bg="#1B0E3B")
        self.signal_icons.pack(side="right")
        
        # title
        self.title_label = tk.Label(self.main_frame, text="Lottery", fg="white", bg="#1B0E3B", 
                                  font=("Montserrat", 18, "bold"))
        self.title_label.pack(pady=10)
        
        # winning numbers container
        self.numbers_frame = tk.Frame(self.main_frame, bg="#4B2D82")
        self.numbers_frame.pack(padx=20, pady=10, fill="x")
        
        self.winning_label = tk.Label(self.numbers_frame, text="Winning Numbers", fg="white", 
                                     bg="#4B2D82", font=("Montserrat", 12, "bold"))
        self.winning_label.pack(pady=10)
        
        self.numbers_display = tk.Frame(self.numbers_frame, bg="#4B2D82")
        self.numbers_display.pack(pady=10)

        # --- Place the iteration input below the numbers_display area ---
        self.iter_frame = tk.Frame(self.numbers_frame, bg="#4B2D82")
        self.iter_frame.pack(pady=(0, 10))
        self.iter_label = tk.Label(self.iter_frame, text="Number of Iterations:", fg="white", bg="#4B2D82", font=("Montserrat", 10))
        self.iter_label.pack(side="left", padx=(0, 5))
        self.iter_var = tk.StringVar(value="1000")
        self.iter_entry = tk.Entry(self.iter_frame, textvariable=self.iter_var, width=8, font=("Montserrat", 10))
        self.iter_entry.pack(side="left")

        # frequency analysis container
        self.freq_frame = tk.Frame(self.main_frame, bg="#4B2D82")
        self.freq_frame.pack(padx=20, pady=10, fill="x")
        self.freq_title = tk.Label(
            self.freq_frame,
            text="Frequency Analysis",
            fg="white",
            bg="#4B2D82",
            font=("Montserrat", 12, "bold"),
            anchor="center",
            justify="center"
        )
        self.freq_title.pack(pady=(10, 0), fill="x")
        
        self.freq_label = tk.Label(self.freq_frame, text="", fg="white", bg="#4B2D82",
                                  font=("Montserrat", 10), wraplength=280, justify="left")
        self.freq_label.pack(pady=10)
        
        # number grid
        self.grid_frame = tk.Frame(self.numbers_frame, bg="#4B2D82")
        self.grid_frame.pack(pady=10)
        
        self.number_labels = []  # Store references to number grid labels
        self.create_number_grid()
        
        # generate button
        self.generate_btn = tk.Button(self.main_frame, text="Generate Lucky Numbers", 
                                     command=self.generate_numbers, bg="#FF004F", fg="white", 
                                     font=("Montserrat", 12, "bold"), bd=0, padx=20, pady=10)
        self.generate_btn.pack(pady=20)
        
        # Draw blank circles at start
        self.draw_blank_circles()

    def draw_blank_circles(self):
        # Draw 6 blank circles (no numbers)
        for widget in self.numbers_display.winfo_children():
            widget.destroy()
        colors = ["#FFA500", "#FFB800", "#FFB800", "#FFB800", "#FFB800", "#FF004F"]
        for i in range(6):
            circle = tk.Canvas(self.numbers_display, width=32, height=32, bg="#4B2D82", highlightthickness=0)
            circle.create_oval(0, 0, 32, 32, fill=colors[i])
            circle.grid(row=0, column=i, padx=5)

    def create_number_grid(self):
        for i in range(7):
            for j in range(7):
                num = i * 7 + j + 1
                if num <= 45:
                    label = tk.Label(self.grid_frame, text=str(num), width=3, height=1, 
                                     bg="#3B2A7A", fg="white", font=("Montserrat", 10, "bold"))
                    label.grid(row=i, column=j, padx=2, pady=2)
                    self.number_labels.append(label)
    
    def generate_numbers(self):
        # Get user input for iterations, default to 1000 if invalid
        try:
            iterations = int(self.iter_var.get())
            if iterations < 1:
                iterations = 1000
        except ValueError:
            iterations = 1000

        numbers = list(range(1, 46))
        all_combinations = list(itertools.combinations(numbers, 6))
        
        selected = random.sample(all_combinations, min(iterations, len(all_combinations)))
        
        all_numbers = [num for combo in selected for num in combo]
        frequency = Counter(all_numbers)
        
        top_6 = frequency.most_common(6)
        winning_numbers = [num for num, count in top_6]
        
        # Draw circles with numbers
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
        
        for label in self.number_labels:
            label_num = int(label.cget("text"))
            if label_num in winning_numbers:
                label.configure(bg="#FFB800", fg="black")
            else:
                label.configure(bg="#3B2A7A", fg="white")
        
        freq_text = ""
        for num, count in top_6:
            freq_text += f"Number {num}: Appeared {count} times\n"
        self.freq_label.config(text=freq_text)
        
        # print sample output
        print("Sample Output:")
        print("Top 6 Most Frequent Numbers:")
        for num, count in top_6:
            print(f"Number {num}: {count} occurrences")

if __name__ == "__main__":
    root = tk.Tk()
    app = LotteryApp(root)
    root.mainloop()