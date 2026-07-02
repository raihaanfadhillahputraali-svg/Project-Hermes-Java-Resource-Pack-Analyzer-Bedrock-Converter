from pathlib import Path
import zipfile

from rich.console import Console
from rich.table import Table


class ResourceScanner:

    def __init__(self, zip_path):
        self.console = Console()
        self.zip_path = Path(zip_path)

    def scan(self):

        self.console.print("[cyan]📦 Opening Resource Pack...[/cyan]")

        if not self.zip_path.exists():
            self.console.print("[red]❌ Resource pack not found![/red]")
            return

        with zipfile.ZipFile(self.zip_path, "r") as pack:

            files = pack.namelist()

            models = [
                f for f in files
                if "/models/" in f and f.endswith(".json")
            ]

            textures = [
                f for f in files
                if "/textures/" in f and f.endswith(".png")
            ]

            sounds = [
                f for f in files
                if f.endswith(".ogg")
            ]

            languages = [
                f for f in files
                if "/lang/" in f
            ]

            namespaces = set()

            for file in files:
                if file.startswith("assets/"):
                    parts = file.split("/")

                    if len(parts) > 1 and parts[1]: 
                        namespaces.add(parts[1])

            table = Table(title="Project Hermes")

            table.add_column("Category", style="cyan")
            table.add_column("Count", justify="right", style="green")

            table.add_row("Total Files", str(len(files)))
            table.add_row("Namespaces", str(len(namespaces)))
            table.add_row("Models", str(len(models)))
            table.add_row("Textures", str(len(textures)))
            table.add_row("Sounds", str(len(sounds)))
            table.add_row("Languages", str(len(languages)))

            self.console.print()
            self.console.print(table)
            self.console.print()

            self.console.print("[bold yellow]Namespaces Found[/bold yellow]")

            for namespace in sorted(namespaces):
                self.console.print(f" • {namespace}")
