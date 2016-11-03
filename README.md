# Evaluating Cloud File Synchronizers
These scripts evaluate how cloud file synchronization services (e.g. Dropbox) deal with conflicts.
A conflict might be introduced by two users concurrently adding a file with the same name, or by user `A` deleting a folder `f` while user `B` updates a file in `f`.

## Usage

**Requirements**

- two identical VMs with the sync clients installed
- these scripts in the VM user's home directory
- these scripts on your host machine

**Rough Outline**

1. set up initial state on one VM, and then disconnect both VMs from the network
2. perform changes on both VMs, and reconnect them one after the other
3. copy resulting states to host machine
4. evaluate

**Detailed Steps**

1. `python run.py setup` set up the initial test scenarios on _one_ VM
2. wait for the initial setup to sync to the other VM
  1. once the tray icons of all clients on both VMs are showing a green tick mark or similar, the initial sync should be completed
3. disable networking on the VMs (e.g. through the VM management software)
4. `python run.py change 1` on the first VM
5. `python run.py change 2` on the second VM
6. enable networking _only_ on VM 1
7. wait for the changes on VM 1 to be synced to the servers (green tick marks in tray icons on VM 1)
8. enable networking also on VM 2
9. wait for the changes of VM 2 to be synced to VN 1 (green tick marks in tray icons of both VMs)
10. copy all sync client folders from both VM user home directories to your host machine
  1. copy the folders of VM 1 to a folder named `1`
  2. copy the folders of VM 2 to a folder named `2`
12. `python run.py evaluate` on your host machine
13. view results in the folder `eval` on your host machine


## Structure
- The test cases are defined in the folder [tests](tests/).
[run.py](run.py) runs and evaluates these tests.
