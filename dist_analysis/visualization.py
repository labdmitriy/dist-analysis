import matplotlib.pyplot as plt
from matplotlib_venn import venn3, venn3_circles
import numpy as np


def plot_names_with_punctuation(
    names_with_hyphens, names_with_underscores, names_with_dots, image_file_path=None
):
    label_fontsize = 16
    title_fontsize = 20
    fig, axes = plt.subplots(figsize=(14, 14))

    subsets = set(names_with_hyphens), set(names_with_underscores), set(names_with_dots)
    set_labels = ('', '', '')
    v = venn3(subsets=subsets, set_labels=set_labels, ax=axes)
    v.get_label_by_id('100').set_position(xy=(0.25, 0.04))

    venn3_circles(subsets=subsets, linewidth=0.3, ax=axes)

    for text in v.subset_labels:
        text.set_fontsize(label_fontsize)

    axes.annotate(
        'Only hyphens',
        xy=v.get_label_by_id('100').get_position() - np.array([0, 0.02]),
        xytext=(0, -20),
        ha='center',
        textcoords='offset points',
        fontsize=label_fontsize,
        bbox=dict(boxstyle='round,pad=0.5', fc='gray', alpha=0.1)
    )
    axes.annotate(
        'Only underscores',
        xy=v.get_label_by_id('010').get_position() + np.array([0.025, 0.005]),
        xytext=(150, 20),
        ha='center',
        textcoords='offset points',
        fontsize=label_fontsize,
        bbox=dict(boxstyle='round,pad=0.5', fc='gray', alpha=0.1),
        arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0', color='gray')
    )
    axes.annotate(
        'Hyphens and underscores',
        xy=v.get_label_by_id('110').get_position() + np.array([0, 0.015]),
        xytext=(120, 150),
        ha='center',
        textcoords='offset points',
        fontsize=label_fontsize,
        bbox=dict(boxstyle='round,pad=0.5', fc='gray', alpha=0.1),
        arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.4', color='gray')
    )
    axes.annotate(
        'Hyphens, underscores and dots',
        xy=v.get_label_by_id('111').get_position() + np.array([0.01, 0]),
        xytext=(370, -40),
        ha='center',
        textcoords='offset points',
        fontsize=label_fontsize,
        bbox=dict(boxstyle='round,pad=0.5', fc='gray', alpha=0.1),
        arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.2', color='gray')
    )
    axes.annotate(
        'Underscores and dots',
        xy=v.get_label_by_id('011').get_position() + np.array([0.015, 0]),
        xytext=(200, -100),
        ha='center',
        textcoords='offset points',
        fontsize=label_fontsize,
        bbox=dict(boxstyle='round,pad=0.5', fc='gray', alpha=0.1),
        arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.2', color='gray')
    )
    axes.annotate(
        'Hyphens and dots',
        xy=v.get_label_by_id('101').get_position() - np.array([0, 0.02]),
        xytext=(-20, -210),
        ha='center',
        textcoords='offset points',
        fontsize=label_fontsize,
        bbox=dict(boxstyle='round,pad=0.5', fc='gray', alpha=0.1),
        arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.2', color='gray')
    )
    axes.annotate(
        'Only dots',
        xy=v.get_label_by_id('001').get_position() + np.array([0.025, 0]),
        xytext=(120, -40),
        ha='center',
        textcoords='offset points',
        fontsize=label_fontsize,
        bbox=dict(boxstyle='round,pad=0.5', fc='gray', alpha=0.1),
        arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.2', color='gray')
    )
    axes.set_title(
        'Python distribution names\nwith punctuation',
        loc='center',
        x=0.7,
        y=0.93,
        fontsize=title_fontsize
    )
    axes.set_xlim(xmin=0.1)
    axes.set_ylim(ymin=-0.45, ymax=0.3)

    if image_file_path:
        plt.savefig(image_file_path, bbox_inches='tight')

    plt.show()
