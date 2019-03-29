# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 09:15:19 2019

@author: Ian
"""
from transitions import Machine

class RackHarvest(object):
    
    states = ['listening', 'processing', 'confirming']
    
    def __init__(self, *args, **kwargs):
        super(RackHarvest, self).__init__(*args, **kwargs)
    
        
        #Initialise the state machine
        self.machine = Machine(model= self, #object on which the library attaches trigger functions
                               states= self.states,
                               initial= 'listening')
        
        #add transitions to state machine 
        self.machine.add_transition(trigger= 'isReceivedfromrobot',
                                    source= 'listening',
                                    dest= 'processing',
                                    after= 'sent_to_and_await_from_rackservo',
                                    )
        
        self.machine.add_transition(trigger= 'isReceivedfromrack',
                                    source= 'processing',
                                    dest= 'confirming',
                                    after= 'sent_to_robotrpi',
                                    )
        
        self.machine.add_transition(trigger= 'isSenttorobot',
                                    source= 'confirming',
                                    dest= 'listening',
                                    after= 'listen_to_robotrpi',
                                    )
        
    
    def listen_to_robotrpi(self):
        #if msg.payload is not None:
        #   
        return self.isReceivedfromrobot()
    
    def sent_to_and_await_from_rackservo(self):
        #call listtray() here
        #call sendData() here
        #
        #
        #while ser.read(1) != b'%d' %i:
        #    sleep(0.4)
        #    ser.read(1)
        #
        return self.isfirstReceivedfromrack()
        
    def sent_to_robotrpi(self):
        ##publish to robotrpi to confirm slider release 
        #
        return self.isSenttorobot()
    