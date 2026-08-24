from pathlib import Path
import pandas as pd

RAW = Path("data/raw")


def load_sources():
    return {
        "customers.csv": pd.read_csv(RAW / "customers.csv"),
        "orders.json": pd.read_json(RAW / "orders.json"),
        "products.parquet": pd.read_parquet(RAW / "products.parquet"),
    }


def profile(name: str, df: pd.DataFrame, path: Path) -> None:
    print(f"\n{'=' * 60}")
    print(f"=== {name} ===")
    print(f"{'=' * 60}")

    size_kb = round(path.stat().st_size / 1024, 2)
    print(f"file size: {size_kb} KB")
    print(f"shape (rows, cols): {df.shape}")
    print(f"columns in original order: {list(df.columns)}")

    print("\n-- dtypes --")
    print(df.dtypes)

    print("\n-- nulls per column --")
    print(df.isna().sum())

    try:
        dup_count = df.duplicated().sum()
    except TypeError:
        # Some columns (e.g. orders.json's nested 'shipping' dicts) are
        # unhashable, so pandas can't compare full rows directly. Cast
        # unhashable columns to strings just for this duplicate check.
        comparable = df.copy()
        for col in comparable.columns:
            if comparable[col].apply(lambda v: isinstance(v, (dict, list))).any():
                comparable[col] = comparable[col].astype(str)
        dup_count = comparable.duplicated().sum()
    print(f"\nfully duplicated rows: {dup_count}")

    print("\n-- distinct values per column --")
    for col in df.columns:
        try:
            print(f"  {col}: {df[col].nunique()}")
        except TypeError:
            print(f"  {col}: (unhashable/nested type - nunique skipped)")

    print("\n-- first 5 records --")
    print(df.head())

    numeric_cols = df.select_dtypes(include="number").columns
    if len(numeric_cols):
        print("\n-- numeric ranges --")
        for col in numeric_cols:
            print(f"  {col}: min={df[col].min()}, max={df[col].max()}")

    print("\n-- date/time-like columns (safe-parsed) --")
    found_date_col = False
    for col in df.columns:
        if "date" in col.lower() or "time" in col.lower():
            parsed = pd.to_datetime(df[col], errors="coerce")
            if parsed.notna().any():
                found_date_col = True
                unparseable = parsed.isna().sum()
                print(
                    f"  {col}: earliest={parsed.min()}, latest={parsed.max()}, "
                    f"unparseable_after_coercion={unparseable}"
                )
    if not found_date_col:
        print("  (no date/time-like columns detected by name heuristic)")


def main():
    files = {
        "customers.csv": RAW / "customers.csv",
        "orders.json": RAW / "orders.json",
        "products.parquet": RAW / "products.parquet",
    }
    dataframes = load_sources()
    for name, df in dataframes.items():
        profile(name, df, files[name])


if __name__ == "__main__":
    main()
