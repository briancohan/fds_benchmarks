from pathlib import Path
from typing import List, Dict
import pandas as pd


LABELS = {
    'chipset': 'Chipset',
    'cores': 'Physical Cores',
    'HD time': 'Heat Detector',
    'logical': 'Logical Cores',
    'OMP': 'Threads',
    'RAM': 'RAM [GB]',
    'resolution': 'Resolution [cm]',
    'speed': 'Speed [GHz]',
    'Wall time': 'Wall Time [sec]',
}

IMAGE_DIR = Path('images')
IMAGE_DIR.mkdir(exist_ok=True)


def category_orders(df: pd.DataFrame) -> Dict[str, List[float]]:
    return {
        col: sorted(df[col].dropna().unique())
        for col in df.loc[:, df.dtypes == 'category']
    }


def save(fig, stem):
    fig.write_image(str(IMAGE_DIR / f'{stem}.png'), engine='kaleido')
