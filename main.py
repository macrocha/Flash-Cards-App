from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}

try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


def next_card():
    # function goes to the next card once the
    # user hits the right/wrong button
    global current_card, flip_timer
    window.after_cancel((flip_timer))
    current_card = random.choice(to_learn)
    canvas.itemconfig(language, text="French", fill="black")
    canvas.itemconfig(vocab, text=current_card["French"], fill="black")
    canvas.itemconfig(card_background, image=card_front_img)
    # flip card after 3 seconds
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    # function flips card over after 3 seconds
    # revealing the english translation
    canvas.itemconfig(language, text="English", fill="white")
    canvas.itemconfig(vocab, text=current_card["English"], fill="white")
    canvas.itemconfig(card_background, image=card_back_img)


def is_correct():
    to_learn.remove(current_card)
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    next_card()

window = Tk()
window.title("Flash Cards")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

# add the front of flash card on to the window
canvas = Canvas(width=800, height=570, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
card_background = canvas.create_image(400, 263, image=card_front_img)

# create text in the flashcard
language = canvas.create_text(400, 150, text="Title", fill="black", font=("Arial", 30, "italic"))
vocab = canvas.create_text(400, 263, text="word", fill="black", font=("Arial", 60, "bold"))
canvas.grid(column=0, row=0, columnspan=2)

# add the correct and incorrect buttons
correct_button_image = PhotoImage(file="images/right.png")
correct_button = Button(image=correct_button_image, highlightthickness=0, command=is_correct)
correct_button.grid(column=1, row=1)
incorrect_button_image = PhotoImage(file="images/wrong.png")
incorrect_button = Button(image=incorrect_button_image, highlightthickness=0, command=next_card)
incorrect_button.grid(column=0, row=1)

next_card()

window.mainloop()