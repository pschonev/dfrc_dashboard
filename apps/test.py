import marimo

__generated_with = "0.11.20"
app = marimo.App(width="medium")


@app.cell
def hello():
    def hello(name: str = "world") -> None:
        print(f"hello {name}")
    return (hello,)


@app.cell
def _(hello):
    hello("Devcontainer")
    return


if __name__ == "__main__":
    app.run()
