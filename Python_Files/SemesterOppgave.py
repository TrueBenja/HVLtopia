import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import RadioButtons
import matplotlib.image as mpimg
import matplotlib.patches as mpatches

#Generater random data for a year
# centervals are values average values for each month
# samedata = false, new data each time program is called
import random
from random import randint
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
#lille_nox_year = genereate_random_year_dataList(intencity=.6, seed = 3)
kron_asfaltstov_year = genereate_random_year_dataList(intencity=2.0, seed = 5)
nord_asfaltstov_year = genereate_random_year_dataList(intencity=0.7, seed = 4)
#lille_asfaltstov_year = genereate_random_year_dataList(intencity=1.2, seed = 2)

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
    xlabels = ['J' ,'F' ,'M' ,'A' ,'M' ,'J', 'J', 'A', 'S', 'O', 'N', 'D']
    xticks = np.linspace(15, 345, num_labels)
    if days_interval[1] == 90:
        xticks = [15,45,75]
        xlabels = ['Jan', 'Feb', 'Mars']
    if days_interval[1] == 180:
        xticks = [15,45,75]
        xlabels = ['April', 'Mai', 'Juni']
    if days_interval[1] == 270:
        xticks = [15, 45, 75]
        xlabels = ['July', 'Aug', 'Sept']
    if days_interval[0] == 270:
        xticks = [15, 45, 75]
        xlabels = ['Okt', 'Nov', 'Des']
    axNok.set_xticks(xticks)
    axNok.set_xticklabels(xlabels)

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

