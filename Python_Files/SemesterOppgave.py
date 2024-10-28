import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import RadioButtons
import matplotlib.image as mpimg
import matplotlib.patches as mpatches
from matplotlib.widgets import Button
#Generater random data for a year
# centervals are values average values for each month
# samedata = false, new data each time program is called
import random
from random import randint

def create_dates() -> list:
    num_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    months = [x for x in range(1, 13)]
    dates = []

    for i in range(len(months)):
        for j in range(num_days[i]):
            dates.append(str(j + 1) + "." + str(months[i]))
    datoer = []
    i = 0
    j = 0
    while (j < 51):
        datoer.append(dates[i])
        i += 7
        j += 1
    datoer.append('31.12')
    return datoer
print(create_dates())

def genereate_random_year_dataList(intencity:float, seed:int=0) -> list[int]:
    """
    :param intencity: Number specifying size, amplitude
    :param seed: If given, same data with seed is generated
    :return:
    """
    if seed != 0:
        random.seed(seed)
    centervals = [200,150,100, 75,75,75, 50, 75, 100, 150, 200, 250, 300]
    centervals = [x * intencity for x in centervals]
    nox = centervals[0]
    inc = True
    noxList = []
    for index in range(1,365):
        if randint(1, 100) > 50:
            inc = not inc
        center = centervals[int(index / 30)]
        dx = min(2.0, max(0.5, nox / center ))
        nox =  nox + randint(1,5) / dx if inc else nox - randint( 1, 5) * dx
        nox = max(10, nox)
        noxList.append(nox)
    return noxList

kron_nox_year = genereate_random_year_dataList(intencity=1.0, seed = 2)
nord_nox_year = genereate_random_year_dataList(intencity=.3, seed = 1)


def gjennomsnitt(nordnes, kronstad):
    avg = []
    for index in range(0,len(nordnes)):
        avg.append((nordnes[index]+kronstad[index])/2)
    return avg

gjen_nox_year = gjennomsnitt(kron_nox_year,nord_nox_year)


#create figure and 3 axis
fig = plt.figure(figsize=(13, 5))

axNok = fig.add_axes((0.05, 0.05, 0.45, 0.9))
axInterval = fig.add_axes((0.4, 0.5, 0.1, 0.25))
axBergen = fig.add_axes((0.5, 0.05, 0.5, 0.9))

axInterval.patch.set_alpha(0.5)

coordinates_Nordnes = (90, 60)
coordinates_Kronstad = (600, 750)
coordinates_LilleLongGardsvann = (450, 335)
days_interval = (1,366)
marked_point = (0,0)



def on_day_interval(kvartal):
    global days_interval, marked_point
    axNok.cla()
    days_interval = (1,366)
    if kvartal == '1. Kvartal':
        days_interval = (1,90)
    if kvartal == '2. Kvartal':
        days_interval = (90, 180)
    if kvartal == '3. Kvartal':
        days_interval = (180,270)
    if kvartal == '4. Kvartal':
        days_interval = (270,366)
    marked_point = (0, 0)
    plot_graph()
        

def on_click(event) :
    global marked_point
    if ax := event.inaxes:
        if ax == axBergen:
            marked_point = (event.xdata, event.ydata)
            plot_graph()

#estimate NOX value based on the two measuring stations
def calc_point_value(valN, valK):
    dist_nordnes = math.dist(coordinates_Nordnes, marked_point)
    dist_kronstad = math.dist(coordinates_Kronstad, marked_point)
    distNordnesKronstad = math.dist(coordinates_Nordnes, coordinates_Kronstad)
    val = (1 - dist_kronstad / (dist_kronstad + dist_nordnes)) * valK + (1 - dist_nordnes / (dist_kronstad + dist_nordnes)) * valN
    val = val * (distNordnesKronstad / (dist_nordnes + dist_kronstad)) ** 4

    return val

def lille_longgardsvann (valN, valK):
    dist_nordnes = math.dist(coordinates_Nordnes, coordinates_LilleLongGardsvann)
    dist_kronstad = math.dist(coordinates_Kronstad, coordinates_LilleLongGardsvann)
    distNordnesKronstad = math.dist(coordinates_Nordnes, coordinates_Kronstad)
    val = (1 - dist_kronstad / (dist_kronstad + dist_nordnes)) * valK + (1 - dist_nordnes / (dist_kronstad + dist_nordnes)) * valN
    val = val * (distNordnesKronstad / (dist_nordnes + dist_kronstad)) ** 4

    return val

