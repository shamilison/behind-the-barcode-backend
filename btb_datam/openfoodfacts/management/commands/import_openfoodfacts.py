import os.path
import time
import pandas as pd
from django.core.management.base import BaseCommand
from openfoodfacts.models import OpenFoodFact


class Command(BaseCommand):
    help = 'Import brand raw_data from Open Food Facts TSV file in chunks using bulk operations'

    def handle(self, *args, **kwargs):
        file_path = os.path.join('raw_data', 'en.openfoodfacts.org.products.csv')

        chunk_size = 10000
        insert_count = update_count = 0
        chunk_num = 0

        for chunk in pd.read_csv(
            file_path,
            sep='\t',
            usecols=[
                'code', 'product_name', 'brands', 'brands_tags', 'brands_en',
                'origins', 'origins_tags', 'origins_en', 'countries', 'countries_en', 'countries_tags',
                'cities', 'cities_tags', 'manufacturing_places', 'manufacturing_places_tags',
            ],
            dtype={'code': str},
            chunksize=chunk_size,
            low_memory=False
        ):
            chunk_num += 1
            start_time = time.time()
            self.stdout.write(self.style.NOTICE(f"\n📦 Processing chunk {chunk_num} (up to {chunk_size} records)"))

            chunk = chunk.dropna(subset=['code'])

            # Prepare a dict of barcode -> data
            chunk_records = {
                row['code']: {
                    'product_name': row.get('product_name'),
                    'brands': row.get('brands'),
                    'brands_en': row.get('brands_en'),
                    'brands_tags': row.get('brands_tags'),
                    'origins': row.get('origins'),
                    'origins_tags': row.get('origins_tags'),
                    'origins_en': row.get('origins_en'),
                    'countries': row.get('countries'),
                    'countries_en': row.get('countries_en'),
                    'countries_tags': row.get('countries_tags'),
                    'cities': row.get('cities'),
                    'cities_tags': row.get('cities_tags'),
                    'manufacturing_places': row.get('manufacturing_places'),
                    'manufacturing_places_tags': row.get('manufacturing_places_tags'),
                }
                for _, row in chunk.iterrows()
            }

            barcodes = list(chunk_records.keys())

            # Fetch existing barcodes from DB
            existing = OpenFoodFact.objects.filter(barcode__in=barcodes)
            existing_barcodes = set(existing.values_list('barcode', flat=True))

            # Prepare lists for bulk insert and update
            to_create = []
            to_update = []

            for barcode, data in chunk_records.items():
                if barcode in existing_barcodes:
                    obj = OpenFoodFact(barcode=barcode, **data)
                    to_update.append(obj)
                else:
                    to_create.append(OpenFoodFact(barcode=barcode, **data))

            if to_create:
                OpenFoodFact.objects.bulk_create(to_create, batch_size=1000)
                insert_count += len(to_create)

            if to_update:
                OpenFoodFact.objects.bulk_update(
                    to_update,
                    fields=[
                        'product_name', 'brands', 'brands_en', 'brands_tags',
                        'origins', 'origins_tags', 'origins_en',
                        'countries', 'countries_en', 'countries_tags',
                        'cities', 'cities_tags', 'manufacturing_places', 'manufacturing_places_tags'
                    ],
                    batch_size=1000
                )
                update_count += len(to_update)

            elapsed = time.time() - start_time
            self.stdout.write(
                self.style.SUCCESS(
                    f"✅ Chunk {chunk_num} done in {elapsed:.2f}s: Inserted {len(to_create)}, Updated {len(to_update)}"
                )
            )
            self.stdout.write(
                f"📊 Totals so far → Inserted: {insert_count:,}, Updated: {update_count:,}"
            )

        self.stdout.write(self.style.SUCCESS(
            f"\n🎉 Finished importing! Total Inserted: {insert_count:,}, Updated: {update_count:,}"
        ))
