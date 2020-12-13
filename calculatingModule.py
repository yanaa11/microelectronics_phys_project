import math
from fompy import constants
from fompy import materials
from fompy import models

from scipy.optimize import fsolve


def checkparms(params, Nc, Nv):
    
    message = 'ok'
    
    if(params['E_as'] > params['E_gap']): 
        message = 'Ошибка! Поверхностные состояния по энергии НЕ попадают в запрещенную зону полупроводника'
    if(params['E_out'] * 3.3*1e-5 > params['N_as'] * constants.e):
        message = 'Ошибка! Внешнее поле больше, чем поле создаваемое поверхностными акцепторами'
    if(params['N_d0'] > Nc or params['N_d0'] > Nv ):
         message = 'Ошибка! Концентрация доноров больше, чем концентрация собственных плотностей состояний в валентной зоне и зоне проводимости' 
    
    return message

def create_scond(parms):
    
    if parms['mat'] == 'GaAs':
        mat_scond = materials.GaAs
        
    if parms['mat'] == 'Si':
        mat_scond = materials.Si
        
    if parms['mat'] =='Ge':
        mat_scond = materials.Ge
        
    if parms['mat'] == 'custom':
        scond = models.Semiconductor(parms['m_e']*constants.me,parms['m_h']*constants.me, parms['E_gap'] * constants.eV, eps=parms['epsilon'], chi=None)
    else:      
        parms['E_gap'] = mat_scond.Eg / constants.eV #eV
        parms['epsilon'] = mat_scond.eps 
        parms['m_h'] = mat_scond.mh 
        parms['m_e'] = mat_scond.me 
        E_d_fp = (parms['E_gap'] - parms['E_d']) * constants.eV
        scond = models.DopedSemiconductor(mat=mat_scond, Na=0, Ea=0, Nd=parms['N_d0'], Ed=E_d_fp)
    
    return scond

# x == phi_s в эВ !!!!
def f_left(x, parms):
    x_erg = x * constants.eV
    return math.sqrt(parms['epsilon'] * x_erg * parms['N_d0']/(2*math.pi*(constants.e)**2))

def f_right(x, parms):
    x_erg = x * constants.eV
    return (parms['N_as']*(1/(1 + math.exp((parms['E_as'] + x_erg - parms['E_f'])/(constants.k*parms['T'])))) + parms['E_out']/(4*math.pi*constants.e))

def f(x, parms):
    return f_left(x, parms) - f_right(x, parms)

def W(phi, params):
    #phi в эВ
    phi_erg = phi * constants.eV
    return math.sqrt(params['epsilon']*phi_erg/(params['N_d0']*2*math.pi*(constants.e)**2))

def phi(params):
    x_0 = 0.001
    root = fsolve(f,x_0, args = params)
    return root[0]

def make_points(phi, W, parms):
    #phi в эВ
    #W в см
    
    N = 30
    h = W*2/N
    
    #парабола: ax^2 + bx + c
    c = phi
    a = c/(W**2)
    b = -2 * W * a
        
    x_s = [] #координата
    E_f_s = [] # энергия ферми
    E_v_s = [] # потолок валентной зоны
    E_c_s = [] # дно зоны проводимости
    E_d_s = [] # энергия доноров
    E_as_s = [] #энергия поверхностных акцепторов
    
    E_f = parms['E_f'] / constants.eV
    E_gap = parms['E_gap'] / constants.eV
    E_d = parms['E_d'] / constants.eV
    E_as_eV = parms['E_as'] / constants.eV
     
    
    for i in range(N+1):
        x_s.append(i*h)
        E_f_s.append(E_f)
        E_as_s.append(E_as_eV)
        
        if x_s[i] > W:
            E_v_s.append(0)
            E_c_s.append(E_gap)
            E_d_s.append(E_d)
            
        else:
            bend = a*x_s[i]**2 + b*x_s[i] + c
            E_v_s.append(bend)
            E_c_s.append(E_gap + bend)
            E_d_s.append(E_d + bend)
            
    return x_s, E_f_s, E_v_s, E_c_s, E_d_s, E_as_s

def calculate(parms):
    scond = create_scond(parms)
    T = parms['T'] 
    message = checkparms(parms, scond.Nc(T), scond.Nc(T))
    results = dict(message = '', x_s = 0, E_f_s = 0 , E_v_s = 0, E_c_s = 0, E_d_s = 0, E_as_s = 0, phi = 0, W = 0)
    if message == 'ok':
        results['message'] = message
        
        #Переведем все в СГС
        parms['E_gap'] = parms['E_gap'] * constants.eV
        parms['E_d'] = parms['E_d'] * constants.eV
        parms['E_as'] = parms['E_as'] * constants.eV
        parms['E_out'] = parms['E_out'] * 3.3*1e-5
        
        
        try:
            parms['E_f'] = scond.fermi_level(T)
            results['phi'] = phi(parms) #eV
            results['W'] = W(results['phi'], parms) #cm
            results['x_s'], results['E_f_s'], results['E_v_s'],results['E_c_s'], results['E_d_s'], results['E_as_s'] = make_points(results['phi'], results['W'], parms)
        except Exception:
            message = 'Ошибка! Некорректные данные'
            results['message'] = message
            return results
        
    else: results['message'] = message
    return results

