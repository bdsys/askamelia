#/bin/bash
echo "Starting http://dev.askamelia.bdsys.net:5000 on Flask as background process with nohup..."
nohup flask run --host=0.0.0.0 --port=5000 &
echo "Started!"
echo "Starting http://askamelia.bdsys.net:80 on Flask as background process with nohup..."
nohup flask run --host=0.0.0.0 --port=80 &
echo "Started!"
echo "Done!"
