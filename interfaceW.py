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
    band_gap = float(values['-IN1-'])  # Band gap [eV]
    donor_level = float(values['-IN2-'])  # Donors level [eV]
    donor_conc = float(values['-IN3-'])  # Concentration of donors 10^27 [cm^(-3)]
    surf_accept_level = float(values['-IN4-'])  # Surface acceptors level [eV]
    surf_accept_conc = float(values['-IN5-'])  # Concentration of surface acceptors 10^27 [cm^(-3)]
    eff_el_mass = float(values['-IN6-'])  # Effective electron mass [m_0]
    eff_hole_mass = float(values['-IN7-'])  # Effective hole mass [m_0]
    diel_permittivity = float(values['-IN8-'])  # Dielectric permittivity
    temperature = float(values['-IN9-'])  # Temperature [K]
    external_el_field = float(values['-IN10-'])  # External electric field
    """
    t, func = calculatingModule.calculate(values['-IN1-'], values['-IN2-'], ...)
    fig.add_subplot(111).plot(t, func)
    """
    # a,b,c after connection of the calculate module should be deleted
    a = band_gap * 0.1
    b = donor_level * 0.1
    c = donor_conc * 0.1

    # clear figure from plot
    ax.cla()
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.grid()

    t = np.arange(0, 10, .01)
    ax.plot(t, a * np.sin(t + b) + c)

    figure_canvas_agg.draw()


# set theme for the window-interface
sg.theme('LightGrey2')

# define layout

# define plot column for layout

plot_col = \
    [
        [sg.Canvas(key='-CANVAS-', size=(640, 640))],
        [sg.Text('Legend', size=(50, 10))],
    ]

# define settings column for layout
"""
Adjusting of the settings column
{pfr} - padding from frame ((left, right), (top, bottom))
{nps} - name parameters size (width, high) in characters
{font} - font of scriptions
{sinp} - size of input block (width, high) in characters
{ssld} - size of slider (width, high) in characters
{sphp} - size of physical parameters (width, high) in characters
{pinp} - padding from the input block ((left, right), (top, bottom))
{bw} - border width of the input block
"""
pfr = ((0, 0), (0, 25))
nps = (30, 1)
font = ("Helvetica", 10)
ssld = (25, 10)
sinp = (5, 1)
sphp = (15, 1)
pinp = ((35, 0), (0, 0))
bw = 1.5

settings_col = \
    [
        # 1. Bad gap Row
        [sg.Frame('', border_width=0, pad=pfr, layout=[[
            sg.Text('Band gap:', nps, font=font),
            sg.Slider(key='SL1', range=(1, 100), orientation='h', size=ssld, default_value=1, enable_events=True),
            sg.Input('1.0', key='-IN1-', size=sinp, border_width=bw, font=font, pad=pinp),
            sg.Text('[eV]', size=sphp, font=font),
        ]])],
        # 2. Donor level Row
        [sg.Frame('', border_width=0, pad=pfr, layout=[[
            sg.Text('Donor level:', nps, font=font),
            sg.Slider(key='SL2', range=(1, 100), orientation='h', size=ssld, default_value=1, enable_events=True),
            sg.Input('1.0', key='-IN2-', size=sinp, border_width=bw, font=font, pad=pinp),
            sg.Text('[eV]', size=sphp, font=font),
        ]])],
        # 3. Concentration of donors Row
        [sg.Frame('', border_width=0, pad=pfr, layout=[[
            sg.Text('Concentration of donors:', nps, font=font),
            sg.Slider(key='SL3', range=(1, 100), orientation='h', size=ssld, default_value=1, enable_events=True),
            sg.Input('1.0', key='-IN3-', size=sinp, border_width=bw, font=font, pad=pinp),
            sg.Text('10^27[cm^(-3)]', size=sphp, font=font),
        ]])],
        # 4. Surface acceptors level Row
        [sg.Frame('', border_width=0, pad=pfr, layout=[[
            sg.Text('Surface acceptors level:', nps, font=font),
            sg.Slider(key='SL4', range=(1, 100), orientation='h', size=ssld, default_value=1, enable_events=True),
            sg.Input('1.0', key='-IN4-', size=sinp, border_width=bw, font=font, pad=pinp),
            sg.Text('[eV]', size=sphp, font=font),
        ]])],
        # 5. Concentration of surface acceptors Row
        [sg.Frame('', border_width=0, pad=pfr, layout=[[
            sg.Text('Concentration of surface acceptors:', nps, font=font),
            sg.Slider(key='SL5', range=(1, 100), orientation='h', size=ssld, default_value=1, enable_events=True),
            sg.Input('1.0', key='-IN5-', size=(5, 10), border_width=bw, font=font, pad=pinp),
            sg.Text('10^27[cm^(-3)]', size=sphp, font=font),
        ]])],
        # 6. Effective electron mass Row
        [sg.Frame('', border_width=0, pad=pfr, layout=[[
            sg.Text('Effective electron mass:', nps, font=font),
            sg.Slider(key='SL6', range=(1, 100), orientation='h', size=ssld, default_value=1, enable_events=True),
            sg.Input('1.0', key='-IN6-', size=sinp, border_width=bw, font=font, pad=pinp),
            sg.Text('[m_0]', size=sphp, font=font),
        ]])],
        # 7. Effective hole mass Row
        [sg.Frame('', border_width=0, pad=pfr, layout=[[
            sg.Text('Effective hole mass:', nps, font=font),
            sg.Slider(key='SL7', range=(1, 100), orientation='h', size=ssld, default_value=1, enable_events=True),
            sg.Input('1.0', key='-IN7-', size=sinp, border_width=bw, font=font, pad=pinp),
            sg.Text('[m_0]', size=sphp, font=font),
        ]])],
        # 8. Dielectric permittivity Row
        [sg.Frame('', border_width=0, pad=pfr, layout=[[
            sg.Text('Dielectric permittivity:', nps, font=font),
            sg.Slider(key='SL8', range=(1, 100), orientation='h', size=ssld, default_value=1, enable_events=True),
            sg.Input('1.0', key='-IN8-', size=sinp, border_width=bw, font=font, pad=pinp),
            sg.Text('', size=sphp, font=font),
        ]])],
        # 9. Temperature Row
        [sg.Frame('', border_width=0, pad=pfr, layout=[[
            sg.Text('Temperature:', nps, font=font),
            sg.Slider(key='SL9', range=(1, 100), orientation='h', size=ssld, default_value=1, enable_events=True),
            sg.Input('1.0', key='-IN9-', size=sinp, border_width=bw, font=font, pad=pinp),
            sg.Text('[K]', size=sphp, font=font),
        ]])],
        # 10. External electric field Row
        [sg.Frame('', border_width=0, pad=pfr, layout=[[
            sg.Text('External electric field:', nps, font=font),
            sg.Slider(key='SL10', range=(1, 100), orientation='h', size=ssld, default_value=1, enable_events=True),
            sg.Input('1.0', key='-IN10-', size=sinp, border_width=bw, font=font, pad=pinp),
            sg.Text('[V/m]', size=sphp, font=font),
        ]])],
        # 11. Draw Row
        [sg.Frame('', border_width=0, pad=((0, 0), (25, 25)), layout=[[
            sg.Text('Draw plot:', font=font, pad=((550, 0), (0, 0))),
            sg.Button('Draw', key='Draw', font=font, pad=((10, 0), (0, 0)))
        ]])],
        # 11. Save Row
        [sg.Frame('', border_width=0, pad=pfr, layout=[[
            sg.Text('Save plot:', font=font, pad=((550, 0), (0, 0))),
            sg.FolderBrowse('Save', key='Save', font=font, pad=((10, 0), (0, 0)), enable_events=True)
        ]])],
    ]

