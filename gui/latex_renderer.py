# gui/latex_renderer.py

from matplotlib import pyplot as plt
from io import BytesIO
from PyQt5.QtGui import QPixmap

def render_latex_to_pixmap(latex_str):
    buffer = BytesIO()
    plt.figure(figsize=(6,2))
    plt.text(0.5, 0.5, latex_str, fontsize=16, ha='center', va='center')
    plt.axis('off')
    plt.savefig(buffer, format='png', bbox_inches='tight', pad_inches=0.1)
    plt.close()
    buffer.seek(0)
    pixmap = QPixmap()
    pixmap.loadFromData(buffer.getvalue())
    return pixmap
