# SYNOPSIS:
#
#   $ cd ~/Projects/PatentSwim/SwimServer
#   $ python swim_server.py
#
# In web brower,
#   http://0.0.0.0:8080/api/patents/6028857,10015143

if __name__ == "__main__":
    import rest_agent
    rest_agent.runServer('0.0.0.0', debug=True);
