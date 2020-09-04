# prometheus-python-log-histogram
Prometheus python log histogram

This is a python prometheus client that generate a log file and use histogram to save into buckets


use:

# install requirement packages
pip install -r requirements.txt


# grant execution permison
chmod +x app-server.py

# run
./app-server.py


# go to localhost:5000/generate to generate the log file this will take long time to respond due the proccess
# generating this log file writting a lot of lines 
# go to localhost:5000/metrics to see the result

