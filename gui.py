import FreeSimpleGUI as sg
from tensorflow import keras
from keras import layers, models

def create_model_gui():
    '''
    Gui that allows user to choose the season data and parameters for keras neural network model
    '''

    sg.theme('BlueMono')

    num_hidden_layers = 1  # Default number of hidden layers
    layout = [[sg.Text('Network Parameters', font = ("Arial", 16))],
              [sg.Text('Number of Hidden Layers:'), sg.Input(key='-NUM_LAYERS-', default_text=num_hidden_layers, size=(5, 1)), sg.Button('Update')],
              [sg.Text('Hidden Layers Configuration:')]
              ]


    # Create the Window
    # Event Loop to process "events" and get the "values" of the inputs
    season = ""

    while True:
        window = sg.Window('Neural Network Constructor', layout, resizable=True)
        # Read in any events and the current state of the window
        event, values = window.read()
        # close window or cancel => break loop
        if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
            break

        # Season and hidden layer customization
        elif event == "Update": 
            num_hidden_layers = int(values['-NUM_LAYERS-'])
            window.close()
            
            layout = [
            [sg.Text('Number of Hidden Layers:'), sg.Input(key='-NUM_LAYERS-', default_text=num_hidden_layers, size=(5, 1)), sg.Button('Update')],
            [sg.Text('Hidden Layer Configurations:')],
            
            ]
            # customize hidden layer units and activation functions
            for i in range(num_hidden_layers):
                layout.append([
                sg.Text(f'Layer {i + 1} Size:'),
                sg.Input(key=f'-LAYER_{i + 1}_SIZE-', size=(10, 1)),
                sg.Text('Activation Function:'),
                sg.Combo(['linear','relu', 'sigmoid','logistic', 'softmax'], key=f'-LAYER_{i + 1}_ACTIVATION-', default_value='relu'),
                ])

            # select season
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
        
        # User presses "Ok" = done building model => set values to dictionary
        elif event == "Submit":
            # Process the entered values
            hidden_layer_configurations = []
            for i in range(num_hidden_layers):
                layer_config = {
                'size': int(values[f'-LAYER_{i + 1}_SIZE-']),
                'activation': values[f'-LAYER_{i + 1}_ACTIVATION-']
                }

                hidden_layer_configurations.append(layer_config)

            season = values['season']
            break

    window.close()
    # Construct the Keras Sequential model
    model = models.Sequential()
    #add input layer with shape 26
    model.add(layers.InputLayer(input_shape = (26,)))

    # Add the specified hidden layers
    for layer_config in hidden_layer_configurations:
        layer_size = layer_config['size']
        activation_function = layer_config['activation']
        # create layers with/without activations
        if (activation_function == "linear"):
            model.add(layers.Dense(units = layer_size))
        else:
            model.add(layers.Dense(units = layer_size, activation=activation_function))

    # Add the output layer
    model.add(layers.Dense(1, activation='sigmoid')) # win probability between 0 and 1

    # Display the model summary
    model.summary()

    return model, season