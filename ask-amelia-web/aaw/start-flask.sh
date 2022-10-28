#/bin/bash
echo "Starting Flask as background process with nohup..."
nohup flask run --host=0.0.0.0 &
echo "Started!"
