"""
A neat application to store details of various crypto.

"""

import pandas
from datetime import datetime

from rich import box
from rich.align import Align
from rich.console import Console, Group
from rich.layout import Layout
from rich.panel import Panel
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn
from rich.syntax import Syntax
from rich.table import Table
from rich.spinner import Spinner, SPINNERS

console = Console()

def make_layout() -> Layout:
    layout = Layout(name="root")
    
    layout.split(
        Layout(name="header", size=3),
        Layout(name="main", ratio=1),
        Layout(name="footer", size=15),
    )

    layout["main"].split_row(
        Layout(name="side"),
        Layout(name="body", ratio=2, minimum_size=60),
    )
    layout["side"].split(Layout(name="box1"), Layout(name="box2"))
    return layout

def make_sponsor_message() -> Panel:
    """Some example content."""
    sponsor_message = Table.grid(padding=1)
    sponsor_message.add_column(style="black", justify="right")
    sponsor_message.add_column(no_wrap=True)
    sponsor_message.add_row(
        "AssetDash",
        "[u blue link=https://members.assetdash.com/portfolio]https://members.assetdash.com/portfolio",
    )
    sponsor_message.add_row(
        "Twitter",
        "[u blue link=https://twitter.com/home]https://twitter.com/home",
    )
    sponsor_message.add_row(
        "Jupiter",
        "[u blue link=https://jup.ag/]https://jup.ag/"
    )

    message = Table.grid(padding=1)
    message.add_column()
    message.add_column(no_wrap=True)
    message.add_row(sponsor_message)

    message_panel = Panel(
        Align.center(
            Group("\n", Align.center(sponsor_message)),
            vertical="middle",
        ),
        box=box.ROUNDED,
        padding=(1, 2),
        title="[b black]Portfolio Links",
        border_style="black",
    )
    return message_panel


class Header:
    """Display header with clock."""

    def __rich__(self) -> Panel:
        grid = Table.grid(expand=True)
        grid.add_column(justify="center", ratio=1)
        grid.add_column(justify="right")
        grid.add_row(
            "Portfolio Application",
            datetime.now().ctime().replace(":", "[blink]:[/]"),
        )
        return Panel(grid, style="red on black")
    
def make_syntax() -> Syntax:
    code = """\
def ratio_resolve(total: int, edges: List[Edge]) -> List[int]:
    sizes = [(edge.size or None) for edge in edges]

    # While any edges haven't been calculated
    while any(size is None for size in sizes):
        # Get flexible edges and index to map these back on to sizes list
        flexible_edges = [
            (index, edge)
            for index, (size, edge) in enumerate(zip(sizes, edges))
            if size is None
        ]
        # Remaining space in total
        remaining = total - sum(size or 0 for size in sizes)
        if remaining <= 0:
            # No room for flexible edges
            sizes[:] = [(size or 0) for size in sizes]
            break
        # Calculate number of characters in a ratio portion
        portion = remaining / sum((edge.ratio or 1) for _, edge in flexible_edges)

        # If any edges will be less than their minimum, replace size with the minimum
        for index, edge in flexible_edges:
            if portion * edge.ratio <= edge.minimum_size:
                sizes[index] = edge.minimum_size
                break
        else:
            # Distribute flexible space and compensate for rounding error
            # Since edge sizes can only be integers we need to add the remainder
            # to the following line
            _modf = modf
            remainder = 0.0
            for index, edge in flexible_edges:
                remainder, size = _modf(portion * edge.ratio + remainder)
                sizes[index] = int(size)
            break
    # Sizes now contains integers only
    return cast(List[int], sizes)
    """
    syntax = Syntax(code, "python", line_numbers=True)
    return syntax    
    
    

job_progress = Progress(
    "{task.description}",
    SpinnerColumn(),
    BarColumn(),
    TextColumn("[progress.percentage]{task.percentage:>10.0f}%"),
)
job_progress.add_task("[green]Cooking")
job_progress.add_task("[magenta]Baking", total=1000000000)
job_progress.add_task("[cyan]Mixing", total=1000000000)

total = sum(task.total for task in job_progress.tasks)
overall_progress = Progress()
overall_task = overall_progress.add_task("All Jobs", total=int(total))

progress_table = Table.grid(expand=True)
progress_table.add_row(
    Panel(
        overall_progress,
        title="Overall Progress",
        border_style="green",
        padding=(2, 2),
    ),
    Panel(job_progress, title="[b]Jobs", border_style="red", padding=(1, 2)),
)

dropList = Table.grid(pad_edge=True,padding=1)
dropList.add_row(f"[green]Jupiter: [white]6200")
dropList.add_row(f"[blue]Phantom: [i black]farming...")
dropList.add_row(f"[red]Metamask: [i black]farming...")


airdrop = Panel(
    dropList,
    title="Airdrop Amount",
    border_style="green",
    padding=(2, 2),
)
    
table = Table(show_header=True, header_style="bold red", show_lines=True, expand=True, border_style="black")
table.add_column("Wallet Name", style="dim", width=15)
table.add_column("Address")
table.add_column("Private Key")
table.add_column("Network")

df = pandas.read_csv("data.csv")

columns = len(df.columns)
rows = len(df.index)

for i in range (rows):
    table.add_row(
        f"{df['wallet_name'][i]}", f"{df['address'][i]}", f"{df['privatekey'][i]}", f"{df['network'][i]}"
    )

panel = Panel(table, title="Wallet", subtitle="List", border_style="red", padding=(1, 2))

layout = make_layout()
layout["header"].update(Header())
layout["body"].update(make_sponsor_message())
layout["box2"].update(airdrop)
layout["box1"].update(Panel(layout.tree, border_style="red"))
layout["footer"].update(panel)

from time import sleep

from rich.live import Live

with Live(layout, refresh_per_second=10, screen=True):
    while not overall_progress.finished:
        sleep(0.1)
        for job in job_progress.tasks:
            if not job.finished:
                job_progress.advance(job.id)

        completed = sum(task.completed for task in job_progress.tasks)
        overall_progress.update(overall_task, completed=completed)