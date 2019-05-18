import PySimpleGUI as sg

def ecobinGUI(percentage = 50, x = "Trash"):
    sg.ChangeLookAndFeel('GreenTan')

    # ------ Menu Definition ------ #
    menu_def = [['File', ['Open', 'Save', 'Exit', 'Properties']],
                ['Edit', ['Paste', ['Special', 'Normal', ], 'Undo'], ],
                ['Help', 'About...'], ]

    # ------ Column Definition ------ #
    column1 = [[sg.Text('Column 1', background_color='#F7F3EC', justification='center', size=(10, 1))],
               [sg.Spin(values=('Spin Box 1', '2', '3'), initial_value='Spin Box 1')],
               [sg.Spin(values=('Spin Box 1', '2', '3'), initial_value='Spin Box 2')],
               [sg.Spin(values=('Spin Box 1', '2', '3'), initial_value='Spin Box 3')]]
    
    #Select the percentage
    n = percentage;
    
    #Select the object type
    if(x == 'Recyclable'):
        a = 'Recyclable'
        b = 'Trash'
    else:
        a = 'Trash'
        b = 'Recylable'
    
    #Layout Design
    layout = [
        [sg.Menu(menu_def, tearoff=True)],
        [sg.Text('Ecobin Classifier!', size=(30, 1), justification='center', font=("Helvetica", 25), relief=sg.RELIEF_RIDGE)],
        [sg.Text('Classification results')],
        [sg.InputText('Trash vs  Recyclable')],

        [sg.InputCombo((a,b), size=(20, 1)),
         sg.Slider(range=(1, 100), orientation='h', size=(34, 20), default_value=n)],

    ]


    window = sg.Window('ECOBIN', default_element_size=(40, 1), grab_anywhere=False).Layout(layout)

    event, values = window.Read()

    sg.Popup('Title',
             'The results of the window.',
             'The button clicked was "{}"'.format(event),
             'The values are', values)


