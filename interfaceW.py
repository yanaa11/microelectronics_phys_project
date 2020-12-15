import PySimpleGUI as sg
from matplotlib.ticker import NullFormatter  # useful for `logit` scale
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
import calculatingModule

matplotlib.use('TkAgg')

# coef_phys_parameters on interface
cpp = {'N_d0': 1e12, 'N_as': 1e13, 'E_out': 1e4}


def draw_figure(ax, figure_canvas_agg, results):
    """
    Redraw plot for each new event.

    {ax} is responsible for adjusting of the plot

    {figure_canvas_agg} helps draw plot in the window-interface
    """

    ax.cla()
    ax.set_xlabel("x [cm]")
    ax.set_ylabel("E [eV]")
    ax.grid()
    # update plots
    if results['message'] == 'ok':
        ax.plot(results['x_s'], results['E_f_s'], label='Fermi Energy')
        ax.plot(results['x_s'], results['E_v_s'], label='Valence Band')
        ax.plot(results['x_s'], results['E_c_s'], label='Conduction Band')
        ax.plot(results['x_s'], results['E_d_s'], label='Donor Energy')
        ax.plot(results['x_s'], results['E_as_s'], label='Acceptor Energy')
        ax.axhline(results['phi'], c='k', linestyle='dashed')
        ax.text(0.002, results['phi'] + 0.02, 'phi = ' + str(round(results['phi'], 4)) + ' [eV]')
        ax.axvline(results['W'], c='k', linestyle='dashed')
        ax.text(results['W'] + 0.0001, 0.2, 'W = ' + str(round(results['W'], 4)) + ' [cm]')
        ax.legend(bbox_to_anchor=(1., 0.5), fontsize=10, loc='right')

    figure_canvas_agg.draw()


def getCalculatedValues(values):
    args = {
        "E_gap": float(values['-IN1-']),  # Band gap [eV]
        "E_d": float(values['-IN2-']),  # Donors level [eV]
        "N_d0": float(values['-IN3-']) * cpp['N_d0'],  # Concentration of donors 10^27 [cm^(-3)]
        "E_as": float(values['-IN4-']),  # Surface acceptors level [eV]
        "N_as": float(values['-IN5-']) * cpp['N_as'],  # Concentration of surface acceptors 10^27 [cm^(-3)]
        "m_e": float(values['-IN6-']),  # Effective electron mass [m_0]
        "m_h": float(values['-IN7-']),  # Effective hole mass [m_0]
        "epsilon": float(values['-IN8-']),  # Dielectric permittivity
        "T": float(values['-IN9-']),  # Temperature [K]
        "E_out": float(values['-IN10-']) * cpp['E_out'],  # External electric field
        "mat": values['-Mats-']  # Material
    }

    return calculatingModule.calculate(args)


# handling of events
def update_sliders(vals):
    for i in range(1, 11):
        window['SL' + str(i)].update(vals[i - 1])


def update_inputs(vals):
    for i in range(1, 11):
        window['-IN' + str(i) + '-'].update(vals[i - 1])


def update_bounderies(vals):
    window['SL4'].update(float(vals[0]) / 2, range=(0.1, vals[0]))


def block_unblock_properties_SC(block):
    """
    If you choose specific Semiconducter, then some property should be blocked
    If you pick "another", then all property will be unblocked
    """

    window['SL1'].update(disabled=block)  # blocked Band gap
    window['-IN1-'].update(disabled=block)
    window['SL6'].update(disabled=block)  # blocked Effective electron mass
    window['-IN6-'].update(disabled=block)
    window['SL7'].update(disabled=block)  # blocked Effective hole mass
    window['-IN7-'].update(disabled=block)
    window['SL8'].update(disabled=block)  # blocked Dielectric permittivity
    window['-IN8-'].update(disabled=block)

    simg = (20, 20)
    if block == False:
        for i in range(1, 11):
            window['I' + str(i)].update('unlock.png', size=simg)
    else:
        window['I1'].update('lock.png', size=simg)
        window['I2'].update('unlock.png', size=simg)
        window['I3'].update('unlock.png', size=simg)
        window['I4'].update('unlock.png', size=simg)
        window['I5'].update('unlock.png', size=simg)
        window['I6'].update('lock.png', size=simg)
        window['I7'].update('lock.png', size=simg)
        window['I8'].update('lock.png', size=simg)
        window['I9'].update('unlock.png', size=simg)
        window['I10'].update('unlock.png', size=simg)


