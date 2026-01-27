from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text
from rich.color import Color

console = Console()

START_COLOR = "#F54800" 
END_COLOR = "#F5B800"   

ICON = """
   █████████   █████    ███████████  ███████████  
  ███░░░░░███ ░░███    ░░███░░░░░███░░███░░░░░███ 
 ░███    ░███  ░███     ░███    ░███ ░███    ░███ 
 ░███████████  ░███     ░██████████  ░██████████  
 ░███░░░░░███  ░███     ░███░░░░░░   ░███░░░░░███ 
 ░███    ░███  ░███     ░███         ░███    ░███ 
 █████   █████ █████    █████        █████   █████
░░░░░   ░░░░░ ░░░░░    ░░░░░        ░░░░░   ░░░░░ 
                                                  
                                                  
                                                  
"""

def get_transition_color(start_hex, end_hex, fraction):
    """Calculates a color between start and end based on a fraction (0.0 to 1.0)."""
    start_rgb = Color.parse(start_hex).get_truecolor()
    end_rgb = Color.parse(end_hex).get_truecolor()
    
    r = int(start_rgb.red + (end_rgb.red - start_rgb.red) * fraction)
    g = int(start_rgb.green + (end_rgb.green - start_rgb.green) * fraction)
    b = int(start_rgb.blue + (end_rgb.blue - start_rgb.blue) * fraction)
    
    return f"rgb({r},{g},{b})"

def show_icon():
    STRETCH = 1.0 
    
    lines = ICON.strip('\n').splitlines()
    if not lines: return
    
    max_y = len(lines)
    max_x = max(len(line) for line in lines)
    max_distance = max_x + max_y
    
    for y, line in enumerate(lines):
        rich_line = Text()
        for x, char in enumerate(line):
            distance = x + y
            
            fraction = distance / (max_distance * STRETCH)
            
            fraction = max(0.0, min(1.0, fraction))
            
            color = get_transition_color(START_COLOR, END_COLOR, fraction)
            rich_line.append(char, style=color)
        
        console.print(rich_line)


def show_error(message):
    console.print(f"[bold red]❌ {message}[/bold red]")


def show_info(message):
    console.print(f"[bold blue]🔍 {message}[/bold blue]")


def show_warning(message):
    console.print(f"[bold yellow]⚠️ {message}[/bold yellow]")


def show_success(message):
    console.print(f"[bold green]🚀 {message}[/bold green]")


def display_draft(title, body):
    console.print(
        Panel(
            f"[bold]TITLE:[/bold] {title}\n\n[bold]BODY:[/bold]\n{body}",
            title="[magenta]Draft Pull Request[/magenta]",
            border_style="cyan",
        )
    )


def get_action_choice():
    return Prompt.ask(
        "What would you like to do?",
        choices=["create", "refine", "cancel"],
        default="create",
    )


def get_refinement_feedback():
    return Prompt.ask("[bold yellow]What should I change?[/bold yellow]")
