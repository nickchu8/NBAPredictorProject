import PySimpleGUI as sg
from tensorflow import keras
from keras import datasets, layers, models
from scipy.signal import convolve2d

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

    # ask for number of layers, then for each layer have a dropdown for like different types of layers to use

    # layout = [  [sg.Text('Season Selection', font = ('Arial', 16))],
    #             [sg.Text('Season')],
    #             [sg.Combo(['2000','2001','2002','2003','2004','2005','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015',
    #                     '2016','2017','2018','2019','2020','2021','2022'], key = 'season')],
    #             [sg.HorizontalSeparator()],

    #             [sg.Text('Network Parameters', font = ("Arial", 16))],
    #             [sg.Text('Hidden layer size'), sg.InputText(size=(3, 1), key = 'hiddensize'), sg.Text('Number of hidden layers'), sg.InputText(size=(3, 1), key = 'hiddenlayers')],
    #             [sg.Text('Activation Function')],
    #             [sg.Combo(['ReLU', 'Sigmoid', 'Linear', 'Logistic'], key='activation')],
    #             [sg.HorizontalSeparator()],

    #             [sg.Text('Loss Functions', font = ("Arial", 16))],
    #             [sg.Radio('Cross Entropy', 'radio_group', default=True, key='crossentropy'), sg.Radio('Logistic', 'radio_group', key='logistic')],
    #             [sg.Radio('Hinge', 'radio_group', key='hinge'), sg.Radio('Huber', 'radio_group', key='huber')],
    #             [sg.HorizontalSeparator()] ,

    #             [sg.Button('Submit'), sg.Button('Cancel')],
    #             ]

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
                [sg.HorizontalSeparator()],

                [sg.Text('Loss Functions', font = ("Arial", 16))],
                [sg.Radio('Cross Entropy', 'radio_group', default=True, key='crossentropy'), sg.Radio('Logistic', 'radio_group', key='logistic')],
                [sg.Radio('Hinge', 'radio_group', key='hinge'), sg.Radio('Huber', 'radio_group', key='huber')],
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

                # if layer_config['type'] == 'Dropout':
                #     dropout_rate_str = sg.popup_get_text(f'Enter Dropout Rate for Layer {i + 1}:', default_text='', title='Dropout Rate Input')
                #     layer_config['dropout_rate'] = float(dropout_rate_str) if dropout_rate_str else 0.0
                #     # dropout_rate_str = values.get(f'-LAYER_{i + 1}_DROPOUT-', '')
                #     # layer_config['dropout_rate'] = float(dropout_rate_str) if dropout_rate_str else 0.0
                # elif layer_config['type'] == 'Conv2D':
                #     kernel_size_str = values.get(f'-LAYER_{i + 1}_KERNEL_SIZE-', '')
                #     layer_config['kernel_size'] = int(kernel_size_str) if kernel_size_str else 3  # Default kernel size


                hidden_layer_configurations.append(layer_config)
            
            # for i in range(num_hidden_layers):
            #     layer_type = values.get(f'-LAYER_{i + 1}_TYPE-', '')  # Use get with a default value of ''
            #     window[f'-LAYER_{i + 1}_DROPOUT-'].update(visible=layer_type == 'Dropout')
            #     window[f'-LAYER_{i + 1}_KERNEL_SIZE-'].update(visible=layer_type == 'Conv2D')

            season = values['season']
            if values['crossentropy'] == True: lossfunction = 'Cross Entropy'
            if values['logistic'] == True: lossfunction = 'Logistic'
            if values['hinge'] == True: lossfunction = 'Hinge'
            if values['huber'] == True: lossfunction = 'Huber'
            break


    window.close()
    #after getting data, instead of building a dictionary, build a keras model
    # first layer should be input 
    model = models.Sequential()
    params_dict = {"Season": season,
                    "loss function": lossfunction}


    # Construct the Keras Sequential model
    model = models.Sequential()

    #add input layer with shape 26
    model.add(layers.InputLayer(input_shape = (26,)))

        # Add the specified hidden layers
    for layer_config in hidden_layer_configurations:
        #layer_type = layer_config['type']
        layer_size = layer_config['size']
        activation_function = layer_config['activation']

        #if layer_type == 'Dense':
        #want to be abel to create layers with and without activation functions
        if (activation_function == "linear"):
            model.add(layers.Dense(units = layer_size))
        else:
            model.add(layers.Dense(units = layer_size, activation=activation_function))
        # elif layer_type == 'Dropout':
        #     model.add(layers.Dropout(0.5))  # You might want to customize the dropout rate
        # elif layer_type == 'Conv2D':
        #     model.add(layers.Conv2D(layer_size, kernel_size=(3, 3), activation=activation_function))  # You might want to customize the kernel size
        # elif layer_type == 'Flatten':
        #     model.add(layers.Flatten())

    # Add the output layer
    model.add(layers.Dense(2))  # You can customize the output layer as needed

    # Build the model
    input_size = 26
    #model.build(input_shape=(None, input_size))  # Replace input_size with the appropriate input size for your data

    # Display the model summary
    model.summary()

    return model, params_dict