import importlib.metadata
from pathlib import Path


import typer

from typer import Typer


from plumbum import local
    
from rich.markdown import Markdown
from rich.columns import Columns
from rich.text import Text
from rich.panel import Panel
from rich.align import Align


from zoo.user_experience import c

from zoo.package import package

from zoo.base import base




__version__ = importlib.metadata.version("zoo")


# Zoo CLI #
zoo = Typer()


@zoo.callback(invoke_without_command=True)
def callback(ctx: typer.Context):
	if ctx.invoked_subcommand is None:
		c.print(
		  Align.center(
			 Panel.fit(f"[bold italic white]Zoo[/] [bold italic blue]v{__version__}[/]", border_style="dim white")
    	   )
		)
	

# zoo base ... #
zoo.add_typer(base, name="base")    


# zoo package ... #
zoo.add_typer(package, name="package")