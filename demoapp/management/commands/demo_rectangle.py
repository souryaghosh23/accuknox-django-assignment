from django.core.management.base import BaseCommand
from demoapp.rectangle import Rectangle


class Command(BaseCommand):

    help = "Demonstrate Rectangle iteration"

    def handle(self,*args,**kwargs):

        rectangle=Rectangle(10,5)

        self.stdout.write(
            self.style.SUCCESS(
                "Rectangle iteration output:"
            )
        )

        for item in rectangle:
            self.stdout.write(str(item))