# define whole layout
layout = \
    [
        [sg.Column(plot_col, vertical_alignment='top', justification='C', expand_x=True, size=(800, 800)),
         sg.VerticalSeparator(color='006699'),
         sg.Column(settings_col, vertical_alignment='top', justification='C', size=(1000, 800))],
    ]

# Create interface-window
window = sg.Window('Pinning of Fermi Level', layout, finalize=True, resizable=True, size=(1800, 800), location=(0, 0))

# Create figure for plotting
fig = matplotlib.figure.Figure(figsize=(8, 6), dpi=100)
ax = fig.add_subplot(111)
ax.grid()
ax.set_xlabel("X")
ax.set_ylabel("Y")
# Create canvas that we can display matplotlib graph in the interface
figure_canvas_agg = FigureCanvasTkAgg(fig, window['-CANVAS-'].TKCanvas)
# Adjust placement of the canvas
figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)

# handling of events
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event in ('SL1', 'SL2', 'SL3', 'SL4', 'SL5', 'SL6', 'SL7', 'SL8', 'SL9', 'SL10'):
        window['-IN1-'].update(values['SL1'])
        window['-IN2-'].update(values['SL2'])
        window['-IN3-'].update(values['SL3'])
        window['-IN4-'].update(values['SL4'])
        window['-IN5-'].update(values['SL5'])
        window['-IN6-'].update(values['SL6'])
        window['-IN7-'].update(values['SL7'])
        window['-IN8-'].update(values['SL8'])
        window['-IN9-'].update(values['SL9'])
        window['-IN10-'].update(values['SL10'])
        draw_figure(ax, figure_canvas_agg, values)
    if event == 'Draw':
        window['SL1'].update(values['-IN1-'])
        window['SL2'].update(values['-IN2-'])
        window['SL3'].update(values['-IN3-'])
        window['SL4'].update(values['-IN4-'])
        window['SL5'].update(values['-IN5-'])
        window['SL6'].update(values['-IN6-'])
        window['SL7'].update(values['-IN7-'])
        window['SL8'].update(values['-IN8-'])
        window['SL9'].update(values['-IN9-'])
        window['SL10'].update(values['-IN10-'])
        draw_figure(ax, figure_canvas_agg, values)
    if event == 'Save':
        # print('hi')
        print(f'I chose: {values["Save"]}')
        # print(values['NamePicture'])
        # fig.savefig('file.png')
        # fig.savefig(values['Save'] + '/' + values['NamePicture'] + '.png')
window.close()
