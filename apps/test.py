import marimo

__generated_with = "0.10.9"
app = marimo.App(width="medium")


@app.cell
def _():
    def hello(name: str = "world") -> None:
        print(f"hello {name}")

    hello("Devcontainer")
    return (hello,)


if __name__ == "__main__":
    app.run()
