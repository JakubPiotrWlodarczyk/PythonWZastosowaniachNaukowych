import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import odeint 
from bokeh.io import curdoc
from bokeh.plotting import figure, show
from bokeh.layouts import row, column, gridplot, layout
from bokeh.models import Slider, Div

#stale

N = 19000
beta = 0.65
gamma = 0.2

# warunki poczatkowe

S_0 = 19000
I_0 = 5
R_0 = 0


#funkcja na pochodna

def funkcja_pochodna(y, t, beta, gamma, N):
    S, I, R = y
    return -beta * S * I / N, beta * S * I / N - gamma * I, gamma * I


#kroki czasowe 

t = np.linspace(0, 100, 1000)


#rozwiazanie ukladu rownan

wyniki = odeint(funkcja_pochodna, (S_0, I_0, R_0), t, args=(beta, gamma, N))



fig = figure(sizing_mode='stretch_width', 
            aspect_ratio=2,
            title='Model SIR',
            x_axis_label='Czas t',
            y_axis_label='Ilość osób w danym stanie')
fig.toolbar.logo = None 
fig.toolbar.autohide = True

fig.line(t, wyniki[:,0], color='green', line_width=2, legend_label='S')
fig.line(t, wyniki[:,1], color='red', line_width=2, legend_label='I')
fig.line(t, wyniki[:,2], color='blue', line_width=2, legend_label='R')

def callback_I(attr, old, new):
    I_0 = new
    wyniki = odeint(funkcja_pochodna, (S_0, I_0, R_0), t, args=(beta, gamma, N))

    fig.renderers = []

    fig.line(t, wyniki[:,0], color='green', line_width=2, legend_label='S')
    fig.line(t, wyniki[:,1], color='red', line_width=2, legend_label='I')
    fig.line(t, wyniki[:,2], color='blue', line_width=2, legend_label='R')

def callback_beta(attr, old, new):
    beta = new
    wyniki = odeint(funkcja_pochodna, (S_0, I_0, R_0), t, args=(beta, gamma, N))

    fig.renderers = []

    fig.line(t, wyniki[:,0], color='green', line_width=2, legend_label='S')
    fig.line(t, wyniki[:,1], color='red', line_width=2, legend_label='I')
    fig.line(t, wyniki[:,2], color='blue', line_width=2, legend_label='R')

def callback_gamma(attr, old, new):
    gamma = new
    wyniki = odeint(funkcja_pochodna, (S_0, I_0, R_0), t, args=(beta, gamma, N))

    fig.renderers = []

    fig.line(t, wyniki[:,0], color='green', line_width=2, legend_label='S')
    fig.line(t, wyniki[:,1], color='red', line_width=2, legend_label='I')
    fig.line(t, wyniki[:,2], color='blue', line_width=2, legend_label='R')

def callback_N(attr, old, new):
    N = new
    wyniki = odeint(funkcja_pochodna, (S_0, I_0, R_0), t, args=(beta, gamma, N))

    fig.renderers = []

    fig.line(t, wyniki[:,0], color='green', line_width=2, legend_label='S')
    fig.line(t, wyniki[:,1], color='red', line_width=2, legend_label='I')
    fig.line(t, wyniki[:,2], color='blue', line_width=2, legend_label='R')

slider_I = Slider(start = 0, end = 10000, step = 1, value = 5, title = 'I_0', sizing_mode='stretch_width')
slider_I.on_change('value_throttled', callback_I)

slider_beta = Slider(start = 0, end = 1, step = 0.05, value = 0.65, title = 'beta', sizing_mode='stretch_width')
slider_beta.on_change('value_throttled', callback_beta)

slider_gamma = Slider(start = 0, end = 1, step = 0.05, value = 0.2, title = 'gamma', sizing_mode='stretch_width')
slider_gamma.on_change('value_throttled', callback_gamma)

slider_N = Slider(start = 0, end = 100000, step = 1000, value = 19000, title = 'N', sizing_mode='stretch_width')
slider_N.on_change('value_throttled', callback_N)

curdoc().add_root(column(Div(text='Liczba osobników zarazonych'), row(column(slider_I, width=200)), column(Div(text='Beta')), row(column(slider_beta, width=200)), column(Div(text='Gamma')), row(column(slider_gamma, width=200)), column(Div(text='Calkowita liczba osobników')), row(column(slider_N, width=200)), fig, width=1000))

#poetry run bokeh serve --show .\app.py