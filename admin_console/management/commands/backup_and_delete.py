
import os
import datetime
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.utils import timezone
from admin_console.models import User
from datetime import timedelta

class Command(BaseCommand):
    help = 'Backup the database and delete inactive users'

    def handle(self, *args, **kwargs):
        # Backup the database
        backup_file = f"db_backup_{datetime.datetime.now().strftime('%Y%m%d')}.json"
        backup_path = os.path.join('D:\\project\\E_com_25_oct\\E_Commerce\\backup', backup_file)

        # Call dumpdata and specify the output file path
        call_command('dumpdata', output=backup_path)

        self.stdout.write(self.style.SUCCESS(f'Successfully backed up the database to {backup_path}'))

        # Define the cutoff date for inactive users
        cutoff_date = timezone.now() - timedelta(days=30)

        # Fetch users that are deactivated and have last_login older than the cutoff date
        users_to_delete = User.objects.filter(
            account_status=User.DEACTIVATED,
            last_login__lt=cutoff_date
        )

        # Count and delete users
        count = users_to_delete.count()
        users_to_delete.delete()

        self.stdout.write(self.style.SUCCESS(f'Successfully deleted {count} inactive users.'))





# import os
# import datetime
# from django.core.management.base import BaseCommand
# from django.core.management import call_command

# class Command(BaseCommand):
#     help = 'Load data into the database from a backup JSON file'

#     def add_arguments(self, parser):
#         parser.add_argument('backup_file', type=str, help='The path to the backup JSON file')

#     def handle(self, *args, **kwargs):
#         backup_file = kwargs['backup_file']

#         # Check if the backup file exists
#         if not os.path.isfile(backup_file):
#             self.stdout.write(self.style.ERROR(f'Backup file not found: {backup_file}'))
#             return

#         # Load data from the backup file
#         try:
#             call_command('loaddata', backup_file)
#             self.stdout.write(self.style.SUCCESS(f'Successfully loaded data from {backup_file}'))
#         except Exception as e:
#             self.stdout.write(self.style.ERROR(f'Error loading data: {e}'))
