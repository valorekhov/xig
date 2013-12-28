"""\
    XIG Configuration File

    Modify the contents of the below XigConfig object in order to
    change the configuration of the Xig.  Each option is
    commented as to what it does.
"""

class XigConfig(object):
    
    ## Session Types
    
    # Enable/disable session types; disable sessions by commenting
    # them out.  Disabling sessions may be advantageous if you
    # find you are running out of memory on your ConnectPort.
    #
    # The "xig" session is always available.  It is required by
    # the system.
    #
    session_types = [
        "http",               # HTTP (fetch web pages)
        "http_sample_reporter",       # UDP URL destination support
    ]
    

    httpSampleReporter_weather = [{
            "_method"       : "GET",
            "_destination"  : "http://api.thingspeak.com/update",
            "key"           : "XXXXXXXX",
            "field1"        : "{Temp}",
            "field2"        : "{RH}",
            "field3"        : "{AtmoPressure}",
            "field4"        : "{AmbientLight}",
            "field5"        : "{BroadbandLight}",
            "field6"        : "{Infrared}",
        }]


    ## Global Configuration Variables
    
    # You shouldn't need to change anything in this section unless
    # you know what you've been doing or you've been instructed to
    # do so.
 
    # Should we send the helpfile for all unknown commands or
    # simply ignore them?
    global_always_send_help = False

    # Controls how long must buffers in the system may reach before
    # they are trimmed.  This setting also happens to control the
    # maximum length of a URL or XIG command.
    global_max_buf_size = 256
    
    # Controls how many sessions are allowed to queue up for a
    # single XBee destination.  Normally XBees only request a single
    # session at a time but automatic services may queue up several
    # session requests, such as the I/O service.
    global_max_dest_session_q_len = 8
    
    # How often (in seconds) to call the garbage collector:
    global_gc_interval = 60

    # Log-levels for various sub systems:
    log_level_global = "info"
    log_level_io_kernel = "debug"
     
    # Controls which UDP port number to receive requests
    xbee_udp_port = 5649
   
