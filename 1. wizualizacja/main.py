import matplotlib.pyplot as plt

plt.rcParams.update({
    'font.family': 'Times New Roman', 'font.size': 8,
    'xtick.direction': 'in', 'ytick.direction': 'in',  # Kierunek znaczników na osiach
    'grid.linestyle': [1, 4],  # Styl linii siatki
})

labels = ['1-Evol-RS', '1-Coev-RS', '2-Coev-RS', '1-Coev', '2-Coev']
colors = ['blue', 'green', 'red', 'black', 'magenta']
markers = ['o', 'v', 'D', 's', 'd']


def load_file(path):
    with open(path, 'r') as file:
        data = file.readlines()
    return [line.strip().split(',') for line in data]


def line_plot(ax0, algorithms):
    for i, algorithm_data in enumerate(algorithms):
        # Przeksztalca dane z 2. kolumny pliku (effort) na oś X – liczba rozegranych gier (x1000)
        x_axis_effort = [float(row[1]) / 1000.0 for row in algorithm_data[1:]]

        # Srednia wartosc procentowa wygranych gier
        y_axis = []
        for j in algorithm_data[1:]:  # Pomin wiersz z naglowkami
            values = [float(value) for value in j[2:]]  # Dane od 3. kolumny
            avarage = sum(values) / len(values) * 100.0  # Mnozenie przez 100, aby uzyskac wartosc procentowa
            y_axis.append(avarage)

        ax0.plot(x_axis_effort,
                 y_axis,
                 label=labels[i],
                 color=colors[i],
                 linewidth=0.9,
                 marker=markers[i],
                 markevery=25,
                 markersize=5,
                 markeredgecolor='black',
                 markeredgewidth=0.5)

    # Formatowanie osi X
    ax0.set_xlabel("Rozegranych gier (x1000)")
    ax0.set_xlim(0, 500)  # Zakres osi X
    ax0.set_xticks(range(0, 501, 100))  # Zakres etykiet osi X

    ax0.set_ylabel("Odsetek wygranych gier [%]")
    ax0.set_ylim(60, 100)  # Zakres osi Y
    ax0.set_yticks(range(60, 101, 5))  # Zakres etykiet osi Y

    # Dodanie dodatkowej gornej osi X
    x_axis_top = ax0.twiny()
    x_axis_top.set_xlabel("Pokolenie")
    top_ticks = range(0, 201, 40)  # Zakres wartosci dla gornej osi X
    x_axis_top.set_xticks(top_ticks)

    ax0.legend(loc=4)  # Legenda - prawy dolny rog
    ax0.grid()  # Wlaczenie siatki


def box_plot(ax1, algorithms):
    box_data = []
    for algorithm_data in algorithms:
        # Pobranie danych z ostatniego wiersza i przekształcenie ich na wartosci procentowe
        last_row = [float(value) * 100 for value in algorithm_data[-1][2:]]
        box_data.append(last_row)

    ax1.boxplot(box_data,
                notch=True,  # wciecie w pudelku
                boxprops={'color': 'blue'},  # kolor pudelka
                showmeans=True,  # srednie wartosci
                meanprops={'marker': 'o', 'markersize': 4, 'markerfacecolor': 'blue', 'markeredgecolor': 'black'},
                medianprops={'color': 'red'},  # kolor median
                flierprops={'marker': '+', 'markersize': 4, 'markeredgewidth': 0.9, 'markerfacecolor': 'blue',
                            'markeredgecolor': 'blue'},  # wlasciwosci punktow odstajacych
                capprops={'color': 'black'},  # min/max
                whiskerprops={'color': 'blue', 'linestyle': '-', 'dashes': (6, 5)}  # wasy
                )

    # Formatowanie osi X
    ax1.set_xticklabels(labels, rotation=20)

    # Formatowanie osi Y
    ax1.yaxis.tick_right()
    ax1.set_ylim(60, 100)
    ax1.set_yticks(range(60, 101, 5))

    # Dodanie dodatkowej gornej osi X (bez etykiet)
    ax1_1 = ax1.twiny()
    ax1_1.set_xlim(-0.5, 4.5)
    ax1_1.set_xticks(range(0, 5))
    ax1_1.set_xticklabels([])

    ax1.grid(True) 


def main():
    # Wczytanie danych z plikow
    rsel = load_file('./results/rsel.csv')
    cel_rs = load_file('./results/cel-rs.csv')
    cel_rs2 = load_file('./results/2cel-rs.csv')
    cel = load_file('./results/cel.csv')
    cel2 = load_file('./results/2cel.csv')

    algorithms = [rsel, cel_rs, cel_rs2, cel, cel2]

    fig, ax = plt.subplots(ncols=2)
    fig.set_figwidth(6.7)

    line_plot(ax[0], algorithms)

    box_plot(ax[1], algorithms)

    plt.savefig('plot.pdf')
    plt.close()


if __name__ == '__main__':
    main()
