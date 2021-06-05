from django.core.management import call_command
from boot_django import boot_django

if __name__ == "__main__":
    boot_django()
    call_command("makemigrations", "robitcontrol")
