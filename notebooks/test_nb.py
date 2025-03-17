import marimo

__generated_with = "0.11.20"
app = marimo.App(width="medium")


@app.cell
def _():
    number = 3

    print(f"4 + {number} = {4+number}")
    return (number,)


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
