from tkinter import *
from tkinter import messagebox

with open('words.txt') as f:
    all_sentences = f.readlines()

def choose_sentence():
    global words, choosen_sentence
    import random
    choosen_sentence =random.choice(all_sentences).strip()
    words = choosen_sentence.split(' ')

def count_words ():
    user_words = user_input.get()
    user_words = user_words.split(' ')
    correct_word = 0
    for _ in range(len(words)):
        try:
            if words[_] == user_words[_]:
                correct_word += 1
        except:
            pass

    return correct_word

def bind_key():
    global first_letter
    first_letter = words[0][0]
    window.bind(first_letter, start_timer)

def reset ():
    # Restart the Entire Programm
    try:
        window.after_cancel(timer)
    except:
        pass
    user_input.delete(0, END)
    choose_sentence()
    display_text()
    time_left.config(text='Time left 00:00')
    bind_key()

def read_score():
    try:
        with open('highscore.txt', 'r') as f:
            high_score = int(f.readline())
            return high_score

    except:
        with open('highscore.txt', 'w') as f:
            return 0

def save_score(score):
    with open('highscore.txt', 'w') as f:
        f.write(str(score))

def count_down(count):
    count_min = count // 60
    count_sec = count % 60
    
    if count_sec < 10:
        count_sec =f'0{count_sec}'

    time_left.config(text=f'Time left {count_min}:{count_sec}')
    if count > 0:
        global timer
        timer = window.after(1000, count_down, count-1)

    else:
        score = count_words()
        messagebox.showinfo(title='Results', message=f'Your Score: {score} WPM')
        if score > read_score():
            save_score(score)
            high_score.config(text =f"Your best: {read_score()} WPM")

        reset()

def start_timer(e):
    count_down(1 * 60)
    window.unbind(first_letter)

canvas_text_items = []

def display_text():
    text_to_display = []
    for item_text in canvas_text_items:
        canvas.delete(item_text)
    start = 0
    end = 0
    while start < len(choosen_sentence):
        end += 50
        text_to_display.append(choosen_sentence[start : end])
        start += 50
    x= 300
    y = 30
    for text in text_to_display:
        canvas_text_items.append(canvas.create_text(x, y, text=text, font=('Arial', 15, "normal")))
        y += 35


# UI SETUP
window = Tk()
window.title('Typing Speed Test')
window.minsize(width=700, height=500)
window.config(padx=50, pady=50)

# Labels
high_score_text = read_score()
high_score = Label(text=f"Your best: {high_score_text} WPM")
high_score.grid(row=0, column=0)
time_left = Label(text='Time left: 00:00')
time_left.grid(row=0, column=1)

canvas = Canvas(width=600, height=400, bg="white")
choose_sentence()
display_text()
canvas.grid(row=1, column=0, columnspan=3, pady=50)

# Entry
user_input = Entry(width=80)
user_input.grid(row=2, column=0, columnspan=3, pady=50, padx=50)
user_input.focus()

# Button
Button(text='Reset', command=reset).grid(row=0, column=2)

bind_key()
window.mainloop()
