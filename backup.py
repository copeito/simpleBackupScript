"""Configura un objeto del tipo backup.

Este objeto del tipo backup que sera gestionado por
backupManager.

Probado en Python 3.5:

"""

from pathlib import Path


class Backup(object):
    """Configura un backup."""

    def __init__(self, args=None):
        """Inicializa un backup."""
        self.configs = dict()
        if args is not None:
            self.set(args)

    def set(self, args):
        """Configura como se ejecutara el backup."""
        for arg in args:
            argType = type(args[arg])

            if arg == 'sourcePath' or arg == 'destinationPath':
                if isinstance(args[arg], Path):
                    config = args[arg]
                elif (argType == str):
                    config = Path(args[arg])
                else:
                    # Lanzar excepcion
                    pass
            elif arg == 'maxNumber' or arg == 'minDaysBackup':
                if argType != int:
                    # Lanzar excepcion
                    pass

            self.configs[arg] = config

    def run(self):
        """Ejecuta el backup."""


backup = Backup({
    'sourcePath': Path('/home/copeito/Projects'),
    'destinationPath': '/media/local/data',
    'maxNumber': 10,
    'minDaysBackup': 15
})
