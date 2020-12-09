import PySimpleGUI as sg 
from matplotlib.ticker import NullFormatter  # useful for `logit` scale
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
import calculatingModule
matplotlib.use('TkAgg')

def draw_figure(ax, figure_canvas_agg, results):
    """
    Redraw plot for each new event.
    
    {ax} is responsible for adjusting of the plot
    
    {figure_canvas_agg} helps draw plot in the window-interface
    """
    
    ax.cla()                 
    ax.set_xlabel("t")
    ax.set_ylabel("E")
    ax.grid()
# update plots
    if results['message'] == 'ok':
        ax.plot(results['x_s'], results['E_f_s'], label='E_f_s')
        ax.plot(results['x_s'], results['E_v_s'], label='E_v_s')
        ax.plot(results['x_s'], results['E_c_s'], label='E_c_s')
        ax.plot(results['x_s'], results['E_d_s'], label='E_d_s')
        ax.plot(results['x_s'], results['E_as_s'], label='E_as_s')
        ax.axhline(results['phi'], c='k', linestyle='dashed')
        ax.axvline(results['W'], c='k', linestyle='dashed')
        ax.legend(bbox_to_anchor=(1., 0.5), fontsize=12, loc='right')
    
    figure_canvas_agg.draw()

def getCalculatedValues(values):
    args = {
        "E_gap":   float(values['-IN1-']),    # Band gap [eV]
        "E_d":     float(values['-IN2-']),    # Donors level [eV]
        "N_d0":    float(values['-IN3-']),    # Concentration of donors 10^27 [cm^(-3)]
        "E_as":    float(values['-IN4-']),    # Surface acceptors level [eV]
        "N_as":    float(values['-IN5-']),    # Concentration of surface acceptors 10^27 [cm^(-3)]
        "m_e":     float(values['-IN6-']),    # Effective electron mass [m_0]
        "m_h":     float(values['-IN7-']),    # Effective hole mass [m_0]
        "epsilon": float(values['-IN8-']),    # Dielectric permittivity
        "T":       float(values['-IN9-']),    # Temperature [K]
        "E_out":   float(values['-IN10-']),   # External electric field
        "mat":     values['-Mats-']           # Material
    }
    
    return calculatingModule.calculate(args)


# handling of events
def update_sliders(vals):
    window['SL1'].update(vals[0])
    window['SL2'].update(vals[1])
    window['SL3'].update(vals[2])
    window['SL4'].update(vals[3])
    window['SL5'].update(vals[4])
    window['SL6'].update(vals[5])
    window['SL7'].update(vals[6])
    window['SL8'].update(vals[7])
    window['SL9'].update(vals[8])
    window['SL10'].update(vals[9])
    
def update_inputs(vals):
    window['-IN1-'].update(vals[0])
    window['-IN2-'].update(vals[1])
    window['-IN3-'].update(vals[2])
    window['-IN4-'].update(vals[3])
    window['-IN5-'].update(vals[4])
    window['-IN6-'].update(vals[5])
    window['-IN7-'].update(vals[6])
    window['-IN8-'].update(vals[7])
    window['-IN9-'].update(vals[8])
    window['-IN10-'].update(vals[9])    

def block_unblock_properties_SC(block):
    """
    If you choose specific Semiconducter, then some property should be blocked
    If you pick "another", then all property will be unblocked
    """
    window['SL2'].update(disabled=block)     # blocked Donors level
    window['-IN2-'].update(disabled=block)   
    window['SL3'].update(disabled=block)     # blocked Concentration of donors
    window['-IN3-'].update(disabled=block)  
    window['SL4'].update(disabled=block)     # blocked Surface acceptors level
    window['-IN4-'].update(disabled=block)   
    window['SL5'].update(disabled=block)     # blocked Concentration of surface acceptors
    window['-IN5-'].update(disabled=block)   
    window['SL9'].update(disabled=block)     # blocked Temperature
    window['-IN9-'].update(disabled=block)   
    window['SL10'].update(disabled=block)    # blocked External electric field
    window['-IN10-'].update(disabled=block)  
    
    simg = (20, 20)
    if block==False:
        for i in range(1, 11):
            window['I' + str(i)].update('unlock.png', size=simg)
    else:
        window['I1'].update('unlock.png', size=simg)
        window['I2'].update('lock.png', size=simg)
        window['I3'].update('lock.png', size=simg)
        window['I4'].update('lock.png', size=simg)
        window['I5'].update('lock.png', size=simg)
        window['I6'].update('unlock.png', size=simg)
        window['I7'].update('unlock.png', size=simg)
        window['I8'].update('unlock.png', size=simg)
        window['I9'].update('lock.png', size=simg)
        window['I10'].update('lock.png', size=simg)
    
def output_info(results):
    if results['message'] != 'ok':
            window['-PlotINFO-'].update(results['message'], text_color='red', background_color='yellow')
    else:
        window['-PlotINFO-'].update(f"phi:    {results['phi']:.3f}\nW:     {results['W']:.3f}", text_color='black', background_color='white')

