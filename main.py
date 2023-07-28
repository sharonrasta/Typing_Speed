from tkinter import *
import ctypes
import random

texts = [
    'At the edge of the serene lake, a group of friends gathered to celebrate their annual reunion. They reminisced '
    'about the days of their youth, when time seemed to stretch endlessly before them. Laughter filled the air as '
    'they shared tales of their past adventures, each story more captivating than the last. As the sun dipped below '
    'the horizon, casting a golden glow across the tranquil water, they marveled at the enduring bonds they had '
    'forged over the years. In that moment, surrounded by the people who knew them best, they felt a profound sense '
    'of gratitude for the memories they had created and the lifelong friendships that had blossomed from their shared '
    'experiences.',
    'Deep within the heart of the ancient forest, a hidden sanctuary lay nestled among the towering trees. This '
    'secluded haven, known only to a select few, was a place where weary travelers could find solace and '
    'rejuvenation. A crystal-clear spring fed a gently babbling brook, its soothing melody harmonizing with the '
    'chorus of birdsong that filled the air. Lush ferns and vibrant wildflowers carpeted the forest floor, '
    'while the dappled sunlight filtering through the dense canopy overhead created an enchanting play of light and '
    'shadow. For those fortunate enough to discover this magical oasis, it was a place where the stresses of the '
    'outside world seemed to fade away, replaced by a profound sense of peace and serenity.',
    'The majestic lighthouse stood sentinel on the rocky cliff, its brilliant beacon guiding mariners safely through '
    'the treacherous waters below. For generations, the lighthouse keeper had diligently maintained the light, '
    'ensuring that its reassuring glow never wavered, even during the most ferocious storms. As he climbed the '
    'spiraling staircase each evening, the keeper was acutely aware of the immense responsibility that rested upon '
    'his shoulders. The lives of countless sailors depended on his unwavering dedication to his duties. It was a '
    'legacy he bore with immense pride, knowing that he played a vital role in safeguarding the seafaring community '
    'that had come to rely on the steadfast presence of the lighthouse and its devoted keeper.',
]

mistakes = 0
timer_running = False
keypress_run = False

text = random.choice(texts)
split_point = 0

# DPI Improvement
ctypes.windll.shcore.SetProcessDpiAwareness(1)


# Functions ----------------------------------------------------------

# Define flicker border that will act as writing marker
def write_marker():
    # Get current container background color
    current_color = left_container.cget("bg")

    # Set a conditional coloring
    new_color = "black" if current_color == "white" else "white"

    # Set the current color
    left_container.config(bg=new_color, borderwidth=1, border=1)

    # repeat
    root.after(500, write_marker)


# Start button function
def start_test():
    global timer_running, keypress_run
    if not timer_running:
        timer_running = True
        write_marker()
        countdown(timer, 60)
        if not keypress_run:
            keypress_run = True
            root.bind('<Key>', keypress)


# Timer
def countdown(clock_label, total_secs):
    global timer_running, mistakes, text_left, keypress_run

    # If time's up
    if total_secs == 0:
        clock_label.bell()
        root.unbind('<Key>')
        text_res = text_left.cget('text')
        text_res = len(text_res.split(' ')) - 9
        clock_label.config(text=f"you had {mistakes} mistakes and got {text_res} words", font=("arial", 22, "normal"))
        timer_running = False
        keypress_run = False
        return

    # Calculate minutes and seconds
    minutes, seconds = divmod(total_secs, 60)
    clock_label.config(text=f'Time Left: {minutes:02}:{seconds:02}')

    root.after(1000, countdown, clock_label, total_secs - 1)


# Define the binding event with conditional moving and coloring text
def keypress(event=None):
    global mistakes, keypress_run
    keypress_run = True

    try:
        if event.char.lower() == text_right.cget('text')[0].lower():

            # Deleting one from the right side.
            text_right.configure(text=text_right.cget('text')[1:])

            # Adding one to the left side.
            text_left.configure(text=text_left.cget('text') + event.char.lower())

            # set the next text letter
            current_letter.configure(text=text_right.cget('text')[0], foreground='blue')
        else:
            current_letter.bell()
            current_letter.configure(foreground='red')
            mistakes += 1
    except TclError:
        pass


# Window settings ----------------------------------------------------------
root = Tk()
root.minsize(1000, 650)
root.config(bg='white')
root.title("Writing Speed Checker")

# Image
image_a = PhotoImage(file='typingspeed.png')

# Frame layout ----------------------------------------------------------
img_frame = Frame(root)
top_frame = Frame(root, background='white')
test_frame = Frame(root)
left_container = Frame(test_frame, height=66, background='white')
bottom_frame = Frame(root, background='white')

# Widgets ----------------------------------------------------------
image = Label(img_frame,
              image=image_a,
              background='white'
              )
t_button = Button(top_frame,
                  text="Start Timer",
                  command=start_test,
                  background='white',
                  font=("Tekton Pro Cond", 35, "bold"),
                  foreground='green',
                  relief='solid'
                  )
text_left = Label(left_container,
                  text='         ' + text[0:split_point],
                  font=("Consolas", 40, "bold"),
                  foreground='grey',
                  background='white'
                  )
text_right = Label(test_frame,
                   text=text[split_point:],
                   font=("Consolas", 40, "bold"),
                   background='white'
                   )
current_letter = Label(test_frame,
                       text=text[split_point],
                       font=("Consolas", 40, "bold"),
                       background='white',
                       )
timer = Label(bottom_frame,
              text=f"01:00",
              font=("arial", 30, "bold"),
              background='white'
              )

# Layout ----------------------------------------------------------
img_frame.pack(side='right', fill='x')
top_frame.pack(side='top', fill='x', pady=(70, 20))
test_frame.pack(side='top', fill='x', pady=100, padx=30)
left_container.pack(fill='x', padx=(0, 2))
bottom_frame.pack(fill='x')

image.pack()
t_button.pack()
text_left.place(relx=0.5, rely=0.5, anchor="e")
text_right.place(relx=0.5, rely=0.5, anchor="w")
current_letter.place(relx=0.5, rely=0.5, anchor="w")
timer.pack()


root.mainloop()
