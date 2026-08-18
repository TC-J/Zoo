import typer
from typer import Typer
    
base = Typer()

@base.callback()
def _base(ctx: Typer):
    pass


