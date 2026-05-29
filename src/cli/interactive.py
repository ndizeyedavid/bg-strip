import sys
import click
from InquirerPy import inquirer
from InquirerPy.base import Choice
from src.ui import animated_banner

def interactive_menu():
    """Builds a responsive keyboard navigation menu using InquirerPy."""
    animated_banner()
    
    mode = inquirer.select(
        message="Select an execution mode:",
        choices=[
            Choice(value="all", name="1) Process entire current directory (.)"),
            Choice(value="custom_dir", name="2) Process a custom folder path"),
            Choice(value="single", name="3) Process a single image file"),
            Choice(value="exit", name="4) Exit Application")
        ],
        pointer="⚡"
    ).execute()

    if mode == "exit":
        click.secho("\n👋 Exiting engine. See you space cowboy!", fg="magenta")
        sys.exit(0)

    input_target = "."
    if mode == "custom_dir":
        input_target = inquirer.text(message="Enter the target folder path:").execute()
    elif mode == "single":
        input_target = inquirer.text(message="Enter the explicit image file path (e.g. input.jpg):").execute()

    output_target = inquirer.text(
        message="Enter the output directory for finished assets:",
        default="./processed_output"
    ).execute()

    model_choice = inquirer.select(
        message="Select the AI segmentation model model:",
        choices=[
            Choice(value="birefnet-general", name="🔥 BiRefNet (Ultra Detailed - Best for Hair & Clothing)"),
            Choice(value="rmbg", name="⚡ BRIA RMBG-1.4 (Fast & Lightweight commercial choice)"),
            Choice(value="u2net", name="📦 U2Net (Standard balanced classic)")
        ],
        pointer="🧠"
    ).execute()

    return input_target, output_target, model_choice
