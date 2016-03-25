# TRECevalProject

Lab Wednesday 2-4 Group C

***
##Project Members

2085099 - Maximilian Morell, 2085099M

2078910A - Blair Aitcheson, 2078910A

tierney12 - Sean Tierney, 2140573T

zixk - Dominik Bladek, 2144751B

***
##Steps to run:

1. Download files: 
```
git clone https://github.com/2078910A/TRECevalProject

Navigate to TRECevalProject/TRECappProject/trec_eval.8.1 then in the terminal, type:
make
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
python [population script]
```

6. Run project:
```
python manage.py runserver
```

7. Find server on http://127.0.0.1:8000/TRECapp/


