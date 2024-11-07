import matplotlib
import matplotlib.pyplot as plt
from matplotlib import rc
import numpy as np
from matplotlib import colors

def hsv2rgb(h, s, v):
    return colors.hsv_to_rgb((h, s, v))

# poniżej znajdują się funkcje modelujące kolejne gradienty z zadania.
# v to pozycja na osi ox: v jest od 0 do 1. Zewnetrzna funkcja wywołuje te metody podając
# różne v i oczekując trójki RGB bądź HSV reprezentującej kolor. Np. (0,0,0) w RGB to kolor czarny. 
# Należy uwikłać v w funkcję modelującą kolor. W tym celu dla kolejnych gradientów trzeba przyjąć 
# sobie jakieś punkty charakterystyczne,
# np. widzimy, że po lewej stronie (dla v = 0) powinien być kolor zielony a w środku niebieski (dla v = 0.5),
# a wszystkie punkty pomiędzy należy interpolować liniowo (proporcjonalnie). 

def gradient_rgb_bw(v):
    return (v, v, v)

def gradient_rgb_gbr(v):
    if v < 0.5:
        return (0, 1 - 2*v, 2*v)  # Od zielonego (0,1,0) do niebieskiego (0,0,1)
    else:
        return (2*(v - 0.5), 0, 1 - 2*(v - 0.5))  # Od niebieskiego do czerwonego (1,0,0)

#010 011 001 101 100
def gradient_rgb_gbr_full(v):
    if v < 0.25:
        # Od zielonego (0, 1, 0) do zielono-niebieskiego (0, 1, 1)
        return (0, 1, 4*v)  # Różnicowanie niebieskiego w górę
    elif v < 0.5:
        # Od zielono-niebieskiego (0, 1, 1) do niebieskiego (0, 0, 1)
        return (0, 1 - 4*(v - 0.25), 1)  # Zmniejszamy zielony, utrzymujemy niebieski
    elif v < 0.75:
        # Od niebieskiego (0, 0, 1) do fioletowego (1, 0, 1)
        return (4*(v - 0.5), 0, 1)  # Różnicowanie czerwonego w górę
    else:
        # Od fioletowego (1, 0, 1) do czerwonego (1, 0, 0)
        return (1, 0, 1 - 4*(v - 0.75))  # Zmniejszamy niebieski


#bialy niebieski zielony czerwony czarny
#111 101 001 011 010 110 100 000
def gradient_rgb_wb_custom(v):
    if v < 0.14:
        # Od białego (1, 1, 1) do czerwonego (1, 0, 1)
        return (1, 1 - 7.14*v, 1)  # Zmniejszamy zielony w miarę wzrostu v
    elif v < 0.28:
        # Od czerwonego (1, 0, 1) do niebieskiego (0, 0, 1)
        return (1 - 7.14*(v - 0.14), 0, 1)  # Zmniejszamy czerwony w miarę wzrostu v, niebieski pozostaje na 1
    elif v < 0.42:
        # Od niebieskiego (0, 0, 1) do zielono-niebieskiego (0, 1, 1)
        return (0, 7.14*(v - 0.28), 1)  # Zwiększamy zielony, niebieski jest na 1
    elif v < 0.57:
        # Od zielono-niebieskiego (0, 1, 1) do zielonego (0, 1, 0)
        return (0, 1, 1 - 7.14*(v - 0.42))  # Zmniejszamy niebieski
    elif v < 0.71:
        # Od zielonego (0, 1, 0) do zielono-czerwonego (1, 1, 0)
        return (7.14*(v - 0.57), 1, 0)  # Zwiększamy czerwony, zielony jest na 1
    elif v < 0.85:
        # Od zielono-czerwonego (1, 1, 0) do czerwonego (1, 0, 0)
        return (1, 1 - 7.14*(v - 0.71), 0)  # Zmniejszamy zielony
    else:
        # Od czerwonego (1, 0, 0) do czarnego (0, 0, 0)
        return (1 - 7.14*(v - 0.85), 0, 0)  # Zmniejszamy czerwony


def gradient_hsv_bw(v):
    return hsv2rgb(0, 0, v)  # Wartość `v` wzrasta od 0 do 1


#120 240 0s
def gradient_hsv_gbr(v):
    h = (120 + (v * 240)) /360  # Zwiększa hue od 120° do 240°
    return hsv2rgb(h, 1, 1)  # Maksymalne nasycenie i jasność

#120 1
def gradient_hsv_unknown(v):
    h = (120 - (v * 120)) /360  # Zwiększa hue od 120° do 240°
    return hsv2rgb(h, 0.5, 1)  # Maksymalne nasycenie i jasność


def gradient_hsv_custom(v):
    h = v  # Pełne koło kolorów w odwrotnym kierunku
    s = 1 - v  # Nasycenie rośnie
    return hsv2rgb(h, s, 1)


def plot_color_gradients(gradients, names):
    # For pretty latex fonts (commented out, because it does not work on some machines)
    #rc('text', usetex=True) 
    #rc('font', family='serif', serif=['Times'], size=10)
    rc('legend', fontsize=10)

    column_width_pt = 400         # Show in latex using \the\linewidth
    pt_per_inch = 72
    size = column_width_pt / pt_per_inch

    fig, axes = plt.subplots(nrows=len(gradients), sharex=True, figsize=(size, 0.75 * size))
    fig.subplots_adjust(top=1.00, bottom=0.05, left=0.25, right=0.95)


    for ax, gradient, name in zip(axes, gradients, names):
        # Create image with two lines and draw gradient on it
        img = np.zeros((2, 1024, 3))
        for i, v in enumerate(np.linspace(0, 1, 1024)):
            img[:, i] = gradient(v)

        im = ax.imshow(img, aspect='auto')
        im.set_extent([0, 1, 0, 1])
        ax.yaxis.set_visible(False)

        pos = list(ax.get_position().bounds)
        x_text = pos[0] - 0.25
        y_text = pos[1] + pos[3]/2.
        fig.text(x_text, y_text, name, va='center', ha='left', fontsize=10)

    fig.savefig('my-gradients.pdf')

def toname(g):
    return g.__name__.replace('gradient_', '').replace('_', '-').upper()
    
gradients = (gradient_rgb_bw, gradient_rgb_gbr, gradient_rgb_gbr_full, gradient_rgb_wb_custom,
                 gradient_hsv_bw, gradient_hsv_gbr, gradient_hsv_unknown, gradient_hsv_custom)

plot_color_gradients(gradients, [toname(g) for g in gradients])
