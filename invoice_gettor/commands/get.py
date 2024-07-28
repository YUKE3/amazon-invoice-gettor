import click

@click.command()
@click.option('--gpt', is_flag=True, default=False, help="Enable GPT summarization.")
@click.option('--actual', is_flag=True, default=False, help="Enable Actual Integration.")
@click.option('--no_pdf', is_flag=True, default=False, help="Don't download PDF.")
def get(gpt, actual, no_pdf):
    if gpt:
        click.echo("GPT is enabled!")
    if actual:
        click.echo("Acutal is enabled!")
    if no_pdf:
        click.echo("nopdf is enabled!")
    click.echo("This is the get command!")