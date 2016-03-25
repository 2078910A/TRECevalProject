# TRECevalProject

Lab Wednesday 2-4 Group C

***
##Project Members (github account - name, student matriculation number)

2085099 - Maximilian Morell, 2085099M

2078910A - Blair Aitcheson, 2078910A

tierney12/Sean Tierney (switched github accounts early on) - Sean Tierney, 2140573T

zixk - Dominik Bladek, 2144751B

***
##Steps to run:

1. Download files: 
```
git clone https://github.com/2078910A/TRECevalProject

Navigate to TRECevalProject/TRECappProject/trec_eval.8.1 then in the terminal, type:
make (should be done on linux operating systems for the best results, this is incompatible with Windows OS)
```

2. Setup virtual environment: 
```
mkvirtualenv trecapp
```

3. Work on new virtual environment:
```
workon trecapp
```

4. Install requirements:
```
pip install -r requirements.txt
```

5. Setup database:
```
python manage.py makemigrations
python manage.py migrate
python populate_TREC.py
```

6. Run project:
```
python manage.py runserver
```

7. Find server on http://127.0.0.1:8000/TRECapp/
(use linux operating system for best results, limited functionality on Windows OS)

