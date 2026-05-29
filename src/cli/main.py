import sys
import click
from colorama import init
from src.cli import interactive_menu
from src.core import process_images
from src.ui import animated_banner

init(autoreset=True)

@click.command()
@click.option('-i', '--input', 'input_flag', help='Path to an image file or folder.')
@click.option('-o', '--output', 'output_flag', help='Target output directory.')
@click.option('--all', 'process_all', is_flag=True, help='Scan current directory automatically.')
@click.option('-m', '--model', default='birefnet-general', help='Model choice: birefnet-general, rmbg, u2net')
def main(input_flag, output_flag, process_all, model):
    """🚀 Premium Structural Background Segmentation Interface CLI."""
    
    if not input_flag and not output_flag and not process_all:
        input_target, output_target, model = interactive_menu()
    else:
        animated_banner()
        if process_all:
            input_target = "."
            output_target = output_flag if output_flag else "./processed_output"
        else:
            if not input_flag or not output_flag:
                click.secho("❌ Error: Missing arguments. Provide both -i and -o, or use --all.", fg="red", bold=True)
                sys.exit(1)
            input_target = input_flag
            output_target = output_flag

    process_images(input_target, output_target, model)
