"""Configura un objeto del tipo backup.

Este objeto del tipo backup que sera gestionado por
backupManager.
"""


class Backup(object):
    """Configura un backup."""

    def __init__(self, args=None):
        """Inicializa un backup."""
        self.config = dict()
        if args is not None:
            self.set(args)

    def set(self, args):
        """Configura como se ejecutara el backup."""
        for arg in args:
            
        self.config = args

    def run(self):
        """Ejecuta el backup."""


backup = Backup({
    'sourcePath': '/home/copeito/Projects',
    'destinationPath': '/media/local/data',
    'maxNumber': 10,
    'minDaysBackup': 15
})
