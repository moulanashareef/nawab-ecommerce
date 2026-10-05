NAWAB - COMPLETE 150-PRODUCT IMAGE MATCH FIX

This update replaces the old remote/mismatched product images with 150 local product-specific images and updates seed_demo.py so product names and images stay aligned.

Categories:
- Electronics: 30
- Fashion: 30
- Accessories: 30
- Home: 30
- Gaming: 30

Apply to the current Windows project:
1. Stop Django: Ctrl+C
2. Extract this ZIP into C:\Users\Md.Shabana\Downloads\nawab\ecommerce and choose Replace/Overwrite.
3. Open CMD there and run:
   venv\Scripts\activate
   python manage.py seed_demo
   python manage.py runserver
4. Open http://127.0.0.1:8000/ and press Ctrl+F5.

No makemigrations/migrate is required because the database schema is unchanged.
