import pandas as pd
from typing import List, Dict


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


def category_orders(df: pd.DataFrame) -> Dict[str, List[float]]:
    return {
        col: sorted(df[col].dropna().unique())
        for col in df.loc[:, df.dtypes == 'category']
    }
