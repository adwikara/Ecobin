import sys
import time 
from Phidget22.Devices.Stepper import *
from Phidget22.PhidgetException import *
from Phidget22.Phidget import *
from Phidget22.Net import *

try:
    from motorfunctions import *
except ImportError:
    sys.stderr.write("\nCould not find PhidgetHelperFunctions. Either add PhdiegtHelperFunctions.py to your project folder "
                      "or remove the import from your project.")
    sys.stderr.write("\nPress ENTER to end program.")
    readin = sys.stdin.readline()
    sys.exit()

'''
* Configures the device's DataInterval
* Displays info about the attached Phidget channel.  
* Fired when a Phidget channel with onAttachHandler registered attaches
*
* @param self The Phidget channel that fired the attach event
'''
def onAttachHandler(self):
    
    ph = self

    try:

        print("\nAttach Event:")

        """
        * Get device information and display it.
        """
        channelClassName = ph.getChannelClassName()
        serialNumber = ph.getDeviceSerialNumber()
        channel = ph.getChannel()
        if(ph.getDeviceClass() == DeviceClass.PHIDCLASS_VINT):
            hubPort = ph.getHubPort()
            print("\n\t-> Channel Class: " + channelClassName + "\n\t-> Serial Number: " + str(serialNumber) +
                "\n\t-> Hub Port: " + str(hubPort) + "\n\t-> Channel:  " + str(channel) + "\n")
        else:
            print("\n\t-> Channel Class: " + channelClassName + "\n\t-> Serial Number: " + str(serialNumber) +
                    "\n\t-> Channel:  " + str(channel) + "\n")
    
        """
        * Set the DataInterval inside of the attach handler to initialize the device with this value.
        * DataInterval defines the minimum time between PositionChange events.
        * DataInterval can be set to any value from MinDataInterval to MaxDataInterval.
        """
        print("\tSetting DataInterval to 1000ms")
        try:
            ph.setDataInterval(1000)
        except PhidgetException as e:
            sys.stderr.write("Runtime Error -> Setting DataInterval: \n\t")
            DisplayError(e)
            return
        
        """
        * Engage the Stepper inside of the attach handler to allow the motor to move to its target position
        * The motor will only track a target position if it is engaged.
        * Engaged can be set to True to enable the servo, or False to disable it.
        """
        print("\tEngaging Stepper")
        try:
            ph.setEngaged(True)
        except PhidgetException as e:
            sys.stderr.write("Runtime Error -> Setting Engaged: \n\t")
            DisplayError(e)
            return
        
    except PhidgetException as e:
        print("\nError in Attach Event:")
        DisplayError(e)
        traceback.print_exc()
        return

"""
* Displays info about the detached Phidget channel.
* Fired when a Phidget channel with onDetachHandler registered detaches
*
* @param self The Phidget channel that fired the attach event
"""
def onDetachHandler(self):

    ph = self

    try:

        print("\nDetach Event:")
        """
        * Get device information and display it.
        """
        channelClassName = ph.getChannelClassName()
        serialNumber = ph.getDeviceSerialNumber()
        channel = ph.getChannel()
        if(ph.getDeviceClass() == DeviceClass.PHIDCLASS_VINT):
            hubPort = ph.getHubPort()
            print("\n\t-> Channel Class: " + channelClassName + "\n\t-> Serial Number: " + str(serialNumber) +
                "\n\t-> Hub Port: " + str(hubPort) + "\n\t-> Channel:  " + str(channel) + "\n")
        else:
            print("\n\t-> Channel Class: " + channelClassName + "\n\t-> Serial Number: " + str(serialNumber) +
                    "\n\t-> Channel:  " + str(channel) + "\n")

    except PhidgetException as e:
        print("\nError in Detach Event:")
        DisplayError(e)
        traceback.print_exc()
        return

"""
* Writes Phidget error info to stderr.
* Fired when a Phidget channel with onErrorHandler registered encounters an error in the library
*
* @param self The Phidget channel that fired the attach event
* @param errorCode the code associated with the error of enum type ph.ErrorEventCode
* @param errorString string containing the description of the error fired
"""
def onErrorHandler(self, errorCode, errorString):

    sys.stderr.write("[Phidget Error Event] -> " + errorString + " (" + str(errorCode) + ")\n")

