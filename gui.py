import PySimpleGUI as sg
from tensorflow import keras
from keras import datasets, layers, models

# Based on https://www.pysimplegui.org/en/latest/cookbook/#recipe-pattern-2a-persistent-window-multiple-reads-using-an-event-loop

#WHAT TO WORK ON:
# Incorporate the datetime stuff into the season selection

#Set a color scheme for the window
# https://www.pysimplegui.org/en/latest/cookbook/#themes-window-beautification
def create_model_gui():
    '''
    Gui that allows user to choose the season data and parameters for keras neural network model
    '''

    sg.theme('BlueMono')

    num_hidden_layers = 1  # Default number of hidden layers
    layout = [ 
                [sg.Text('Network Parameters', font = ("Arial", 16))],
                [sg.Text('Number of Hidden Layers:'), sg.Input(key='-NUM_LAYERS-', default_text=num_hidden_layers, size=(5, 1)), sg.Button('Update')],
                [sg.Text('Hidden Layers Configuration:')]
                
                ]


    # Create the Window
    # Event Loop to process "events" and get the "values" of the inputs
    season = ""
    lossfunction = ""

    while True:
        window = sg.Window('Neural Network Constructor', layout, resizable=True)
        # Read in any events and the current state of the window
        event, values = window.read()
        # If we eclosed the window or clicked the Cancel button, break out of the
        # loop
        if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
            break
        # Season and Training Data Selection
        #assign season

        #assign training data type
        elif event == "Update": 
            num_hidden_layers = int(values['-NUM_LAYERS-'])
            window.close()

            layout = [
            [sg.Text('Number of Hidden Layers:'), sg.Input(key='-NUM_LAYERS-', default_text=num_hidden_layers, size=(5, 1)), sg.Button('Update')],
            [sg.Text('Hidden Layer Configurations:')],
            
            ]

            for i in range(num_hidden_layers):
                layout.append([
                sg.Text(f'Layer {i + 1} Size:'),
                sg.Input(key=f'-LAYER_{i + 1}_SIZE-', size=(10, 1)),
                #sg.Text('Layer Type:'),
                #sg.Combo(['Dense', 'Dropout', 'Conv2D', 'Flatten'], key=f'-LAYER_{i + 1}_TYPE-', default_value='Dense'),
                sg.Text('Activation Function:'),
                sg.Combo(['linear','relu', 'sigmoid','logistic', 'softmax'], key=f'-LAYER_{i + 1}_ACTIVATION-', default_value='relu'),
                # sg.Text('Dropout Rate:'),
                # sg.Input(key=f'-LAYER_{i + 1}_DROPOUT-', size=(5, 1), visible=False),
                # sg.Text('Conv2D Kernel Size:'),
                # sg.Input(key=f'-LAYER_{i + 1}_KERNEL_SIZE-', size=(5, 1), visible=False),
                # sg.Button(f'-LAYER_{i + 1}_DROPOUT_BTN-', visible=False)  # Button to open input box for dropout rate
                ])

            # after asking for the , add the other stuff
            layout += [
                [sg.Text('Season Selection', font = ('Arial', 16))],
                [sg.Text('Season')],
                [sg.Combo(['2000-2001','2001-2002','2002-2003','2003-2004','2004-2005','2005-2006',
                           '2006-2007','2007-2008','2008-2009','2009-2010','2010-2011','2011-2012',
                           '2012-2013','2013-2014','2014-2015','2015-2016',
                        '2016-2017','2017-2018','2018-2019','2019-2020','2020-2021','2021-2022','2022-2023'], key = 'season')],
                [sg.HorizontalSeparator()] ,

            ]
            layout.append([sg.Button('Submit')])
        
        # If user presses "Ok", then set values to the dictionary
        elif event == "Submit":
            # Process the entered values
            hidden_layer_configurations = []
            for i in range(num_hidden_layers):
                layer_config = {
                'size': int(values[f'-LAYER_{i + 1}_SIZE-']),
                #'type': values[f'-LAYER_{i + 1}_TYPE-'],
                'activation': values[f'-LAYER_{i + 1}_ACTIVATION-']
                }   


                hidden_layer_configurations.append(layer_config)

            season = values['season']
            break


    window.close()
    #after getting data, instead of building a dictionary, build a keras model
    # first layer should be input 
    model = models.Sequential()


    # Construct the Keras Sequential model
    model = models.Sequential()

    #add input layer with shape 26
    model.add(layers.InputLayer(input_shape = (26,)))

        # Add the specified hidden layers
    for layer_config in hidden_layer_configurations:
        layer_size = layer_config['size']
        activation_function = layer_config['activation']

        #want to be able to create layers with and without activation functions
        if (activation_function == "linear"):
            model.add(layers.Dense(units = layer_size))
        else:
            model.add(layers.Dense(units = layer_size, activation=activation_function))

    # Add the output layer
    model.add(layers.Dense(1, activation='sigmoid'))  # You can customize the output layer as needed

    # Display the model summary
    model.summary()

    return model, season