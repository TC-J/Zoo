import typer
from typer import Typer
    
from plumbum import local
    
from zoo.user_experience import c
    
### zoo package ... ###
package = Typer()


@package.callback(invoke_without_command=True)
def callback():
    c.print("zoo pkg")


@package.command("cargo")
def _cargo():
    local["cargo"]()

