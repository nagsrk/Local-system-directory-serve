# -*- coding: utf-8 -*-
from logging import getLogger, StreamHandler, DEBUG
import subprocess
import os
import shutil
import MySQLdb
import ConfigParser
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)


#
# retrieve db information from MySQL DB
#
def retrieve_db_info():
    
    # define array
    customer_name_ip_list = []
    
    # config file read
    conf = ConfigParser.SafeConfigParser()
    try:
        conf.read('/home/nag/Desktop/project/logd/lib/database.config')
        db_host = conf.get('database', 'host')
        db_name = conf.get('database','dbname')
        db_user = conf.get('database', 'user')
        db_pass = conf.get('database', 'pass')
        db_backup = conf.get('backup', 'file')
        
        # open a database connection
        connection = MySQLdb.connect (host=db_host, user=db_user, passwd=db_pass, db=db_name)
        # prepare a cursor object using cursor() method
        cursor = connection.cursor ()
        # execute the SQL query using execute() method.
        cursor.execute ("select username,IP_Address_1, IP_Address_2 from auth_user left join logd_customerdetail on auth_user.id = logd_customerdetail.user_id")
        # fetch all of the rows from the query
        data = cursor.fetchall ()
        
        if open(db_backup).read() == str(data):
            logger.debug("db state is same previous states")
            return None
        
        f = open(db_backup, "w")
        f.write(str(data))
        f.close()
        # print the rows
        for row in data :
            if row[1] is not None and row[2] is not None:
                #print row[0], row[1], row[2]
                customer_name_ip_list.append([row[0], row[1]])
                customer_name_ip_list.append([row[0], row[2]])
            
        # close the cursor object
        cursor.close ()
        # close the connection
        connection.close ()
        
        # return list of customerName & customerIp
        return customer_name_ip_list
    
    except Exception as e:
        logger.debug(str(e))
        raise

#
# Edit rsyslog config function
#
def append_config(customer_name_ip_list):
    
    # open the rsyslog config file
    try:
        # current config all delete
        shutil.copyfile("/etc/rsyslog.d/log-service.conf", "/etc/rsyslog.d/log-service.conf.bak")
        os.remove("/etc/rsyslog.d/log-service.conf")
        f = open("/etc/rsyslog.d/log-service.conf", "a+")
    except:
        logger.debug("cannot open rsyslog config file.")
        raise
    
    
    
    
    try:
        # create template config
        template_string = create_template_string()
        f.write(template_string)
        
        # add each ip_address rule
        for customer_name_ip in customer_name_ip_list:
            customer_name = customer_name_ip[0]
            customer_ip = customer_name_ip[1]
            config_string = create_config_string(customer_name, customer_ip)
            f.write(config_string)
        
    except:
        logger.debug("cannot write to rsyslog config file")
        raise
    
    f.close()
    # rsyslog service restart(apply config)
    subprocess.call('service rsyslog restart', shell=True)
    
    # log directory owner change
    subprocess.call('chown -R apache:apache /var/log/remote/', shell=True)
    
    logger.info("append rsyslog config success")



#
# Create String for rsyslog
#
def create_config_string(customer_name, ip_address):
    config = ":msg, contains, \"fromhost:%s\" /var/log/remote/%s/%s/message.log;AddTemp\n" % (ip_address,customer_name, ip_address)
    return config

def create_template_string():
    template_string = "$template AddTemp, \"%rawmsg:::drop-last-lf%\\n\"\n"
    return template_string


#
# main
#
if __name__ == "__main__":
    try:
        temporary_list = retrieve_db_info()
        if temporary_list is not None:
            append_config(temporary_list)
        else:
            logger.debug("getting DB information is None")
    
    except Exception as e:
        logger.debug(str(e))
    
    
