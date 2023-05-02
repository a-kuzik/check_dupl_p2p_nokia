# Check the duplicating p2p networks for nokia

This is a simple tool for checking the duplicating p2p networks for nokia network. 
In some cases not all routes are visible in the RTM. For example p2p local routes with ISIS as IGP protocol where will be used with advertise-passive-only. And if as result an administartive mistake ocurs, another overlay protocols like RSVP will be impacted. 
The tool contain two scripts, first for get information from routers, and second for parsing this information and analyze the duplicating addresses. All hosts to be checked must be listed in the yaml file. 