def output_info(results):
    if results['message'] != 'ok':
        window['-PlotINFO-'].update(results['message'], text_color='red', background_color='yellow')
    else:
        window['-PlotINFO-'].update(
            f"bending of zone phi:          {results['phi']:.4f} [eV]\nSpace charge region W:     {results['W']:.4f} [cm]",
            text_color='black', background_color='white')


# set theme for the window-interface
sg.theme('LightGrey2')

# define layout

# ------ Menu Definition ------ #
menu_def = [['File', ['Open', 'Save', 'Exit']],
            ['Help', 'About...'], ]

# ------ Column Definition ------ #

plot_col = \
    [
        [sg.Canvas(key='-CANVAS-', size=(640, 640))],
        [sg.Text('', key='-PlotINFO-', size=(60, 3), pad=((75, 0), (15, 0)), font=('Helvetica', 15),
                 justification='c')],
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
font = ("Helvetica", 11)
ssld = (20, 10)
sinp = (7, 1)
sphp = (15, 1)
simg = (20, 20)
pinp = ((35, 0), (0, 0))
bw = 1.5
dnd = True
vimg = True

settings_col = \
    [
        # 1. Bad gap Row
        [sg.Frame('', border_width=0, pad=pfr, layout=[[
            sg.Text('Band gap:', nps, font=font),
            sg.Slider(key='SL1', range=(0, 10), orientation='h', resolution=0.01, size=ssld, default_value=5,
                      enable_events=True, disable_number_display=dnd),
            sg.Input('5', key='-IN1-', size=sinp, border_width=bw, font=font, pad=pinp),
            sg.Text('[eV]', size=sphp, font=font),
            sg.Image('unlock.png', key='I1', size=simg, visible=vimg)
        ]])],
        # 2. Donor level Row
        [sg.Frame('', border_width=0, pad=pfr, layout=[[
            sg.Text('Donor level:', nps, font=font),
            sg.Slider(key='SL2', range=(0, 2.5), orientation='h', resolution=0.01, size=ssld, default_value=0.5,
                      enable_events=True, disable_number_display=dnd),
            sg.Input('0.5', key='-IN2-', size=sinp, border_width=bw, font=font, pad=pinp),
            sg.Text('[eV]', size=sphp, font=font),
            sg.Image('unlock.png', key='I2', size=simg, visible=vimg)
        ]])],
        # 3. Concentration of donors Row
        [sg.Frame('', border_width=0, pad=pfr, layout=[[
            sg.Text('Concentration of donors:', nps, font=font),
            sg.Slider(key='SL3', range=(1e-3, 100), orientation='h', resolution=0.1, size=ssld, default_value=50,
                      enable_events=True, disable_number_display=dnd),
            sg.Input('50', key='-IN3-', size=sinp, border_width=bw, font=font, pad=pinp),
            sg.Text('10^12*[cm^(-3)]', size=sphp, font=font),
            sg.Image('unlock.png', key='I3', size=simg, visible=vimg)
        ]])],
        # 4. Surface acceptors level Row
        [sg.Frame('', border_width=0, pad=pfr, layout=[[
            sg.Text('Surface acceptors level:', nps, font=font),
            sg.Slider(key='SL4', range=(0.1, 5), orientation='h', resolution=0.01, size=ssld, default_value=2.5,
                      enable_events=True, disable_number_display=dnd),
            sg.Input('2.5', key='-IN4-', size=sinp, border_width=bw, font=font, pad=pinp),
            sg.Text('[eV]', size=sphp, font=font),
            sg.Image('unlock.png', key='I4', size=simg, visible=vimg)
        ]])],
        # 5. Concentration of surface acceptors Row
        [sg.Frame('', border_width=0, pad=pfr, layout=[[
            sg.Text('Concentration of surface acceptors:', nps, font=font),
            sg.Slider(key='SL5', range=(1e-3, 100), orientation='h', resolution=0.1, size=ssld, default_value=50,
                      enable_events=True, disable_number_display=dnd),
            sg.Input('50', key='-IN5-', size=sinp, border_width=bw, font=font, pad=pinp),
            sg.Text('10^13*[cm^(-2)]', size=sphp, font=font),
            sg.Image('unlock.png', key='I5', size=simg, visible=vimg)
        ]])],
        # 6. Effective electron mass Row
        [sg.Frame('', border_width=0, pad=pfr, layout=[[
            sg.Text('Effective electron mass:', nps, font=font),
            sg.Slider(key='SL6', range=(0.01, 1), orientation='h', resolution=0.01, size=ssld, default_value=0.5,
                      enable_events=True, disable_number_display=dnd),
            sg.Input('0.5', key='-IN6-', size=sinp, border_width=bw, font=font, pad=pinp),
            sg.Text('[m_0]', size=sphp, font=font),
            sg.Image('unlock.png', key='I6', size=simg, visible=vimg)
        ]])],
        # 7. Effective hole mass Row
        [sg.Frame('', border_width=0, pad=pfr, layout=[[
            sg.Text('Effective hole mass:', nps, font=font),
            sg.Slider(key='SL7', range=(0.01, 1), orientation='h', resolution=0.01, size=ssld, default_value=0.5,
                      enable_events=True, disable_number_display=dnd),
            sg.Input('0.5', key='-IN7-', size=sinp, border_width=bw, font=font, pad=pinp),
            sg.Text('[m_0]', size=sphp, font=font),
            sg.Image('unlock.png', key='I7', size=simg, visible=vimg)
        ]])],
        # 8. Dielectric permittivity Row
        [sg.Frame('', border_width=0, pad=pfr, layout=[[
            sg.Text('Dielectric permittivity:', nps, font=font),
            sg.Slider(key='SL8', range=(5, 20), orientation='h', resolution=0.1, size=ssld, default_value=12.5,
                      enable_events=True, disable_number_display=dnd),
            sg.Input('12.5', key='-IN8-', size=sinp, border_width=bw, font=font, pad=pinp),
            sg.Text('', size=sphp, font=font),
            sg.Image('unlock.png', key='I8', size=simg, visible=vimg)
        ]])],
        # 9. Temperature Row
        [sg.Frame('', border_width=0, pad=pfr, layout=[[
            sg.Text('Temperature:', nps, font=font),
            sg.Slider(key='SL9', range=(100, 3000), orientation='h', resolution=1, size=ssld, default_value=300,
                      enable_events=True, disable_number_display=dnd),
            sg.Input('300', key='-IN9-', size=sinp, border_width=bw, font=font, pad=pinp),
            sg.Text('[K]', size=sphp, font=font),
            sg.Image('unlock.png', key='I9', size=simg, visible=vimg)
        ]])],
        # 10. External electric field Row
        [sg.Frame('', border_width=0, pad=pfr, layout=[[
            sg.Text('External electric field:', nps, font=font),
            sg.Slider(key='SL10', range=(1, 200), orientation='h', resolution=1, size=ssld, default_value=20,
                      enable_events=True, disable_number_display=dnd),
            sg.Input('20', key='-IN10-', size=sinp, border_width=bw, font=font, pad=pinp),
            sg.Text('10^4*[V/m]', size=sphp, font=font),
            sg.Image('unlock.png', key='I10', size=simg, visible=vimg)
        ]])],
        # 11. Draw and Set Material Row
        [sg.Frame('', border_width=0, pad=((0, 0), (25, 25)), layout=[[
            sg.Text('Material:', font=font, pad=((0, 0), (0, 0))),
            sg.Combo(('Si', 'Ge', 'GaAs', 'custom'), key='-Mats-', default_value='custom', size=(8, 1), font=font,
                     enable_events=False),
            sg.Button('Set', key='SetMat', font=font, pad=((10, 0), (0, 0))),
            sg.Text('Draw plot:', font=font, pad=((238, 0), (0, 0))),
            sg.Button('Draw', key='Draw', font=font, pad=((10, 0), (0, 0)))
        ]])],
        # 12. Save Row
        [sg.Frame('', border_width=0, pad=pfr, layout=[[
            sg.Text('Save plot:', font=font, pad=((433, 0), (0, 0))),
            sg.FolderBrowse('Save', key='Save', font=font, pad=((10, 0), (0, 0)), enable_events=True)
        ]])],
    ]

# define whole layout
layout = \
    [
        [sg.Menu(menu_def)],
        [sg.Column(plot_col, vertical_alignment='top', justification='C', expand_x=True, size=(700, 800)),
         sg.VerticalSeparator(color='006699'),
         sg.Column(settings_col, vertical_alignment='top', justification='C', size=(800, 800))],
    ]

# --------------Setting of help---------------#
help_text = '                                           Как пользоваться этой программой:\n\nДанная программа иллюстрирует пиннинг уровня Ферми поверхностными акцепторами.\n\nДля начала программы необходимо выбрать тип полупроводника в выпадающем списке: это может быть Si, Ge, GaAs или Custom(пользовательский режим).\n\nЗатем нажать кнопку SET - она настроит все параметры. После этого нажать кнопку Draw - она нарисует графики.\n\nПосле настройки можно работать со слайдерами и полями для ввода.\n\nЗамечания:\n1)Изменяя значения с помощью слайдера, графики обновляются автоматически и не требуется нажимать кнопку Draw.\n\n2)Если значения были изменены в окнах вывода, то для обновления графиков нужно нажать кнопку Draw.\n\n3)Некоторые параметры нельзя изменять, если выбран конкретный полупроводник. Такие параметры маркируются красным квадратом справа. Значения, которые можно изменить, маркируются зеленым квадратом.\n\n5)Если график не отрисовывается, то заданы некорректные значения и под графиком высветится предупреждающее сообщение.'
# Create interface-window
window = sg.Window('Pinning of Fermi Level', layout, finalize=True, resizable=True, size=(1500, 800), location=(0, 0))

# Create figure for plotting
fig = matplotlib.figure.Figure(figsize=(7, 5), dpi=100)
ax = fig.add_subplot()
ax.grid()
ax.set_xlabel("x [cm]")
ax.set_ylabel("E [eV]")
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
            vals = (5, 0.5, 10, 2.5, 10, 0.5, 0.5, 10.0, 300, 1)
            update_sliders(vals)
            update_inputs(vals)
            update_bounderies(vals)
            block_unblock_properties_SC(False)

        if values['-Mats-'] == 'Si':
            vals = (1.12, 1e-2, 10, 1.12 / 2, 10, 0.36, 0.81, 11.7, 300, 1)
            update_sliders(vals)
            update_inputs(vals)
            update_bounderies(vals)
            block_unblock_properties_SC(True)

        if values['-Mats-'] == 'Ge':
            vals = (0.661, 1e-2, 101, 0.661 / 2, 10, 0.22, 0.34, 16.2, 300, 1)
            update_sliders(vals)
            update_inputs(vals)
            update_bounderies(vals)
            block_unblock_properties_SC(True)

        if values['-Mats-'] == 'GaAs':
            vals = (1.424, 1e-2, 10, 1.424 / 2, 10, 0.063, 0.53, 12.9, 300, 1)
            update_sliders(vals)
            update_inputs(vals)
            block_unblock_properties_SC(True)

    if event == 'Save':
        # print('hi')
        print(f'I chose: {values["Save"]}')
        # print(values['NamePicture'])
        # fig.savefig('file.png')
        # fig.savefig(values['Save'] + '/' + values['NamePicture'] + '.png')

    if event == 'About...':
        sg.popup(help_text, title='Help', font=font, line_width=80, background_color='#ffffe8')

window.close()
