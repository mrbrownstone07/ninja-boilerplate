import os
import sys
from pathlib import Path
from typing import Dict, Union

class AppCreationError(Exception):
    """Custom exception for app creation errors"""
    pass

class AppStructureGenerator:
    def __init__(self):
        self.BASE_DIR = Path(__file__).resolve().parent
        self.SETTINGS_FILE = self.BASE_DIR / "core/settings.py"
        self.MODULES_DIR = self.BASE_DIR / "modules"

    def _generate_app_config(self, app_name: str) -> str:
        """Generate the content for apps.py"""
        return f"""from django.apps import AppConfig

class {app_name.capitalize()}Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    label = '{app_name}'
    name = 'modules.{app_name}'
"""

    def _generate_models_init(self) -> str:
        """Generate the content for models/__init__.py"""
        return """import os
import importlib
import inspect
from django.db import models

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Loop through all .py files in the models directory
for file_name in os.listdir(current_dir):
    if file_name.endswith('.py') and file_name != '__init__.py':
        # Import the module
        module_name = file_name[:-3]  # Remove .py extension
        module = importlib.import_module(f'.{module_name}', package=__package__)
        
        # Find all Django Model classes in the module
        for name, obj in inspect.getmembers(module):
            if inspect.isclass(obj) and issubclass(obj, models.Model) and obj != models.Model:
                # Add the model to the current namespace
                globals()[name] = obj
"""

    def get_app_structure(self, app_name: str) -> Dict[str, Union[Dict, str]]:
        """Define the app structure with all necessary files and directories"""
        return {
            "delivery": {
                "__init__.py": "",
                "api.py": "#write API endpoints and controllers here.",
                "schemas.py": "#write ninja schemas here",
                "middlewares.py": """#write your api middlewares here if needed"""
            },
            "repository": {
                "__init__.py": "",
            },
            "services": {
                "__init__.py": "",
            },
            "usecases": {
                "__init__.py": "",
            },
            "models": {
                "__init__.py": self._generate_models_init(),
            },
            "migrations": {
                "__init__.py": "",
            },
#             "tests": {
#                 "__init__.py": "",
#                 "test_api.py": "",
#                 "test_services.py": "",
#                 "test_repository.py": ""
#             },
            "__init__.py": "",
            "apps.py": self._generate_app_config(app_name)
        }

    def create_app(self, app_name: str) -> None:
        """Create a new Django app with the enhanced structure"""
        app_dir = self.MODULES_DIR / app_name

        try:
            if app_dir.exists():
                raise AppCreationError(f"App '{app_name}' already exists")

            print(f"\n📦 Creating new app: {app_name}")
            self._create_structure(app_dir, self.get_app_structure(app_name))
            print(f"✅ App structure created successfully")

            self._register_app_in_settings(app_name)
            print(f"✅ App registered in settings.py")

        except Exception as e:
            print(f"\n❌ Error: Failed to create app: {str(e)}")
            raise AppCreationError(f"App creation failed: {str(e)}")

    def _create_structure(self, base_path: Path, structure: Dict) -> None:
        """Recursively create directories and files"""
        try:
            os.makedirs(base_path, exist_ok=True)
            
            for name, content in structure.items():
                current_path = base_path / name
                
                if isinstance(content, dict):
                    self._create_structure(current_path, content)
                else:
                    print(f"   Creating: {current_path.relative_to(self.MODULES_DIR)}")
                    current_path.write_text(content)
                    
        except Exception as e:
            print(f"\n❌ Error: Failed to create structure at {base_path}: {str(e)}")
            raise AppCreationError(f"Structure creation failed: {str(e)}")

    def _register_app_in_settings(self, app_name: str) -> None:
        """Register the app in Django settings"""
        try:
            if not self.SETTINGS_FILE.exists():
                raise AppCreationError("settings.py not found")

            app_config = f"    'modules.{app_name}.apps.{app_name.capitalize()}Config',\n"
            content = self.SETTINGS_FILE.read_text().splitlines()

            # Find LOCAL_APPS section
            try:
                start_index = content.index("LOCAL_APPS = [")
            except ValueError:
                raise AppCreationError("LOCAL_APPS section not found in settings.py")

            # Check if app is already registered
            if any(app_name in line for line in content):
                print(f"\n⚠️  Warning: App '{app_name}' is already registered in settings.py")
                return

            # Insert the app configuration
            content.insert(start_index + 1, app_config)
            self.SETTINGS_FILE.write_text('\n'.join(content))

        except Exception as e:
            print(f"\n❌ Error: Failed to register app in settings: {str(e)}")
            raise AppCreationError(f"App registration failed: {str(e)}")

def main():
    """Main entry point for the script"""
    if len(sys.argv) != 2:
        print("\n❌ Error: Invalid number of arguments")
        print("Usage: python create_app.py <app_name>")
        sys.exit(1)

    app_name = sys.argv[1].lower()
    
    # Validate app name
    if not app_name.isidentifier():
        print(f"\n❌ Error: Invalid app name: {app_name}")
        print("App name must be a valid Python identifier")
        sys.exit(1)

    try:
        generator = AppStructureGenerator()
        generator.create_app(app_name)
        print(f"\n🎉 Successfully created app: {app_name}")
        print("\nStructure created:")
        print(f"   modules/{app_name}/")
        print(f"   ├── delivery/")
        print(f"   ├── repository/")
        print(f"   ├── services/")
        print(f"   ├── usecases/")
        print(f"   ├── models/")
        print(f"   ├── migrations/")
        # print(f"   └── tests/")
    except AppCreationError as e:
        print(f"\n❌ Error: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()