__author__ = 'kosala atapattu'
import time
from ansible import errors

def net_interface_list(values=[]):
    return ','.join(str(':'.join(i)) for i in values)

def array_to_csv(values=[]):
    return ','.join(values)

def get_image_name (values, resttime, strict):
    from datetime import datetime
    from ansible import errors
    import json
    
    tf = "%Y-%m-%d %H:%M:%S"
    if resttime != "latest":
        if resttime is not None:
            try:
                restoretime = datetime.strptime (resttime, tf)
            except:
                raise errors.AnsibleFilterError('Icorrect date format ['+resttime+']')
    else:
        restoretime = datetime.now()
    
    preferedtime = None
    preferedimg = None

    snap_pref_time = None
    snap_pref_img = None
    lc_pref_time = None
    mount_pref_time = None
    onvault_pref_time = None
    dedup_pref_time = None

    for image in values['results']:
        try:
            # Start time of the recovery range
            starttime = datetime.strptime (image['json']['result']['consistencydate'][:-4], tf)
        except:
            raise errors.AnsibleFilterError('Unable to read start time of the image.')

        try:
            # End time of the recovery range
            endtime = datetime.strptime (image['json']['result']['endpit'], tf)
        except:
            endtime = None
            pass
        # Component type (need to elimitate LogSmart images)
        componenttype = image['json']['result']['componenttype']
        # Mounted host name. Set to 0 if not mounted. Need to eliminate already mounted images.
        mountedhost = image['json']['result']['mountedhost']
        # Job class of the image
        jobclass = image['json']['result']['jobclass']
        # For skipping further mountedhost check if liveclone
        if jobclass == 'liveclone':
            mountedhost = '0'

        if componenttype == '0' and mountedhost == '0':
            # We need to track the previous closest image to check the this image is close in time
            # However, this is only valid for strict_policy=no scenarios
            if preferedtime == None:
                preferedtime = starttime
                if preferedtime > restoretime:
                    prevdiff = preferedtime - restoretime
                else:
                    prevdiff = restoretime - preferedtime

            # If strict_policy= yes
            if strict:
                if endtime != None:
                    if starttime < restoretime < endtime: # is this a valid image to meet the restore point
                        if starttime > preferedtime: # is this image better than the one we know already
                            preferedtime = starttime
                            preferedimg = image
            else: # if strict_policy=no (default)
                if restoretime > starttime:
                    currdif = restoretime - starttime
                else:
                    currdif = starttime - restoretime 
                
                if prevdiff.total_seconds() >= currdif.total_seconds(): #this is python 2.7 function
                    preferedtime = starttime
                    preferedimg = image
                    prevdiff = currdif
            
            if preferedimg != None:
            # this is to check whether there're liveclones or mounts
            # available  
                if jobclass == "snapshot":
                    snap_pref_time = preferedtime
                    snap_pref_img = preferedimg
                elif jobclass == "liveclone":
                    lc_pref_time = preferedtime
                    lc_pref_img = preferedimg
                elif jobclass == "mount":
                    mount_pref_time = preferedtime
                    mount_pref_img = preferedimg
                elif jobclass == "OnVault":
                    onvault_pref_time = preferedtime
                    onvault_pref_img = preferedimg
                elif jobclass == "dedup":
                    dedup_pref_time = preferedtime
                    dedup_pref_img = preferedimg
                    
    if snap_pref_img != None:        
        if lc_pref_time == snap_pref_time:
            preferedimg = snap_pref_img
        elif mount_pref_time == snap_pref_time:
            preferedimg = snap_pref_img
        elif onvault_pref_time == snap_pref_time:
            preferedimg = snap_pref_img
        elif dedup_pref_time == snap_pref_time:
            preferedimg = snap_pref_img

    if preferedimg != None:
        return preferedimg['json']['result']['backupname']
    else:
        return ""

class FilterModule(object):
    def filters(self):
        return {
            'net_interface_list': net_interface_list, 
            'get_image_name': get_image_name, 
            'array_to_csv': array_to_csv
            }
        
