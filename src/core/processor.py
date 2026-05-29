import os
import time
import glob
from pathlib import Path
import click
from rembg import remove, new_session
from PIL import Image
from tqdm import tqdm
from colorama import Fore, Style
from src.ui import fake_loading_animation

def apply_background(image: Image.Image, bg_color: tuple[int, int, int] | None) -> Image.Image:
    """Apply background color to image with alpha channel"""
    if bg_color is None:
        return image
    
    bg = Image.new("RGB", image.size, bg_color)
    bg.paste(image, mask=image.split()[3] if image.mode == "RGBA" else None)
    return bg

def process_images(input_target, output_target, model, bg_color: tuple[int, int, int] | None = None):
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

    output_path = Path(output_target)
    output_path.mkdir(parents=True, exist_ok=True)

    fake_loading_animation("Initializing environment buffers...", duration=0.8)
    fake_loading_animation(f"Mounting neural runtime for [{model}]...", duration=1.2)

    try:
        session = new_session(model)
    except Exception as e:
        click.secho(f"❌ Core Initialization Failed: {e}", fg="red", bold=True)
        return

    bg_desc = "transparent" if bg_color is None else f"RGB{bg_color}"
    click.secho(f"\n🚀 Pipeline active. Extracting {len(images)} assets with {bg_desc} background...\n", fg="cyan", bold=True)
    
    success_count = 0
    failed_count = 0
    start_bench = time.time()

    with tqdm(total=len(images), 
              desc="📊 AI Pipeline Tracker", 
              unit="img", 
              bar_format="{l_bar}{bar:25}{r_bar}",
              dynamic_ncols=True,
              mininterval=0.1) as pbar:
        for idx, img_path_str in enumerate(images, 1):
            img_path = Path(img_path_str)
            out_name = f"{img_path.stem}.png"
            out_file_path = output_path / out_name
            
            pbar.write(Fore.WHITE + f"  [{idx}/{len(images)}] " + Fore.BLUE + f"Processing: {img_path.name}")
            
            img_start = time.time()
            try:
                with Image.open(img_path) as src_img:
                    alpha_masked = remove(src_img, session=session)
                    final_img = apply_background(alpha_masked, bg_color)
                    final_img.save(out_file_path, format="PNG")
                
                img_elapsed = time.time() - img_start
                pbar.write(Fore.GREEN + f"  ✔ Success -> Created {out_name} ({img_elapsed:.2f}s)")
                success_count += 1
            except Exception as e:
                pbar.write(Fore.RED + f"  ✘ Error extracting {img_path.name}: {e}")
                failed_count += 1
            
            pbar.update(1)

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
