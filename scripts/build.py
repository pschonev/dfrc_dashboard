#!/usr/bin/env python3

import os
import subprocess
import argparse
from typing import List
from pathlib import Path


def export_html_wasm(notebook_path: str, output_dir: str, as_app: bool = False) -> bool:
    """Export a single marimo notebook to HTML format.

    Returns:
        bool: True if export succeeded, False otherwise
    """
    suffix = "_app.html" if as_app else "_notebook.html"
    output_path = notebook_path.replace(".py", suffix)

    cmd = ["marimo", "export", "html-wasm"]
    if as_app:
        print(f"Exporting {notebook_path} to {output_path} as app")
        cmd.extend(["--mode", "run", "--no-show-code"])
    else:
        print(f"Exporting {notebook_path} to {output_path} as notebook")
        cmd.extend(["--mode", "edit"])

    try:
        output_file = os.path.join(output_dir, output_path)
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        cmd.extend([notebook_path, "-o", output_file])

        # Here we're explicitly providing input to accept prompts
        # Convert single newline input to handle the overwrite prompt
        process_result = subprocess.run(
            cmd, input="Y\ny\n", capture_output=True, text=True, check=True
        )

        if process_result.returncode == 0:
            return True
        else:
            print(f"Error exporting {notebook_path}:")
            print(process_result.stderr)
            return False
    except subprocess.CalledProcessError as e:
        print(f"Error running export command: {e.stderr}")
        return False
    except Exception as e:
        print(f"Unexpected error exporting {notebook_path}: {e}")
        return False


def generate_index(all_notebooks: List[str], output_dir: str) -> None:
    """Generate the index.html file."""
    print("Generating index.html")

    index_path = os.path.join(output_dir, "index.html")
    os.makedirs(output_dir, exist_ok=True)

    try:
        with open(index_path, "w") as f:
            f.write(
                """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>marimo</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
  </head>
  <body class="font-sans max-w-2xl mx-auto p-8 leading-relaxed">
    <div class="mb-8">
      <img src="https://raw.githubusercontent.com/marimo-team/marimo/main/docs/_static/marimo-logotype-thick.svg" alt="marimo" class="h-20" />
    </div>
    <div class="grid gap-4">
"""
            )
            for notebook in all_notebooks:
                notebook_name = notebook.split("/")[-1].replace(".py", "")
                display_name = notebook_name.replace("_", " ").title()

                f.write(
                    f'      <div class="p-4 border border-gray-200 rounded">\n'
                    f'        <h3 class="text-lg font-semibold mb-2">{display_name}</h3>\n'
                    f'        <div class="flex gap-2">\n'
                    f'          <a href="{notebook.replace(".py", "_app.html")}" class="px-3 py-1 bg-gray-100 hover:bg-gray-200 rounded">Open {display_name} App</a>\n'
                    f'          <a href="{notebook.replace(".py", "_notebook.html")}" class="px-3 py-1 bg-gray-100 hover:bg-gray-200 rounded">Open {display_name} Notebook</a>\n'
                    f"        </div>\n"
                    f"      </div>\n"
                )
            f.write(
                """    </div>
  </body>
</html>"""
            )
    except IOError as e:
        print(f"Error generating index.html: {e}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build marimo notebooks")
    parser.add_argument(
        "--output-dir", default="_site", help="Output directory for built files"
    )
    args = parser.parse_args()

    notebooks_dir = Path("notebooks")
    if not notebooks_dir.exists():
        print("Warning: Directory not found: notebooks")
        return

    all_notebooks: List[str] = list(str(path) for path in notebooks_dir.rglob("*.py"))

    if not all_notebooks:
        print("No notebooks found!")
        return

    # Export notebooks as both app and notebook
    for nb in all_notebooks:
        export_html_wasm(nb, args.output_dir, as_app=True)
        export_html_wasm(nb, args.output_dir, as_app=False)

    # Generate index file
    generate_index(all_notebooks, args.output_dir)


if __name__ == "__main__":
    main()
