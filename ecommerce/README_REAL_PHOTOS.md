# Nawab — Real Product Photography

This build uses 150 distinct real stock photographs hosted by Pexels: 30 each for Electronics, Fashion, Accessories, Home, and Gaming. The catalog entries and photo URLs are paired in `store/management/commands/seed_demo.py`.

## Setup

1. Activate the virtual environment.
2. Run `python manage.py migrate` if needed.
3. Run `python manage.py seed_demo`.
4. Run `python manage.py download_real_images` to download the Pexels photos into `media/products/` and switch the catalog to local `/media/` images.
5. Run `python manage.py runserver`.

Pexels states that its photos can be downloaded and used for free, including on websites and apps, without required attribution. Review the current Pexels license before production use.