# Make two circles in Nordnes and Kronstad
def draw_circles_stations():
    circle = mpatches.Circle((90,60), 25, color='blue')
    axBergen.add_patch(circle)
    circle = mpatches.Circle((600, 750), 25, color='red')
    axBergen.add_patch(circle)
    circle = mpatches.Circle((450,335),25,color="green")
    axBergen.add_patch(circle)

def draw_label_and_ticks():
    num_labels = 12
    xlabels = create_dates()
    xticks = np.linspace(1, 365, 52)
    if days_interval[1] == 90:

       xlabels = ['1.1', '8.1', '15.1', '22.1', '29.1', '5.2', '12.2', '19.2', '26.2', '5.3', '12.3', '19.3', '26.3']
       xticks = [1,7,15,22,30,37,43,50,57,65,72,80,87]
    if days_interval[1] == 180:
       xticks = [1,7,15,22,30,37,43,50,57,65,72,80,87]
       xlabels = ['2.4', '9.4', '16.4', '23.4', '30.4', '7.5', '14.5', '21.5', '28.5', '4.6', '11.6', '18.6', '25.6']
    if days_interval[1] == 270:
       xticks = [1,7,15,22,30,37,43,50,57,65,72,80,87]
       xlabels = ['2.7', '9.7', '16.7', '23.7', '30.7', '6.8', '13.8', '20.8', '27.8', '3.9', '10.9', '17.9', '24.9']
    if days_interval[0] == 270:
       xticks = [1,7,15,22,30,37,43,50,57,65,72,80,87]
       xlabels = ['1.10', '8.10', '15.10', '22.10', '29.10', '5.11', '12.11', '19.11', '26.11', '3.12', '10.12', '17.12', '31.12']

    #plt.xticks(rotation = 120)
    axNok.set_xticks(xticks)
    axNok.set_xticklabels(xlabels, rotation = 70)

def plot_graph():

    axNok.cla()
    axBergen.cla()
    nord_nox = nord_nox_year[days_interval[0]:days_interval[1]]
    kron_nox = kron_nox_year[days_interval[0]:days_interval[1]]
    days = len(nord_nox)
    lille_nox = [lille_longgardsvann(nord_nox[i], kron_nox[i]) for i in range(days)]
    gjen_nox = gjen_nox_year[days_interval[0]:days_interval[1]]


    list_days = np.linspace(1, days, days)

#draw the marked point & the orange graph
    l5 = None
    if marked_point != (0,0):
        nox_point = [calc_point_value(nord_nox[i], kron_nox[i]) for i in range(days)]
        l5, = axNok.plot(list_days, nox_point, 'darkorange')
        circle = mpatches.Circle((marked_point[0], marked_point[1]), 25, color='orange')
        axBergen.add_patch(circle)

    l1, = axNok.plot(list_days, nord_nox, 'blue')
    l2, = axNok.plot(list_days, kron_nox, 'red')
    l3, = axNok.plot(list_days, lille_nox, 'green')
    l4, = axNok.plot(list_days,gjen_nox,'black' )
    axNok.set_title("NOX verdier")
    axInterval.set_title("Intervall")

    lines = [l1, l2, l3, l4] if l5 is None else [l1,l2, l3, l4, l5]
    axNok.legend(lines, ["Nordnes", "Kronstad", "Lille Longgårdsvann","Gjennomsnitt", "Markert plass"])
    axNok.grid(linestyle='--')
    draw_label_and_ticks()

    #Plot Map of Bergen
    axBergen.axis('off')
    img = mpimg.imread('bergen.png')
    img = axBergen.imshow(img)
    axBergen.set_title("Kart Bergen")
    draw_circles_stations()
    plt.draw()




#plot_graph_nox()

plot_graph()

# draw radiobutton interval
listFonts = [12] * 5
listColors = ['yellow'] * 5
radio_button = RadioButtons(axInterval, ('2023',
                                          '1. Kvartal',
                                          '2. Kvartal',
                                          '3. Kvartal',
                                          '4. Kvartal'),
                            label_props={'color': listColors, 'fontsize' : listFonts},
                            radio_props={'facecolor': listColors,  'edgecolor': listColors},
                            )
axInterval.set_facecolor('darkblue')
radio_button.on_clicked(on_day_interval)
# noinspection PyTypeChecker
plt.connect('button_press_event', on_click)

plt.show()

