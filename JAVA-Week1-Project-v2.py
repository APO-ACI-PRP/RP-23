#!/usr/bin/env python

import xmltodict
import json
import sys

from device import Device

def show_intf(sw, interface):
    
    #define argument for interface name
    command = 'show interface ' + interface
    
    sh_int = sw.show(command)
    sh_interface_dict = xmltodict.parse(sh_int[1])
    
    #prefix dictionary for the show interface facts
    prefix = sh_interface_dict['ins_api']['outputs']['output']['body']['TABLE_interface']['ROW_interface']
    
    #dictionary for argument #2
    int_dict = {}
    
    int_dict['Name'] = prefix ['interface']           
    int_dict['State'] = prefix ['state']       
    int_dict['Admin State'] = prefix ['admin_state'] 
    int_dict['Share'] = prefix ['share_state'] 
    int_dict['Hardware Description'] = prefix ['eth_hw_desc'] 
    int_dict['MAC Address - HW'] = prefix ['eth_hw_addr'] 
    int_dict['Ethernet BIA'] = prefix ['eth_bia_addr']
    int_dict['Interface Description'] = prefix ['desc']        
    int_dict['IP Address'] = prefix ['eth_ip_addr'] 
    int_dict['Mask'] = prefix ['eth_ip_mask'] 
    int_dict['IP Prefix'] = prefix ['eth_ip_prefix']   
    int_dict['MTU'] = prefix ['eth_mtu']     
    int_dict['ETH BW'] = prefix ['eth_bw']      
    int_dict['ETH DLY'] = prefix ['eth_dly']     
    int_dict['ETH Reliability'] = prefix ['eth_reliability'] 
    int_dict['TX Load'] = prefix ['eth_txload']  
    int_dict['RX Load'] = prefix ['eth_rxload']  
    int_dict['Medium'] = prefix ['medium']      
    int_dict['Duplex'] = prefix ['eth_duplex']  
    int_dict['Speed'] = prefix ['eth_speed']           
    int_dict['Beacon'] = prefix ['eth_beacon']          
    int_dict['Auto Negoiate'] = prefix ['eth_autoneg']         
    int_dict['Flow In'] = prefix ['eth_in_flowctrl']     
    int_dict['Flow Out'] = prefix ['eth_out_flowctrl']    
    int_dict['MDI X'] = prefix ['eth_mdix']            
    int_dict['SWT Monitor'] = prefix ['eth_swt_monitor']     
    int_dict['Ethertype'] = prefix ['eth_ethertype']       
    int_dict['EEE State'] = prefix ['eth_eee_state']       
    int_dict['Last Link Flapped'] = prefix ['eth_link_flapped']    
    int_dict['Clear Counters'] = prefix ['eth_clear_counters']  
    int_dict['Reset Counters'] = prefix ['eth_reset_cntr']      
    int_dict['Load Interval RX'] = prefix ['eth_load_interval1_rx']   
    int_dict['Inrate Bits'] = prefix ['eth_inrate1_bits']    
    int_dict['Inrate Packets'] = prefix ['eth_inrate1_pkts']    
    int_dict['Load Interval TX'] = prefix ['eth_load_interval1_tx']   
    int_dict['Outrate Bits'] = prefix ['eth_outrate1_bits']   
    int_dict['Outrate Packets'] = prefix ['eth_outrate1_pkts']   
    int_dict['Unicast In'] = prefix ['eth_inucast']         
    int_dict['Multicast In'] = prefix ['eth_inmcast']         
    int_dict['Broadcast In'] = prefix ['eth_inbcast']         
    int_dict['In Packets'] = prefix ['eth_inpkts']          
    int_dict['In Bytes'] = prefix ['eth_inbytes']         
    int_dict['Jumbo In Packets'] = prefix ['eth_jumbo_inpkts']    
    int_dict['Storm Support'] = prefix ['eth_storm_supp']      
    int_dict['Runts'] = prefix ['eth_runts']           
    int_dict['Giants'] = prefix ['eth_giants']          
    int_dict['CRC'] = prefix ['eth_crc']             
    int_dict['No Buffer'] = prefix ['eth_nobuf']           
    int_dict['In Errors'] = prefix ['eth_inerr']           
    int_dict['Frames'] = prefix ['eth_frame']           
    int_dict['Overrun'] = prefix ['eth_overrun']         
    int_dict['Underrun'] = prefix ['eth_underrun']        
    int_dict['Ignored'] = prefix ['eth_ignored']         
    int_dict['Watchdog'] = prefix ['eth_watchdog']        
    int_dict['Bad Ethernet'] = prefix ['eth_bad_eth']         
    int_dict['Bad Protocol'] = prefix ['eth_bad_proto']       
    int_dict['Interface Drops In'] = prefix ['eth_in_ifdown_drops'] 
    int_dict['Dribble'] = prefix ['eth_dribble']         
    int_dict['In Discards'] = prefix ['eth_indiscard']       
    int_dict['In Pause'] = prefix ['eth_inpause']         
    int_dict['Out Multicast'] = prefix ['eth_outucast']        
    int_dict['Out Multicast'] = prefix ['eth_outmcast']        
    int_dict['Out Broadcast'] = prefix ['eth_outbcast']        
    int_dict['Out Packets'] = prefix ['eth_outpkts']         
    int_dict['Out Jumbo'] = prefix ['eth_outbytes']        
    int_dict['Out Jumbo'] = prefix ['eth_jumbo_outpkts']   
    int_dict['Out Error'] = prefix ['eth_outerr']          
    int_dict['Collisions'] = prefix ['eth_coll']            
    int_dict['Deferred'] = prefix ['eth_deferred']        
    int_dict['Late Collisions'] = prefix ['eth_latecoll']        
    int_dict['Lost Carrier'] = prefix ['eth_lostcarrier']     
    int_dict['No Carrier'] = prefix ['eth_nocarrier']       
    int_dict['Babbles'] = prefix ['eth_babbles']         
    int_dict['Out Discard'] = prefix ['eth_outdiscard']      
    int_dict['Out Pause'] = prefix ['eth_outpause']
        
    return int_dict

def main():

    sw1 = Device(ip='198.18.134.140', username='admin', password='C1sco12345')
   
    args = sys.argv

    if len(args) == 3:
        interface_name = args[1]
        
        try:
            sw1.open()
            
            intf = show_intf(sw1,args[1])
            
            print args[2].upper() + ': ' + json.dumps(intf[args[2]], indent=4)
        except:
            #exception for incorrect fact argument
            print 'Invalid interface parameter specified - argument #2'
            for k,v in intf.iteritems():
                print k
    else:
        #else for incorrect augments
        print 'Review input parameters - Ethernet1/X first and interface parameter second'

if __name__ == "__main__":
    main()