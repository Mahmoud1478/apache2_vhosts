#!/media/mahmoud/GitHub/apache2_vhosts/venv/bin/python3
import os, glob
from string import Template

import click
from click_params import DOMAIN


class Default(Template):
    delimiter = '%'

CONF_STUBS = '''<VirtualHost *:80>
    ServerName %{domain}
    ServerAdmin %{admin}
    DocumentRoot %{path}
    <Directory / >
        Options Indexes FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>
    <FilesMatch ".php$">
        SetHandler "proxy:unix:%{php}|fcgi://localhost/"
    </FilesMatch>
    ErrorLog ${APACHE_LOG_DIR}/%{domain_log}/error.log
    CustomLog ${APACHE_LOG_DIR}/%{domain_log}/access.log combined
</VirtualHost>'''


def get_file_path():
    return os.path.abspath(f'{os.path.sep}'.join(__file__.split(os.path.sep)[0:-1]))


def resolve_domain_name_from_path(dir_path: str):
    return dir_path.split(os.path.sep)[-1].lower()


@click.group('Vhost', help='Help you to managing your web server domains')
@click.version_option('0.1', prog_name='hosts')
def main():
    """ Managing your domains """
    ...


def get_php_socks() -> dict:
    PHP_SOCK_PATH = '/var/run/php/'

    return {file.replace(PHP_SOCK_PATH, '').replace('-fpm.sock', '').replace('php', '') or 'auto': file for file in
            glob.glob(f'{PHP_SOCK_PATH}*.sock')}


@main.command()
def update():
    click.secho(get_php_socks())
    # raise 'Not Implemented yet'


@main.command()
def delete():
    raise 'Not Implemented yet'


@main.command(help='Create new vhost in apache configration')
@click.argument("domain", type=DOMAIN)
@click.argument("folder", type=click.Path())
@click.option(
    "--php", "-p",
    prompt='Select Php Version',
    help="set the php version to new domain",
    type=click.Choice(list(get_php_socks().keys())),
    show_default='8.1',
)
@click.option(
    "--etc-hosts", "-e",
    default=False,
    help="set the new domain in /etc/hosts file", type=bool,
    show_default=False,
)
@click.option(
    '--admin', '-a',
    default='mah.mostafa18@gmail.com',
    show_default='mah.mostafa18@gmail.com',
    help='Set Domain Email Admin',
    type=str,
)
def create(domain, folder, php, etc_hosts, admin):
    SITES_AVAILABLE = '/etc/apache2/sites-available/'
    LOG = '/var/log/apache2/'
    ETC_HOSTS = '/etc/hosts'
    n = 80
    AVALIABLE_PHP_SOCK = get_php_socks()
    path = os.path.abspath(os.path.join(os.getcwd(), folder))

    if etc_hosts:
        with open(ETC_HOSTS, 'a', encoding='utf8') as etc:
            etc.write(f'''127.0.0.1\t{domain}\n''')
    template = Default(CONF_STUBS)
    with open(f'{SITES_AVAILABLE}{domain}.conf', 'w') as file:
        file.write(template.substitute({
            "domain": domain,
            'admin': admin,
            'path': path,
            'domain_log': domain,
            'php': AVALIABLE_PHP_SOCK.get(php)
        }))
    if not os.path.exists(f'{LOG}{domain}'):
        os.mkdir(f'{LOG}{domain}')
    os.system(f'a2ensite {domain} && systemctl reload apache2')
    click.secho("=" * n, fg='red')
    click.secho(
        f'''Domain Configurations
        -> Domain: {domain}
        -> Folder: {path}
        -> PHP version: {php}
        -> PHP fpm: {AVALIABLE_PHP_SOCK.get(php)}
        -> Domain Admin: {admin}
        -> Domain Configration: {SITES_AVAILABLE}{domain}.conf
        -> Domain Log Folder: {LOG}{domain}
        -> Modify in "/etc/hosts": {etc_hosts}
        ''',
        fg='yellow'
    )
    click.secho("=" * n, fg='red')


if __name__ == "__main__":
    main()
