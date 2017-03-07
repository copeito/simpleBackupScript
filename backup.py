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

        """Create nedded file structure"""
        self.backups = self.createAppPath(
            {
                'Path': Path('tmp/backups.txt')
            }
        )

    def createAppPath(self, args):
        """Create path."""
        if not args['Path'].exists():
            try:
                if not args['Path'].parent.exists():
                    args['Path'].parent.mkdir()
                args['Path'].touch(0o642, True)
            except:
                print('Path '+str(args['Path'])+' cannot be initialized.')

        return args['Path']

    def set(self, args):
        """Manage how will be exetuted the backup."""
        paths = ['sourcePath', 'destinationPath']
        integers = ['minSavedBackups', 'minDaysBackup']

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

    def create(self):
        """Create new backup."""
        """Append the name of the backup to the end of destinationPath"""
        backupPath = Path(
            self.params['destinationPath'].joinpath(
                self.params['sourcePath'].name +
                '.'+time.strftime("%Y%m%d.%H%M%S")+'.tgz'
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

        if str(backupPath) not in self.backups.read_text().split("\n"):
            self.backups.write_text(
                self.backups.read_text()+str(backupPath)+"\n"
            )

    def delete(self):
        """Delete old backups."""

    def run(self):
        """Check given parameters."""
        self.checkParams()
        """Create new backup"""
        self.create()
        """Delete old backups"""
        self.delete()


backup = Backup({
    'sourcePath': Path('/home/copeito/Projects'),
    'destinationPath': '/media/local/data/',
    'minSavedBackups': 10,
    'minDaysBackup': 15
})

backup.run()
