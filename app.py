import os
import sys
import glob
import time
from pathlib import Path
import click
from rembg import remove, new_session
from PIL import Image
from tqdm import tqdm
from colorama import init, Fore, Style
from InquirerPy import inquirer
from InquirerPy.base import Choice

# Initialize colorama for clean terminal layout processing
init(autoreset=True)

def animated_banner():
    """Renders a gorgeous stylized ASCII banner with a slight typing delay."""
    banner = f"""
{Fore.CYAN}{Style.BRIGHT}    ██████╗  ██████╗     ███████╗████████╗██████╗ ██╗ ██████╗ 
{Fore.CYAN}{Style.BRIGHT}    ██╔══██╗██╔════╝     ██╔════╝╚══██╔══╝██╔══██╗██║ ██╔══██╗
{Fore.BLUE}{Style.BRIGHT}    ██████╔╝██║  ███╗    ███████╗   ██║   ██████╔╝██║ ██████╔╝
{Fore.BLUE}{Style.BRIGHT}    ██╔══██╗██║   ██║    ╚════██║   ██║   ██╔══██╗██║ ██╔═══╝ 
{Fore.MAGENTA}{Style.BRIGHT}    ██████╔╝╚██████╔╝    ███████║   ██║   ██║  ██║██║ ██║     
{Fore.MAGENTA}{Style.BRIGHT}    ╚═════╝  ╚═════╝     ╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝ ╚═╝     
    """
    for line in banner.split('\n'):
        click.echo(line)
        time.sleep(0.03)
    click.echo(Fore.BLACK + Style.BRIGHT + "        ⚡ Native High-Performance AI Segmentation Suite ⚡\n")

def fake_loading_animation(text, duration=1.5):
    """Simulates a sleek terminal spinner animation."""
    spinner = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        sys.stdout.write(f"\r{Fore.CYAN}{spinner[i % len(spinner)]} {text}")
        sys.stdout.flush()
        time.sleep(0.08)
        i += 1
    sys.stdout.write(f"\r{Fore.GREEN}✔ {text} Done!\n")
    sys.stdout.flush()

def interactive_menu():
    """Builds a responsive keyboard navigation menu using InquirerPy."""
    animated_banner()
    
    # 1. Choose Execution Mode
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

    # 2. Collect relevant paths based on chosen mode
    input_target = "."
    if mode == "custom_dir":
        input_target = inquirer.text(message="Enter the target folder path:").execute()
    elif mode == "single":
        input_target = inquirer.text(message="Enter the explicit image file path (e.g. input.jpg):").execute()

    output_target = inquirer.text(
        message="Enter the output directory for finished assets:",
        default="./processed_output"
    ).execute()

    # 3. Choose the Neural Model Architecture
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

@click.command()
@click.option('-i', '--input', 'input_flag', help='Path to an image file or folder.')
@click.option('-o', '--output', 'output_flag', help='Target output directory.')
@click.option('--all', 'process_all', is_flag=True, help='Scan current directory automatically.')
@click.option('-m', '--model', default='birefnet-general', help='Model choice: birefnet-general, rmbg, u2net')
def main(input_flag, output_flag, process_all, model):
    """🚀 Premium Structural Background Segmentation Interface CLI."""
    
    # Check if we should route to the interactive terminal UI
    if not input_flag and not output_flag and not process_all:
        input_target, output_target, model = interactive_menu()
    else:
        # Standard fallback inline argument behavior
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

    # 1. Resolve matching image assets
    input_path = Path(input_target)
    if input_path.is_dir():
        files = glob.glob(os.path.join(input_target, '*.*'))
    elif input_path.is_file():
        files = [str(input_path)]
    else:
        files = glob.glob(input_target)

    valid_extensions = {'.jpg', '.jpeg', '.png', '.webp', '.bmp'}
    images = [f for f in files if Path(f).suffix.lower() in valid_extensions]

    if not images:
        click.secho(f"\n❌ No valid source images found matching target: '{input_target}'", fg="red", bold=True)
        return

    # Ensure destination path exists
    output_path = Path(output_target)
    output_path.mkdir(parents=True, exist_ok=True)

    # Renders our premium mini terminal animation sequences
    fake_loading_animation("Initializing environment buffers...", duration=0.8)
    fake_loading_animation(f"Mounting neural runtime for [{model}]...", duration=1.2)

    try:
        session = new_session(model)
    except Exception as e:
        click.secho(f"❌ Core Initialization Failed: {e}", fg="red", bold=True)
        return

    click.secho(f"\n🚀 Pipeline active. Extracting {len(images)} assets...\n", fg="cyan", bold=True)
    
    success_count = 0
    failed_count = 0
    start_bench = time.time()

    # 3. Execution Processing Core Loop
    with tqdm(total=len(images), desc="📊 AI Pipeline Tracker", unit="img", bar_format="{l_bar}{bar:25}{r_bar}") as pbar:
        for idx, img_path_str in enumerate(images, 1):
            img_path = Path(img_path_str)
            out_name = f"{img_path.stem}.png"
            out_file_path = output_path / out_name
            
            tqdm.write(Fore.WHITE + f"  [{idx}/{len(images)}] " + Fore.BLUE + f"Processing: {img_path.name}")
            
            img_start = time.time()
            try:
                with Image.open(img_path) as src_img:
                    alpha_masked = remove(src_img, session=session)
                    alpha_masked.save(out_file_path, format="PNG")
                
                img_elapsed = time.time() - img_start
                tqdm.write(Fore.GREEN + f"  ✔ Success -> Created {out_name} ({img_elapsed:.2f}s)\n")
                success_count += 1
            except Exception as e:
                tqdm.write(Fore.RED + f"  ✘ Error extracting {img_path.name}: {e}\n")
                failed_count += 1
            
            pbar.update(1)

    # 4. Final Claude Code Style Summary Card
    total_elapsed = time.time() - start_bench
    
    click.echo("\n" + Fore.MAGENTA + "═" * 60)
    click.secho("✨ EXTRACTION TASK COMPLETE", fg="magenta", bold=True)
    click.echo(Fore.MAGENTA + "═" * 60)
    click.echo(f"  Processed Assets:   {Fore.WHITE}{len(images)}")
    click.echo(f"  Clean Cutouts:       {Fore.GREEN}{success_count} successful")
    if failed_count > 0:
        click.echo(f"  Engine Errors:       {Fore.RED}{failed_count} failed")
    click.echo(f"  Total Run Duration:  {Fore.YELLOW}{total_elapsed:.2f}s")
    if success_count > 0:
        click.echo(f"  Throughput Speed:    {Fore.YELLOW}{total_elapsed/len(images):.2f}s per image")
    click.echo(Fore.MAGENTA + "═" * 60 + "\n")

if __name__ == '__main__':
    main()