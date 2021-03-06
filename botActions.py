#!/usr/bin/env python

#This is a list of actions which the robot can perform
#If you add a new function put it into the actions dictionary
import os
import rospy
import baxter_interface
import subprocess

class botActions():
    def __init__(self):
        try:
            rospy.init_node('botActions', anonymous=True)
            os.system('rosrun baxter_interface joint_trajectory_action_server.py --mode velocity &')
        except rospy.ROSInterruptException:
            pass

    def destructor(self):
        bashCommand = "rosrun baxter_tools tuck_arms.py -t"
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        os.system('rosnode kill rsdk_velocity_joint_trajectory_action_server')
        os.system('rosnode kill botActions')
        return

    def template(response):
        context = {'action-succes':'succes'}
        context = {'action-error': 'error'}
        print 'TUUUUUUUUUUUUUCK'
        print response['entities']['tuckArm'][0]['value']
        return context

    def default(response):
        return

    def tuckArms(response):

        try:
            value = response['result']['parameters']['eTuckUntuck']
        except KeyError:
            context = {'missing-key': 'tuckArm'}
            return context

        if value == 'untuck':
            bashCommand = "rosrun baxter_tools tuck_arms.py -u"
            process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
            output, error = process.communicate()
        elif value == 'tuck':
            bashCommand = "rosrun baxter_tools tuck_arms.py -t"
            process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
            output, error = process.communicate()

        context = {'action-succes': 'succes'}
        return context

    def gripperControl(response):

        try:
            value_side = response['result']['parameters']['side']
            value_action = response['result']['parameters']['eOpenClose']
        except KeyError:
            return

        if( value_side == 'both'):
            value_sides = {'left','right'}

            for value_side in value_sides:
                gripper = baxter_interface.Gripper(value_side)
                gripper.calibrate()
                if value_action == 'open':
                    gripper.open()
                elif value_action == 'close':
                    gripper.close()

        elif( value_side == 'right' or value_side == 'left'):
            gripper = baxter_interface.Gripper(value_side)
            gripper.calibrate()
            if value_action == 'open':
                gripper.open()
            elif value_action == 'close':
                gripper.close()

        context = {'action-succes': 'succes'}
        return context

    def waveHand(response):

        try:
            value_side = response['result']['parameters']['side']
        except KeyError:
            return

        if(value_side[0] == 'left'):
            side_explicit = 'left'
        elif(value_side[0] == 'right'):
            side_explicit = 'right'
        print value_side
        print side_explicit

        bashCommand = 'rosrun baxter_examples joint_trajectory_file_playback.py -f wave_hand_' + side_explicit
        subprocess.call(bashCommand.split(), stdout=subprocess.PIPE)

        context = {'action-succes': 'succes'}
        return context


    actions = {
        'aTuckArm': tuckArms,
        'aCloseHand':gripperControl,
        'aWaveHand':waveHand,
        'aSessionOver':destructor,
    }