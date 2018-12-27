ansible_newvm_mount
======================

This is a ansible role to perform Actifio VMware or Hyper-V VM mounts to ESXi/Hyper-V hosts as new VM.

Role Variables
--------------

Following variables are accepted/required for this role. 

### Actifio Applinace Related 

| Variable Name    | Description | Required (Y/N) |
|------------------|---|---|
| act_appliance    | Actifio Appliance IP or FQDN. | Y               |
| act_user         | Actifio username. This should be a Actifio user with System Manage priviledges | Y
| act_pass         | Password for the Actifio User | Y
| act_vendorkey    | Vendor key can be obtained by the customer through opening a Support Case with the CSE. | Y
| act_appname 	   | Source Application (VM) name | Y
| act_restoretime  | Desired time to recover the database to. Based on the time specified, the appropriate image will be selected (if an image is not specified). If a recovery image is not availble for the stipulated restore time, and if the strict_policy is set to no, then the closest image to the restore time will be selected. | N
| strict_policy    | See act_restoretime | N
| act_job_class    | snapshot, dedup, dedupasync, liveclone, syncback and OnVault. If not specified would select any based on the Restore time, without any preference to the jobclass. | N
| act_imagename    | Actifio Image Name to be mounted. This parameter overrides act_appname, act_restoretime and act_job_class. | N 
| act_nowait_mount  | If set to true waits for the mount job to complete. Else return after submitting the job. | N
| act_imagelabel   | Label for mounted image. Default is 'Ansible_Playbook'. | N
| vm_src_esxhost 	   | Source ESXi host where the VM is protected from. (Using for identifying VM ) | N
| vm_tgt_esxhost 	   | Target ESXi or Hyper-V host where the VM to be mounted. | Y
| vm_mgmtserver    | vCenter Server or System Center hostname of target ESXi/Hyper-V host. Must be same with hostname which is registered within Actifio appliance. | N
| vm_type          | Need to specify vmware or hyperv. Default is vmware. | Y
| vm_name	   | New VM name. | Y
| vm_datastore	   | Target datastore or directory path which is located on new VM's meta, swap and RDM map file. (VM itself will be mounted to ESXi/Hyper-V host as RDM) | Y
| vm_physicalrdm   | Type of RDM volumes. Default is virtual RDM. (VMware Only)| N
| vm_restoremac:   | Restore original MAC address to the new VM. Default is false. (VMware Only) | N
| vm_mapdiskstoallesx      | Map RDM volumes to all ESXi hosts that are belong to the cluster. Default is false. (VMware Only) | N


Example Playbook
----------------

### Mount VMware VM image as New VM Example

```
- name: testng mount image as new vm
  hosts: "{{ host_group }}"
  become: yes
  become_method: sudo
  roles:
    - { role: ansible_newvm_mount, act_appliance: my-actifio, act_user: ansible, act_pass: mypassword }
  vars:
    act_vendorkey: "{{ contact CSE to get yours }}"
    act_appname: "SourceVM"
    act_job_class: "snapshot"
    vm_src_esxhost: "esxi1"
    vm_mgmtserver: "vCenterServer"
    vm_tgt_esxhost: "esxi2"
    vm_name: "TargetVM"
    vm_datastore: "datastore1"

```


License
-------

Copyright 2018 <Hiroshi Takeuchi hiroshi.takeuchi@actifio.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
