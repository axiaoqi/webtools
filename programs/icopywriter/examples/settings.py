from pathlib import Path

SynologyDrive = Path.home() / 'SynologyDrive'
if not SynologyDrive.exists():
    SynologyDrive = Path(r'D:\SynologyDrive')
