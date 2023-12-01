import PySimpleGUI as sg
# Based on https://www.pysimplegui.org/en/latest/cookbook/#recipe-pattern-2a-persistent-window-multiple-reads-using-an-event-loop



#Set a color scheme for the window
# https://www.pysimplegui.org/en/latest/cookbook/#themes-window-beautification
sg.theme('BlueMono')


layout = [  [sg.Text('Season and Training Data Selection', font = ('Arial', 16))],
            [sg.Text('Season')],
            [sg.Combo(['2000','2001','2002','2003','2004','2005','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015',
                       '2016','2017','2018','2019','2020','2021','2022'], key = 'season')],
            [sg.Text('Training Data Type:')],
            [sg.Radio('Individual games', 'training', default = True, key = "games"), sg.Radio('Season data', 'training', key = "season")],
            [sg.HorizontalSeparator()],

            [sg.Text('Network Parameters', font = ("Arial", 16))],
            [sg.Text('Input layer size'), sg.InputText(size=(3, 1), key = 'inputsize')],
            [sg.Text('Hidden layer size'), sg.InputText(size=(3, 1), key = 'hiddensize'), sg.Text('Number of hidden layers'), sg.InputText(size=(3, 1), key = 'hiddenlayers')],
            [sg.Text('Activation Function')],
            [sg.Combo(['ReLU', 'Sigmoid', 'Linear', 'Logistic'], key='activation')],
            [sg.HorizontalSeparator()],

            [sg.Text('Loss Functions', font = ("Arial", 16))],
            [sg.Radio('Cross Entropy', 'radio_group', default=True, key='crossentropy'), sg.Radio('Logistic', 'radio_group', key='logistic')],
            [sg.Radio('Hinge', 'radio_group', key='hinge'), sg.Radio('Huber', 'radio_group', key='huber')],
            [sg.HorizontalSeparator()] ,

            [sg.Button('Submit'), sg.Button('Cancel')],
             ]

# Create the Window
window = sg.Window('Window Title', layout)
# Event Loop to process "events" and get the "values" of the inputs

output = ""
season = ""
trainingtype = ""
inputsize = ""
hiddensize = ""
hiddenlayers = ""
activation = ""
lossfunction = ""

while True:
    # Read in any events and the current state of the window
    event, values = window.read()
    # If we eclosed the window or clicked the Cancel button, break out of the
    # loop
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break
    # Season and Training Data Selection
    #assign season

    #assign training data type
    
    # If user presses "Ok"
    if event == "Submit":
        season = values['season']
        #trainingtype
        if values['games'] == True: trainingtype = "Individual games"
        else: trainingtype = 'Season data'
        inputsize = values['inputsize']
        hiddensize = values['hiddensize']
        hiddenlayers = values['hiddenlayers']
        activation = values['activation']
        if values['crossentropy'] == True: lossfunction = 'Cross Entropy'
        if values['logistic'] == True: lossfunction = 'Logistic'
        if values['hinge'] == True: lossfunction = 'Hinge'
        if values['huber'] == True: lossfunction = 'Huber'

        break


window.close()
print(season)
print(trainingtype)
print(inputsize)
print(hiddensize)
print(hiddenlayers)
print(activation)
print(lossfunction)