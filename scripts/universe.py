# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "rich>=15.0.0",
#     "typer>=0.27.2",
# ]
# ///

################################################################################
## Imports #####################################################################
################################################################################
import typer

import rich
from rich.console import Console

import builtins
builtins.print = rich.print

import os

################################################################################
## Constants ###################################################################
################################################################################


################################################################################
## Static ######################################################################
################################################################################
c = Console()
app = typer.Typer(rich_markup_mode="rich")


################################################################################
## Functions ###################################################################
################################################################################
def the_universe():
    c.print("The universe...")


################################################################################
## CLI #########################################################################
################################################################################
@app.command()
def universe(
):
    pass


################################################################################
## Main ########################################################################
################################################################################
def main() -> None:
    app()


if __name__ == "__main__":
    main()

#system: bool = typer.Option(False, help="List system."),
#daemons: bool = typer.Option(False, help="List daemons."),
#machines: bool = typer.Option(False, help="List machines."),
#containers: bool = typer.Option(False, help="List containers."),
#networks: bool = typer.Option(False, help="List networks."),
#volumes: bool = typer.Option(False, help="List volumes."),
#images: bool = typer.Option(False, help="List images."),
#services: bool = typer.Option(False, help="List services."),
#secrets: bool = typer.Option(False, help="List secrets."),
#config: bool = typer.Option(False, help="List config."),
#logs: bool = typer.Option(False, help="List logs."),
#events: bool = typer.Option(False, help="List events."),
#metrics: bool = typer.Option(False, help="List metrics."),
#alerts: bool = typer.Option(False, help="List alerts."),
#dashboards: bool = typer.Option(False, help="List dashboards."),