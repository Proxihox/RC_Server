#! /bin/bash

kill -9 $(lsof -t -i :65432)
python3 server.py

cleanup() {
    echo "Cleanup started."
    kill -9 $(lsof -t -i :65432)
    echo "Cleanup completed."
}

trap cleanup EXIT
wait