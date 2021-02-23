"""Process data from excel file."""
import re
import pandas as pd


CHIPSET = re.compile(r'^[^@]+', re.IGNORECASE)
SPEED = re.compile(r'[\d\.]+(?=\s*[GM]Hz)', re.IGNORECASE)
CORES = re.compile(r'\d+(?=\s?Core)', re.IGNORECASE)
LOGICAL = re.compile(r'\d+(?=\sLogical)', re.IGNORECASE)
WS_GRID = 'Grid_Size'
WS_OMP = 'Multiple_Meshes'

GRID = [
    'Student',
    '20 cm - HD', '20 cm - Wall',
    '10 cm - HD', '10 cm - Wall',
    '5 cm - HD', '5 cm - Wall',
]
OMP = ['Student', 'OMP 1', 'OMP 2', 'OMP 3', 'OMP 4']
KEEP = ['Student', 'Remarks', 'RAM', 'chipset', 'speed', 'cores', 'logical']


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
    data = data.reset_index().rename(columns={'index': 'Student'})

    for col in ['Student', 'RAM', 'cores', 'logical']:
        data[col] = pd.Categorical(data[col])

    return data


def grid_data(df: pd.DataFrame) -> pd.DataFrame:
    """Grid resolution modeling data suitable for plotting."""
    _df = df[GRID].melt(id_vars='Student')

    parts = _df.variable.str.split('-', expand=True)
    parts.columns = ['resolution', 'component']
    parts['resolution'] = pd.to_numeric(
        [i[0] for i in parts.resolution.str.split()]
    )
    _df = _df.join(parts)

    _df = _df.pivot(
        index=['Student', 'resolution'],
        columns='component',
        values='value'
    ).reset_index()

    _df = _df.rename(columns={' HD': 'HD time', ' Wall': 'Wall time'})

    _df['resolution'] = pd.Categorical(_df['resolution'])

    return _df.merge(df[KEEP], on='Student')


def omp_data(df: pd.DataFrame) -> pd.DataFrame:
    """OMP modeling data suitable for plotting."""
    _df = df[OMP].melt(id_vars='Student', value_name='Wall time')

    _df['OMP'] = [i[1] for i in _df.variable.str.split()]
    _df['OMP'] = pd.to_numeric(_df['OMP'])
    _df = _df.drop(columns=['variable'])

    _df['OMP'] = pd.Categorical(_df['OMP'])

    return _df.merge(df[KEEP], on='Student')
