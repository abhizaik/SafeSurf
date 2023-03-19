import click
from urllib.parse import urlparse

import socket

def display_url_part(url, piecename, allowfail):
    'This function is the primary logic for the whole program.'

    # Automatically use the "default" schema if none are present. Otherwise the urlparse function will return nothing.
    if '//' not in url:
        url = '//%s' % (url)
    o = urlparse(url)

    # The cli functions below will request a specific urlparse attribute. If it is present we return it and exit.
    value = getattr(o, piecename)
    if value:
        click.echo(value)
        exit(0)

    # If we're looking for the port and it isn't present return the default port for the specific scheme.
    if piecename is 'port' and o.scheme:
        click.echo(socket.getservbyname(o.scheme))
        exit(0)

    # Some shell scripts may want to treat blank values as legitimate responses.
    if allowfail:
        exit(0)

    # No match was found so we return an error response.
    exit(1)


@click.group()
@click.pass_context
def cli(ctx):
    if ctx.parent:
        print(ctx.parent.get_help())


@cli.command(short_help="Get scheme from URL")
@click.argument('url')
@click.option('-f', '--allowfail', is_flag=True)
def scheme(url, allowfail):
    display_url_part(url, 'scheme', allowfail)


@cli.command(short_help="Get netloc from URL")
@click.argument('url')
@click.option('-f', '--allowfail', is_flag=True)
def netloc(url, allowfail):
    display_url_part(url, 'netloc', allowfail)


@cli.command(short_help="Get path from URL")
@click.argument('url')
@click.option('-f', '--allowfail', is_flag=True)
def path(url, allowfail):
    display_url_part(url, 'path', allowfail)


@cli.command(short_help="Get params from URL")
@click.argument('url')
@click.option('-f', '--allowfail', is_flag=True)
def params(url, allowfail):
    display_url_part(url, 'params', allowfail)


@cli.command(short_help="Get query from URL")
@click.argument('url')
@click.option('-f', '--allowfail', is_flag=True)
def query(url, allowfail):
    display_url_part(url, 'query', allowfail)


@cli.command(short_help="Get fragment from URL")
@click.argument('url')
@click.option('-f', '--allowfail', is_flag=True)
def fragment(url, allowfail):
    display_url_part(url, 'fragment', allowfail)


@cli.command(short_help="Get username from URL")
@click.argument('url')
@click.option('-f', '--allowfail', is_flag=True)
def username(url, allowfail):
    display_url_part(url, 'username', allowfail)


@cli.command(short_help="Get password from URL")
@click.argument('url')
@click.option('-f', '--allowfail', is_flag=True)
def password(url, allowfail):
    display_url_part(url, 'password', allowfail)


@cli.command(short_help="Get hostname from URL")
@click.argument('url')
@click.option('-f', '--allowfail', is_flag=True)
def hostname(url, allowfail):
    display_url_part(url, 'hostname', allowfail)


@cli.command(short_help="Get port from URL")
@click.argument('url')
@click.option('-f', '--allowfail', is_flag=True)
def port(url, allowfail):
    display_url_part(url, 'port', allowfail)


if __name__ == '__main__':
    cli()
