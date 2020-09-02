
docker build -t fda .
docker run -d -p 10000:8888 -e JUPYTER_ENABLE_LAB=yes -v "$PWD":/home/jovyan fda jupyter lab --NotebookApp.token='' --NotebookApp.password=''
open http://localhost:10000
