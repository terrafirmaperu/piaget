"""Copia alumna-huancavelicana.png a static/img/website si falta."""
import os
import shutil


def ensure_alumna_image(base_dir=None):
    if base_dir is None:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    dest_dir = os.path.join(base_dir, 'static', 'img', 'website')
    dest = os.path.join(dest_dir, 'alumna-huancavelicana.png')
    if os.path.isfile(dest) and os.path.getsize(dest) > 0:
        return dest

    home = os.path.expanduser('~')
    candidates = [
        os.path.join(
            home,
            '.cursor',
            'projects',
            'c-Users-ASUS-Desktop-sistemas-piayetIa',
            'assets',
            'alumna-huancavelicana.png',
        ),
        os.path.join(base_dir, 'assets', 'alumna-huancavelicana.png'),
        os.path.join(dest_dir, 'inicio.png'),
    ]

    os.makedirs(dest_dir, exist_ok=True)
    for src in candidates:
        if os.path.isfile(src) and os.path.getsize(src) > 0:
            shutil.copy2(src, dest)
            return dest
    return None


if __name__ == '__main__':
    path = ensure_alumna_image()
    print('OK:' if path else 'FALTA:', path)
