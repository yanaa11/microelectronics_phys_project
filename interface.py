import PySimpleGUI as sg 
from matplotlib.ticker import NullFormatter  # useful for `logit` scale
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
matplotlib.use('TkAgg')

def draw_figure(ax, figure_canvas_agg, values):
    """
    Redraw plot for each new event.
    
    {ax} is responsible for adjusting of the plot
    
    {figure_canvas_agg} helps draw plot in the window-interface
    
    {values} are data in the window-interface. They update each time when event happens
    """
    a = float(values['-IN1-']) * 0.1
    b = float(values['-IN2-']) * 0.1
    c = float(values['-IN3-']) * 0.1
    """
    t, func = calculatingModule.calculate(values['-IN1-'], values['-IN2-'], ...)
    fig.add_subplot(111).plot(t, func)
    """
    
    # clear figure from plot 
    ax.cla()                 
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.grid()
    
    t = np.arange(0, 10, .01)
    ax.plot(t, a*np.sin(t + b) + c)
    
    figure_canvas_agg.draw()

# set theme for the window-interface
sg.theme('LightGrey2') 

# define layout

# define plot column for layout

plot_col =      [
                    [sg.Canvas(key='-CANVAS-', size=(640, 640))],
                    [sg.Text('Legend', size=(50, 10))],
                ]

# define settings column for layout

settings_col =  [
                    [sg.Text('Settings', size=(10, 1))],
                    [sg.Slider(key='SL1', range=(1, 100), orientation='h', size=(15, 20), default_value=1, enable_events=True)],
                    [sg.Input('1.0', key='-IN1-', size=(10, 1), border_width=1.5, font=("Helvetica", 20), pad=(5,20))],
                    [sg.Slider(key='SL2', range=(1, 100), orientation='h', size=(15, 20), default_value=1, enable_events=True)],
                    [sg.Input('1.0', key='-IN2-', size=(10, 1), border_width=1.5, font=("Helvetica", 20), pad=(5,20))],
                    [sg.Slider(key='SL3', range=(1, 100), orientation='h', size=(15, 20), default_value=1, enable_events=True)],
                    [sg.Input('1.0', key='-IN3-', size=(10, 1), border_width=1.5, font=("Helvetica", 20), pad=(5,20))],
                    [sg.Button('Draw', key='Draw', size=(8, 1))]
                ]

# define whole layout
layout =    [
                [sg.Column(plot_col, vertical_alignment='top', justification='C', expand_x=True, size=(800, 800)),
                 sg.VerticalSeparator(color='006699', pad=(10, 0)),
                 sg.Column(settings_col, vertical_alignment='top', justification='C', size=(400, 800))],
            ]

# Create interface-window
window = sg.Window('Pinning of Fermi Level', layout, finalize=True, resizable=True, size=(1200, 800), location=(0, 0))

# Create figure for plotting
fig = matplotlib.figure.Figure(figsize=(8, 6), dpi=100)
ax = fig.add_subplot(111)
# Create canvas that we can display matplotlib graph in the interface
figure_canvas_agg = FigureCanvasTkAgg(fig, window['-CANVAS-'].TKCanvas)
# Adjust placement of the canvas
figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)

# handling of events
while True:  # Event Loop
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == 'SL1' or event == 'SL2' or event == 'SL3':
        window['-IN1-'].update(values['SL1'])
        window['-IN2-'].update(values['SL2'])
        window['-IN3-'].update(values['SL3'])
        draw_figure(ax, figure_canvas_agg, values)
    if event == 'Draw':
        window['SL1'].update(values['-IN1-'])
        window['SL2'].update(values['-IN2-'])
        window['SL3'].update(values['-IN3-'])
        draw_figure(ax, figure_canvas_agg, values)
window.close()
