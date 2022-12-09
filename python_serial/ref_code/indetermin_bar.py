import PySimpleGUI as sg

window = sg.Window('test', layout=[[sg.ProgressBar(max_value=100, size=(30, 10), key='bar', metadata=5)]], finalize=True)

window['bar'].Widget.config(mode='indeterminate')

while True:
    if window(timeout=100)[0] is None:
        break
    window['bar'].Widget['value'] += window['bar'].metadata