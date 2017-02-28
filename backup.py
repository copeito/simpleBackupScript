"""Configure a Backup class object.

This object will be managed by backupManager.

Tested in Python 3.5.


"""

from pathlib import Path
import sys
import tarfile
import time


class Backup(object):
    """Configure a backup."""

    def __init__(self, args=None):
        """Initialize a backup."""
        self.params = dict()
        if args is not None:
            self.set(args)

    def set(self, args):
        """Manage how will be exetuted the backup."""
        paths = ['sourcePath', 'destinationPath']
        integers = ['maxNumber', 'minDaysBackup']

        for arg in args:
            argType = type(args[arg])

            if paths.count(arg):
                if isinstance(args[arg], Path):
                    param = args[arg]
                elif (argType == str):
                    param = Path(args[arg])
                else:
                    sys.exit(
                        "Error: sourcePath and destinationPath must be "
                        "strings or objects from Path class"
                    )
                if not param.exists():
                    sys.exit(
                        'Error: path '+str(param)+' dont exist'
                    )

            elif integers.count(arg):
                if argType != int:
                    sys.exit(
                        'Error: '+arg+' must be an integer'
                    )
                else:
                    param = args[arg]

            self.params[arg] = param

    def checkParams(self):
        """Check if params are ok."""
        for mandatoryPath in ['sourcePath', 'destinationPath']:
            try:
                self.params[mandatoryPath]
            except:
                sys.exit(
                    'Error: '+mandatoryPath+' must be defined'
                )
        if not self.params['destinationPath'].is_dir():
                sys.exit(
                    'Error: destinationPath must be a directory'
                )

    def run(self):
        """Create the backup."""
        self.checkParams()

        backupPath = Path(
            self.params['destinationPath'].joinpath(
                self.params['sourcePath'].name +
                '.'+time.strftime("%Y%m%d")+'.tgz'
            )
        )

        tar = tarfile.open(
            str(backupPath),
            'w:gz'
        )
        tar.add(
            str(self.params['sourcePath']),
            self.params['sourcePath'].name
        )
        tar.close()


backup = Backup({
    'sourcePath': Path('/home/copeito/Projects'),
    'destinationPath': '/media/local/data/',
    'maxNumber': 10,
    'minDaysBackup': 15
})

backup.run()
