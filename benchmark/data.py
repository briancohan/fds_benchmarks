"""Process data from excel file."""
import re
import pandas as pd


CHIPSET = re.compile(r'^[^@]+', re.IGNORECASE)
SPEED = re.compile(r'[\d\.]+(?=\s*[GM]Hz)', re.IGNORECASE)
CORES = re.compile(r'\d+(?=\s?Core)', re.IGNORECASE)
LOGICAL = re.compile(r'\d+(?=\sLogical)', re.IGNORECASE)
WS_GRID = 'Grid_Size'
WS_OMP = 'Multiple_Meshes'


ID_VARS = ['Remarks', 'RAM', 'chipset', 'speed', 'cores', 'logical']
GRID = ID_VARS + [
    '20 cm - HD', '20 cm - Wall',
    '10 cm - HD', '10 cm - Wall',
    '5 cm - HD', '5 cm - Wall',
]
OMP = ID_VARS + ['OMP 1', 'OMP 2', 'OMP 3', 'OMP 4']


def search(pattern, text):
    try:
        match = pattern.search(text)
    except TypeError:
        return
    if match is not None:
        return match.group(0)


def processor_data(txt):
    return {
        'chipset': search(CHIPSET, txt),
        'speed': search(SPEED, txt),
        'cores': search(CORES, txt),
        'logical': search(LOGICAL, txt),
    }


def used_range(file: str, sheet: str) -> pd.DataFrame:
    """Get used range of worksheet.

    Reads in worksheet and drops rows and columns that are completly null.
    """
    return (
        pd.read_excel(file, sheet, index_col=0)
        .dropna(how='all', axis=0)
        .dropna(how='all', axis=1)
    )


def remove_names(df: pd.DataFrame) -> pd.DataFrame:
    """Convert personal names to numerical values."""
    df = df.reset_index()
    df.drop(columns='Name', inplace=True)
    return df


def parse_cpu(df: pd.DataFrame, col: str = 'Chip') -> pd.DataFrame:
    """Parse CPU strings into data."""
    proc = pd.DataFrame([processor_data(i) for i in df[col]])
    df.drop(columns=[col], inplace=True)
    for col in ['speed', 'cores', 'logical']:
        proc[col] = pd.to_numeric(proc[col])
    proc.loc[proc.speed > 100, 'speed'] /= 1000
    return df.join(proc)


def parse_ram(df: pd.DataFrame, col: str = 'RAM') -> pd.DataFrame:
    """Convert RAM column to numeirc."""
    mask = ~df.RAM.isna()
    df.loc[mask, 'RAM'] = [m[0] for m in df.loc[mask, 'RAM'].str.split()]
    df['RAM'] = pd.to_numeric(df.RAM)
    return df


def parse_excel(file: str) -> pd.DataFrame:
    grid = used_range(file, WS_GRID)
    omp = used_range(file, WS_OMP)

    data = grid.join(omp, how='outer')
    data = remove_names(data)
    data = parse_cpu(data)
    data = parse_ram(data)
    return data


def grid_data(df: pd.DataFrame) -> pd.DataFrame:
    """Grid resolution modeling data suitable for plotting."""
    df = df[GRID].melt(id_vars=ID_VARS)

    parts = df.variable.str.split('-', expand=True)
    parts.columns = ['resolution', 'component']
    df = df.join(parts)
    df['resolution'] = [i[0] for i in df.resolution.str.split()]

    return df
