import os

def concatenate_backend_files(output_filename="runThis.py"):
    folder = os.path.dirname(os.path.abspath(__file__))
    files_order = [
        "walls.py",
        "ghosts.py",
        "poi.py",
        "map.py",
        "hero.py",
        "actions.py",
        "endpoint.py",
    ]
    with open(os.path.join(folder, output_filename), "w", encoding="utf-8") as outfile:
        for fname in files_order:
            path = os.path.join(folder, fname)
            if os.path.exists(path):
                outfile.write(f"# --- {fname} ---\n")
                with open(path, "r", encoding="utf-8") as infile:
                    skip = False
                    for line in infile:
                        # Start skipping at 'from typing import TYPE_CHECKING'
                        if line.strip().startswith("from typing import TYPE_CHECKING"):
                            skip = "TYPE_CHECKING"
                            continue
                        # Start skipping at 'if TYPE_CHECKING:'
                        if line.strip().startswith("if TYPE_CHECKING:"):
                            skip = True
                            continue
                        # Stop skipping when indentation returns to top-level
                        if skip:
                            if line.strip() == "" or line.startswith(" "):
                                continue
                            else:
                                skip = False
                        outfile.write(line)
                    outfile.write("\n\n")
            else:
                print(f"Warning: {fname} not found.")

if __name__ == "__main__":
    concatenate_backend_files()