"""
* Outputs the Stepper's most recently reported Position.
* Fired when a Stepper channel with onPositionChangeHandler registered meets DataInterval criteria
*
* @param self The Stepper channel that fired the PositionChange event
* @param Position The reported Position from the Stepper channel
"""
def onPositionChangeHandler(self, Position):
    print("[Position Event] -> Position: " + str(Position))
"""
* Prints descriptions of how events related to this class work
"""
def PrintEventDescriptions():

    #print("\n--------------------\n"
    #    "\n  | Position update events will call their associated function every time new Position data is received from the device.\n"
    #    "  | The rate of these events can be set by adjusting the DataInterval for the channel.\n"
    #    "  | Press ENTER once you have read this message.")
    readin = sys.stdin.readline(1)
    
    print("\n--------------------")
            
"""
* Creates, configures, and opens a Stepper channel.
* Provides interface for controlling TargetPosition of the Stepper.
* Closes out Stepper channel
*
* @return 0 if the program exits successfully, 1 if it exits with errors.
"""
def sort(pos = 5000):
    try:
        """
        * Allocate a new Phidget Channel object
        """
        ch = Stepper()
        
        """
        * Set matching parameters to specify which channel to open
        """
        #You may remove this line and hard-code the addressing parameters to fit your application
        channelInfo = AskForDeviceParameters(ch)
        
        ch.setDeviceSerialNumber(channelInfo.deviceSerialNumber)
        ch.setHubPort(channelInfo.hubPort)
        ch.setIsHubPortDevice(channelInfo.isHubPortDevice)
        ch.setChannel(channelInfo.channel)   
        
        if(channelInfo.netInfo.isRemote):
            ch.setIsRemote(channelInfo.netInfo.isRemote)
            if(channelInfo.netInfo.serverDiscovery):
                try:
                    Net.enableServerDiscovery(PhidgetServerType.PHIDGETSERVER_DEVICEREMOTE)
                except PhidgetException as e:
                    PrintEnableServerDiscoveryErrorMessage(e)
                    raise EndProgramSignal("Program Terminated: EnableServerDiscovery Failed")
            else:
                Net.addServer("Server", channelInfo.netInfo.hostname,
                    channelInfo.netInfo.port, channelInfo.netInfo.password, 0)

        """
        * Add event handlers before calling open so that no events are missed.
        """
        print("\n--------------------------------------")
        #print("\nSetting OnAttachHandler...")
        ch.setOnAttachHandler(onAttachHandler)
        
        #print("Setting OnDetachHandler...")
        ch.setOnDetachHandler(onDetachHandler)
        
        #print("Setting OnErrorHandler...")
        ch.setOnErrorHandler(onErrorHandler)
        
        #print("\nSetting OnPositionChangeHandler...")
        ch.setOnPositionChangeHandler(onPositionChangeHandler)
        
        """
        * Open the channel with a timeout
        """
        #print("\nOpening and Waiting for Attachment...")
        
        try:
            ch.openWaitForAttachment(5000)
        except PhidgetException as e:
            PrintOpenErrorMessage(e, ch)
            raise EndProgramSignal("Program Terminated: Open Failed")

        """
        * Sorting process, set position for the stepper to move
        """
        end = False
        buf = pos
        ch.setVelocityLimit(50000)
        ch.setAcceleration(200000)
        while (end != True):
            if (buf == 0):
                end = True
                break

            targetPosition = buf

            if (targetPosition > ch.getMaxPosition() or targetPosition < ch.getMinPosition()):
                print("TargetPosition must be between %.2f and %.2f\n" % (ch.getMinPosition(), ch.getMaxPosition()))
                continue

            #print("Setting Stepper TargetPosition to " + str(targetPosition))
            ch.setTargetPosition(targetPosition)
            #print("Position is " + str(ch.getPosition()))

            if (targetPosition == ch.getPosition()):
                buf = 0


        '''
        * Perform clean up and exit
        '''
        print("Cleaning up...")
        ch.close()
        return 0

    except PhidgetException as e:
        sys.stderr.write("\nExiting with error(s)...")
        DisplayError(e)
        #traceback.print_exc()
        print("Cleaning up...")
        ch.close()
        return 1
        
    except EndProgramSignal as e:
        print(e)
        print("Cleaning up...")
        ch.close()
        return 1
    
    except RuntimeError as e:
         sys.stderr.write("Runtime Error: \n\t" + e)
         traceback.print_exc()
         return 1
         
    finally:
        print(print("\nExiting..."))
#sort(-20000)
#sort(150000)