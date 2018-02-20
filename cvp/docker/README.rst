Docker Deployment
=================

To deploy the OVP Dashboard perform the following steps:

 #. Copy config.env.sample to config.env

     cp config.env.sample config.env

 #. Copy vhost.env.sample to vhost.env

     cp vhost.env.sample vhost.env

 #. Modify config.env and vhost.env to you liking

 #. Bring the services up

     docker-compose up -d
 
 #. Navigate to the site listed in vhost.env in your browser of choice

     google-chrome-stable http://ovp.localhost

     .. note::

        If you're using the default sitename 'ovp.localhost', you'll
        need to add the following line to /etc/hosts:
        
          127.0.0.1 ovp.localhost
