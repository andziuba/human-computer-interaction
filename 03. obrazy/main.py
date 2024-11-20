import matplotlib.pyplot as plt
from skimage import io
from skimage.color import rgb2gray
from skimage.feature import canny
from skimage.morphology import dilation, disk, remove_small_objects
from skimage.measure import find_contours
from scipy.ndimage import binary_fill_holes

img_paths = ['./planes/samolot00.jpg', './planes/samolot01.jpg', './planes/samolot03.jpg', './planes/samolot04.jpg',
             './planes/samolot05.jpg', './planes/samolot07.jpg', './planes/samolot08.jpg', './planes/samolot09.jpg',
             './planes/samolot10.jpg', './planes/samolot11.jpg', './planes/samolot12.jpg', './planes/samolot13.jpg',
             './planes/samolot14.jpg', './planes/samolot15.jpg', './planes/samolot16.jpg', './planes/samolot17.jpg',
             './planes/samolot18.jpg', './planes/samolot20.jpg']

colors = ['#D62728', '#2CA02C', '#FF7F0E', '#8C564B', '#9467BD', '#17BECF', '#BCBD22', '#E377C2']


def main():
    fig, axes = plt.subplots(3, 6, figsize=(24, 12))
    axes = axes.flatten()

    for i, img_path in enumerate(img_paths):
        img = io.imread(img_path)
        gray_img = rgb2gray(img)  # konwersja na skale szarosci
        gamma_img = gray_img ** 0.4  # wzmocnienie kontrastu przez korekcje gamma
        edges_img = canny(gamma_img, sigma=3.0)  # wykrywanie krawedzi
        dilated_img = dilation(edges_img, disk(4))  # dylatacja w celu pogrubienia krawedzi
        filled_edges_img = binary_fill_holes(dilated_img)  # wypelnianie krawedzi
        cleared_img = remove_small_objects(filled_edges_img, 1000)  # usuwanie malych obiektow

        contours = find_contours(cleared_img, 0.8)

        ax = axes[i]
        ax.axis('off')
        ax.imshow(img)

        for j, contour in enumerate(contours):
            ax.plot(contour[:, 1], contour[:, 0], linewidth=1.5, color=colors[j % len(colors)])
            center = (sum(contour[:, 1]) / len(contour[:, 1]), sum(contour[:, 0]) / len(contour[:, 0]))
            ax.scatter(center[0], center[1], color='white', s=10)

    plt.tight_layout()
    plt.savefig('detected.jpg', dpi=400)
    plt.show()


if __name__ == '__main__':
    main()
