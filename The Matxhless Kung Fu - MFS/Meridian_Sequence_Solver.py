#Original script made by Lemiru, i just changed some things and put a GUI on it. All credit goes to Lemiru.
#This script sorts your inner kung fu in the shortest possible path for your meridian sequence.
#You select which abilities you want in the list and click ok, if you reach over 45 you will get
#a message saying it dint work, 45 is currently the max length of your meridian sequence.

import os
import pandas as pd
from itertools import permutations
from tkinter import Tk, Button, Label, Listbox, Scrollbar, filedialog, END, Text, DISABLED, NORMAL, font

max_length = 45

def check_substring(a, b):
    if not a or not b:
        return b or a
    if b in a:
        return a
    for i in range(1, len(b)):
        if a[len(a) - i:] == b[:i]:
            return a + b[i:]
    return a + b

def shortest_substring(a, b):
    x = check_substring(a, b)
    return x


def shortest_sequence_in_order(incomplete_sequence, text_result_widget):
    sequence = incomplete_sequence[0]
    sequences_to_add = incomplete_sequence[1]
    for seq in sequences_to_add:
        common_prefix = os.path.commonprefix([sequence[::-1], seq[::-1]])
        sequence = sequence + seq[len(common_prefix):]

    # Show the debug information directly in the text_result_widget
    text_result_widget.config(state=NORMAL)
    text_result_widget.insert(END, f"Result after processing: {sequence} ")
    text_result_widget.see(END)  # Scroll to the end
    text_result_widget.config(state=DISABLED)

    return sequence


def process_selected_sequences(selected_sequences, text_result, listbox, debug_text_widget):
    required_sequences = selected_sequences
    temp = [x for x in required_sequences if not any(x in y for y in required_sequences if x != y)]
    required_sequences = temp
    all_sequence_orders = permutations(required_sequences)
    found_sequences = []  # Use a list to store sequences
    processed_sequences = set()  # Use a set to store processed sequences

    for sequence_order in all_sequence_orders:
        processed_sequence_order = tuple(sorted(sequence_order))
        if processed_sequence_order in processed_sequences:
            continue  # Skip if sequence order has already been processed

        debug_text_widget.config(state=NORMAL)
        debug_text_widget.insert(END, f"Checking sequence order: {sequence_order}\n")
        debug_text_widget.see(END)  # Scroll to the end
        debug_text_widget.config(state=DISABLED)

        result = shortest_sequence_in_order((sequence_order[0], list(sequence_order[1:])), debug_text_widget)
        if len(result) < max_length and result not in found_sequences:
            debug_text_widget.config(state=NORMAL)
            debug_text_widget.insert(END, f"Adding result to found sequences: {result}\n")
            debug_text_widget.see(END)  # Scroll to the end
            debug_text_widget.config(state=DISABLED)
            found_sequences.append(result)  # Use list append() method

        processed_sequences.add(processed_sequence_order)  # Mark the processed sequence

    # Filter out duplicate sequences
    unique_sequences = list(set(found_sequences))

    if unique_sequences:
        unique_sequences = sorted(unique_sequences, key=lambda x: len(x))
        shortest_len = len(unique_sequences[0])
        result_text = f'Shortest sequences (length of {shortest_len}) found:\n\n'
        for sequence in unique_sequences:
            truncated_result = format_result(sequence, max_length=45)
            result_text += truncated_result + '\n'
    else:
        result_text = 'No sequences found'

    text_result.config(state=NORMAL)
    text_result.delete(1.0, END)
    text_result.insert(END, result_text)
    text_result.config(state=DISABLED)

def format_result(sequence, max_length=45):
    # Replace 'O' with a circle, 'A' with a triangle, and 'N' with a square
    formatted_sequence = sequence.replace('O', '⭕').replace('A', '▲').replace('N', '■')
    truncated_sequence = formatted_sequence[:max_length]

    if len(sequence) > max_length:
        truncated_sequence += f'... and more'

    return truncated_sequence

# Automatically choose 'inner.csv' in the current directory
csv_path = 'Sequences.csv'

# GUI setup
root = Tk()
root.title("Meridian Sequence Solver")

# Create a text widget for debug information
debug_text_widget = Text(root, wrap="word", height=10, width=70, font=("Helvetica", 10))

# Hide the debug window initially
debug_text_widget.pack_forget()

# Global variable to keep track of debug visibility (disabled by default)
debug_visible = True

def toggle_debug():
    global debug_visible
    debug_visible = not debug_visible

    if debug_visible:
        debug_text_widget.pack()
    else:
        debug_text_widget.pack_forget()

# Create a button to toggle debug visibility
toggle_debug_button = Button(root, text="Toggle Debug", command=toggle_debug)
toggle_debug_button.pack()

label = Label(root, text="Select desired sequences:")
label.pack()

listbox = Listbox(root, selectmode="multiple", exportselection=False)
scrollbar = Scrollbar(root, command=listbox.yview)
scrollbar.pack(side="right", fill="y")
listbox.config(yscrollcommand=scrollbar.set)

df = pd.read_csv(csv_path, index_col=0, names=['Sequence'])
for seq_name in df.index:
    listbox.insert(END, seq_name)

listbox.pack()
debug_text_widget = Text(root, wrap="word", height=10, width=70, font=("Helvetica", 10))
debug_text_widget.pack()

result_text = Text(root, wrap="word", height=5, width=42, font=("Helvetica", 12))
result_text.pack()

def on_ok_button():
    selected_indices = listbox.curselection()
    selected_sequences = [df.at[df.index[index], 'Sequence'] for index in selected_indices]
    process_selected_sequences(selected_sequences, result_text, listbox, debug_text_widget)

ok_button = Button(root, text="OK", command=on_ok_button)
ok_button.pack()



root.mainloop()
