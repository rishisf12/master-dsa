import socket

domains = [
    'kyro.com', 'kyro.io', 'kyro.app', 'kyro.ai', 'kyro.dev', 'kyro.xyz', 'kyro.co',
    'veyana.com', 'veyana.io', 'veyana.app',
    'zent.io', 'zent.app', 'zent.dev', 'zent.ai',
    'kairo.io', 'kairo.app', 'kairo.dev',
    'novex.io', 'novex.app', 'novex.ai',
    'orix.io', 'orix.app', 'orix.ai',
    'aeris.io', 'aeris.app', 'aeris.ai',
    'solen.io', 'solen.app', 'solen.ai',
    'vexel.io', 'vexel.app', 'vexel.ai',
    'quanta.io', 'quanta.app', 'quanta.ai',
    'nexum.io', 'nexum.app', 'nexum.ai',
    'vincul.io', 'vincul.app', 'vincul.ai',
    'lygon.io', 'lygon.app', 'lygon.ai',
    'synap.io', 'synap.app', 'synap.ai',
    'axial.io', 'axial.app', 'axial.ai',
    'radial.io', 'radial.app', 'radial.ai',
    'orbita.io', 'orbita.app', 'orbita.ai',
    'vektr.io', 'vektr.app', 'vektr.ai',
    'nexu.io', 'nexu.app', 'nexu.ai',
    'vexis.io', 'vexis.app', 'vexis.ai',
    'apax.io', 'apax.app', 'apax.ai',
    'zenth.io', 'zenth.app', 'zenth.ai',
    'horizn.io', 'horizn.app', 'horizn.ai',
    'signl.io', 'signl.app', 'signl.ai',
    'signa.io', 'signa.app', 'signa.ai',
    'pulz.io', 'pulz.app', 'pulz.ai',
    'pulsa.io', 'pulsa.app', 'pulsa.ai',
    'pulso.io', 'pulso.app', 'pulso.ai',
]

for domain in domains:
    try:
        socket.gethostbyname(domain)
        print(f'{domain}: TAKEN')
    except:
        print(f'{domain}: AVAILABLE')