from datetime import datetime
from pathlib import Path
import os


class SessionService:
    def __init__(self, report_folder, login=None, started=None):
        self.report_folder = Path(report_folder)
        self.login = login or os.environ.get('USERNAME') or os.environ.get('USER') or 'student'
        self.started = started or datetime.now()

    def finish(self, ended=None):
        ended = ended or datetime.now()
        self.report_folder.mkdir(parents=True, exist_ok=True)
        report = self.report_folder / 'work_report.txt'
        with report.open('a', encoding='utf-8') as file:
            file.write('+------------------+---------------------+---------------------+\n')
            file.write('| login            | time_in             | time_out            |\n')
            file.write('+------------------+---------------------+---------------------+\n')
            file.write(f'| {self.login[:16]:<16} | {self.started:%d.%m.%Y %H:%M:%S} | {ended:%d.%m.%Y %H:%M:%S} |\n')
            file.write('+------------------+---------------------+---------------------+\n\n')
        return report
