from typing import List
import pandas as pd

def get_labels(df: pd.DataFrame) -> List[str]:
    """Extract column labels from a DataFrame."""
    if df is not None and not df.empty:
        return df.columns.tolist()
    return []
