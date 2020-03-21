# PatentSwim
Effortlessly navigate and discover relationships among patents

## Overview
PatentSwim is implemented in two parts:

`SwimServer` is a micro-service that fetches patent information from the
`www.patentsview.org` online service and caches the information locally.  It
is implemented in Python and uses the `bottle` framework to implement a RESTful
API.

`SwimClient` is a web-based interface that lets the user interactively load a
patent and discover all of the patents cited by that patent as well as all the
patents that refer to that patent.

And so on transitively...

## To run the SwimServer

    $ cd {ProjectRoot}/SwimServer
    $ pipenv shell
    (SwimServer) $ python swim-server.py

## To run the SwimClient

Open a browser and enter:

    file://{ProjectRoot}/SwimClient/index.html
