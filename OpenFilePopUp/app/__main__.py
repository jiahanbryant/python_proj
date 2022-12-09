import PySimpleGUI as sg
#sg.theme('DarkAmber')   # Add a little color to your windows
# All the stuff inside your window. This is the PSG magic code compactor...
layout = [  [sg.Text('Get file path and print its content')],
            [[sg.Text('Filename')], [sg.Input(sg.user_settings_get_entry('-filename-', ''), key='-FILEPATH-'), sg.FileBrowse()]],
            [sg.OK(), sg.Cancel()]]

# Create the Window
window = sg.Window('Window Title', layout)
# Event Loop to process "events"
def main() -> None:
    while True:             
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Cancel'):
            break
        elif event == 'OK':
            sg.user_settings_set_entry('-filename-', values['-FILEPATH-'])
            file = values['-FILEPATH-']
            try:
                with open(file, 'r+') as f:
                    print(f.read())
                    f.close()
                break
            except FileNotFoundError:
                window['-FILEPATH-'].update(f"Enter a valid file name here", text_color="Red")

    window.close()

if __name__ == "__main__":
    main()
    