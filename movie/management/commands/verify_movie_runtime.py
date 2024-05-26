from django.core.management.base import BaseCommand
from movie.models import Movie

class Command(BaseCommand):
    help = 'Verify and update movie runtime values'

    def handle(self, *args, **kwargs):
        movies = Movie.objects.all()
        updated_count = 0
        for movie in movies:
            if movie.runtime is None or movie.runtime <= 0:
                movie.runtime = 90  # Set a default runtime value (90 minutes in this case)
                movie.save()
                updated_count += 1
        self.stdout.write(self.style.SUCCESS(f'Successfully updated {updated_count} movies with invalid runtime values'))
