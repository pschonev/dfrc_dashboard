import marimo

__generated_with = "0.11.20"
app = marimo.App(
    width="medium",
    app_title="Double Fischer Random Chess Analysis",
    layout_file="layouts/analysis_dashboard.grid.json",
)


@app.cell
def _():
    import marimo as mo
    import polars as pl

    import pyarrow as pa

    FEN_TEMPLATE = "https://lichess.org/analysis/{black}/pppppppp/8/8/8/8/PPPPPPPP/{white}_w_KQkq_-_0_1?color=white"
    data_path = mo.notebook_location() / "public" / "analysis_results.parquet"
    return FEN_TEMPLATE, data_path, mo, pl, pa


@app.cell
def _(data_path, mo, pl, pa):
    import io
    import urllib.request

    def flexible_read_parquet(path):
        path_str = str(path)

        # Check if it's a URI (starts with http)
        if path_str.startswith(("http://", "https://")):
            # For HTTP URIs, fetch the content as bytes
            with urllib.request.urlopen(path_str) as response:
                parquet_bytes = response.read()
            # Read from bytes with use_pyarrow=True
            return pl.read_parquet(io.BytesIO(parquet_bytes), use_pyarrow=True)
        else:
            # Try direct read first
            try:
                return pl.read_parquet(path)
            except Exception:
                # If direct read fails, try reading as bytes with use_pyarrow=True
                with open(path, "rb") as f:
                    parquet_bytes = f.read()
                return pl.read_parquet(io.BytesIO(parquet_bytes), use_pyarrow=True)

    # Use the flexible function
    df = flexible_read_parquet(data_path)
    table = mo.ui.table(df, selection="single")
    table
    return df, flexible_read_parquet, io, table, urllib


@app.cell
def _(FEN_TEMPLATE, table):
    fen_white = table.value["white"][0] if not table.value.is_empty() else "rnbqkbnr"
    fen_black = table.value["black"][0] if not table.value.is_empty() else "rnbqkbnr"
    dfrc_id = table.value["dfrc_id"][0] if not table.value.is_empty() else "518"
    fen = FEN_TEMPLATE.format(black=fen_black, white=fen_white.upper())
    return dfrc_id, fen, fen_black, fen_white


@app.cell
def _(dfrc_id, fen, mo):
    mo.md(f"[Open lichess Analysis board for {dfrc_id}]({fen})")
    return


@app.cell
def _(fen, mo):
    mo.Html(
        f'<iframe src="{fen}" style="width: 900px; aspect-ratio: 12/11;" allowtransparency="true" frameborder="0"></iframe>'
    )
    return


if __name__ == "__main__":
    app.run()
