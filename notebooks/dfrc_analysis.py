# /// script
# [tool.marimo.display]
# theme = "system"
# ///

import marimo

__generated_with = "0.11.20"
app = marimo.App(
    width="medium",
    app_title="Double Fischer Random Chess Analysis",
    layout_file="layouts/dfrc_analysis.grid.json",
)


@app.cell
def _(mo, num_positions):
    mo.md(f"""
    # 🎯 Double Fischer Random Chess Analysis

        <div style="text-align: center;">
            A list of all the <strong>{num_positions}</strong> currently analyzed DFRC positions.
        </div>
    """)
    return


@app.cell
def _():
    import marimo as mo

    with mo.status.spinner(title="Loading dependencies..."):
        import polars as pl

        import pyarrow as pa

        FEN_TEMPLATE = "https://lichess.org/analysis/{black}/pppppppp/8/8/8/8/PPPPPPPP/{white}_w_KQkq_-_0_1?color=white"
        data_path = mo.notebook_location() / "public" / "analysis_results.parquet"
    return FEN_TEMPLATE, data_path, mo, pa, pl


@app.cell
def _(data_path, mo, pl):
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
    num_positions = df.shape[0]
    table = mo.ui.table(df, selection="single")
    table
    return df, flexible_read_parquet, io, num_positions, table, urllib


@app.cell
def _(FEN_TEMPLATE, table):
    fen_white = table.value["white"][0] if not table.value.is_empty() else "rnbqkbnr"
    fen_black = table.value["black"][0] if not table.value.is_empty() else "rnbqkbnr"
    dfrc_id = table.value["dfrc_id"][0] if not table.value.is_empty() else "518"
    fen = FEN_TEMPLATE.format(black=fen_black, white=fen_white.upper())
    return dfrc_id, fen, fen_black, fen_white


@app.cell
def _(dfrc_id, fen, mo):
    mo.md(f"""
        **DFRC ID:** {dfrc_id}  
        [![Open Lichess Analysis Board](https://img.shields.io/badge/Lichess-Open%20Analysis%20Board-brown?style=for-the-badge&logo=lichess&logoColor=white)]({fen})
    """)
    return


@app.cell
def _(fen, mo):
    mo.Html(
        f'<iframe src="{fen}&bg=system" style="width: 900px; aspect-ratio: 12/11;" allowtransparency="true" frameborder="0"></iframe>'
    )
    return


@app.cell
def _(mo):
    mo.md("""
    ## Glossary

    - **white/black ID:** The Chess960 IDs
    - **DFRC ID:** Unique ID that corresponds to Chess960 IDs for mirrored positions
    - **sharpness score:** If this this 1, the position has a forcing line while a 0 indicates that there are plenty of good moves for both sides
    - **playability score:** a combination of the centipawn loss and the sharpness score
    """)
    return


if __name__ == "__main__":
    app.run()
