# File: core/management/commands/start_module.py
import os
from pathlib import Path
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = 'Creates a new module (enhanced Django app) and registers it in settings.'

    def add_arguments(self, parser):
        parser.add_argument('module_name', type=str, help='Name of the module to create')

    def handle(self, *args, **options):
        module_name = options['module_name']
        base_dir = Path(settings.BASE_DIR)
        modules_dir = base_dir / 'modules'
        module_dir = modules_dir / module_name

        # Check if the module already exists
        if module_dir.exists():
            raise CommandError(f"The module '{module_name}' already exists.")

        # Create module directories
        try:
            module_dir.mkdir(parents=True, exist_ok=True)
            # Create subdirectories and files
            structure = [
                ('delivery/dtos', 'user.dtos.py'),
                ('delivery/handlers', 'user.controller.py'),
                ('delivery/middlewares', None),
                ('delivery/routes', 'user.routes.py'),
                ('repository', 'user.repository.py'),
                ('services', 'user.services.py'),
                ('usecases', 'user.usecases.py'),
            ]

            for sub_dir, file_name in structure:
                full_path = module_dir / sub_dir
                full_path.mkdir(parents=True, exist_ok=True)
                if file_name:
                    (full_path / file_name).touch()

            # Create __init__.py files
            for sub_dir in ['', 'delivery', 'delivery/dtos', 'delivery/handlers', 
                            'delivery/middlewares', 'delivery/routes', 
                            'repository', 'services', 'usecases']:
                (module_dir / sub_dir / '__init__.py').touch()

            # Create apps.py
            apps_file = module_dir / 'apps.py'
            apps_file.write_text(
                f"""
from django.apps import AppConfig

class {module_name.capitalize()}Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'modules.{module_name}'
"""
            )

            self.stdout.write(self.style.SUCCESS(f"Module '{module_name}' created successfully."))

            # Register the module in settings
            settings_file = base_dir / 'core/settings.py'
            with settings_file.open('r') as f:
                settings_content = f.read()

            if f"'modules.{module_name}'" not in settings_content:
                # Add the module to INSTALLED_APPS
                new_settings_content = settings_content.replace(
                    "INSTALLED_APPS = [",
                    f"INSTALLED_APPS = [\n    'modules.{module_name}',"
                )
                with settings_file.open('w') as f:
                    f.write(new_settings_content)

                self.stdout.write(self.style.SUCCESS(f"Module '{module_name}' registered in settings.INSTALLED_APPS."))

        except Exception as e:
            raise CommandError(f"An error occurred while creating the module: {e}")
