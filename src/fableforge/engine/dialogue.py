from dataclasses import dataclass
from typing import Dict, Optional
from rich.console import Console

console = Console()

@dataclass
class NPC:
    """Simple NPC with a dialogue tree."""
    name: str
    tree: Dict[str, Dict[str, Optional[str]]]


def run_dialogue(npc: NPC) -> None:
    """Walk through ``npc.tree`` using a simple key-based structure."""
    node = "start"
    while node and node in npc.tree:
        entry = npc.tree[node]
        console.print(f"[bold cyan]{npc.name}[/bold cyan]: {entry['text']}")
        options = {k: v for k, v in entry.get('options', {}).items() if v is not None}
        if not options:
            break
        for i, prompt in enumerate(options, 1):
            console.print(f"[bold]{i}.[/bold] {prompt}")
        choice = console.input("Choose: ").strip()
        try:
            idx = int(choice) - 1
            node = list(options.values())[idx]
        except (ValueError, IndexError):
            console.print("[red]Invalid choice[/red]")
            continue
    console.print("[green]Conversation ended.[/green]")
