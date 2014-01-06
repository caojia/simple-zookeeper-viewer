### simple-zookeeper-viewer

A simple ZooKeeper viewer. Enough said. 
Original Source: https://github.com/davidwen/simple-zookeeper-viewer

#### Setup

Requires [kazoo](https://github.com/python-zk/kazoo) and [Flask](https://github.com/mitsuhiko/flask)

Requirements can be installed via pip and the provided requirements file.

    $ pip install -r requirements.txt

#### Usage

To run simple-zookeeper-viewer, execute

    $ python viewer.py
    
Then navigate to http://localhost:5000/ to view the root of the ZooKeeper server. Host/port can be configured via Flask

* Click on a node to view data and metadata on that node
* Double click on a node to view that node and its children
