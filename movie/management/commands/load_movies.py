import csv
from django.core.management.base import BaseCommand
from movie.models import Movie
from datetime import datetime

class Command(BaseCommand):
    help = 'Load movies from CSV file'

    def handle(self, *args, **kwargs):
        processed_count = 0
        skipped_count = 0
        batch_size = 100  # Print progress every 100 movies
        preview_rows = 5  # Number of rows to preview

        try:
            with open('data/movies_metadata3.csv', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)

                # Print the first few rows
                for i, row in enumerate(reader):
                    if i < preview_rows:
                        self.stdout.write(self.style.NOTICE(f'Preview row {i + 1}: {row}'))
                    else:
                        break

                # Reset the reader
                csvfile.seek(0)
                reader = csv.DictReader(csvfile)

                for row in reader:
                    # Handle empty or invalid dates
                    release_date = row['release_date']
                    if not release_date or release_date == '':
                        release_date = '2000-01-01'
                    else:
                        try:
                            # Try to convert MM/DD/YYYY to YYYY-MM-DD
                            release_date = datetime.strptime(release_date, '%m/%d/%Y').strftime('%Y-%m-%d')
                        except ValueError:
                            try:
                                # If already in YYYY-MM-DD, validate it
                                datetime.strptime(release_date, '%Y-%m-%d')
                            except ValueError:
                                release_date = '2000-01-01'

                    # Handle empty string and invalid runtime values
                    runtime = row['runtime']
                    if runtime is None or runtime.strip() == '' or not runtime.replace('.', '', 1).isdigit():
                        print(f'Skipping movie with invalid runtime: {runtime}')
                        skipped_count += 1
                        continue  # Skip this movie if runtime is empty or invalid

                    runtime = int(float(runtime))

                    # Handle empty or missing price values
                    price = row['price'].strip()  # Ensure no leading/trailing whitespace
                    if price is None or price == '' or not price.isdigit():
                        print(f'Skipping movie with invalid price: {price}')
                        skipped_count += 1
                        continue  # Skip this movie if price is empty or invalid

                    price = int(price)
                    print(f"Processed movie: {row['title']} with price: {price}")  # Debugging statement
                    if price < 30 or price > 50:
                        print(f'Skipping movie with out of range price: {price}')
                        skipped_count += 1
                        continue  # Skip this movie if price is out of the valid range

                    # Check if the movie already exists
                    if not Movie.objects.filter(movie_id=int(row['id'])).exists():
                        # Add more debug information here
                        print(f"Creating movie: {row['title']} with price: {price}")
                        movie = Movie(
                            title=row['title'],
                            overview=row['overview'],
                            poster_path=row['poster_path'],
                            runtime=runtime,
                            release_date=release_date,
                            genres=row['genres'],
                            movie_id=int(row['id']),
                            price=price  # Set the price here
                        )
                        movie.save()
                        print(f"Saved movie: {movie.title} with price: {movie.price}")

                    # Update and print progress
                    processed_count += 1
                    if processed_count % batch_size == 0:
                        self.stdout.write(f'Processed {processed_count} movies...')

            self.stdout.write(self.style.SUCCESS(f'Successfully loaded {processed_count} movies'))
            self.stdout.write(self.style.WARNING(f'Skipped {skipped_count} movies due to invalid runtime or price'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error occurred: {e}'))