# set theme for the window-interface
sg.theme('LightGrey2') 

# define layout

# define plot column for layout

plot_col =\
[
    [sg.Canvas(key='-CANVAS-', size=(640, 640))],
    [sg.Text('', key='-PlotINFO-', size=(60, 2), pad=((75, 0), (15, 0)), font=('Helvetica', 15), justification='c')],
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
pfr = ((0,0), (0, 25))
nps = (30,1)
font = ("Helvetica", 15)
ssld = (30, 10)
sinp = (7, 1)
sphp = (10, 1)
simg = (20, 20)
pinp = ((35, 0), (0, 0))
bw = 1.5
dnd=True
vimg=True

settings_col =\
[
    # 1. Bad gap Row
    [sg.Frame('', border_width=0, pad = pfr, layout=[[
        sg.Text('Band gap:', nps, font=font),
        sg.Slider(key='SL1', range=(1e-5, 1e-2), orientation='h', resolution=1e-6, size=ssld, default_value=1, enable_events=True, disable_number_display=dnd),
        sg.Input('1.0', key='-IN1-', size=sinp, border_width=bw, font=font, pad=pinp),
        sg.Text('[eV]', size=sphp, font=font),
        sg.Image('unlock.png', key='I1', size=simg, visible=vimg)
    ]])],
    # 2. Donor level Row
    [sg.Frame('', border_width=0, pad = pfr, layout=[[
        sg.Text('Donor level:', nps, font=font),
        sg.Slider(key='SL2', range=(1e-4, 1e-2), orientation='h', resolution=1e-5, size=ssld, default_value=1, enable_events=True, disable_number_display=dnd),
        sg.Input('1.0', key='-IN2-', size=sinp, border_width=bw, font=font, pad=pinp),
        sg.Text('[eV]', size=sphp, font=font),
        sg.Image('unlock.png', key='I2', size=simg, visible=vimg)
    ]])],
    # 3. Concentration of donors Row
    [sg.Frame('', border_width=0, pad = pfr, layout=[[
        sg.Text('Concentration of donors:', nps, font=font),
        sg.Slider(key='SL3', range=(1e9, 1e10), orientation='h', size=ssld, default_value=1, enable_events=True, disable_number_display=dnd),
        sg.Input('1.0', key='-IN3-', size=sinp, border_width=bw, font=font, pad=pinp),
        sg.Text('[cm^(-3)]', size=sphp, font=font),
        sg.Image('unlock.png', key='I3', size=simg, visible=vimg)
    ]])],
    # 4. Surface acceptors level Row
    [sg.Frame('', border_width=0, pad = pfr, layout=[[
        sg.Text('Surface acceptors level:', nps, font=font),
        sg.Slider(key='SL4', range=(0, 1), orientation='h', resolution=0.01, size=ssld, default_value=0, enable_events=True, disable_number_display=dnd),
        sg.Input('1.0', key='-IN4-', size=sinp, border_width=bw, font=font, pad=pinp),
        sg.Text('[eV]', size=sphp, font=font),
        sg.Image('unlock.png', key='I4', size=simg, visible=vimg)
    ]])],
    # 5. Concentration of surface acceptors Row
    [sg.Frame('', border_width=0, pad = pfr, layout=[[
        sg.Text('Concentration of surface acceptors:', nps, font=font),
        sg.Slider(key='SL5', range=(1.5e10, 1.5e15), orientation='h', size=ssld, default_value=1, enable_events=True, disable_number_display=dnd),
        sg.Input('1.0', key='-IN5-', size=sinp, border_width=bw, font=font, pad=pinp),
        sg.Text('[cm^(-2)]', size=sphp, font=font),
        sg.Image('unlock.png', key='I5', size=simg, visible=vimg)
    ]])],
    # 6. Effective electron mass Row
    [sg.Frame('', border_width=0, pad = pfr, layout=[[
        sg.Text('Effective electron mass:', nps, font=font),
        sg.Slider(key='SL6', range=(0, 1), orientation='h', resolution=0.01, size=ssld, default_value=0, enable_events=True, disable_number_display=dnd),
        sg.Input('1.0', key='-IN6-', size=sinp, border_width=bw, font=font, pad=pinp),
        sg.Text('[m_0]', size=sphp, font=font),
        sg.Image('unlock.png', key='I6', size=simg, visible=vimg)
    ]])],
    # 7. Effective hole mass Row
    [sg.Frame('', border_width=0, pad = pfr, layout=[[
        sg.Text('Effective hole mass:', nps, font=font),
        sg.Slider(key='SL7', range=(0, 1), orientation='h', resolution=0.01, size=ssld, default_value=0, enable_events=True, disable_number_display=dnd),
        sg.Input('1.0', key='-IN7-', size=sinp, border_width=bw, font=font, pad=pinp),
        sg.Text('[m_0]', size=sphp, font=font),
        sg.Image('unlock.png', key='I7', size=simg, visible=vimg)
    ]])],
    # 8. Dielectric permittivity Row
    [sg.Frame('', border_width=0, pad = pfr, layout=[[
        sg.Text('Dielectric permittivity:', nps, font=font),
        sg.Slider(key='SL8', range=(10, 20), orientation='h', resolution=0.1, size=ssld, default_value=10, enable_events=True, disable_number_display=dnd),
        sg.Input('1.0', key='-IN8-', size=sinp, border_width=bw, font=font, pad=pinp),
        sg.Text('', size=sphp, font=font),
        sg.Image('unlock.png', key='I8', size=simg, visible=vimg)
    ]])],
    # 9. Temperature Row
    [sg.Frame('', border_width=0, pad = pfr, layout=[[
        sg.Text('Temperature:', nps, font=font),
        sg.Slider(key='SL9', range=(300, 400), orientation='h', size=ssld, default_value=1, enable_events=True, disable_number_display=dnd),
        sg.Input('1.0', key='-IN9-', size=sinp, border_width=bw, font=font, pad=pinp),
        sg.Text('[K]', size=sphp, font=font),
        sg.Image('unlock.png', key='I9', size=simg, visible=vimg)
    ]])],
    # 10. External electric field Row
    [sg.Frame('', border_width=0, pad = pfr, layout=[[
        sg.Text('External electric field:', nps, font=font),
        sg.Slider(key='SL10', range=(1e3, 1e4), orientation='h', size=ssld, default_value=1, enable_events=True, disable_number_display=dnd),
        sg.Input('1.0', key='-IN10-', size=sinp, border_width=bw, font=font, pad=pinp),
        sg.Text('[V/m]', size=sphp, font=font),
        sg.Image('unlock.png', key='I10', size=simg, visible=vimg)
    ]])],
    # 11. Draw and Set Material Row 
    [sg.Frame('', border_width=0, pad = ((0,0), (25, 25)), layout=[[
        sg.Text('Material:', font=font, pad=((0, 0),(0, 0))),
        sg.Combo(('Si', 'Ge', 'GaAs', 'custom'), key='-Mats-', default_value='custom', size=(8, 1), font=font, enable_events=False),
        sg.Button('Set', key='SetMat', font=font, pad=((10, 0), (0, 0))),
        sg.Text('Draw plot:', font=font, pad=((285, 0),(0, 0))),
        sg.Button('Draw', key='Draw', font=font, pad=((10, 0), (0, 0)))
    ]])],
    # 12. Save Row
    [sg.Frame('', border_width=0, pad = pfr, layout=[[
        sg.Text('Save plot:', font=font, pad=((550, 0),(0, 0))),
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
ax = fig.add_subplot()
ax.grid()
ax.set_xlabel("t")
ax.set_ylabel("E")
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
        vals = (values['SL1'], values['SL2'], values['SL3'], values['SL4'], values['SL5'], 
                values['SL6'], values['SL7'], values['SL8'], values['SL9'], values['SL10'])
        update_inputs(vals)
        results = getCalculatedValues(values)
        draw_figure(ax, figure_canvas_agg, results)
        output_info(results)
    
    if event == 'Draw':
        vals = (values['-IN1-'], values['-IN2-'], values['-IN3-'], values['-IN4-'], values['-IN5-'], 
                values['-IN6-'], values['-IN7-'], values['-IN8-'], values['-IN9-'], values['-IN10-'])
        update_sliders(vals)
        results = getCalculatedValues(values)
        draw_figure(ax, figure_canvas_agg, results)
        output_info(results)
    
    if event == 'SetMat':
        """
        vals = (E_gap, E_d, N_d0, E_as, N_as, m_e, m_h, epsilon, T, E_out)
        """
        if values['-Mats-'] == 'custom':
            vals = (1e-5, 1e-2, 1e10, 0.96, 1.3e10, 0.5, 0.5, 10.0, 300, 1e4)
            update_sliders(vals)
            update_inputs(vals)
            block_unblock_properties_SC(False)
        
        if values['-Mats-'] == 'Si':
            vals = (1e-5, 1e-2, 1e10, 0.96, 1.5e15, 0.5, 0.5, 11.7, 300, 1e4)
            update_sliders(vals)
            update_inputs(vals)
            block_unblock_properties_SC(True)
            
        if values['-Mats-'] == 'Ge':
            vals = (1e-5, 1e-2, 1e10, 0.96, 1.5e15, 0.5, 0.5, 16.2, 300, 1e4)
            update_sliders(vals)
            update_inputs(vals)
            block_unblock_properties_SC(True)
            
        if values['-Mats-'] == 'GaAs':
            vals = (1e-5, 1e-2, 1e10, 0.96, 1.5e15, 0.5, 0.5, 10.89, 300, 1e4)
            update_sliders(vals)
            update_inputs(vals)
            block_unblock_properties_SC(True)
    
    if event == 'Save':
        #print('hi')
        print(f'I chose: {values["Save"]}')
        #print(values['NamePicture'])
        #fig.savefig('file.png')
        #fig.savefig(values['Save'] + '/' + values['NamePicture'] + '.png')
window.close()
