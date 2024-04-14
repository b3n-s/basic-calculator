import PySimpleGUI as sg
from collections import deque
import math

def shunting_yard(input_string):
    stack = deque()
    output_queue = deque()
    
    precedence = {'+': 2, '-': 2, '*': 3, '/': 3, '^': 4}
    associativity = {'+': 'L', '-': 'L', '*': 'L', '/': 'L', '^': 'R'}
    tokens = input_string.split()

    for token in tokens:
        if token.isdigit():
            output_queue.append(token)
        elif token in precedence:
            while (stack and stack[-1] != '(' and 
                  (precedence[stack[-1]] > precedence[token] or
                   (precedence[stack[-1]] == precedence[token] and associativity[token] == 'L'))):
                output_queue.append(stack.pop())
            stack.append(token)
        elif token == '(':
            stack.append(token)
        elif token == ')':
            while stack and stack[-1] != '(':
                output_queue.append(stack.pop())
            stack.pop()

    while stack:
        output_queue.append(stack.pop())

    return list(output_queue)


def evaluate_postfix(postfix_tokens):
    stack = []

    for token in postfix_tokens:
        if token.isdigit():
            stack.append(int(token))
        else:
            print(stack)
            b, a = stack.pop(), stack.pop()
            if token == '+':
                stack.append(a + b)
            elif token == '-':
                stack.append(a - b)
            elif token == '*':
                stack.append(a * b)
            elif token == '/':
                if b != 0:
                    stack.append(a / b)
                else:
                    return "Error: Division by zero"
            elif token == '^':
                stack.append(math.pow(a, b))
                

    return stack.pop()

sg.theme('DarkBlue')

layout = [
    [sg.Input(key='-IN-', size=(25, 1), justification='right', text_color='white', background_color='black')],
    [sg.Button('C', button_color=('white', 'red'))],
    [sg.Button('7',button_color=('white', 'blue')), sg.Button('8', button_color=('white', 'blue')), sg.Button('9', button_color=('white', 'blue')), sg.Button('/')],
    [sg.Button('4', button_color=('white', 'blue')), sg.Button('5', button_color=('white', 'blue')), sg.Button('6', button_color=('white', 'blue')), sg.Button('*')],
    [sg.Button('1', button_color=('white', 'blue')), sg.Button('2', button_color=('white', 'blue')), sg.Button('3', button_color=('white', 'blue')), sg.Button('-')],
    [sg.Button('0', button_color=('white', 'blue')), sg.Button('.'), sg.Button('='), sg.Button('+')],
    [sg.Text('Result:'), sg.Text(size=(20, 1), key='-OUTPUT-', text_color='yellow')],
]


window = sg.Window("Basic Calculator", layout, resizable=True)

while True:
    event, values = window.read()
    if event in (sg.WINDOW_CLOSED, "Cancel"):
        break

    if event in list(map(str, range(0, 10))) + ["+", "-", "*", "/", "^"]:
        current_input = values['-IN-']
        if event in ["+", "-", "*", "/", "^"]:
            if current_input and not current_input.endswith(' '):
                event = ' ' + event
            event += ' '
        updated_input = current_input + event
        window['-IN-'].update(updated_input)

    elif event == "=":
        input_string = values['-IN-'].strip()
        postfix = shunting_yard(input_string)
        result = evaluate_postfix(postfix)
        window['-OUTPUT-'].update(f'{result}')
        
    elif event == "C":
        window['-IN-'].update('')
        window['-OUTPUT-'].update('0')
    

window.close()