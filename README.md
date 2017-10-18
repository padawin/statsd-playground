# Statsd

## Install

    pip install -r requirements.txt

## Usage

First, start graphite:

    docker run -d\
        --name graphite\
        --restart=always\
        -p 80:80\
        -p 2003-2004:2003-2004\
        -p 2023-2024:2023-2024\
        -p 8125:8125/udp\
        -p 8126:8126\
        graphiteapp/graphite-statsd

Then use the application to aggregate some usage metrics:

    ./main.py + 20 22

Yes, the application is a calculator.

After having done all your maths, head to graphite to see the numbers at
http://localhost to see the figures.
