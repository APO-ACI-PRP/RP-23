#!/usr/bin/env python

from device import Device
import xmltodict
import json
import sys
import time


#This function extracts vlan database from switches and returns it as a list of dictionaries.
def show_vlan(sw):
	 
	vlan_output = {} 
	show_vl = sw.show('show vlan')
	show_vl_result = xmltodict.parse(show_vl[1])
	vlan_data = show_vl_result['ins_api']['outputs']['output']['body']["TABLE_vlanbrief"]["ROW_vlanbrief"]

	'''this if statement is necessary to accomodate for a corner case when there is only one vlan configured
	on a switch. In this case vlan_data object that is created based on NX-OS API response is not a list of d
	ictionaries but a single dictionary.     vlan_data = [vlan_data]	statement
	converts dictionary into a list with a single element of type dictionary'''

	if type(vlan_data) is not list:			
		vlan_data = [vlan_data]	

	return vlan_data

	
def vlan_delete(sw, vlan):
	#This function deletes vlan from the switch. 
	vlan_delete_result = sw.conf('no vlan ' + vlan['vlanshowbr-vlanid'])
	return None

def vlan_add(sw, vlan):
	#This function adds vlan to the switch. 
	vlan_add_result = sw.conf('vlan ' + vlan['vlanshowbr-vlanid'])
	return None

def main():
	
	'''This script will run continuously and will output elapsed time every 20 seconds. 20 seconds is the
	interval to poll switches and make changes to vlan database configuration'''

	count = 1
	while count > 0:
		switches = []
		vlan_db = []

		'''This loop goes through all 4 switches in dCloud Open NX-OS Lab and imports their vlan configuration
		into a list of vlan databases where each element represents vlan configuraiton of one switch'''
		for i in range(4):
			switches.append(Device(ip="198.18.134.14" + str(i), username='admin', password='C1sco12345'))
			switches[i].open()			
			vlan_db.append(show_vlan(switches[i]))

		
		'''seed switch denotes the master switch in the network where all vlan changes will be made
		all other switches will be slaves. Every polling interval vlan configuration of slaves will be
		syncronized with the master. This means that all vlans not present on the master/seed switch 
		will be deleted from slaves and all vlans missing on slave switches will be created. Think of
		master switch as a single VTP Server and all the slave switches as VTP Clients'''
		seed_sw = 0

		''' this loop goes through all switches and deletes all the vlans not present in the master 
		vlan database of the seed switch '''
		for i in range(4):
			if i == seed_sw:
				continue
			elif vlan_db[i] == vlan_db[seed_sw]:
				continue
			else:
				for vlan in vlan_db[i]:
					if vlan in vlan_db[seed_sw]:
						continue
					else:
						vlan_delete(switches[i], vlan)


		'''this loop goes through all switches and adds all the vlans that are present in the master 
		vlan database of the seed switch but do not exist in the slave switch databases'''
		for i in range(4):
			if i == seed_sw:
				continue
			elif vlan_db[i] == vlan_db[seed_sw]:
				continue
			else:
				for vlan in vlan_db[seed_sw]:
					if vlan in vlan_db[i]:
						continue
					else:
						vlan_add(switches[i], vlan)
		time.sleep(20)	
		print "Number of seconds since the script was started: ",  20 * count
		count = count + 1


if __name__ == "__main__":
	main()
