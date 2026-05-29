import time
import sys
import click
from colorama import Fore, Style

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
