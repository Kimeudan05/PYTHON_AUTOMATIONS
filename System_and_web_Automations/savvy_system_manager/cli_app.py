import click
from core import system_actions, update_manager, auth_manager, logger


@click.group()
def cli():
    """SavvySystem CLI - Automate and control your PC."""
    pass


@cli.command()
@click.option("--rename", default=None, help="Rename the computer before restart.")
def restart(rename):
    if auth_manager.verify_user():
        if rename:
            renamed = system_actions.rename_computer(rename)
            if renamed:
                click.echo(f"Computer renamed to {rename}. Restarting...")
        system_actions.restart_computer()
        logger.log_action("Restart initiated")


@cli.command()
def shutdown():
    if auth_manager.verify_user():
        system_actions.shutdown_computer()
        logger.log_action("Shutdown initiated")


@cli.command()
def update():
    if auth_manager.verify_user():
        click.echo(update_manager.check_updates())
        update_manager.install_updates()
        logger.log_action("System update initiated")


def run_cli(args=None):
    cli(args=args)
