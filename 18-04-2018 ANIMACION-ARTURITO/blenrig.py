# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####
#
# ##### ACKNOWLEDGEMENTS #####
#
# BlenRig by: Juan Pablo Bouza
# Original script programming: Bart Crouch
# Current maintainer and developer: Juan Pablo Bouza
#
# Synoptic Panel/Rig Picker based on work by: Salvador Artero     
#
# Special thanks on python advice to: Campbell Barton, Bassam Kurdali, Daniel Salazar, CodeManX, Patrick Crawford
# Special thanks for feedback and ideas to: Jorge Rausch, Gabriel Sabsay, Hjalti Hjálmarsson, Beorn Leonard
#
# #########################################################################################################



bl_info = {
    'name': 'BlenRig 5 GUI',
    'author': 'Juan Pablo Bouza',
    'version': (216,),
    'blender': (2, 76, 0),
    'api': 55057,
    'location': 'View3D > Properties > BlenRig 5 Controls panel',
    'warning': '',
    'description': 'Tools for controlling BlenRig rigs',
    'wiki_url': 'http://www.jpbouza.com.ar',
    'tracker_url': '',
    'category': 'Rigging'}


import bpy
rig_name = "BlenRig_5"

# global group lists
all_bones = hand_l = hand_r = arm_l = arm_r = leg_l = leg_r = foot_l = foot_r = head = torso = []

####### Bones Hiding System #######

from bpy.props import FloatProperty



def bone_auto_hide(context):  
    if not bpy.context.screen:
        return False
    if bpy.context.screen.is_animation_playing == True:
        return False    
    if not bpy.context.active_object:
        return False
    if (bpy.context.active_object.type in ["ARMATURE"]) and (bpy.context.active_object.mode == 'POSE'):   
        for b_prop in bpy.context.active_object.data.items():
            if b_prop[0] == 'bone_auto_hide' and b_prop[1] == 0:
                return False          
        for prop in bpy.context.active_object.data.items():
            if prop[0] == 'rig_name' and prop[1] == 'BlenRig_5':     
                                                   
                arm = bpy.context.active_object.data 
                p_bones = bpy.context.active_object.pose.bones
                
                for b in p_bones:
                    if ('properties' in b.name):
                        if ('torso' in b.name):

                        # Torso FK/IK   
                            prop = int(b.ik_torso)
                            prop_inv = int(b.inv_torso)  
                        
                            for bone in arm.bones:          
                                if (bone.name in b['bones_ik']):
                                    if prop == 1 or prop_inv == 1:
                                        bone.hide = 1   
                                    else:
                                        bone.hide = 0    
                                if (bone.name in b['bones_fk']):
                                    if prop != 1 or prop_inv == 1:
                                        bone.hide = 1 
                                    else:
                                        bone.hide = 0            
                                
                        # Torso INV   
                            for bone in arm.bones:   
                                if (bone.name in b['bones_inv']):
                                    if prop_inv == 1:
                                        bone.hide = 0
                                    else:
                                        bone.hide = 1                                 
                        if ('head' in b.name):
                        # Neck FK/IK          
                            prop = int(b.ik_head)
                            for bone in arm.bones:
                                if (bone.name in b['bones_fk']):
                                    if prop == 1:
                                        bone.hide = 0
                                    else:
                                        bone.hide = 1                                      
                                if (bone.name in b['bones_ik']):
                                    if prop == 0:
                                        bone.hide = 0
                                    else:
                                        bone.hide = 1                                                                         

                        # Head Hinge         
                            prop_hinge = int(b.hinge_head)
                            for bone in arm.bones:       
                                if (bone.name in b['bones_fk_hinge']):
                                    if prop == 1 or prop_hinge == 0:
                                        bone.hide = 0
                                    else:
                                        bone.hide = 1                              
                                if (bone.name in b['bones_ik_hinge']):
                                    if prop == 0 or prop_hinge == 1:
                                        bone.hide = 0
                                    else:
                                        bone.hide = 1     
                        #Left Properties                
                        if ('_L' in b.name): 
                            if ('arm' in b.name):
                                                               
                            # Arm_L FK/IK           
                                prop = int(b.ik_arm_L)
                                prop_hinge = int(b.hinge_hand_L)
                                for bone in arm.bones:       
                                    if (bone.name in b['bones_fk_L']):
                                        if prop == 1:
                                            bone.hide = 0
                                        else:
                                            bone.hide = 1                           
                                    if (bone.name in b['bones_ik_L']):
                                        if prop == 0:
                                            bone.hide = 0
                                        else:
                                            bone.hide = 1                      

                            # HAND_L
                                    if arm['rig_type'] == "Biped":    
                                        if (bone.name in b['bones_ik_hand_L']):  
                                            if prop == 1 and prop_hinge == 0:
                                                bone.hide = 1
                                            else:
                                                bone.hide = 0  
                                        if (bone.name in b['bones_fk_hand_L']):   
                                            if prop_hinge == 1:
                                                bone.hide = 1
                                            else:
                                                bone.hide = 0                              
                                        if (bone.name in b['bones_ik_palm_L']):                      
                                            if prop == 1 or prop_hinge == 0:      
                                                bone.hide = 1
                                            else:
                                                bone.hide = 0                       
                                        if (bone.name in b['bones_fk_palm_L']):                      
                                            if prop == 1 or prop_hinge == 0:      
                                                bone.hide = 0
                                            else:
                                                bone.hide = 1   
                                                                            
                            # Fingers_L   
                                prop_ik_all = int(b.ik_fing_all_L)  
                                prop_hinge_all = int(b.hinge_fing_all_L)   
                               
                                def fingers_hide(b_name):                                              
                                    for bone in arm.bones:
                                        ik_bones = [b_name]   
                                        if (bone.name in b_name):
                                            if prop == 1 or prop_hinge == 1 or prop_ik_all == 1 or prop_hinge_all == 1:
                                                bone.hide = 0
                                            if prop == 0 and prop_hinge == 0 and prop_ik_all == 0 and prop_hinge_all == 0:
                                                bone.hide = 1  
                                    return {"FINISHED"}      

                                prop_hinge = int(b.hinge_fing_ind_L)
                                prop = int(b.ik_fing_ind_L)                                                                                           
                                fingers_hide('fing_ind_ik_L')     
                                prop_hinge = int(b.hinge_fing_mid_L)
                                prop = int(b.ik_fing_mid_L)                                                                                           
                                fingers_hide('fing_mid_ik_L')  
                                prop_hinge = int(b.hinge_fing_ring_L)
                                prop = int(b.ik_fing_ring_L)                                                                                           
                                fingers_hide('fing_ring_ik_L')   
                                prop_hinge = int(b.hinge_fing_lit_L)
                                prop = int(b.ik_fing_lit_L)                                                                                           
                                fingers_hide('fing_lit_ik_L')   
                                prop_hinge = int(b.hinge_fing_thumb_L)
                                prop = int(b.ik_fing_thumb_L)                                                                                           
                                fingers_hide('fing_thumb_ik_L')                                                                     
                                       
                            if ('leg' in b.name):                                       
                            # Leg_L FK/IK           
                                prop = int(b.ik_leg_L)
                                for bone in arm.bones:     
                                    if (bone.name in b['bones_fk_L']):   
                                        if prop == 1:
                                            bone.hide = 0
                                        else:
                                            bone.hide = 1                               
                                    if (bone.name in b['bones_ik_L']):   
                                        if prop == 0:
                                            bone.hide = 0
                                        else:
                                            bone.hide = 1   
                                 
                            # Toes_L FK/IK          
                                prop = int(b.ik_toes_all_L)
                                prop_hinge = int(b.hinge_toes_all_L)                                
                                for bone in arm.bones:           
                                    if (bone.name in b['bones_fk_foot_L']):   
                                        if prop == 1:
                                            bone.hide = 0
                                        else:
                                            bone.hide = 1  
                                    if (bone.name in b['bones_ik_foot_L']):  
                                        if prop == 0 or prop_hinge == 1:
                                            bone.hide = 0
                                        else:
                                            bone.hide = 1  

                        #Right Properties                
                        if ('_R' in b.name): 
                            if ('arm' in b.name):
                                                               
                            # Arm_R FK/IK           
                                prop = int(b.ik_arm_R)
                                prop_hinge = int(b.hinge_hand_R)
                                for bone in arm.bones:       
                                    if (bone.name in b['bones_fk_R']):
                                        if prop == 1:
                                            bone.hide = 0
                                        else:
                                            bone.hide = 1                           
                                    if (bone.name in b['bones_ik_R']):
                                        if prop == 0:
                                            bone.hide = 0
                                        else:
                                            bone.hide = 1                      

                            # HAND_R
                                    if arm['rig_type'] == "Biped":    
                                        if (bone.name in b['bones_ik_hand_R']):  
                                            if prop == 1 and prop_hinge == 0:
                                                bone.hide = 1
                                            else:
                                                bone.hide = 0  
                                        if (bone.name in b['bones_fk_hand_R']):   
                                            if prop_hinge == 1:
                                                bone.hide = 1
                                            else:
                                                bone.hide = 0                              
                                        if (bone.name in b['bones_ik_palm_R']):                      
                                            if prop == 1 or prop_hinge == 0:      
                                                bone.hide = 1
                                            else:
                                                bone.hide = 0                       
                                        if (bone.name in b['bones_fk_palm_R']):                      
                                            if prop == 1 or prop_hinge == 0:      
                                                bone.hide = 0
                                            else:
                                                bone.hide = 1   
                                                                            
                            # Fingers_R   
                                prop_ik_all = int(b.ik_fing_all_R)  
                                prop_hinge_all = int(b.hinge_fing_all_R)   
                               
                                def fingers_hide(b_name):                                              
                                    for bone in arm.bones:
                                        ik_bones = [b_name]   
                                        if (bone.name in b_name):
                                            if prop == 1 or prop_hinge == 1 or prop_ik_all == 1 or prop_hinge_all == 1:
                                                bone.hide = 0
                                            if prop == 0 and prop_hinge == 0 and prop_ik_all == 0 and prop_hinge_all == 0:
                                                bone.hide = 1  
                                    return {"FINISHED"}      

                                prop_hinge = int(b.hinge_fing_ind_R)
                                prop = int(b.ik_fing_ind_R)                                                                                           
                                fingers_hide('fing_ind_ik_R')     
                                prop_hinge = int(b.hinge_fing_mid_R)
                                prop = int(b.ik_fing_mid_R)                                                                                           
                                fingers_hide('fing_mid_ik_R')  
                                prop_hinge = int(b.hinge_fing_ring_R)
                                prop = int(b.ik_fing_ring_R)                                                                                           
                                fingers_hide('fing_ring_ik_R')   
                                prop_hinge = int(b.hinge_fing_lit_R)
                                prop = int(b.ik_fing_lit_R)                                                                                           
                                fingers_hide('fing_lit_ik_R')   
                                prop_hinge = int(b.hinge_fing_thumb_R)
                                prop = int(b.ik_fing_thumb_R)                                                                                           
                                fingers_hide('fing_thumb_ik_R')                                                                     
                                       
                            if ('leg' in b.name):                                       
                            # Leg_R FK/IK           
                                prop = int(b.ik_leg_R)
                                for bone in arm.bones:     
                                    if (bone.name in b['bones_fk_R']):   
                                        if prop == 1:
                                            bone.hide = 0
                                        else:
                                            bone.hide = 1                               
                                    if (bone.name in b['bones_ik_R']):   
                                        if prop == 0:
                                            bone.hide = 0
                                        else:
                                            bone.hide = 1   
                                 
                            # Toes_R FK/IK          
                                prop = int(b.ik_toes_all_R)
                                prop_hinge = int(b.hinge_toes_all_R)
                                for bone in arm.bones:           
                                    if (bone.name in b['bones_fk_foot_R']):   
                                        if prop == 1:
                                            bone.hide = 0
                                        else:
                                            bone.hide = 1  
                                    if (bone.name in b['bones_ik_foot_R']):  
                                        if prop == 0 or prop_hinge == 1:
                                            bone.hide = 0
                                        else:
                                            bone.hide = 1  
                                
####### Reproportion Toggle #######

from bpy.props import IntProperty, BoolProperty

def reproportion_toggle(context):
    if not bpy.context.screen:
        return False
    if bpy.context.screen.is_animation_playing == True:
        return False    
    if not bpy.context.active_object:
        return False
    if (bpy.context.active_object.type in ["ARMATURE"]) and (bpy.context.active_object.mode == 'POSE'):   
        for prop in bpy.context.active_object.data.items():
            if prop[0] == 'rig_name' and prop[1] == 'BlenRig_5':  
                prop = bool(bpy.context.active_object.data.reproportion)        
                p_bones = bpy.context.active_object.pose.bones
                if prop == True:
                    bpy.context.active_object.data.layers[31] = True 
                    for b in p_bones:      
                        for C in b.constraints:
                            if ('REPROP' in C.name):
                                C.mute = False 
                            if ('NOREP' in C.name):
                                C.mute = True   
                                                   
                elif prop == 0:
                    bpy.context.active_object.data.layers[31] = False   
                    for b in p_bones:     
                        for C in b.constraints:
                            if ('REPROP' in C.name):
                                C.mute = True 
                            if ('NOREP' in C.name):
                                C.mute = False   
        
                        if ('properties' in b.name):            
                            if ('L' in b.name):
                                if ('leg'in b.name):
                                    prop_toes = int(b.toggle_toes)    
                                    if prop_toes == 0:                                        
                                        for pbone in p_bones:
                                            if (pbone.name in b['bones_toes_ctrl_2_L']):
                                                for C in pbone.constraints:
                                                    if C.type == 'IK':
                                                        C.mute = True    
                                    else:
                                        for pbone in p_bones:
                                            if (pbone.name in b['bones_toes_ctrl_2_L']):
                                                for C in pbone.constraints:
                                                    if C.type == 'IK':
                                                        C.mute = False   
                                                                                       
                            if ('R' in b.name):
                                if ('leg'in b.name):
                                    prop_toes = int(b.toggle_toes)    
                                    if prop_toes == 0:                                        
                                        for pbone in p_bones:
                                            if (pbone.name in b['bones_toes_ctrl_2_R']):
                                                for C in pbone.constraints:
                                                    if C.type == 'IK':
                                                        C.mute = True   
                                    else:
                                        for pbone in p_bones:
                                            if (pbone.name in b['bones_toes_ctrl_2_R']):
                                                for C in pbone.constraints:
                                                    if C.type == 'IK':
                                                        C.mute = False                                        

####### Rig Toggles #######

from bpy.props import IntProperty, BoolProperty

def rig_toggles(context):
    if not bpy.context.screen:
        return False
    if bpy.context.screen.is_animation_playing == True:
        return False    
    if not bpy.context.active_object:
        return False
    if (bpy.context.active_object.type in ["ARMATURE"]) and (bpy.context.active_object.mode == 'POSE'):   
        for prop in bpy.context.active_object.data.items():
            if prop[0] == 'rig_name' and prop[1] == 'BlenRig_5':                
                p_bones = bpy.context.active_object.pose.bones
                arm = bpy.context.active_object.data 

                for b in p_bones:
                    if ('properties' in b.name):
                        # Left Properties
                        #Fingers_L 
                        if ('L' in b.name):
                            if ('arm'in b.name):
                                prop_fing = int(b.toggle_fingers)
                                for bone in arm.bones:  
                                    if (bone.name in b['bones_fingers_def_1_L']):   
                                        if prop_fing == 1:
                                            bone.layers[15] = 1
                                        else:
                                            bone.layers[15] = 0 
                                    if (bone.name in b['bones_fingers_def_2_L']):   
                                        if prop_fing == 1:
                                            bone.layers[15] = 1
                                            bone.layers[31] = 1                                                
                                        else:
                                            bone.layers[15] = 0  
                                            bone.layers[31] = 0                                                
                                    if (bone.name in b['bones_fingers_str_L']):   
                                        if prop_fing == 1:
                                            bone.layers[31] = 1
                                        else:
                                            bone.layers[31] = 0                                                                                        
                                    if (bone.name in b['bones_fingers_ctrl_1_L']):  
                                        if prop_fing == 1:
                                            bone.layers[0] = 1
                                        else:
                                            bone.layers[0] = 0                                                
                                    if (bone.name in b['bones_fingers_ctrl_2_L']):  
                                        if prop_fing == 1:
                                            bone.layers[2] = 1                                            
                                            for pbone in p_bones:
                                                if (pbone.name in b['bones_fingers_ctrl_2_L']):
                                                    for C in pbone.constraints:
                                                        if C.type == 'IK':
                                                            C.mute = False           
                                        else:
                                            bone.layers[2] = 0  
                                            for pbone in p_bones:
                                                if (pbone.name in b['bones_fingers_ctrl_2_L']):
                                                    for C in pbone.constraints:
                                                        if C.type == 'IK':
                                                            C.mute = True                                                                                    
                        #Toes_L
                        if ('L' in b.name):
                            if ('leg'in b.name):
                                prop_toes = int(b.toggle_toes)
                                for bone in arm.bones:         
                                    if (bone.name in b['bones_toes_def_1_L']): 
                                        if prop_toes == 1:
                                            bone.layers[15] = 1
                                        else:
                                            bone.layers[15] = 0 
                                    if (bone.name in b['bones_toes_def_2_L']): 
                                        if prop_toes == 1:
                                            bone.layers[15] = 1
                                            bone.layers[31] = 1                                                
                                        else:
                                            bone.layers[15] = 0    
                                            bone.layers[31] = 0                                                                                       
                                    if (bone.name in b['bones_no_toes_def_L']): 
                                        if prop_toes == 1:
                                            bone.layers[15] = 0
                                        else:
                                            bone.layers[15] = 1   
                                    if (bone.name in b['bones_toes_str_L']):   
                                        if prop_toes == 1:
                                            bone.layers[31] = 1
                                        else:
                                            bone.layers[31] = 0                                                                                          
                                    if (bone.name in b['bones_toes_ctrl_1_L']): 
                                        if prop_toes == 1:
                                            bone.layers[0] = 1
                                        else:
                                            bone.layers[0] = 0     
                                    if (bone.name in b['bones_no_toes_ctrl_L']): 
                                        if prop_toes == 1:
                                            bone.layers[0] = 0
                                        else:
                                            bone.layers[0] = 1                                                                                       
                                    if (bone.name in b['bones_toes_ctrl_2_L']): 
                                        if prop_toes == 1:
                                            bone.layers[2] = 1                                            
                                            for pbone in p_bones:
                                                if (pbone.name in b['bones_toes_ctrl_2_L']):
                                                    for C in pbone.constraints:
                                                        if C.type == 'IK':
                                                            C.mute = False           
                                        else:
                                            bone.layers[2] = 0  
                                            for pbone in p_bones:
                                                if (pbone.name in b['bones_toes_ctrl_2_L']):
                                                    for C in pbone.constraints:
                                                        if C.type == 'IK':
                                                            C.mute = True                                                                                    

                        # Right Properties
                        #Fingers_R 
                        if ('R' in b.name):
                            if ('arm'in b.name):
                                prop_fing = int(b.toggle_fingers)
                                for bone in arm.bones:         
                                    if (bone.name in b['bones_fingers_def_1_R']):   
                                        if prop_fing == 1:
                                            bone.layers[15] = 1
                                        else:
                                            bone.layers[15] = 0
                                    if (bone.name in b['bones_fingers_def_2_R']):   
                                        if prop_fing == 1:
                                            bone.layers[15] = 1
                                            bone.layers[31] = 1                                                
                                        else:
                                            bone.layers[15] = 0
                                            bone.layers[31] = 0                                                
                                    if (bone.name in b['bones_fingers_str_R']):   
                                        if prop_fing == 1:
                                            bone.layers[31] = 1
                                        else:
                                            bone.layers[31] = 0                                                                                            
                                    if (bone.name in b['bones_fingers_ctrl_1_R']):  
                                        if prop_fing == 1:
                                            bone.layers[0] = 1
                                        else:
                                            bone.layers[0] = 0                                                
                                    if (bone.name in b['bones_fingers_ctrl_2_R']):  
                                        if prop_fing == 1:
                                            bone.layers[2] = 1                                            
                                            for pbone in p_bones:
                                                if (pbone.name in b['bones_fingers_ctrl_2_R']):
                                                    for C in pbone.constraints:
                                                        if C.type == 'IK':
                                                            C.mute = False           
                                        else:
                                            bone.layers[2] = 0  
                                            for pbone in p_bones:
                                                if (pbone.name in b['bones_fingers_ctrl_2_R']):
                                                    for C in pbone.constraints:
                                                        if C.type == 'IK':
                                                            C.mute = True                                                                                     
                        #Toes_R
                        if ('R' in b.name):
                            if ('leg'in b.name):
                                prop_toes = int(b.toggle_toes)
                                for bone in arm.bones:         
                                    if (bone.name in b['bones_toes_def_1_R']): 
                                        if prop_toes == 1:
                                            bone.layers[15] = 1
                                        else:
                                            bone.layers[15] = 0
                                    if (bone.name in b['bones_toes_def_2_R']): 
                                        if prop_toes == 1:
                                            bone.layers[15] = 1
                                            bone.layers[31] = 1
                                        else:
                                            bone.layers[15] = 0
                                            bone.layers[31] = 0                                          
                                    if (bone.name in b['bones_no_toes_def_R']): 
                                        if prop_toes == 1:
                                            bone.layers[15] = 0
                                        else:
                                            bone.layers[15] = 1      
                                    if (bone.name in b['bones_toes_str_R']):   
                                        if prop_toes == 1:
                                            bone.layers[31] = 1
                                        else:
                                            bone.layers[31] = 0                                                                                        
                                    if (bone.name in b['bones_toes_ctrl_1_R']): 
                                        if prop_toes == 1:
                                            bone.layers[0] = 1
                                        else:
                                            bone.layers[0] = 0     
                                    if (bone.name in b['bones_no_toes_ctrl_R']): 
                                        if prop_toes == 1:
                                            bone.layers[0] = 0
                                        else:
                                            bone.layers[0] = 1                                                                                       
                                    if (bone.name in b['bones_toes_ctrl_2_R']): 
                                        if prop_toes == 1:
                                            bone.layers[2] = 1                                            
                                            for pbone in p_bones:
                                                if (pbone.name in b['bones_toes_ctrl_2_R']):
                                                    for C in pbone.constraints:
                                                        if C.type == 'IK':
                                                            C.mute = False           
                                        else:
                                            bone.layers[2] = 0  
                                            for pbone in p_bones:
                                                if (pbone.name in b['bones_toes_ctrl_2_R']):
                                                    for C in pbone.constraints:
                                                        if C.type == 'IK':
                                                            C.mute = True                                                                                    

 
           
######### Update Function for Properties ##########

def prop_update(self, context):
    bone_auto_hide(context)

def reprop_update(self, context):
    reproportion_toggle(context)
    
def rig_toggles_update(self, context):
    rig_toggles(context)
                    
######### Hanlder for update on load and frame change #########

from bpy.app.handlers import persistent

@persistent
def load_handler(context):  
    bone_auto_hide(context)       

bpy.app.handlers.load_post.append(load_handler)
bpy.app.handlers.frame_change_post.append(load_handler)

@persistent
def load_reproportion_handler(context):
    reproportion_toggle(context)

bpy.app.handlers.load_post.append(load_reproportion_handler)


######### Properties Creation ############

#FK/IK

bpy.types.PoseBone.ik_head = FloatProperty(
    default=0.000,
    min=0.000,
    max=1.000,
    precision=0,
    step=100,   
    options={'ANIMATABLE'},
    description="IK/FK Toggle",
    update=prop_update,
    name="ik_head"
)

bpy.types.PoseBone.ik_torso = FloatProperty(
    default=0.000,
    min=0.000,
    max=1.000,
    precision=0,
    step=100,
    options={'ANIMATABLE'},
    description="IK/FK Toggle",
    update=prop_update,
    name="ik_torso"
)
bpy.types.PoseBone.inv_torso = FloatProperty(
    default=0.000,
    min=0.000,
    max=1.000,
    precision=0,
    step=100,   
    options={'ANIMATABLE'},
    description="Invert Torso Hierarchy",
    update=prop_update,
    name="inv_torso"
)
bpy.types.PoseBone.ik_arm_L = FloatProperty(
    default=0.000,
    min=0.000,
    max=1.000,
    precision=0,
    step=100,   
    options={'ANIMATABLE'},
    description="IK/FK Toggle",
    update=prop_update,
    name="ik_arm_L"
)
bpy.types.PoseBone.ik_arm_R = FloatProperty(
    default=0.000,
    min=0.000,
    max=1.000,
    precision=0,
    step=100,   
    options={'ANIMATABLE'},
    description="IK/FK Toggle",
    update=prop_update,
    name="ik_arm_R"
)
bpy.types.PoseBone.ik_leg_L = FloatProperty(
    default=0.000,
    min=0.000,
    max=1.000,
    precision=0,
    step=100,   
    options={'ANIMATABLE'},
    description="IK/FK Toggle",
    update=prop_update,
    name="ik_leg_L"
)
bpy.types.PoseBone.ik_toes_all_L = FloatProperty(
    default=0.000,
    min=0.000,
    max=1.000,
    precision=0,
    step=100,   
    options={'ANIMATABLE'},
    description="IK/FK Toggle",
    update=prop_update,
    name="ik_toes_all_L"
)
bpy.types.PoseBone.ik_leg_R = FloatProperty(
    default=0.000,
    min=0.000,
    max=1.000,
    precision=0,
    step=100,   
    options={'ANIMATABLE'},
    description="IK/FK Toggle",
    update=prop_update,
    name="ik_leg_R"
)
bpy.types.PoseBone.ik_toes_all_R = FloatProperty(
    default=0.000,
    min=0.000,
    max=1.000,
    precision=0,
    step=100,   
    options={'ANIMATABLE'},
    description="IK/FK Toggle",
    update=prop_update,
    name="ik_toes_all_R"
)
bpy.types.PoseBone.ik_fing_ind_L = FloatProperty(
    default=0.000,
    min=0.000,
    max=1.000,
    precision=0,
    step=100,   
    options={'ANIMATABLE'},
    description="IK/FK Toggle",
    update=prop_update,
    name="ik_fing_ind_L"
)
bpy.types.PoseBone.ik_fing_mid_L = FloatProperty(
    default=0.000,
    min=0.000,
    max=1.000,
    precision=0,
    step=100,   
    options={'ANIMATABLE'},
    description="IK/FK Toggle",
    update=prop_update,
    name="ik_fing_mid_L"
)
bpy.types.PoseBone.ik_fing_ring_L = FloatProperty(
    default=0.000,
    min=0.000,
    max=1.000,
    precision=0,
    step=100,   
    options={'ANIMATABLE'},
    description="IK/FK Toggle",
    update=prop_update,
    name="ik_fing_mid_L"
)
bpy.types.PoseBone.ik_fing_lit_L = FloatProperty(
    default=0.000,
    min=0.000,
    max=1.000,
    precision=0,
    step=100,   
    options={'ANIMATABLE'},
    description="IK/FK Toggle",
    update=prop_update,
    name="ik_fing_lit_L"
)
bpy.types.PoseBone.ik_fing_thumb_L = FloatProperty(
    default=0.000,
    min=0.000,
    max=1.000,
    precision=0,
    step=100,   
    options={'ANIMATABLE'},
    description="IK/FK Toggle",
    update=prop_update,
    name="ik_fing_thumb_L"
)
bpy.types.PoseBone.ik_fing_ind_R = FloatProperty(
    default=0.000,
    min=0.000,
    max=1.000,
    precision=0,
    step=100,   
    options={'ANIMATABLE'},
    description="IK/FK Toggle",
    update=prop_update,
    name="ik_fing_ind_R"
)
bpy.types.PoseBone.ik_fing_mid_R = FloatProperty(
    default=0.000,
    min=0.000,
    max=1.000,
    precision=0,
    step=100,   
    options={'ANIMATABLE'},
    description="IK/FK Toggle",
    update=prop_update,
    name="ik_fing_mid_R"
)
bpy.types.PoseBone.ik_fing_ring_R = FloatProperty(
    default=0.000,
    min=0.000,
    max=1.000,
    precision=0,
    step=100,   
    options={'ANIMATABLE'},
    description="IK/FK Toggle",
    update=prop_update,
    name="ik_fing_mid_R"
)
bpy.types.PoseBone.ik_fing_lit_R = FloatProperty(
    default=0.000,
    min=0.000,
    max=1.000,
    precision=0,
    step=100,   
    options={'ANIMATABLE'},
    description="IK/FK Toggle",
    update=prop_update,
    name="ik_fing_lit_R"
)
bpy.types.PoseBone.ik_fing_thumb_R = FloatProperty(
    default=0.000,
    min=0.000,
    max=1.000,
    precision=0,
    step=100,   
    options={'ANIMATABLE'},
    description="IK/FK Toggle",
    update=prop_update,
    name="ik_fing_thumb_R"
)
bpy.types.PoseBone.ik_fing_all_R = FloatProperty(
    default=0.000,
    min=0.000,
    max=1.000,
    precision=0,
    step=100,   
    options={'ANIMATABLE'},
    description="IK/FK Toggle",
    update=prop_update,
    name="ik_fing_all_R"
)
bpy.types.PoseBone.ik_fing_all_L = FloatProperty(
    default=0.000,
    min=0.000,
    max=1.000,
    precision=0,
    step=100,   
    options={'ANIMATABLE'},
    description="IK/FK Toggle",
    update=prop_update,
    name="ik_fing_all_L"
)

# HINGE

bpy.types.PoseBone.hinge_head = FloatProperty(
    default=0.000,
    min=0.000,
    max=1.000,
    precision=0,
    step=100,   
    options={'ANIMATABLE'},
    description="Isolate Rotation",
    update=prop_update,
    name="hinge_head"
)
bpy.types.PoseBone.hinge_neck = FloatProperty(
    default=0.000,
    min=0.000,
    max=1.000,
    precision=0,
    step=100,   
    options={'ANIMATABLE'},
    description="Isolate Rotation",
    update=prop_update,
    name="hinge_neck"
)
bpy.types.PoseBone.hinge_arm_L = FloatProperty(
    default=0.000,
    min=0.000,
    max=1.000,
    precision=0,
    step=100,   
    options={'ANIMATABLE'},
    description="Isolate Rotation",
    update=prop_update,
    name="hinge_arm_L"
)
bpy.types.PoseBone.hinge_arm_R = FloatProperty(
    default=0.000,
    min=0.000,
    max=1.000,
    precision=0,
    step=100,   
    options={'ANIMATABLE'},
    description="Isolate Rotation",
    update=prop_update,
    name="hinge_arm_R"
)
bpy.types.PoseBone.hinge_hand_L = FloatProperty(
    default=0.000,
    min=0.000,
    max=1.000,
    precision=0,
    step=100,   
    options={'ANIMATABLE'},
    description="Isolate Rotation",
    update=prop_update,
    name="hinge_hand_L"
)
bpy.types.PoseBone.hinge_hand_R = FloatProperty(
    default=0.000,
    min=0.000,
    max=1.000,
    precision=0,
    step=100,   
    options={'ANIMATABLE'},
    description="Isolate Rotation",
    update=prop_update,
    name="hinge_hand_R"
)
bpy.types.PoseBone.hinge_fing_ind_L = FloatProperty(
    default=0.000,
    min=0.000,
    max=1.000,
    precision=0,
    step=100,   
    options={'ANIMATABLE'},
    description="Isolate Rotation",
    update=prop_update,
    name="hinge_fing_ind_L"
)
bpy.types.PoseBone.hinge_fing_mid_L = FloatProperty(
    default=0.000,
    min=0.000,
    max=1.000,
    precision=0,
    step=100,   
    options={'ANIMATABLE'},
    description="Isolate Rotation",
    update=prop_update,
    name="hinge_fing_mid_L"
)
bpy.types.PoseBone.hinge_fing_ring_L = FloatProperty(
    default=0.000,
    min=0.000,
    max=1.000,
    precision=0,
    step=100,   
    options={'ANIMATABLE'},
    description="Isolate Rotation",
    update=prop_update,
    name="hinge_fing_mid_L"
)
bpy.types.PoseBone.hinge_fing_lit_L = FloatProperty(
    default=0.000,
    min=0.000,
    max=1.000,
    precision=0,
    step=100,   
    options={'ANIMATABLE'},
    description="Isolate Rotation",
    update=prop_update,
    name="hinge_fing_lit_L"
)
bpy.types.PoseBone.hinge_fing_thumb_L = FloatProperty(
    default=0.000,
    min=0.000,
    max=1.000,
    precision=0,
    step=100,   
    options={'ANIMATABLE'},
    description="Isolate Rotation",
    update=prop_update,
    name="hinge_fing_thumb_L"
)
bpy.types.PoseBone.hinge_fing_ind_R = FloatProperty(
    default=0.000,
    min=0.000,
    max=1.000,
    precision=0,
    step=100,   
    options={'ANIMATABLE'},
    description="Isolate Rotation",
    update=prop_update,
    name="hinge_fing_ind_R"
)
bpy.types.PoseBone.hinge_fing_mid_R = FloatProperty(
    default=0.000,
    min=0.000,
    max=1.000,
    precision=0,
    step=100,   
    options={'ANIMATABLE'},
    description="Isolate Rotation",
    update=prop_update,
    name="hinge_fing_mid_R"
)
bpy.types.PoseBone.hinge_fing_ring_R = FloatProperty(
    default=0.000,
    min=0.000,
    max=1.000,
    precision=0,
    step=100,   
    options={'ANIMATABLE'},
    description="Isolate Rotation",
    update=prop_update,
    name="hinge_fing_mid_R"
)
bpy.types.PoseBone.hinge_fing_lit_R = FloatProperty(
    default=0.000,
    min=0.000,
    max=1.000,
    precision=0,
    step=100,   
    options={'ANIMATABLE'},
    description="Isolate Rotation",
    update=prop_update,
    name="hinge_fing_lit_R"
)
bpy.types.PoseBone.hinge_fing_thumb_R = FloatProperty(
    default=0.000,
    min=0.000,
    max=1.000,
    precision=0,
    step=100,   
    options={'ANIMATABLE'},
    description="Isolate Rotation",
    update=prop_update,
    name="hinge_fing_thumb_R"
)
bpy.types.PoseBone.hinge_fing_all_R = FloatProperty(
    default=0.000,
    min=0.000,
    max=1.000,
    precision=0,
    step=100,   
    options={'ANIMATABLE'},
    description="Isolate Rotation",
    update=prop_update,
    name="hinge_fing_all_R"
)
bpy.types.PoseBone.hinge_fing_all_L = FloatProperty(
    default=0.000,
    min=0.000,
    max=1.000,
    precision=0,
    step=100,   
    options={'ANIMATABLE'},
    description="Isolate Rotation",
    update=prop_update,
    name="hinge_fing_all_L"
)
bpy.types.PoseBone.hinge_leg_L = FloatProperty(
    default=0.000,
    min=0.000,
    max=1.000,
    precision=0,
    step=100,   
    options={'ANIMATABLE'},
    description="Isolate Rotation",
    update=prop_update,
    name="hinge_leg_L"
)
bpy.types.PoseBone.hinge_toes_all_L = FloatProperty(
    default=0.000,
    min=0.000,
    max=1.000,
    precision=0,
    step=100,   
    options={'ANIMATABLE'},
    description="Isolate Rotation",
    update=prop_update,
    name="hinge_toes_all_L"
)
bpy.types.PoseBone.hinge_leg_R = FloatProperty(
    default=0.000,
    min=0.000,
    max=1.000,
    precision=0,
    step=100,   
    options={'ANIMATABLE'},
    description="Isolate Rotation",
    update=prop_update,
    name="hinge_leg_R"
)           
bpy.types.PoseBone.hinge_toes_all_R = FloatProperty(
    default=0.000,
    min=0.000,
    max=1.000,
    precision=0,
    step=100,   
    options={'ANIMATABLE'},
    description="Isolate Rotation",
    update=prop_update,
    name="hinge_toes_all_R"
)

#Stretchy IK

bpy.types.PoseBone.toon_head = FloatProperty(
    default=0.000,
    min=0.000,
    max=1.000,
    precision=0,
    step=100,   
    options={'ANIMATABLE'},
    description="Stretchy IK Toggle",
    update=prop_update,
    name="toon_head"
)   

bpy.types.PoseBone.toon_torso = FloatProperty(
    default=0.000,
    min=0.000,
    max=1.000,
    precision=0,
    step=100,   
    options={'ANIMATABLE'},
    description="Stretchy IK Toggle",
    update=prop_update,
    name="toon_torso"
) 

bpy.types.PoseBone.toon_arm_L = FloatProperty(
    default=0.000,
    min=0.000,
    max=1.000,
    precision=0,
    step=100,   
    options={'ANIMATABLE'},
    description="Stretchy IK Toggle",
    update=prop_update,
    name="toon_arm_L"
) 

bpy.types.PoseBone.toon_arm_R = FloatProperty(
    default=0.000,
    min=0.000,
    max=1.000,
    precision=0,
    step=100,   
    options={'ANIMATABLE'},
    description="Stretchy IK Toggle",
    update=prop_update,
    name="toon_arm_R"
) 

bpy.types.PoseBone.toon_leg_L = FloatProperty(
    default=0.000,
    min=0.000,
    max=1.000,
    precision=0,
    step=100,   
    options={'ANIMATABLE'},
    description="Stretchy IK Toggle",
    update=prop_update,
    name="toon_leg_L"
) 

bpy.types.PoseBone.toon_leg_R = FloatProperty(
    default=0.000,
    min=0.000,
    max=1.000,
    precision=0,
    step=100,   
    options={'ANIMATABLE'},
    description="Stretchy IK Toggle",
    update=prop_update,
    name="toon_leg_R"
) 

# LOOK SWITCH
bpy.types.PoseBone.look_switch = FloatProperty(
    default=3.000,
    min=0.000,
    max=3.000,
    precision=0,
    step=100,   
    options={'ANIMATABLE'},
    description="Target of Eyes",
    update=prop_update,
    name="look_switch"
) 

# REPROPORTION
bpy.types.Armature.reproportion = BoolProperty(
    default=0,
    description="Toggle Reproportion Mode",
    update=reprop_update,
    name="reproportion"
) 

# TOGGLES
bpy.types.PoseBone.toggle_fingers = BoolProperty(
    default=0,
    description="Toggle fingers in rig",
    update=rig_toggles_update,
    name="toggle_fingers"
) 

bpy.types.PoseBone.toggle_toes = BoolProperty(
    default=0,
    description="Toggle toes in rig",
    update=rig_toggles_update,
    name="toggle_toes"
) 

########### User interface
class BlenRig_5_Interface(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_label = 'BlenRig 5 Controls (V 216)'
    bl_category = "BlenRig 5"
    
    @classmethod
    def poll(cls, context):
        if not bpy.context.active_object:
            return False
        if (bpy.context.active_object.type in ["ARMATURE"]):
            return True
        if (bpy.context.active_object.type in ["MESH"]):
            for mod in bpy.context.active_object.modifiers:          
                if (mod.type in ["ARMATURE", "MESH_DEFORM"]):
                    return True
        if (bpy.context.active_object.type in ["LATTICE", "CURVE"]):
            for mod in bpy.context.active_object.modifiers:          
                if (mod.type in ["HOOK"]):
                    return True                


    def draw(self, context):
        global all_bones, hand_l, hand_r, arm_l, arm_r, leg_l, leg_r, foot_l, foot_r, head, torso
        if not bpy.context.active_object:
            return False  
        layout = self.layout
        props = context.window_manager.blenrig_5_props      
        if (bpy.context.active_object.type in ["ARMATURE"]) and (bpy.context.active_object.mode == 'POSE'):         
            arm = bpy.context.active_object.data
            armobj = bpy.context.active_object
            arm_bones = bpy.context.active_object.pose.bones     
            act_bone = bpy.context.active_pose_bone   

        
        try:
            selected_bones = [bone.name for bone in bpy.context.selected_pose_bones]
        except:
            selected_bones = []
        try:
            blenrig_5 = bpy.context.active_object.data["rig_name"]==rig_name
        except:
            blenrig_5 = False
        
        def is_selected(names):
            for name in names:
                if name in selected_bones:
                    return True
            return False
        
        if bpy.context.mode=="POSE" and blenrig_5:
            
######### Bone groups used for Inherit Scale Checkboxes & Sensible to Selection Sliders Display
            if not all_bones:
                all_bones = []
                for bone in armobj.pose.bones:
                     all_bones.append(bone.name)

                hand_l=[]
                for bone in all_bones[:]:
                    if bone.count("_L"):
                        if bone.count("fing"):
                            hand_l.append(bone)
                hand_r=[]
                for bone in all_bones[:]:
                    if bone.count ("_R"):
                        if bone.count("fing"):
                            hand_r.append(bone)
                  
                arm_l=[]
                for bone in all_bones[:]:
                    if bone.count ("_L"):
                        if bone.count("arm") or bone.count("elbow") or bone.count("shoulder") or bone.count("hand") or bone.count("wrist"):
                            arm_l.append(bone)

                arm_r=[]
                for bone in all_bones[:]:
                    if bone.count ("_R"):
                        if bone.count("arm") or bone.count("elbow") or bone.count("shoulder") or bone.count("hand") or bone.count("wrist"):
                            arm_r.append(bone)

                leg_l=[]
                for bone in all_bones[:]:
                    if bone.count ("_L"):
                        if bone.count("butt") or bone.count("knee") or bone.count("thigh") or bone.count("shin"):
                            leg_l.append(bone)

                leg_r=[]
                for bone in all_bones[:]:
                    if bone.count ("_R"):
                        if bone.count("butt") or bone.count("knee") or bone.count("thigh") or bone.count("shin"):
                            leg_r.append(bone)

                foot_l=[]
                for bone in all_bones[:]:
                    if bone.count ("_L"):
                        if bone.count("toe") or bone.count("foot") or bone.count("heel") or bone.count("sole") or bone.count("floor"):
                            foot_l.append(bone)

                foot_r=[]
                for bone in all_bones[:]:
                    if bone.count ("_R"):
                        if bone.count("toe") or bone.count("foot") or bone.count("heel") or bone.count("sole") or bone.count("floor"):
                            foot_r.append(bone)

                head=[]
                for bone in all_bones[:]:
                    if bone.count("look") or bone.count("head") or bone.count("neck") or bone.count("maxi") or bone.count("cheek") or bone.count("chin") or bone.count("lip") or bone.count("ear_") or bone.count("tongue") or bone.count("eyelid") or bone.count("forehead") or bone.count("brow") or bone.count("nose") or bone.count("nostril") or bone.count("mouth") or bone.count("eye") or bone.count("gorro") or bone.count("teeth") or bone.count("hat") or bone.count("glasses") or bone.count("anteojos") or bone.count("hair") or bone.count("pelo"):
                        head.append(bone)

                torso=['master']
                for bone in all_bones[:]:
                    if bone.count("spine") or bone.count("pelvis") or bone.count("torso") or bone.count("omoplate") or bone.count("chest") or bone.count("body") or bone.count("ball") or bone.count("dicky") or bone.count("butt") or bone.count("back") or bone.count("clavi") or bone.count("look") or bone.count("hip"):
                        torso.append(bone)

########### PANEL #############################################################################            

########### Armature Layers
            if "gui_layers" in arm:
                box = layout.column()
                col = box.column()           
                row = col.row()
            if "gui_layers" in arm and arm["gui_layers"]:
                row.operator("gui.blenrig_5_tabs", icon="DOWNARROW_HLT", emboss = 0).tab = "gui_layers"         
                row.label(text="ARMATURE LAYERS", icon='RENDERLAYERS')
                # expanded box
                col.separator()
                col2 = box.column(align = 1)
                
                row_props = col2.row(align = 0)
                row_props.scale_y = 0.75  
                row_props.scale_x = 1                     
                row_props.alignment = 'LEFT'           
                row_props.prop(arm, '["layers_count"]', "Layers", toggle=True)
                if arm['bone_auto_hide'] == 1:
                    row_props.operator("gui.blenrig_5_tabs",text = "  Bone Auto Hiding", icon="CHECKBOX_HLT", emboss = 0).tab = "bone_auto_hide"   
                else:
                    row_props.operator("gui.blenrig_5_tabs",text = "  Bone Auto Hiding", icon="CHECKBOX_DEHLT", emboss = 0).tab = "bone_auto_hide"                                               
                col2.separator()                
                
                row_layers = col2.row(align = 1)
                
                for l_prop in arm.items():
                    if l_prop[0] == "layers_count":
                        layer_number = l_prop[1]
                for prop in arm.items():                        
                    if prop[0] == "layers_list":
                                                                                                                                       
                        col_1 = row_layers.column(align = 0)               
                        col_1.scale_y = 0.75               
                        col_1.prop(arm, "layers", index=0 , toggle=True, text ='{}'.format(prop[1][0]))
                        if layer_number > 3:
                            col_1.prop(arm, "layers", index=3, toggle=True, text='{}'.format(prop[1][3]))  
                        if layer_number > 6:                            
                            col_1.prop(arm, "layers", index=6, toggle=True, text='{}'.format(prop[1][6]))  
                        if layer_number > 9:                            
                            col_1.prop(arm, "layers", index=17, toggle=True, text='{}'.format(prop[1][9]))     
                        if layer_number > 12:                            
                            col_1.prop(arm, "layers", index=20, toggle=True, text='{}'.format(prop[1][12]))    
                        if layer_number > 15:                            
                            col_1.prop(arm, "layers", index=23, toggle=True, text='{}'.format(prop[1][15]))  
                        if layer_number > 18:                            
                            col_1.prop(arm, "layers", index=10, toggle=True, text='{}'.format(prop[1][18]))  
                        if layer_number > 21:                            
                            col_1.prop(arm, "layers", index=13, toggle=True, text='{}'.format(prop[1][21]))     
                        if layer_number > 24:                            
                            col_1.prop(arm, "layers", index=24, toggle=True, text='{}'.format(prop[1][24]))   
                        if layer_number > 27:                            
                            col_1.prop(arm, "layers", index=27, toggle=True, text='{}'.format(prop[1][27]))   
                        if layer_number > 30:                            
                            col_1.prop(arm, "layers", index=30, toggle=True, text='{}'.format(prop[1][30]))                                                                                                                                                                                                                                     

                        col_2 = row_layers.column(align = 0)                                                             
                        col_2.scale_y = 0.75     
                        if layer_number > 1:                                  
                            col_2.prop(arm, "layers", index=1, toggle=True, text='{}'.format(prop[1][1]))  
                        if layer_number > 4:                            
                            col_2.prop(arm, "layers", index=4, toggle=True, text='{}'.format(prop[1][4]))  
                        if layer_number > 7:                            
                            col_2.prop(arm, "layers", index=7, toggle=True, text='{}'.format(prop[1][7]))   
                        if layer_number > 10:                            
                            col_2.prop(arm, "layers", index=18, toggle=True, text='{}'.format(prop[1][10]))  
                        if layer_number > 13:                            
                            col_2.prop(arm, "layers", index=21, toggle=True, text='{}'.format(prop[1][13]))    
                        if layer_number > 16:                            
                            col_2.prop(arm, "layers", index=8, toggle=True, text='{}'.format(prop[1][16]))      
                        if layer_number > 19:                            
                            col_2.prop(arm, "layers", index=11, toggle=True, text='{}'.format(prop[1][19]))      
                        if layer_number > 22:                            
                            col_2.prop(arm, "layers", index=14, toggle=True, text='{}'.format(prop[1][22]))     
                        if layer_number > 25:                            
                            col_2.prop(arm, "layers", index=25, toggle=True, text='{}'.format(prop[1][25]))     
                        if layer_number > 28:                            
                            col_2.prop(arm, "layers", index=28, toggle=True, text='{}'.format(prop[1][28]))    
                        if layer_number > 31:                           
                            col_2.prop(arm, "layers", index=31, toggle=True, text='{}'.format(prop[1][31]))                                                                                                                                                                                                                                                                                                                 

                        col_3 = row_layers.column(align = 0)                           
                        col_3.scale_y = 0.75    
                        if layer_number > 2:                                                                     
                            col_3.prop(arm, "layers", index=2 , toggle=True, text='{}'.format(prop[1][2]))  
                        if layer_number > 5:                                 
                            col_3.prop(arm, "layers", index=5 , toggle=True, text='{}'.format(prop[1][5]))  
                        if layer_number > 8:                                  
                            col_3.prop(arm, "layers", index=16 , toggle=True, text='{}'.format(prop[1][8]))  
                        if layer_number > 11:                                  
                            col_3.prop(arm, "layers", index=19 , toggle=True, text='{}'.format(prop[1][11]))  
                        if layer_number > 14:                                  
                            col_3.prop(arm, "layers", index=22 , toggle=True, text='{}'.format(prop[1][14]))  
                        if layer_number > 17:                                  
                            col_3.prop(arm, "layers", index=9 , toggle=True, text='{}'.format(prop[1][17]))  
                        if layer_number > 20:                                  
                            col_3.prop(arm, "layers", index=12 , toggle=True, text='{}'.format(prop[1][20]))  
                        if layer_number > 23:                                  
                            col_3.prop(arm, "layers", index=15 , toggle=True, text='{}'.format(prop[1][23]))  
                        if layer_number > 26:                                  
                            col_3.prop(arm, "layers", index=26 , toggle=True, text='{}'.format(prop[1][26]))  
                        if layer_number > 29:                                  
                            col_3.prop(arm, "layers", index=29 , toggle=True, text='{}'.format(prop[1][29]))                                                                                                                                                                                                                                                                                                                                               
                        col2.separator()   
             
                # collapsed box
            elif "gui_layers" in arm:
                row.operator("gui.blenrig_5_tabs", icon="RIGHTARROW", emboss = 0).tab = "gui_layers"
                row.label(text="ARMATURE LAYERS", icon='RENDER_RESULT')  

################# BLENRIG PICKER BODY #############################################
          
            if "gui_picker_body" in arm:  
                box = layout.column()
                col = box.column()
                row = col.row()   
                row.alignment = "LEFT"
            # expanded box            
            if "gui_picker_body" in arm and arm["gui_picker_body"]:
                row.operator("gui.blenrig_5_tabs", icon="DOWNARROW_HLT", emboss = 0).tab = "gui_picker_body"
                row.label(text="BLENRIG PICKER", icon='OUTLINER_OB_ARMATURE')

                row_props = col.row()
                row_props.alignment ='LEFT'
                row_props.prop(props, "gui_picker_body_props", text="PROPERTIES")

                # 3 Columns
                box_row = box.row()
                
                if props.gui_picker_body_props:
                    box_R = box_row.column(align = 1)
                    box_R.scale_x = 0.2
                    box_R.scale_y = 1 
                    box_R.alignment = 'LEFT'   
                        
                    box_body = box_row.column(align = 1)
                    
                    box_L = box_row.column(align = 1)
                    box_L.scale_x = 0.2
                    box_L.scale_y = 1   
                    box_L.alignment = 'RIGHT'            
                else:
                    box_body = box_row.column(align = 1)
                # Look slider
                
                if props.gui_picker_body_props:
                    row_look_title = box_body.row(align = 1)
                    row_look_title.scale_x = 0.7
                    row_look_title.scale_y = 1
                    row_look_title.alignment = 'CENTER'   
                          
                    row_label = row_look_title.row(align = 1)
                    row_label.scale_x = 1
                    row_label.scale_y = 1    
                    row_label.alignment = 'LEFT'                
                    row_label.label("Free")
                    
                    row_label = row_look_title.row(align = 1)
                    row_label.scale_x = 1
                    row_label.scale_y = 1    
                    row_label.alignment = 'CENTER'            
                    row_label.label("Body")
                    
                    row_label = row_look_title.row(align = 1)
                    row_label.scale_x = 1
                    row_label.scale_y = 1    
                    row_label.alignment = 'CENTER'            
                    row_label.label("Torso")         
                    
                    row_label = row_look_title.column(align = 1)  
                    row_label.scale_x = 1
                    row_label.scale_y = 1            
                    row_label.alignment = 'RIGHT'              
                    row_label.label("Head")
                  
                    row_look = box_body.row()
                    row_look.scale_x = 1
                    row_look.scale_y = 1
                    row_look.alignment = 'CENTER'           
                    row_look.prop(arm_bones['properties_head'], 'look_switch', "Eyes Target", slider=True)

                    col_space = box_body.column()  
                    col_space.scale_x = 1
                    col_space.scale_y = 4
                    col_space.separator() 
                else:  
                    col_space = box_body.column()  
                    col_space.scale_x = 1
                    col_space.scale_y = 10
                    col_space.separator() 

                # Head 

                col_head_main = box_body.column(align = 1)
                col_head_main.alignment = 'CENTER'
                
                col_toon = col_head_main.row()
                col_toon.scale_x = 0.5
                col_toon.scale_y = 0.5   
                col_toon.alignment = 'CENTER'         
                col_toon.operator("operator.head_stretch", text="", icon = "SPACE2", emboss = 0) 
                col_toon.operator("operator.head_toon", text="", icon = "SPACE3", emboss = 0) 
                
                row_head_main = col_head_main.row(align = 1)    
                row_head_main.alignment = 'CENTER'   
                      
                col_1 = row_head_main.column()     
                col_1.scale_x = 0.5
                col_1.scale_y = 0.5   
                col_1.alignment = 'CENTER'   
                col_1.operator("operator.head_top_ctrl", text="", icon = "SPACE2", emboss = 0) 
                col_1.operator("operator.head_mid_ctrl", text="", icon = "SPACE2", emboss = 0)  
                col_1.operator("operator.head_mid_curve", text="", icon = "SPACE2", emboss = 0) 
                col_1.operator("operator.mouth_str_ctrl", text="", icon = "SPACE2", emboss = 0)                   
                    
                col_2 = row_head_main.column(align = 1)    
                col_2.scale_x = 1
                col_2.scale_y = 1
                col_2.alignment = 'CENTER'  

                row_eyes = col_2.row() 
                row_eyes.scale_x = 1.1
                row_eyes.scale_y = 0.75 
                row_eyes.alignment = 'CENTER'                  
                box_eyes = row_eyes.box()     
                    
                row = box_eyes.row() 
                row.alignment = 'CENTER'

                col_eye_R = row.column() 
                col_eye_R.scale_x = 0.75
                col_eye_R.scale_y = 0.75   
                col_eye_R.alignment = 'CENTER'    
                col_eye_R.operator("operator.look_r", text="", icon="RESTRICT_VIEW_OFF") 

                col_look = row.column() 
                col_look.scale_x = 0.5
                col_look.scale_y = 1
                col_look.alignment = 'CENTER'
                col_look.operator("operator.look", text="") 

                col_eye_L = row.column() 
                col_eye_L.scale_x = 0.75
                col_eye_L.scale_y = 0.75             
                col_eye_L.alignment = 'CENTER'
                col_eye_L.operator("operator.look_l", text="", icon="RESTRICT_VIEW_OFF")  
                
                col_fk = col_2.row(align = 1)   
                col_fk.scale_x = 1.1
                col_fk.scale_y = 0.75  
                col_fk.alignment = 'CENTER'          
                col_fk.operator("operator.head_fk", text="Head FK") 
                      
                col_ik = col_2.row(align = 1)   
                col_ik.scale_x = 1.15
                col_ik.scale_y = 0.75   
                col_ik.alignment = 'CENTER'         
                col_ik.operator("operator.head_ik_ctrl", text="Head IK") 
                    
                col_toon = col_2.row(align = 1)   
                col_toon.scale_x = 1
                col_toon.scale_y = 0.15
                col_toon.alignment = 'CENTER'           
                col_toon.operator("operator.neck_4_toon", text="", icon = "SPACE2", emboss = 0)  
                                      
                col_3 = row_head_main.column()     
                col_3.scale_x = 0.5
                col_3.scale_y = 0.5   
                col_3.alignment = 'CENTER'   
                col_3.operator("operator.face_toon_up", text="", icon = "SPACE3", emboss = 0) 
                col_3.operator("operator.face_toon_mid", text="", icon = "SPACE3", emboss = 0)  
                col_3.operator("operator.face_toon_low", text="", icon = "SPACE3", emboss = 0)          
                      
                # Neck
                  
                row_neck_main = box_body.row(align = 1) 
                row_neck_main.scale_x = 0.75
                row_neck_main.scale_y = 1
                row_neck_main.alignment = 'CENTER'          
                
                col_neck_fk = row_neck_main.column(align = 1)      
                col_neck_fk.scale_x = 1
                col_neck_fk.scale_y = 1
                col_neck_fk.alignment = 'CENTER'  
                      
                row_neck_1 = col_neck_fk.row(align = 0)   
                row_neck_1.scale_x = 1
                row_neck_1.scale_y = 0.35
                row_neck_1.alignment = 'CENTER'          
                row_neck_1.operator("operator.neck_3", text="") 

                col_toon_2 = col_neck_fk.row(align = 1)   
                col_toon_2.scale_x = 1
                col_toon_2.scale_y = 0.15
                col_toon_2.alignment = 'CENTER'          
                col_toon_2.operator("operator.neck_3_toon", text="", icon = "SPACE2", emboss = 0)   
                
                row_neck_2 = col_neck_fk.row(align = 1)   
                row_neck_2.scale_x = 1
                row_neck_2.scale_y = 0.3
                row_neck_2.alignment = 'CENTER'          
                row_neck_2.operator("operator.neck_2", text="") 

                col_toon_3 = col_neck_fk.column(align = 1)   
                col_toon_3.scale_x = 1
                col_toon_3.scale_y = 0.15
                col_toon_3.alignment = 'CENTER'          
                col_toon_3.operator("operator.neck_2_toon", text="", icon = "SPACE2", emboss = 0)     
                
                row_neck_3 = col_neck_fk.row(align = 1)   
                row_neck_3.scale_x = 1
                row_neck_3.scale_y = 0.3
                row_neck_3.alignment = 'CENTER'          
                row_neck_3.operator("operator.neck_1", text="")  
                      
                row_ctrl = col_neck_fk.row(align = 1)      
                row_ctrl.scale_x = 1
                row_ctrl.scale_y = 0.5
                row_ctrl.alignment = 'CENTER'                                            
                row_ctrl.operator("operator.neck_ctrl", text="Neck Ctrl")   

                # Shoulders
              
                row_shoulder = box_body.row(align = 0)  

                col_2 = row_shoulder.row(align = 1)    
                col_2.scale_x = 0.95
                col_2.scale_y = 1
                col_2.alignment = 'CENTER'  
                
                row_shoulder_R = col_2.row(align = 1)   
                row_shoulder_R.scale_x = 1
                row_shoulder_R.scale_y = 0.75                
                row_shoulder_R.alignment = 'CENTER' 

                col_toon = row_shoulder_R.column(align = 1)
                col_toon.scale_x = 0.25
                col_toon.scale_y = 0.75
                col_toon.alignment = 'CENTER'           
                col_toon.operator("operator.clavi_toon_r", text = "", icon = "SPACE2", emboss = 0)
                
                col_ik = row_shoulder_R.column(align = 1)
                col_ik.scale_x = 0.75
                col_ik.scale_y = 0.75
                col_ik.alignment = 'CENTER'         
                col_ik.operator("operator.shoulder_rot_r", text="IK")         
                
                col_fk = row_shoulder_R.column(align = 1)
                col_fk.scale_x = 1
                col_fk.scale_y = 0.75
                col_fk.alignment = 'CENTER'         
                col_fk.operator("operator.shoulder_r", text="Shldr FK")

                row_neck_scale = col_2.row(align = 1)  
                row_neck_scale.scale_x = 1
                row_neck_scale.scale_y = 0.75
                row_neck_scale.alignment = 'CENTER' 
                row_neck_scale.operator("operator.head_scale", text = "", icon = "MAN_SCALE", emboss = 1)           

                row_shoulder_L = col_2.row(align = 1)  
                row_shoulder_L.scale_x = 1
                row_shoulder_L.scale_y = 0.75
                row_shoulder_L.alignment = 'CENTER' 
                      
                col_fk = row_shoulder_L.column(align = 1)
                col_fk.scale_x = 1
                col_fk.scale_y = 0.75
                col_fk.alignment = 'CENTER'         
                col_fk.operator("operator.shoulder_l", text="Shldr FK")
                
                col_ik = row_shoulder_L.column(align = 1)
                col_ik.scale_x = 0.75
                col_ik.scale_y = 0.75
                col_ik.alignment = 'CENTER'         
                col_ik.operator("operator.shoulder_rot_l", text="IK")
                
                col_toon = row_shoulder_L.column(align = 1)
                col_toon.scale_x = 0.25
                col_toon.scale_y = 0.75
                col_toon.alignment = 'CENTER'           
                col_toon.operator("operator.clavi_toon_l", text="", icon = "SPACE2", emboss = 0)          
                
                # Arm R
                if arm['rig_type'] == "Biped":                  
                    row_torso = box_body.row()
                    row_torso.scale_x = 1
                    row_torso.scale_y = 1
                    row_torso.alignment = 'CENTER'         
                    
                    col_arm_R = row_torso.row(align = 1)
                    col_arm_R.scale_x = 0.5
                    col_arm_R.scale_y = 1
                    col_arm_R.alignment = 'CENTER'   
                    
                    col_arm_toon_R = col_arm_R.column()
                    col_arm_toon_R.scale_x = 1
                    col_arm_toon_R.scale_y = 1
                    col_arm_toon_R.alignment = 'CENTER' 
                    col_arm_toon_R.separator()    
                    col_arm_toon_R.separator() 
                    col_arm_toon_R.separator()            
                    col_arm_toon_R.separator()         
                    col_arm_toon_R.separator()               
                    col_arm_toon_R.operator("operator.arm_toon_r", text="", icon = "SPACE2", emboss = 0)     
                    col_arm_toon_R.separator()  
                    col_arm_toon_R.separator()              
                    col_arm_toon_R.operator("operator.elbow_pole_r", text="", icon = "INLINK", emboss = 0)                 
                    col_arm_toon_R.separator()         
                    col_arm_toon_R.separator()        
                    col_arm_toon_R.separator()    
                    col_arm_toon_R.operator("operator.forearm_toon_r", text="", icon = "SPACE2", emboss = 0)               
                    
                    col_arm_main_R = col_arm_R.column(align = 1)
                    col_arm_main_R.scale_x = 1.2
                    col_arm_main_R.scale_y = 1
                    col_arm_main_R.alignment = 'CENTER'   
                    
                    col_arm_scale_R = col_arm_main_R.row(align = 1)
                    col_arm_scale_R.scale_x = 1.2
                    col_arm_scale_R.scale_y = 1
                    col_arm_scale_R.alignment = 'CENTER'   
                    col_arm_scale_R.operator("operator.arm_scale_r", text = "", icon = "MAN_SCALE", emboss = 1)    
                    
                    col_arm_fk_R = col_arm_main_R.row(align = 1)
                    col_arm_fk_R.scale_x = 1
                    col_arm_fk_R.scale_y = 2.5
                    col_arm_fk_R.alignment = 'CENTER'                                       
                    col_arm_fk_R.operator("operator.arm_fk_r", text="FK") 
                    
                    col_arm_ik_R = col_arm_main_R.row(align = 1)
                    col_arm_ik_R.scale_x = 1
                    col_arm_ik_R.scale_y = 1
                    col_arm_ik_R.alignment = 'CENTER'                                       
                    col_arm_ik_R.operator("operator.arm_ik_r", text="IK")      

                    col_elbow_toon_R = col_arm_main_R.column()
                    col_elbow_toon_R.scale_x = 1
                    col_elbow_toon_R.scale_y = 0.25
                    col_elbow_toon_R.alignment = 'CENTER'            
                    col_elbow_toon_R.operator("operator.elbow_toon_r", text="", icon = "SPACE2", emboss = 0)    
                    
                    col_forearm_fk_R = col_arm_main_R.row(align = 1)
                    col_forearm_fk_R.scale_x = 1
                    col_forearm_fk_R.scale_y = 3
                    col_forearm_fk_R.alignment = 'CENTER'                                       
                    col_forearm_fk_R.operator("operator.forearm_fk_r", text="FK")
                    
                    col_forearm_ik_R = col_arm_main_R.row(align = 1)
                    col_forearm_ik_R.scale_x = 1
                    col_forearm_ik_R.scale_y = 1
                    col_forearm_ik_R.alignment = 'CENTER'                                       
                    col_forearm_ik_R.operator("operator.forearm_ik_r", text="IK")   
                    
                    col_hand_toon_R = col_arm_main_R.column()
                    col_hand_toon_R.scale_x = 1
                    col_hand_toon_R.scale_y = 0.25
                    col_hand_toon_R.alignment = 'CENTER'             
                    col_hand_toon_R.operator("operator.hand_toon_r", text="", icon = "SPACE2", emboss = 0)                            

                # Arm R Quadruped
                
                if arm['rig_type'] == "Quadruped":    
                    row_torso = box_body.row()
                    row_torso.scale_x = 1
                    row_torso.scale_y = 1
                    row_torso.alignment = 'CENTER'                                  
                    col_arm_R = row_torso.row(align = 1)
                    col_arm_R.scale_x = 0.5
                    col_arm_R.scale_y = 1
                    col_arm_R.alignment = 'CENTER'   

                    
                    col_arm_toon_R = col_arm_R.column()
                    col_arm_toon_R.scale_x = 1
                    col_arm_toon_R.scale_y = 1
                    col_arm_toon_R.alignment = 'CENTER' 
                    col_arm_toon_R.separator()    
                    col_arm_toon_R.separator() 
                    col_arm_toon_R.separator()     
                    col_arm_toon_R.operator("operator.arm_toon_r", text="", icon = "SPACE2", emboss = 0)     
                    col_arm_toon_R.separator()    
                    col_arm_toon_R.separator() 
                    col_arm_toon_R.operator("operator.elbow_pole_r", text="", icon = "INLINK", emboss = 0)            
                    col_arm_toon_R.separator()           
                    col_arm_toon_R.operator("operator.forearm_toon_r", text="", icon = "SPACE2", emboss = 0)              
                    col_arm_toon_R.separator()    
                    col_arm_toon_R.separator()    
                    col_arm_toon_R.separator()                  
                    col_arm_toon_R.operator("operator.carpal_toon_r", text="", icon = "SPACE2", emboss = 0) 
                    
                    col_arm_main_R = col_arm_R.column(align = 1)
                    col_arm_main_R.scale_x = 1.2
                    col_arm_main_R.scale_y = 1
                    col_arm_main_R.alignment = 'CENTER'   
                    
                    col_arm_scale_R = col_arm_main_R.row(align = 1)
                    col_arm_scale_R.scale_x = 1.2
                    col_arm_scale_R.scale_y = 1
                    col_arm_scale_R.alignment = 'CENTER'   
                    col_arm_scale_R.operator("operator.arm_scale_r", text = "", icon = "MAN_SCALE", emboss = 1)    
                    
                    col_arm_fk_R = col_arm_main_R.row(align = 1)
                    col_arm_fk_R.scale_x = 1
                    col_arm_fk_R.scale_y = 1.5
                    col_arm_fk_R.alignment = 'CENTER'                                       
                    col_arm_fk_R.operator("operator.arm_fk_r", text="FK") 
                    
                    col_arm_ik_R = col_arm_main_R.row(align = 1)
                    col_arm_ik_R.scale_x = 1
                    col_arm_ik_R.scale_y = 1
                    col_arm_ik_R.alignment = 'CENTER'                                       
                    col_arm_ik_R.operator("operator.arm_ik_r", text="IK")      

                    col_elbow_toon_R = col_arm_main_R.column()
                    col_elbow_toon_R.scale_x = 1
                    col_elbow_toon_R.scale_y = 0.25
                    col_elbow_toon_R.alignment = 'CENTER'            
                    col_elbow_toon_R.operator("operator.elbow_toon_r", text="", icon = "SPACE2", emboss = 0)    
                    
                    col_forearm_fk_R = col_arm_main_R.row(align = 1)
                    col_forearm_fk_R.scale_x = 1
                    col_forearm_fk_R.scale_y = 1.5
                    col_forearm_fk_R.alignment = 'CENTER'                                       
                    col_forearm_fk_R.operator("operator.forearm_fk_r", text="FK")
                    
                    col_forearm_ik_R = col_arm_main_R.row(align = 1)
                    col_forearm_ik_R.scale_x = 1
                    col_forearm_ik_R.scale_y = 1
                    col_forearm_ik_R.alignment = 'CENTER'                                       
                    col_forearm_ik_R.operator("operator.forearm_ik_r", text="IK")   

                    col_ankle_toon_R = col_arm_main_R.column()
                    col_ankle_toon_R.scale_x = 1
                    col_ankle_toon_R.scale_y = 0.25
                    col_ankle_toon_R.alignment = 'CENTER'            
                    col_ankle_toon_R.operator("operator.ankle_toon_r", text="", icon = "SPACE2", emboss = 0)    
                    
                    col_carpal_fk_R = col_arm_main_R.row(align = 1)
                    col_carpal_fk_R.scale_x = 1
                    col_carpal_fk_R.scale_y = 1.5
                    col_carpal_fk_R.alignment = 'CENTER'                                       
                    col_carpal_fk_R.operator("operator.carpal_fk_r", text="FK")
                    
                    col_carpal_ik_R = col_arm_main_R.row(align = 1)
                    col_carpal_ik_R.scale_x = 1
                    col_carpal_ik_R.scale_y = 1
                    col_carpal_ik_R.alignment = 'CENTER'                                       
                    col_carpal_ik_R.operator("operator.carpal_ik_r", text="IK")   
                    
                    col_hand_toon_R = col_arm_main_R.column()
                    col_hand_toon_R.scale_x = 1
                    col_hand_toon_R.scale_y = 0.25
                    col_hand_toon_R.alignment = 'CENTER'             
                    col_hand_toon_R.operator("operator.hand_toon_r", text="", icon = "SPACE2", emboss = 0)                                               

                # Spine
                
                
                row_torso_main = row_torso.row(align = 1)
                row_torso_main.alignment = 'CENTER'
                row_torso_main.scale_x= 1
                row_torso_main.scale_y=1.0        
                
                col_torso = row_torso_main.column(align = 1)
                col_torso.alignment = 'CENTER'
                col_torso.scale_x= 1
                col_torso.scale_y=1.0

                col_spine_ctrl = col_torso.row(align = 0)  
                col_spine_ctrl.scale_x = 1.4
                col_spine_ctrl.scale_y = 0.75
                col_spine_ctrl.alignment = 'CENTER'                  
                col_spine_ctrl.operator("operator.torso_ctrl", text="Torso Ctrl")   

                col_spine_toon_4 = col_torso.row(align = 1)  
                col_spine_toon_4.scale_x = 1
                col_spine_toon_4.scale_y = 0.35
                col_spine_toon_4.alignment = 'CENTER'   
                col_spine_toon_4.operator("operator.spine_4_toon", text="", icon = "SPACE2", emboss = 0)   
                            
                col_spine_3 = col_torso.row(align = 1)  
                col_spine_3.scale_x = 1.5
                col_spine_3.scale_y = 0.75
                col_spine_3.alignment = 'CENTER'  
                col_spine_3.operator("operator.spine_3", text="Spine 3") 
                    
                prop_inv = int(bpy.context.active_object.pose.bones['properties_torso'].inv_torso)   
                if prop_inv == 1:      
                    col_spine_3_inv_ctrl = col_torso.row(align = 1)  
                    col_spine_3_inv_ctrl.scale_x = 0.95
                    col_spine_3_inv_ctrl.scale_y = 0.5
                    col_spine_3.scale_y = 0.5             
                    col_spine_3_inv_ctrl.alignment = 'CENTER'                                       
                    col_spine_3_inv_ctrl.operator("operator.spine_3_inv_ctrl", text="Spine 3 inv Ctrl") 
                
                col_spine_toon_3 = col_torso.row(align = 1)  
                col_spine_toon_3.scale_x = 1
                col_spine_toon_3.scale_y = 0.35
                col_spine_toon_3.alignment = 'CENTER'   
                col_spine_toon_3.operator("operator.spine_3_toon", text="", icon = "SPACE2", emboss = 0)
                    
                col_spine_2 = col_torso.row(align = 1)  
                col_spine_2.scale_x = 1.5
                col_spine_2.scale_y = 0.75
                col_spine_2.alignment = 'CENTER'                     
                col_spine_2.operator("operator.spine_2", text="Spine 2")
                
                col_spine_toon_2 = col_torso.row(align = 1)  
                col_spine_toon_2.scale_x = 1
                col_spine_toon_2.scale_y = 0.35
                col_spine_toon_2.alignment = 'CENTER'   
                col_spine_toon_2.operator("operator.spine_2_toon", text="", icon = "SPACE2", emboss = 0)
                    
                col_spine_1 = col_torso.row(align = 1)  
                col_spine_1.scale_x = 1.5
                col_spine_1.scale_y = 0.75
                col_spine_1.alignment = 'CENTER'                     
                col_spine_1.operator("operator.spine_1", text="Spine 1")      

                col_spine_toon_1 = col_torso.row(align = 1)  
                col_spine_toon_1.scale_x = 1
                col_spine_toon_1.scale_y = 0.25
                col_spine_toon_1.alignment = 'CENTER'   
                col_spine_toon_1.operator("operator.spine_1_toon", text="", icon = "SPACE2", emboss = 0)           

                if props.gui_picker_body_props:
                    col_torso_inv_props = col_torso.row(align = 0)  
                    col_torso_inv_props.scale_x = 1
                    col_torso_inv_props.scale_y = 0.75
                    col_torso_inv_props.alignment = 'CENTER' 
                    col_torso_inv_props.prop(arm_bones['properties_torso'], 'inv_torso', "Invert", toggle=True, icon_only = 1, emboss = 1)                                 

                    col_torso_props = col_torso.row(align = 0)  
                    col_torso_props.scale_x = 0.5
                    col_torso_props.scale_y = 0.75
                    col_torso_props.alignment = 'CENTER'             
                    col_torso_props.prop(arm_bones['properties_torso'], 'ik_torso', "IK/FK", toggle=True, icon_only = 1, emboss = 1)     
                    col_torso_props.prop(arm_bones['properties_torso'], 'toon_torso', "Str IK", toggle=True, icon_only = 1, emboss = 1)   

                    col_mstr_torso_pivot = col_torso.row(align = 1)  
                    col_mstr_torso_pivot.scale_x = 4
                    col_mstr_torso_pivot.scale_y = 0.4
                    col_mstr_torso_pivot.alignment = 'CENTER'                    
                    col_mstr_torso_pivot.operator("operator.master_torso_pivot_point", text="")
              
                    col_mstr_torso = col_torso.row(align = 1)  
                    col_mstr_torso.scale_x = 1.5
                    col_mstr_torso.scale_y = 1
                    col_mstr_torso.alignment = 'CENTER'                  
                    col_mstr_torso.operator("operator.master_torso", text="Mstr Torso")

                else:
                    col_mstr_torso_pivot = col_torso.row(align = 1)  
                    col_mstr_torso_pivot.scale_x = 4
                    col_mstr_torso_pivot.scale_y = 0.4
                    col_mstr_torso_pivot.alignment = 'CENTER'                    
                    col_mstr_torso_pivot.operator("operator.master_torso_pivot_point", text="")
              
                    col_mstr_torso = col_torso.row(align = 1)  
                    col_mstr_torso.scale_x = 1.5
                    col_mstr_torso.scale_y = 2.5
                    col_mstr_torso.alignment = 'CENTER'                  
                    col_mstr_torso.operator("operator.master_torso", text="Mstr Torso")           

                col_pelvis_toon = col_torso.row(align = 1)  
                col_pelvis_toon.scale_x = 1
                col_pelvis_toon.scale_y = 0.25
                col_pelvis_toon.alignment = 'CENTER'    
                col_pelvis_toon.operator("operator.pelvis_toon", text="", icon = "SPACE2", emboss = 0)            
                
                col_pelvis = col_torso.row(align = 0)  
                col_pelvis.scale_x = 1.8
                col_pelvis.scale_y = 1.5
                col_pelvis.alignment = 'CENTER'                  
                col_pelvis.operator("operator.pelvis_ctrl", text="Pelivs Ctrl")                                    
                
                # Arm L
                if arm['rig_type'] == "Biped":      
                    col_arm_L = row_torso.row(align = 1)
                    col_arm_L.scale_x = 0.5
                    col_arm_L.scale_y = 1
                    col_arm_L.alignment = 'CENTER'   
                    
                    col_arm_main_L = col_arm_L.column(align = 1)
                    col_arm_main_L.scale_x = 1.2
                    col_arm_main_L.scale_y = 1
                    col_arm_main_L.alignment = 'CENTER'   
                    
                    col_arm_scale_L = col_arm_main_L.row(align = 1)
                    col_arm_scale_L.scale_x = 1.2
                    col_arm_scale_L.scale_y = 1
                    col_arm_scale_L.alignment = 'CENTER'   
                    col_arm_scale_L.operator("operator.arm_scale_l", text = "", icon = "MAN_SCALE", emboss = 1)    
                    
                    col_arm_fk_L = col_arm_main_L.row(align = 1)
                    col_arm_fk_L.scale_x = 1
                    col_arm_fk_L.scale_y = 2.5
                    col_arm_fk_L.alignment = 'CENTER'                                       
                    col_arm_fk_L.operator("operator.arm_fk_l", text="FK") 
                    
                    col_arm_ik_L = col_arm_main_L.row(align = 1)
                    col_arm_ik_L.scale_x = 1
                    col_arm_ik_L.scale_y = 1
                    col_arm_ik_L.alignment = 'CENTER'                                       
                    col_arm_ik_L.operator("operator.arm_ik_l", text="IK")      

                    col_elbow_toon_L = col_arm_main_L.column()
                    col_elbow_toon_L.scale_x = 1
                    col_elbow_toon_L.scale_y = 0.25
                    col_elbow_toon_L.alignment = 'CENTER'            
                    col_elbow_toon_L.operator("operator.elbow_toon_l", text="", icon = "SPACE2", emboss = 0)    
                    
                    col_forearm_fk_L = col_arm_main_L.row(align = 1)
                    col_forearm_fk_L.scale_x = 1
                    col_forearm_fk_L.scale_y = 3
                    col_forearm_fk_L.alignment = 'CENTER'                                       
                    col_forearm_fk_L.operator("operator.forearm_fk_l", text="FK")
                    
                    col_forearm_ik_L = col_arm_main_L.row(align = 1)
                    col_forearm_ik_L.scale_x = 1
                    col_forearm_ik_L.scale_y = 1
                    col_forearm_ik_L.alignment = 'CENTER'                                       
                    col_forearm_ik_L.operator("operator.forearm_ik_l", text="IK")   
                    
                    col_hand_toon_L = col_arm_main_L.column()
                    col_hand_toon_L.scale_x = 1
                    col_hand_toon_L.scale_y = 0.25
                    col_hand_toon_L.alignment = 'CENTER'             
                    col_hand_toon_L.operator("operator.hand_toon_l", text="", icon = "SPACE2", emboss = 0)                            
                    
                    col_arm_toon_L = col_arm_L.column()
                    col_arm_toon_L.scale_x = 1
                    col_arm_toon_L.scale_y = 1
                    col_arm_toon_L.alignment = 'CENTER' 
                    col_arm_toon_L.separator()    
                    col_arm_toon_L.separator() 
                    col_arm_toon_L.separator()  
                    col_arm_toon_L.separator()            
                    col_arm_toon_L.separator()      
                    col_arm_toon_L.operator("operator.arm_toon_l", text="", icon = "SPACE2", emboss = 0)     
                    col_arm_toon_L.separator()    
                    col_arm_toon_L.separator() 
                    col_arm_toon_L.operator("operator.elbow_pole_l", text="", icon = "INLINK", emboss = 0)            
                    col_arm_toon_L.separator()         
                    col_arm_toon_L.separator()    

                    col_arm_toon_L.separator()    
                    col_arm_toon_L.operator("operator.forearm_toon_l", text="", icon = "SPACE2", emboss = 0)  

                # Arm L Quadruped
                
                if arm['rig_type'] == "Quadruped":                
                    col_arm_L = row_torso.row(align = 1)
                    col_arm_L.scale_x = 0.5
                    col_arm_L.scale_y = 1
                    col_arm_L.alignment = 'CENTER'   
                    
                    col_arm_main_L = col_arm_L.column(align = 1)
                    col_arm_main_L.scale_x = 1.2
                    col_arm_main_L.scale_y = 1
                    col_arm_main_L.alignment = 'CENTER'   
                    
                    col_arm_scale_L = col_arm_main_L.row(align = 1)
                    col_arm_scale_L.scale_x = 1.2
                    col_arm_scale_L.scale_y = 1
                    col_arm_scale_L.alignment = 'CENTER'   
                    col_arm_scale_L.operator("operator.arm_scale_l", text = "", icon = "MAN_SCALE", emboss = 1)    
                    
                    col_arm_fk_L = col_arm_main_L.row(align = 1)
                    col_arm_fk_L.scale_x = 1
                    col_arm_fk_L.scale_y = 1.5
                    col_arm_fk_L.alignment = 'CENTER'                                       
                    col_arm_fk_L.operator("operator.arm_fk_l", text="FK") 
                    
                    col_arm_ik_L = col_arm_main_L.row(align = 1)
                    col_arm_ik_L.scale_x = 1
                    col_arm_ik_L.scale_y = 1
                    col_arm_ik_L.alignment = 'CENTER'                                       
                    col_arm_ik_L.operator("operator.arm_ik_l", text="IK")      

                    col_elbow_toon_L = col_arm_main_L.column()
                    col_elbow_toon_L.scale_x = 1
                    col_elbow_toon_L.scale_y = 0.25
                    col_elbow_toon_L.alignment = 'CENTER'            
                    col_elbow_toon_L.operator("operator.elbow_toon_l", text="", icon = "SPACE2", emboss = 0)    
                    
                    col_forearm_fk_L = col_arm_main_L.row(align = 1)
                    col_forearm_fk_L.scale_x = 1
                    col_forearm_fk_L.scale_y = 1.5
                    col_forearm_fk_L.alignment = 'CENTER'                                       
                    col_forearm_fk_L.operator("operator.forearm_fk_l", text="FK")
                    
                    col_forearm_ik_L = col_arm_main_L.row(align = 1)
                    col_forearm_ik_L.scale_x = 1
                    col_forearm_ik_L.scale_y = 1
                    col_forearm_ik_L.alignment = 'CENTER'                                       
                    col_forearm_ik_L.operator("operator.forearm_ik_l", text="IK")   

                    col_ankle_toon_L = col_arm_main_L.column()
                    col_ankle_toon_L.scale_x = 1
                    col_ankle_toon_L.scale_y = 0.25
                    col_ankle_toon_L.alignment = 'CENTER'            
                    col_ankle_toon_L.operator("operator.ankle_toon_l", text="", icon = "SPACE2", emboss = 0)    
                    
                    col_carpal_fk_L = col_arm_main_L.row(align = 1)
                    col_carpal_fk_L.scale_x = 1
                    col_carpal_fk_L.scale_y = 1.5
                    col_carpal_fk_L.alignment = 'CENTER'                                       
                    col_carpal_fk_L.operator("operator.carpal_fk_l", text="FK")
                    
                    col_carpal_ik_L = col_arm_main_L.row(align = 1)
                    col_carpal_ik_L.scale_x = 1
                    col_carpal_ik_L.scale_y = 1
                    col_carpal_ik_L.alignment = 'CENTER'                                       
                    col_carpal_ik_L.operator("operator.carpal_ik_l", text="IK")   
                    
                    col_hand_toon_L = col_arm_main_L.column()
                    col_hand_toon_L.scale_x = 1
                    col_hand_toon_L.scale_y = 0.25
                    col_hand_toon_L.alignment = 'CENTER'             
                    col_hand_toon_L.operator("operator.hand_toon_l", text="", icon = "SPACE2", emboss = 0)                                              
                    
                    col_arm_toon_L = col_arm_L.column()
                    col_arm_toon_L.scale_x = 1
                    col_arm_toon_L.scale_y = 1
                    col_arm_toon_L.alignment = 'CENTER' 
                    col_arm_toon_L.separator()    
                    col_arm_toon_L.separator() 
                    col_arm_toon_L.separator()     
                    col_arm_toon_L.operator("operator.arm_toon_l", text="", icon = "SPACE2", emboss = 0)     
                    col_arm_toon_L.separator()    
                    col_arm_toon_L.separator() 
                    col_arm_toon_L.operator("operator.elbow_pole_l", text="", icon = "INLINK", emboss = 0)            
                    col_arm_toon_L.separator()           
                    col_arm_toon_L.operator("operator.forearm_toon_l", text="", icon = "SPACE2", emboss = 0)              
                    col_arm_toon_L.separator()    
                    col_arm_toon_L.separator()    
                    col_arm_toon_L.separator()                  
                    col_arm_toon_L.operator("operator.carpal_toon_l", text="", icon = "SPACE2", emboss = 0)  
                             
                # Hand R

                  
                row_legs = box_body.row(align = 0)  
                row_legs.scale_x = 1.2
                row_legs.scale_y = 1
                row_legs.alignment = 'CENTER'            
              
                row_hand_R = row_legs.row(align = 1)       
                row_hand_R.scale_x = 1
                row_hand_R.scale_y = 1
                row_hand_R.alignment = 'CENTER'  

                if arm['rig_type'] == "Biped":                                
                    col_bend_R = row_hand_R.row(align = 1)     
                    col_bend_R.scale_x = 0.5
                    col_bend_R.scale_y = 2
                    col_bend_R.alignment = 'CENTER'                       
                    col_bend_R.operator("operator.hand_roll_r", text="", icon = "LOOP_FORWARDS", emboss = 0)  

                    row_hand_main_R = row_hand_R.row(align = 1)    
                    row_hand_main_R.scale_x = 1
                    row_hand_main_R.scale_y = 1
                    row_hand_main_R.alignment = 'CENTER'  
                                 
                    col_spread_R = row_hand_main_R.column(align = 1)       
                    col_spread_R.scale_x = 0.25
                    col_spread_R.scale_y = 2
                    col_spread_R.alignment = 'CENTER'  
                    col_spread_R.operator("operator.fing_spread_r", text="")            
                  
                    col_hand_main_R = row_hand_main_R.column(align = 1)    
                    col_hand_main_R.scale_x = 0.8
                    col_hand_main_R.scale_y = 1
                    col_hand_main_R.alignment = 'CENTER'  

                    col_hand_pivot_R = col_hand_main_R.column(align = 1)       
                    col_hand_pivot_R.scale_x = 0.75
                    col_hand_pivot_R.scale_y = 0.35
                    col_hand_pivot_R.alignment = 'CENTER'  
                    col_hand_pivot_R.operator("operator.hand_ik_pivot_point_r", text="")  

                    col_hand_ik_R = col_hand_main_R.column(align = 1)      
                    col_hand_ik_R.scale_x = 1
                    col_hand_ik_R.scale_y = 1
                    col_hand_ik_R.alignment = 'CENTER'  
                    col_hand_ik_R.operator("operator.hand_ik_ctrl_r", text="Hand IK")  
                    
                    col_hand_fk_R = col_hand_main_R.column(align = 1)      
                    col_hand_fk_R.scale_x = 1
                    col_hand_fk_R.scale_y = 1
                    col_hand_fk_R.alignment = 'CENTER'  
                    col_hand_fk_R.operator("operator.hand_fk_r", text="Hand FK")  
                        
                    col_fingers_R = col_hand_main_R.row(align = 1)     
                    col_fingers_R.scale_x = 0.25
                    col_fingers_R.scale_y = 1
                    col_fingers_R.alignment = 'CENTER'  

          
                  # Hand R Quadruped 

                if arm['rig_type'] == "Quadruped":     
                    row_hand_main_R = row_hand_R.row(align = 1)    
                    row_hand_main_R.scale_x = 0.5
                    row_hand_main_R.scale_y = 1
                    row_hand_main_R.alignment = 'CENTER'  
                    
                    col_hand_main_R = row_hand_main_R.column(align = 1)    
                    col_hand_main_R.scale_x = 1
                    col_hand_main_R.scale_y = 1
                    col_hand_main_R.alignment = 'CENTER'                      
                                        
                    col_foot_R = col_hand_main_R.column(align = 0)    
                    col_foot_R.scale_x = 1
                    col_foot_R.scale_y = 1
                    col_foot_R.alignment = 'CENTER' 

                    row_foot_R = col_foot_R.row(align = 1)     
                    row_foot_R.scale_x = 1
                    row_foot_R.scale_y = 1
                    row_foot_R.alignment = 'CENTER' 
                    
                    col_toe_1_R = row_foot_R.column(align = 1)     
                    col_toe_1_R.scale_x = 1
                    col_toe_1_R.scale_y = 0.75
                    col_toe_1_R.alignment = 'CENTER'              
                    col_toe_1_R.operator("operator.fing_2_fk_r", text="")

                    col_toe_roll_2_R = row_foot_R.column(align = 1)    
                    col_toe_roll_2_R.scale_x = 0.75
                    col_toe_roll_2_R.scale_y = 0.75
                    col_toe_roll_2_R.alignment = 'CENTER'             
                    col_toe_roll_2_R.operator("operator.fing_roll_2_r", text="", icon = "LOOP_BACK", emboss = 0)         

                    col_toe_2_R = row_foot_R.column(align = 1)     
                    col_toe_2_R.scale_x = 1
                    col_toe_2_R.scale_y = 0.75
                    col_toe_2_R.alignment = 'CENTER'              
                    col_toe_2_R.operator("operator.fing_1_fk_r", text="")               

                    col_toe_roll_1_R = row_foot_R.column(align = 1)    
                    col_toe_roll_1_R.scale_x = 0.75
                    col_toe_roll_1_R.scale_y = 0.75
                    col_toe_roll_1_R.alignment = 'CENTER'             
                    col_toe_roll_1_R.operator("operator.fing_roll_1_r", text="", icon = "LOOP_BACK", emboss = 0) 
                    
                    # Foot R
                    
                    col_foot_R = row_foot_R.column(align = 1)      
                    col_foot_R.scale_x = 1
                    col_foot_R.scale_y = 0.75
                    col_foot_R.alignment = 'CENTER'  
                    col_foot_R.operator("operator.hand_r", text="Hand R")
                  
                    # FootRoll R
                    
                    col_foot_roll_R = row_foot_R.column(align = 0)     
                    col_foot_roll_R.scale_x = 0.5
                    col_foot_roll_R.scale_y = 0.75
                    col_foot_roll_R.alignment = 'CENTER'              
                    col_foot_roll_R.operator("operator.hand_roll_ctrl_r", text="", icon = "LOOP_BACK", emboss = 0)                           
                        
                    col_fingers_R = col_hand_main_R.row(align = 1)     
                    col_fingers_R.scale_x = 0.25
                    col_fingers_R.scale_y = 1
                    col_fingers_R.alignment = 'CENTER'                      

                #Fingers Option
                if arm_bones['properties_arm_R']["toggle_fingers"] == 1:   
                    col_lit_ctrl_R = col_fingers_R.column(align = 0)       
                    col_lit_ctrl_R.scale_x = 1.2
                    col_lit_ctrl_R.scale_y = 2
                    col_lit_ctrl_R.alignment = 'CENTER'         
                    col_lit_ctrl_R.operator("operator.fing_lit_ctrl_r", text="")  

                    col_lit_R = col_fingers_R.column(align = 1)    
                    col_lit_R.scale_x = 1
                    col_lit_R.scale_y = 0.7
                    col_lit_R.alignment = 'CENTER'          
                    col_lit_R.operator("operator.fing_lit_2_r", text="")  
                    col_lit_R.operator("operator.fing_lit_3_r", text="")  
                    col_lit_R.operator("operator.fing_lit_4_r", text="")                      

                    col_ring_ctrl_R = col_fingers_R.column(align = 0)      
                    col_ring_ctrl_R.scale_x = 1.2
                    col_ring_ctrl_R.scale_y = 2.5
                    col_ring_ctrl_R.alignment = 'CENTER'            
                    col_ring_ctrl_R.operator("operator.fing_ring_ctrl_r", text="")        
                    
                    col_ring_R = col_fingers_R.column(align = 1)       
                    col_ring_R.scale_x = 1
                    col_ring_R.scale_y = 0.85
                    col_ring_R.alignment = 'CENTER'         
                    col_ring_R.operator("operator.fing_ring_2_r", text="")  
                    col_ring_R.operator("operator.fing_ring_3_r", text="")  
                    col_ring_R.operator("operator.fing_ring_4_r", text="")                    

                    col_mid_ctrl_R = col_fingers_R.column(align = 0)       
                    col_mid_ctrl_R.scale_x = 1.2
                    col_mid_ctrl_R.scale_y = 3
                    col_mid_ctrl_R.alignment = 'CENTER'         
                    col_mid_ctrl_R.operator("operator.fing_mid_ctrl_r", text="")  

                    col_mid_R = col_fingers_R.column(align = 1)    
                    col_mid_R.scale_x = 1
                    col_mid_R.scale_y = 1
                    col_mid_R.alignment = 'CENTER'          
                    col_mid_R.operator("operator.fing_mid_2_r", text="")  
                    col_mid_R.operator("operator.fing_mid_3_r", text="")  
                    col_mid_R.operator("operator.fing_mid_4_r", text="")                      

                    col_index_ctrl_R = col_fingers_R.column(align = 0)     
                    col_index_ctrl_R.scale_x = 1.2
                    col_index_ctrl_R.scale_y = 2.7
                    col_index_ctrl_R.alignment = 'CENTER'           
                    col_index_ctrl_R.operator("operator.fing_ind_ctrl_r", text="")        
                    
                    col_index_R = col_fingers_R.column(align = 1)      
                    col_index_R.scale_x = 1
                    col_index_R.scale_y = 0.9
                    col_index_R.alignment = 'CENTER'            
                    col_index_R.operator("operator.fing_ind_2_r", text="")  
                    col_index_R.operator("operator.fing_ind_3_r", text="")  
                    col_index_R.operator("operator.fing_ind_4_r", text="")  
                    
                    col_thumb_ctrl_R = col_fingers_R.column(align = 0)     
                    col_thumb_ctrl_R.scale_x = 1.2
                    col_thumb_ctrl_R.scale_y = 1.5
                    col_thumb_ctrl_R.alignment = 'CENTER'           
                    col_thumb_ctrl_R.operator("operator.fing_thumb_ctrl_r", text="")          
                    
                    col_thumb_R = col_fingers_R.column(align = 1)      
                    col_thumb_R.scale_x = 1
                    col_thumb_R.scale_y = 0.5
                    col_thumb_R.alignment = 'CENTER'            
                    col_thumb_R.operator("operator.fing_thumb_1_r", text="")  
                    col_thumb_R.operator("operator.fing_thumb_2_r", text="")  
                    col_thumb_R.operator("operator.fing_thumb_3_r", text="")              

                    col_fing_ik_R = col_hand_main_R.row(align = 0)     
                    col_fing_ik_R.scale_x = 0.25
                    col_fing_ik_R.scale_y = 0.5
                    col_fing_ik_R.alignment = 'CENTER'   
                    col_fing_ik_R.operator("operator.fing_lit_ik_r", text="")  
                    col_fing_ik_R.operator("operator.fing_ring_ik_r", text="")  
                    col_fing_ik_R.operator("operator.fing_mid_ik_r", text="") 
                    col_fing_ik_R.operator("operator.fing_ind_ik_r", text="")   
                    col_fing_ik_R.operator("operator.fing_thumb_ik_r", text="")  
                    
                    col_hand_close_R = col_hand_main_R.column(align = 0)     
                    col_hand_close_R.scale_x = 1
                    col_hand_close_R.scale_y = 0.5
                    col_hand_close_R.alignment = 'CENTER'   
                    col_hand_close_R.separator()
                    col_hand_close_R.operator("operator.hand_close_r", text="")                                               
                else:
                    if arm['rig_type'] == "Biped":  
                        col_hand_main_R.scale_x = 0.112
                    if arm['rig_type'] == "Quadruped":  
                        row_hand_main_R.scale_x = 1                       
                        col_hand_main_R.scale_x = 0.25 
                    
                    # Hand Sole R

                if arm['rig_type'] == "Quadruped":  
                    row_sole_R = col_hand_main_R.row(align = 1)       
                    row_sole_R.scale_x = 2
                    row_sole_R.scale_y = 1
                    row_sole_R.alignment = 'CENTER'  

                    col_sole_R = row_sole_R.column(align = 1)      
                    col_sole_R.scale_x = 1
                    col_sole_R.scale_y = 0.75
                    col_sole_R.alignment = 'CENTER'                   
                    col_sole_R.operator("operator.hand_sole_ctrl_r", text="Hand Sole R")         
                    
                    col_sole_pivot_R = row_sole_R.column(align = 1)    
                    col_sole_pivot_R.scale_x = 0.25
                    col_sole_pivot_R.scale_y = 0.75
                    col_sole_pivot_R.alignment = 'CENTER'                     
                    col_sole_pivot_R.operator("operator.hand_sole_pivot_point_r", text="")                       
                     
                # Leg R
                if arm['rig_type'] == "Biped":                   
                    row_legs_main = row_legs.row(align = 0)
                    row_legs_main.scale_x = 0.75
                    row_legs_main.scale_y = 1
                    row_legs_main.alignment = 'CENTER'   
                    
                    row_leg_main_R = row_legs_main.row(align = 1)
                    row_leg_main_R.scale_x = 1
                    row_leg_main_R.scale_y = 1
                    row_leg_main_R.alignment = 'CENTER'           
                    
                    col_leg_toon_R = row_leg_main_R.column()
                    col_leg_toon_R.scale_x = 0.5
                    col_leg_toon_R.scale_y = 1
                    col_leg_toon_R.alignment = 'CENTER' 
                    col_leg_toon_R.separator()    
                    col_leg_toon_R.separator() 
                    col_leg_toon_R.separator()     
                    col_leg_toon_R.separator() 
                    col_leg_toon_R.separator()                  
                    col_leg_toon_R.operator("operator.thigh_toon_r", text="", icon = "SPACE2", emboss = 0)   
                    col_leg_toon_R.separator()    
                    col_leg_toon_R.separator() 
                    col_leg_toon_R.separator() 
                    col_leg_toon_R.separator() 
                    col_leg_toon_R.separator()                      
                    col_leg_toon_R.operator("operator.knee_pole_r", text="", icon = "INLINK", emboss = 0)                
                    col_leg_toon_R.separator()    
                    col_leg_toon_R.separator()    
                    col_leg_toon_R.separator()    
                    col_leg_toon_R.operator("operator.shin_toon_r", text="", icon = "SPACE2", emboss = 0)              
                    
                    col_leg_main_R = row_leg_main_R.column(align = 1)
                    col_leg_main_R.scale_x = 1
                    col_leg_main_R.scale_y = 1
                    col_leg_main_R.alignment = 'CENTER'   

                    col_pelvis_toon_R = col_leg_main_R.column()
                    col_pelvis_toon_R.scale_x = 1
                    col_pelvis_toon_R.scale_y = 0.1
                    col_pelvis_toon_R.alignment = 'CENTER'           
                    col_pelvis_toon_R.operator("operator.pelvis_toon_r", text="", icon = "SPACE2", emboss = 0)   
                    
                    col_leg_scale_R = col_leg_main_R.row(align = 1)
                    col_leg_scale_R.scale_x = 2
                    col_leg_scale_R.scale_y = 1
                    col_leg_scale_R.alignment = 'CENTER'   
                    col_leg_scale_R.operator("operator.leg_scale_r", text = "", icon = "MAN_SCALE", emboss = 1)    
                    
                    col_leg_fk_R = col_leg_main_R.row(align = 1)
                    col_leg_fk_R.scale_x = 1
                    col_leg_fk_R.scale_y = 3.5
                    col_leg_fk_R.alignment = 'CENTER'                                       
                    col_leg_fk_R.operator("operator.thigh_fk_r", text="FK") 
                    
                    col_leg_ik_R = col_leg_main_R.row(align = 1)
                    col_leg_ik_R.scale_x = 1
                    col_leg_ik_R.scale_y = 1
                    col_leg_ik_R.alignment = 'CENTER'                                       
                    col_leg_ik_R.operator("operator.thigh_ik_r", text="IK")    

                    col_knee_toon_R = col_leg_main_R.column()
                    col_knee_toon_R.scale_x = 1
                    col_knee_toon_R.scale_y = 0.25
                    col_knee_toon_R.alignment = 'CENTER'             
                    col_knee_toon_R.operator("operator.knee_toon_r", text="", icon = "SPACE2", emboss = 0)  
                    
                    col_shin_fk_R = col_leg_main_R.row(align = 1)
                    col_shin_fk_R.scale_x = 1
                    col_shin_fk_R.scale_y = 4
                    col_shin_fk_R.alignment = 'CENTER'                                      
                    col_shin_fk_R.operator("operator.shin_fk_r", text="FK")
                    
                    col_shin_ik_R = col_leg_main_R.row(align = 1)
                    col_shin_ik_R.scale_x = 1
                    col_shin_ik_R.scale_y = 1
                    col_shin_ik_R.alignment = 'CENTER'                                      
                    col_shin_ik_R.operator("operator.shin_ik_r", text="IK") 
                    
                    col_foot_toon_R = col_leg_main_R.column()
                    col_foot_toon_R.scale_x = 1
                    col_foot_toon_R.scale_y = 0.25
                    col_foot_toon_R.alignment = 'CENTER'             
                    col_foot_toon_R.operator("operator.foot_toon_r", text="", icon = "SPACE2", emboss = 0)                            

                # Quadruped Leg R
                if arm['rig_type'] == "Quadruped":                   
                    row_legs_main = row_legs.row(align = 0)
                    row_legs_main.scale_x = 0.75
                    row_legs_main.scale_y = 1
                    row_legs_main.alignment = 'CENTER'   
                    
                    row_leg_main_R = row_legs_main.row(align = 1)
                    row_leg_main_R.scale_x = 1
                    row_leg_main_R.scale_y = 1
                    row_leg_main_R.alignment = 'CENTER'           
                    
                    col_leg_toon_R = row_leg_main_R.column()
                    col_leg_toon_R.scale_x = 0.5
                    col_leg_toon_R.scale_y = 1
                    col_leg_toon_R.alignment = 'CENTER' 
                    col_leg_toon_R.separator()    
                    col_leg_toon_R.separator() 
                    col_leg_toon_R.separator()     
                    col_leg_toon_R.separator() 
                    col_leg_toon_R.separator()                  
                    col_leg_toon_R.operator("operator.thigh_toon_r", text="", icon = "SPACE2", emboss = 0)   
                    col_leg_toon_R.separator()    
                    col_leg_toon_R.separator()                   
                    col_leg_toon_R.operator("operator.knee_pole_r", text="", icon = "INLINK", emboss = 0)                
                    col_leg_toon_R.separator()      
                    col_leg_toon_R.operator("operator.shin_toon_r", text="", icon = "SPACE2", emboss = 0)   
                    col_leg_toon_R.separator()    
                    col_leg_toon_R.separator()    
                    col_leg_toon_R.separator()  
                    col_leg_toon_R.separator()                         
                    col_leg_toon_R.operator("operator.tarsal_toon_r", text="", icon = "SPACE2", emboss = 0)                                  
                    
                    col_leg_main_R = row_leg_main_R.column(align = 1)
                    col_leg_main_R.scale_x = 1
                    col_leg_main_R.scale_y = 1
                    col_leg_main_R.alignment = 'CENTER'   

                    col_pelvis_toon_R = col_leg_main_R.column()
                    col_pelvis_toon_R.scale_x = 1
                    col_pelvis_toon_R.scale_y = 0.1
                    col_pelvis_toon_R.alignment = 'CENTER'           
                    col_pelvis_toon_R.operator("operator.pelvis_toon_r", text="", icon = "SPACE2", emboss = 0)   
                    
                    col_leg_scale_R = col_leg_main_R.row(align = 1)
                    col_leg_scale_R.scale_x = 2
                    col_leg_scale_R.scale_y = 1
                    col_leg_scale_R.alignment = 'CENTER'   
                    col_leg_scale_R.operator("operator.leg_scale_r", text = "", icon = "MAN_SCALE", emboss = 1)    
                    
                    col_leg_fk_R = col_leg_main_R.row(align = 1)
                    col_leg_fk_R.scale_x = 1
                    col_leg_fk_R.scale_y = 2
                    col_leg_fk_R.alignment = 'CENTER'                                       
                    col_leg_fk_R.operator("operator.thigh_fk_r", text="FK") 
                    
                    col_leg_ik_R = col_leg_main_R.row(align = 1)
                    col_leg_ik_R.scale_x = 1
                    col_leg_ik_R.scale_y = 1
                    col_leg_ik_R.alignment = 'CENTER'                                       
                    col_leg_ik_R.operator("operator.thigh_ik_r", text="IK")    

                    col_knee_toon_R = col_leg_main_R.column()
                    col_knee_toon_R.scale_x = 1
                    col_knee_toon_R.scale_y = 0.25
                    col_knee_toon_R.alignment = 'CENTER'             
                    col_knee_toon_R.operator("operator.knee_toon_r", text="", icon = "SPACE2", emboss = 0)  
                    
                    col_shin_fk_R = col_leg_main_R.row(align = 1)
                    col_shin_fk_R.scale_x = 1
                    col_shin_fk_R.scale_y = 2
                    col_shin_fk_R.alignment = 'CENTER'                                      
                    col_shin_fk_R.operator("operator.shin_fk_r", text="FK")
                    
                    col_shin_ik_R = col_leg_main_R.row(align = 1)
                    col_shin_ik_R.scale_x = 1
                    col_shin_ik_R.scale_y = 1
                    col_shin_ik_R.alignment = 'CENTER'                                      
                    col_shin_ik_R.operator("operator.shin_ik_r", text="IK") 

                    col_hock_toon_R = col_leg_main_R.column()
                    col_hock_toon_R.scale_x = 1
                    col_hock_toon_R.scale_y = 0.25
                    col_hock_toon_R.alignment = 'CENTER'             
                    col_hock_toon_R.operator("operator.hock_toon_r", text="", icon = "SPACE2", emboss = 0)  
                    
                    col_tarsal_fk_R = col_leg_main_R.row(align = 1)
                    col_tarsal_fk_R.scale_x = 1
                    col_tarsal_fk_R.scale_y = 2
                    col_tarsal_fk_R.alignment = 'CENTER'                                      
                    col_tarsal_fk_R.operator("operator.tarsal_fk_r", text="FK")
                    
                    col_tarsal_ik_R = col_leg_main_R.row(align = 1)
                    col_tarsal_ik_R.scale_x = 1
                    col_tarsal_ik_R.scale_y = 1
                    col_tarsal_ik_R.alignment = 'CENTER'                                      
                    col_tarsal_ik_R.operator("operator.tarsal_ik_r", text="IK")                     
                    
                    col_foot_toon_R = col_leg_main_R.column()
                    col_foot_toon_R.scale_x = 1
                    col_foot_toon_R.scale_y = 0.25
                    col_foot_toon_R.alignment = 'CENTER'             
                    col_foot_toon_R.operator("operator.foot_toon_r", text="", icon = "SPACE2", emboss = 0)                            


                # Leg L
                if arm['rig_type'] == "Biped":    
                    row_leg_main_L = row_legs_main.row(align = 1)
                    row_leg_main_R.scale_x = 1
                    row_leg_main_R.scale_y = 1
                    row_leg_main_R.alignment = 'CENTER'  
                    
                    col_leg_main_L = row_leg_main_L.column(align = 1)
                    col_leg_main_L.scale_x = 1
                    col_leg_main_L.scale_y = 1
                    col_leg_main_L.alignment = 'CENTER'   

                    col_pelvis_toon_L = col_leg_main_L.column()
                    col_pelvis_toon_L.scale_x = 1
                    col_pelvis_toon_L.scale_y = 0.1
                    col_pelvis_toon_L.alignment = 'CENTER'           
                    col_pelvis_toon_L.operator("operator.pelvis_toon_l", text="", icon = "SPACE2", emboss = 0)  
                    
                    col_leg_scale_L = col_leg_main_L.row(align = 1)
                    col_leg_scale_L.scale_x = 2
                    col_leg_scale_L.scale_y = 1
                    col_leg_scale_L.alignment = 'CENTER'   
                    col_leg_scale_L.operator("operator.leg_scale_l", text = "", icon = "MAN_SCALE", emboss = 1)    
                    
                    col_leg_fk_L = col_leg_main_L.row(align = 1)
                    col_leg_fk_L.scale_x = 1
                    col_leg_fk_L.scale_y = 3.5
                    col_leg_fk_L.alignment = 'CENTER'                                       
                    col_leg_fk_L.operator("operator.thigh_fk_l", text="FK") 
                    
                    col_leg_ik_L = col_leg_main_L.row(align = 1)
                    col_leg_ik_L.scale_x = 1
                    col_leg_ik_L.scale_y = 1
                    col_leg_ik_L.alignment = 'CENTER'                                       
                    col_leg_ik_L.operator("operator.thigh_ik_l", text="IK")    

                    col_knee_toon_L = col_leg_main_L.column()
                    col_knee_toon_L.scale_x = 1
                    col_knee_toon_L.scale_y = 0.25
                    col_knee_toon_L.alignment = 'CENTER'             
                    col_knee_toon_L.operator("operator.knee_toon_l", text="", icon = "SPACE2", emboss = 0)  
                    
                    col_shin_fk_L = col_leg_main_L.row(align = 1)
                    col_shin_fk_L.scale_x = 1
                    col_shin_fk_L.scale_y = 4
                    col_shin_fk_L.alignment = 'CENTER'                                      
                    col_shin_fk_L.operator("operator.shin_fk_l", text="FK")
                    
                    col_shin_ik_L = col_leg_main_L.row(align = 1)
                    col_shin_ik_L.scale_x = 1
                    col_shin_ik_L.scale_y = 1
                    col_shin_ik_L.alignment = 'CENTER'                                      
                    col_shin_ik_L.operator("operator.shin_ik_l", text="IK") 
                    
                    col_foot_toon_L = col_leg_main_L.column()
                    col_foot_toon_L.scale_x = 1
                    col_foot_toon_L.scale_y = 0.25
                    col_foot_toon_L.alignment = 'CENTER'             
                    col_foot_toon_L.operator("operator.foot_toon_l", text="", icon = "SPACE2", emboss = 0)                            

                    
                    col_leg_toon_L = row_leg_main_L.column()
                    col_leg_toon_L.scale_x = 0.5
                    col_leg_toon_L.scale_y = 1
                    col_leg_toon_L.alignment = 'CENTER' 
                    col_leg_toon_L.separator()    
                    col_leg_toon_L.separator() 
                    col_leg_toon_L.separator()     
                    col_leg_toon_L.separator()  
                    col_leg_toon_L.separator()                  
                    col_leg_toon_L.operator("operator.thigh_toon_l", text="", icon = "SPACE2", emboss = 0)   
                    col_leg_toon_L.separator()    
                    col_leg_toon_L.separator() 
                    col_leg_toon_L.separator()  
                    col_leg_toon_L.separator() 
                    col_leg_toon_L.separator()                   
                    col_leg_toon_L.operator("operator.knee_pole_l", text="", icon = "INLINK", emboss = 0)                 
                    col_leg_toon_L.separator()    
                    col_leg_toon_L.separator()    
                    col_leg_toon_L.separator()    
                    col_leg_toon_L.operator("operator.shin_toon_l", text="", icon = "SPACE2", emboss = 0)              

                # Quadruped Leg L
                if arm['rig_type'] == "Quadruped":                   
                    row_legs_main = row_legs.row(align = 0)
                    row_legs_main.scale_x = 0.75
                    row_legs_main.scale_y = 1
                    row_legs_main.alignment = 'CENTER'   
                    
                    row_leg_main_L = row_legs_main.row(align = 1)
                    row_leg_main_L.scale_x = 1
                    row_leg_main_L.scale_y = 1
                    row_leg_main_L.alignment = 'CENTER'                                           
                    
                    col_leg_main_L = row_leg_main_L.column(align = 1)
                    col_leg_main_L.scale_x = 1
                    col_leg_main_L.scale_y = 1
                    col_leg_main_L.alignment = 'CENTER'   

                    col_pelvis_toon_L = col_leg_main_L.column()
                    col_pelvis_toon_L.scale_x = 1
                    col_pelvis_toon_L.scale_y = 0.1
                    col_pelvis_toon_L.alignment = 'CENTER'           
                    col_pelvis_toon_L.operator("operator.pelvis_toon_l", text="", icon = "SPACE2", emboss = 0)   
                    
                    col_leg_scale_L = col_leg_main_L.row(align = 1)
                    col_leg_scale_L.scale_x = 2
                    col_leg_scale_L.scale_y = 1
                    col_leg_scale_L.alignment = 'CENTER'   
                    col_leg_scale_L.operator("operator.leg_scale_l", text = "", icon = "MAN_SCALE", emboss = 1)    
                    
                    col_leg_fk_L = col_leg_main_L.row(align = 1)
                    col_leg_fk_L.scale_x = 1
                    col_leg_fk_L.scale_y = 2
                    col_leg_fk_L.alignment = 'CENTER'                                       
                    col_leg_fk_L.operator("operator.thigh_fk_l", text="FK") 
                    
                    col_leg_ik_L = col_leg_main_L.row(align = 1)
                    col_leg_ik_L.scale_x = 1
                    col_leg_ik_L.scale_y = 1
                    col_leg_ik_L.alignment = 'CENTER'                                       
                    col_leg_ik_L.operator("operator.thigh_ik_l", text="IK")    

                    col_knee_toon_L = col_leg_main_L.column()
                    col_knee_toon_L.scale_x = 1
                    col_knee_toon_L.scale_y = 0.25
                    col_knee_toon_L.alignment = 'CENTER'             
                    col_knee_toon_L.operator("operator.knee_toon_l", text="", icon = "SPACE2", emboss = 0)  
                    
                    col_shin_fk_L = col_leg_main_L.row(align = 1)
                    col_shin_fk_L.scale_x = 1
                    col_shin_fk_L.scale_y = 2
                    col_shin_fk_L.alignment = 'CENTER'                                      
                    col_shin_fk_L.operator("operator.shin_fk_l", text="FK")
                    
                    col_shin_ik_L = col_leg_main_L.row(align = 1)
                    col_shin_ik_L.scale_x = 1
                    col_shin_ik_L.scale_y = 1
                    col_shin_ik_L.alignment = 'CENTER'                                      
                    col_shin_ik_L.operator("operator.shin_ik_l", text="IK") 

                    col_hock_toon_L = col_leg_main_L.column()
                    col_hock_toon_L.scale_x = 1
                    col_hock_toon_L.scale_y = 0.25
                    col_hock_toon_L.alignment = 'CENTER'             
                    col_hock_toon_L.operator("operator.hock_toon_l", text="", icon = "SPACE2", emboss = 0)  
                    
                    col_tarsal_fk_L = col_leg_main_L.row(align = 1)
                    col_tarsal_fk_L.scale_x = 1
                    col_tarsal_fk_L.scale_y = 2
                    col_tarsal_fk_L.alignment = 'CENTER'                                      
                    col_tarsal_fk_L.operator("operator.tarsal_fk_l", text="FK")
                    
                    col_tarsal_ik_L = col_leg_main_L.row(align = 1)
                    col_tarsal_ik_L.scale_x = 1
                    col_tarsal_ik_L.scale_y = 1
                    col_tarsal_ik_L.alignment = 'CENTER'                                      
                    col_tarsal_ik_L.operator("operator.tarsal_ik_l", text="IK")                     
                    
                    col_foot_toon_L = col_leg_main_L.column()
                    col_foot_toon_L.scale_x = 1
                    col_foot_toon_L.scale_y = 0.25
                    col_foot_toon_L.alignment = 'CENTER'             
                    col_foot_toon_L.operator("operator.foot_toon_l", text="", icon = "SPACE2", emboss = 0)                            

                    
                    col_leg_toon_L = row_leg_main_L.column()
                    col_leg_toon_L.scale_x = 0.5
                    col_leg_toon_L.scale_y = 1
                    col_leg_toon_L.alignment = 'CENTER' 
                    col_leg_toon_L.separator()    
                    col_leg_toon_L.separator() 
                    col_leg_toon_L.separator()     
                    col_leg_toon_L.separator() 
                    col_leg_toon_L.separator()                  
                    col_leg_toon_L.operator("operator.thigh_toon_l", text="", icon = "SPACE2", emboss = 0)   
                    col_leg_toon_L.separator()    
                    col_leg_toon_L.separator()                   
                    col_leg_toon_L.operator("operator.knee_pole_l", text="", icon = "INLINK", emboss = 0)                
                    col_leg_toon_L.separator()      
                    col_leg_toon_L.operator("operator.shin_toon_l", text="", icon = "SPACE2", emboss = 0)   
                    col_leg_toon_L.separator()    
                    col_leg_toon_L.separator()    
                    col_leg_toon_L.separator()  
                    col_leg_toon_L.separator()                         
                    col_leg_toon_L.operator("operator.tarsal_toon_l", text="", icon = "SPACE2", emboss = 0)  
                  
                # Hand L
                
                col_hand_L = row_legs.column(align = 1)    
                col_hand_L.scale_x = 1
                col_hand_L.scale_y = 1
                col_hand_L.alignment = 'CENTER' 
                
                row_hand_L = col_hand_L.row(align = 1)     
                row_hand_L.scale_x = 1
                row_hand_L.scale_y = 1
                row_hand_L.alignment = 'CENTER'  
                
                if arm['rig_type'] == "Biped":                 
                    row_hand_main_L = row_hand_L.row(align = 1)    
                    row_hand_main_L.scale_x = 1
                    row_hand_main_L.scale_y = 1
                    row_hand_main_L.alignment = 'CENTER'  
                    
                    col_hand_main_L = row_hand_main_L.column(align = 1)    
                    col_hand_main_L.scale_x = 0.8
                    col_hand_main_L.scale_y = 1
                    col_hand_main_L.alignment = 'CENTER'  

                    col_hand_pivot_L = col_hand_main_L.column(align = 1)       
                    col_hand_pivot_L.scale_x = 0.75
                    col_hand_pivot_L.scale_y = 0.35
                    col_hand_pivot_L.alignment = 'CENTER'  
                    col_hand_pivot_L.operator("operator.hand_ik_pivot_point_l", text="")  

                    col_hand_ik_L = col_hand_main_L.column(align = 1)      
                    col_hand_ik_L.scale_x = 1
                    col_hand_ik_L.scale_y = 1
                    col_hand_ik_L.alignment = 'CENTER'  
                    col_hand_ik_L.operator("operator.hand_ik_ctrl_l", text="Hand IK")  
                    
                    col_hand_fk_L = col_hand_main_L.column(align = 1)      
                    col_hand_fk_L.scale_x = 1
                    col_hand_fk_L.scale_y = 1
                    col_hand_fk_L.alignment = 'CENTER'  
                    col_hand_fk_L.operator("operator.hand_fk_l", text="Hand FK")  

                    col_fingers_L = col_hand_main_L.row(align = 1)     
                    col_fingers_L.scale_x = 0.25
                    col_fingers_L.scale_y = 1
                    col_fingers_L.alignment = 'CENTER'  

                  # Hand R Quadruped 

                if arm['rig_type'] == "Quadruped":     
                    row_hand_main_L = row_hand_L.row(align = 1)    
                    row_hand_main_L.scale_x = 0.5
                    row_hand_main_L.scale_y = 1
                    row_hand_main_L.alignment = 'CENTER'  
                    
                    col_hand_main_L = row_hand_main_L.column(align = 1)    
                    col_hand_main_L.scale_x = 1
                    col_hand_main_L.scale_y = 1
                    col_hand_main_L.alignment = 'CENTER'                      

                    #Foot_L      
                  
                    col_foot_L = col_hand_main_L.column(align = 0)    
                    col_foot_L.scale_x = 1
                    col_foot_L.scale_y = 1
                    col_foot_L.alignment = 'CENTER' 

                    row_foot_L = col_foot_L.row(align = 1)     
                    row_foot_L.scale_x = 1
                    row_foot_L.scale_y = 1
                    row_foot_L.alignment = 'CENTER' 

                    # FootRoll L
                    
                    col_foot_roll_L = row_foot_L.column(align = 0)     
                    col_foot_roll_L.scale_x = 0.5
                    col_foot_roll_L.scale_y = 0.75
                    col_foot_roll_L.alignment = 'CENTER'              
                    col_foot_roll_L.operator("operator.hand_roll_ctrl_l", text="", icon = "LOOP_FORWARDS", emboss = 0)

                    # Foot L
                    
                    col_foot_L = row_foot_L.column(align = 1)      
                    col_foot_L.scale_x = 1
                    col_foot_L.scale_y = 0.75
                    col_foot_L.alignment = 'CENTER'  
                    col_foot_L.operator("operator.hand_l", text="Hand L")

                      # Toes L

                    col_toe_roll_1_L = row_foot_L.row(align = 1)       
                    col_toe_roll_1_L.scale_x = 0.75
                    col_toe_roll_1_L.scale_y = 0.75
                    col_toe_roll_1_L.alignment = 'CENTER'             
                    col_toe_roll_1_L.operator("operator.fing_roll_1_l", text="", icon = "LOOP_FORWARDS", emboss = 0)
                    
                    col_toe_1_L = row_foot_L.row(align = 1)    
                    col_toe_1_L.scale_x = 1
                    col_toe_1_L.scale_y = 0.75
                    col_toe_1_L.alignment = 'CENTER'              
                    col_toe_1_L.operator("operator.fing_1_fk_l", text="")

                    col_toe_roll_2_L = row_foot_L.row(align = 1)       
                    col_toe_roll_2_L.scale_x = 0.75
                    col_toe_roll_2_L.scale_y = 0.75
                    col_toe_roll_2_L.alignment = 'CENTER'             
                    col_toe_roll_2_L.operator("operator.fing_roll_2_l", text="", icon = "LOOP_FORWARDS", emboss = 0)

                    col_toe_2_L = row_foot_L.row(align = 1)    
                    col_toe_2_L.scale_x = 1
                    col_toe_2_L.scale_y = 0.75
                    col_toe_2_L.alignment = 'CENTER'              
                    col_toe_2_L.operator("operator.fing_2_fk_l", text="")
                                                                
                    col_fingers_L = col_hand_main_L.row(align = 1)     
                    col_fingers_L.scale_x = 0.25
                    col_fingers_L.scale_y = 1
                    col_fingers_L.alignment = 'CENTER'    

                #Fingers Option
                if arm_bones['properties_arm_L']["toggle_fingers"] == 1:   
                    col_thumb_L = col_fingers_L.column(align = 1)      
                    col_thumb_L.scale_x = 1.5
                    col_thumb_L.scale_y = 0.5
                    col_thumb_L.alignment = 'CENTER'            
                    col_thumb_L.operator("operator.fing_thumb_1_l", text="")  
                    col_thumb_L.operator("operator.fing_thumb_2_l", text="")  
                    col_thumb_L.operator("operator.fing_thumb_3_l", text="")     

                    col_thumb_ctrl_L = col_fingers_L.column(align = 0)     
                    col_thumb_ctrl_L.scale_x = 1.5
                    col_thumb_ctrl_L.scale_y = 1.5
                    col_thumb_ctrl_L.alignment = 'CENTER'           
                    col_thumb_ctrl_L.operator("operator.fing_thumb_ctrl_l", text="")    

                    col_index_L = col_fingers_L.column(align = 1)      
                    col_index_L.scale_x = 1
                    col_index_L.scale_y = 0.9
                    col_index_L.alignment = 'CENTER'            
                    col_index_L.operator("operator.fing_ind_2_l", text="")  
                    col_index_L.operator("operator.fing_ind_3_l", text="")  
                    col_index_L.operator("operator.fing_ind_4_l", text="")    

                    col_index_ctrl_L = col_fingers_L.column(align = 0)     
                    col_index_ctrl_L.scale_x = 1.2
                    col_index_ctrl_L.scale_y = 2.7
                    col_index_ctrl_L.alignment = 'CENTER'           
                    col_index_ctrl_L.operator("operator.fing_ind_ctrl_l", text="")   
                    
                    col_mid_L = col_fingers_L.column(align = 1)    
                    col_mid_L.scale_x = 1
                    col_mid_L.scale_y = 1
                    col_mid_L.alignment = 'CENTER'          
                    col_mid_L.operator("operator.fing_mid_2_l", text="")  
                    col_mid_L.operator("operator.fing_mid_3_l", text="")  
                    col_mid_L.operator("operator.fing_mid_4_l", text="")                

                    col_mid_ctrl_L = col_fingers_L.column(align = 0)       
                    col_mid_ctrl_L.scale_x = 1.2
                    col_mid_ctrl_L.scale_y = 3
                    col_mid_ctrl_L.alignment = 'CENTER'         
                    col_mid_ctrl_L.operator("operator.fing_mid_ctrl_l", text="")  

                    col_ring_L = col_fingers_L.column(align = 1)       
                    col_ring_L.scale_x = 1
                    col_ring_L.scale_y = 0.85
                    col_ring_L.alignment = 'CENTER'         
                    col_ring_L.operator("operator.fing_ring_2_l", text="")  
                    col_ring_L.operator("operator.fing_ring_3_l", text="")  
                    col_ring_L.operator("operator.fing_ring_4_l", text="")    
                          
                    col_ring_ctrl_L = col_fingers_L.column(align = 0)      
                    col_ring_ctrl_L.scale_x = 1.2
                    col_ring_ctrl_L.scale_y = 2.5
                    col_ring_ctrl_L.alignment = 'CENTER'            
                    col_ring_ctrl_L.operator("operator.fing_ring_ctrl_l", text="")        
                    
                    col_lit_L = col_fingers_L.column(align = 1)    
                    col_lit_L.scale_x = 1
                    col_lit_L.scale_y = 0.7
                    col_lit_L.alignment = 'CENTER'          
                    col_lit_L.operator("operator.fing_lit_2_l", text="")  
                    col_lit_L.operator("operator.fing_lit_3_l", text="")  
                    col_lit_L.operator("operator.fing_lit_4_l", text="")     
                          
                    col_lit_ctrl_L = col_fingers_L.column(align = 0)       
                    col_lit_ctrl_L.scale_x = 0.5
                    col_lit_ctrl_L.scale_y = 2
                    col_lit_ctrl_L.alignment = 'CENTER'         
                    col_lit_ctrl_L.operator("operator.fing_lit_ctrl_l", text="")  

                    col_fing_ik_L = col_hand_main_L.row(align = 0)     
                    col_fing_ik_L.scale_x = 0.25
                    col_fing_ik_L.scale_y = 0.5
                    col_fing_ik_L.alignment = 'CENTER'   
                    col_fing_ik_L.operator("operator.fing_thumb_ik_l", text="")  
                    col_fing_ik_L.operator("operator.fing_ind_ik_l", text="")  
                    col_fing_ik_L.operator("operator.fing_mid_ik_l", text="") 
                    col_fing_ik_L.operator("operator.fing_ring_ik_l", text="")  
                    col_fing_ik_L.operator("operator.fing_lit_ik_l", text="")   
                    
                    col_hand_close_L = col_hand_main_L.column(align = 0)     
                    col_hand_close_L.scale_x = 1
                    col_hand_close_L.scale_y = 0.5
                    col_hand_close_L.alignment = 'CENTER'   
                    col_hand_close_L.separator()
                    col_hand_close_L.operator("operator.hand_close_l", text="")                 

                else:
                    if arm['rig_type'] == "Biped":  
                        col_hand_main_L.scale_x = 0.112
                    if arm['rig_type'] == "Quadruped":  
                        row_hand_main_L.scale_x = 1                       
                        col_hand_main_L.scale_x = 0.25                       

                    # Hand Sole L

                if arm['rig_type'] == "Quadruped":  
                    row_sole_L = col_hand_main_L.row(align = 1)       
                    row_sole_L.scale_x = 2
                    row_sole_L.scale_y = 1
                    row_sole_L.alignment = 'CENTER'  

                    col_sole_pivot_L = row_sole_L.column(align = 1)    
                    col_sole_pivot_L.scale_x = 0.25
                    col_sole_pivot_L.scale_y = 0.75
                    col_sole_pivot_L.alignment = 'CENTER'                     
                    col_sole_pivot_L.operator("operator.hand_sole_pivot_point_l", text="")  

                    col_sole_L = row_sole_L.column(align = 1)      
                    col_sole_L.scale_x = 1
                    col_sole_L.scale_y = 0.75
                    col_sole_L.alignment = 'CENTER'                   
                    col_sole_L.operator("operator.hand_sole_ctrl_l", text="Hand Sole L")         

                #Hand Spread L
                if arm['rig_type'] == "Biped":     
                    col_spread_R = row_hand_main_L.column(align = 0)       
                    col_spread_R.scale_x = 0.25
                    col_spread_R.scale_y = 2
                    col_spread_R.alignment = 'CENTER'  
                    col_spread_R.operator("operator.fing_spread_l", text="")   
                              
                    col_bend_L = row_hand_L.row(align = 1)     
                    col_bend_L.scale_x = 0.5
                    col_bend_L.scale_y = 2
                    col_bend_L.alignment = 'CENTER'                 
                    col_bend_L.operator("operator.hand_roll_l", text="", icon = "LOOP_BACK", emboss = 0)  
                
                
                
                # Toes R

                row_feet = box_body.row(align = 0)  
                row_feet.scale_x = 1
                row_feet.scale_y = 1
                row_feet.alignment = 'CENTER'            
              
                col_foot_R = row_feet.column(align = 0)    
                col_foot_R.scale_x = 1
                col_foot_R.scale_y = 1
                col_foot_R.alignment = 'CENTER' 

                row_foot_R = col_foot_R.row(align = 1)     
                row_foot_R.scale_x = 1
                row_foot_R.scale_y = 1
                row_foot_R.alignment = 'CENTER' 
                
                col_toe_1_R = row_foot_R.column(align = 1)     
                col_toe_1_R.scale_x = 0.75
                col_toe_1_R.scale_y = 0.75
                col_toe_1_R.alignment = 'CENTER'              
                col_toe_1_R.operator("operator.toe_2_fk_r", text="")

                col_toe_roll_2_R = row_foot_R.column(align = 1)    
                col_toe_roll_2_R.scale_x = 0.5
                col_toe_roll_2_R.scale_y = 0.75
                col_toe_roll_2_R.alignment = 'CENTER'             
                col_toe_roll_2_R.operator("operator.toe_roll_2_r", text="", icon = "LOOP_BACK", emboss = 0)         

                col_toe_2_R = row_foot_R.column(align = 1)     
                col_toe_2_R.scale_x = 0.75
                col_toe_2_R.scale_y = 0.75
                col_toe_2_R.alignment = 'CENTER'              
                col_toe_2_R.operator("operator.toe_1_fk_r", text="")               

                col_toe_roll_1_R = row_foot_R.column(align = 1)    
                col_toe_roll_1_R.scale_x = 0.5
                col_toe_roll_1_R.scale_y = 0.75
                col_toe_roll_1_R.alignment = 'CENTER'             
                col_toe_roll_1_R.operator("operator.toe_roll_1_r", text="", icon = "LOOP_BACK", emboss = 0) 
                
                # Foot R
                
                col_foot_R = row_foot_R.column(align = 1)      
                col_foot_R.scale_x = 1
                col_foot_R.scale_y = 0.75
                col_foot_R.alignment = 'CENTER'  
                col_foot_R.operator("operator.foot_r", text="Foot R")
              
                # FootRoll R
                
                col_foot_roll_R = row_foot_R.column(align = 0)     
                col_foot_roll_R.scale_x = 0.5
                col_foot_roll_R.scale_y = 0.75
                col_foot_roll_R.alignment = 'CENTER'              
                col_foot_roll_R.operator("operator.foot_roll_ctrl_r", text="", icon = "LOOP_BACK", emboss = 0)         

                #Foot_L      
              
                col_foot_L = row_feet.column(align = 0)    
                col_foot_L.scale_x = 1
                col_foot_L.scale_y = 1
                col_foot_L.alignment = 'CENTER' 

                row_foot_L = col_foot_L.row(align = 1)     
                row_foot_L.scale_x = 1
                row_foot_L.scale_y = 1
                row_foot_L.alignment = 'CENTER' 

                # FootRoll L
                
                col_foot_roll_L = row_foot_L.column(align = 0)     
                col_foot_roll_L.scale_x = 0.5
                col_foot_roll_L.scale_y = 0.75
                col_foot_roll_L.alignment = 'CENTER'              
                col_foot_roll_L.operator("operator.foot_roll_ctrl_l", text="", icon = "LOOP_FORWARDS", emboss = 0)

                # Foot L
                
                col_foot_L = row_foot_L.column(align = 1)      
                col_foot_L.scale_x = 1
                col_foot_L.scale_y = 0.75
                col_foot_L.alignment = 'CENTER'  
                col_foot_L.operator("operator.foot_l", text="Foot R")

                  # Toes L

                col_toe_roll_1_L = row_foot_L.row(align = 1)       
                col_toe_roll_1_L.scale_x = 0.5
                col_toe_roll_1_L.scale_y = 0.75
                col_toe_roll_1_L.alignment = 'CENTER'             
                col_toe_roll_1_L.operator("operator.toe_roll_1_l", text="", icon = "LOOP_FORWARDS", emboss = 0)
                
                col_toe_1_L = row_foot_L.row(align = 1)    
                col_toe_1_L.scale_x = 0.75
                col_toe_1_L.scale_y = 0.75
                col_toe_1_L.alignment = 'CENTER'              
                col_toe_1_L.operator("operator.toe_1_fk_l", text="")

                col_toe_roll_2_L = row_foot_L.row(align = 1)       
                col_toe_roll_2_L.scale_x = 0.5
                col_toe_roll_2_L.scale_y = 0.75
                col_toe_roll_2_L.alignment = 'CENTER'             
                col_toe_roll_2_L.operator("operator.toe_roll_2_l", text="", icon = "LOOP_FORWARDS", emboss = 0)

                col_toe_2_L = row_foot_L.row(align = 1)    
                col_toe_2_L.scale_x = 0.75
                col_toe_2_L.scale_y = 0.75
                col_toe_2_L.alignment = 'CENTER'              
                col_toe_2_L.operator("operator.toe_2_fk_l", text="")
                      
                # Sole R

                row_sole = box_body.row(align = 0)  
                row_sole.scale_x = 1
                row_sole.scale_y = 1
                row_sole.alignment = 'CENTER'  
                
                row_sole_R = row_sole.row(align = 1)       
                row_sole_R.scale_x = 2
                row_sole_R.scale_y = 1
                row_sole_R.alignment = 'CENTER'  

                col_sole_R = row_sole_R.column(align = 1)      
                col_sole_R.scale_x = 1
                col_sole_R.scale_y = 0.75
                col_sole_R.alignment = 'CENTER'                   
                col_sole_R.operator("operator.sole_ctrl_r", text="Sole R")         
                
                col_sole_pivot_R = row_sole_R.column(align = 1)    
                col_sole_pivot_R.scale_x = 0.25
                col_sole_pivot_R.scale_y = 0.75
                col_sole_pivot_R.alignment = 'CENTER'                     
                col_sole_pivot_R.operator("operator.sole_pivot_point_r", text="")   
              
                # Sole L
                
                row_sole_L = row_sole.row(align = 1)       
                row_sole_L.scale_x = 2
                row_sole_L.scale_y = 1
                row_sole_L.alignment = 'CENTER'  

                col_sole_pivot_L = row_sole_L.column(align = 1)    
                col_sole_pivot_L.scale_x = 0.25
                col_sole_pivot_L.scale_y = 0.75
                col_sole_pivot_L.alignment = 'CENTER'                     
                col_sole_pivot_L.operator("operator.sole_pivot_point_l", text="")     

                col_sole_L = row_sole_L.column(align = 1)      
                col_sole_L.scale_x = 1
                col_sole_L.scale_y = 0.75
                col_sole_L.alignment = 'CENTER'                   
                col_sole_L.operator("operator.sole_ctrl_l", text="Sole R")         
              
                # Master
              
                row_master = box_body.row(align = 0)  
                row_master.scale_x = 5
                row_master.scale_y = 1
                row_master.alignment = 'CENTER' 
                row_master.separator

                col_master = row_master.column(align = 0)  
                col_master.scale_x = 1
                col_master.scale_y = 0.75
                col_master.alignment = 'CENTER' 
                col_master.separator()        
                col_master.operator("operator.master", text="Master") 
                col_master.separator() 
                col_master.separator()               

              # View

                row_view_main = box_body.row(align = 0)  
                row_view_main.scale_x = 1
                row_view_main.scale_y = 1
                row_view_main.alignment = 'CENTER'      
              
                row_view = row_view_main.row(align = 0)  
                row_view.scale_x = 1
                row_view.scale_y = 1
                row_view.alignment = 'CENTER'            
                row_view.operator("operator.zoom", text="Zoom to Selected", icon='ZOOM_IN')

                row_model_res = row_view_main.row(align = 0)  
                row_model_res.scale_x = 0.7
                row_model_res.scale_y = 1
                row_model_res.alignment = 'CENTER'  
                row_model_res.prop(arm_bones['properties'], '["model_res"]', "Model_Res", toggle=True)


                if props.gui_picker_body_props:                      
                 
                  # Sliders_R
                      
                    col_sliders_R = box_R.column()  
                    col_sliders_R.scale_x = 1
                    col_sliders_R.scale_y = 1
                    col_sliders_R.alignment = 'CENTER'              

                    col_space = col_sliders_R.column()
                    col_space.scale_x = 2.5
                    col_space.scale_y = 9
                    col_space.alignment = 'CENTER'  
                    col_space.separator()   
                    
                    col_head_props = col_sliders_R.column()
                    col_head_props.scale_x = 2.5
                    col_head_props.scale_y = 0.75
                    col_head_props.alignment = 'CENTER'   
                    col_head_props.label("HEAD")    
                    col_head_props.prop(arm_bones['properties_head'], 'ik_head', "IK/FK", toggle=True, icon_only = 1, emboss = 1)                           
                    col_head_props.prop(arm_bones['properties_head'], 'hinge_head', "Hinge", toggle=True, icon_only = 1, emboss = 1)  
                    col_head_props.prop(arm_bones['properties_head'], 'toon_head', "Str IK", toggle=True, icon_only = 1, emboss = 1)                               
                    
                    col_neck_props = col_sliders_R.column()
                    col_neck_props.scale_x = 2.5
                    col_neck_props.scale_y = 0.75
                    col_neck_props.alignment = 'CENTER'   
                    col_neck_props.label("NECK")                                                                               
                    col_neck_props.prop(arm_bones['properties_head'], 'hinge_neck', "Hinge", toggle=True, icon_only = 1, emboss = 1) 
                    
                    col_space = col_sliders_R.column()
                    col_space.scale_x = 2.5
                    col_space.scale_y = 9
                    col_space.alignment = 'CENTER'  
                    col_space.separator()    
                                        
                    col_arm_R_props = col_sliders_R.column()
                    col_arm_R_props.scale_x = 2.5
                    col_arm_R_props.scale_y = 0.75
                    col_arm_R_props.alignment = 'CENTER'   
                    col_arm_R_props.label("ARM_R")                                                                            
                    col_arm_R_props.prop(arm_bones['properties_arm_R'], 'ik_arm_R', "IK/FK", toggle=True, icon_only = 1, emboss = 1)                            
                    col_arm_R_props.prop(arm_bones['properties_arm_R'], 'hinge_arm_R', "Hinge", toggle=True, icon_only = 1, emboss = 1)  
                    col_arm_R_props.prop(arm_bones['properties_arm_R'], 'toon_arm_R', "Str IK", toggle=True, icon_only = 1, emboss = 1)                               

                    col_space = col_sliders_R.column()
                    col_space.scale_x = 2.5
                    col_space.scale_y = 8
                    col_space.alignment = 'CENTER'  
                    col_space.separator()  

                    col_hand_R_props = col_sliders_R.column()
                    col_hand_R_props.scale_x = 2.5
                    col_hand_R_props.scale_y = 0.75
                    col_hand_R_props.alignment = 'CENTER'   
                    col_hand_R_props.label("HAND_R")                                                                              
                    col_hand_R_props.prop(arm_bones['properties_arm_R'], 'hinge_hand_R', "Hinge", toggle=True, icon_only = 1, emboss = 1)                           

                    col_space = col_sliders_R.column()
                    col_space.scale_x = 2.5
                    col_space.scale_y = 4
                    col_space.alignment = 'CENTER'  
                    col_space.separator()  

                    col_fing_R_props = col_sliders_R.column()
                    col_fing_R_props.scale_x = 2.5
                    col_fing_R_props.scale_y = 0.75
                    col_fing_R_props.alignment = 'CENTER'   
                    col_fing_R_props.label("FING_R")                                                                              
                    col_fing_R_props.prop(arm_bones['properties_arm_R'], 'ik_fing_all_R', "IK/FK", toggle=True, icon_only = 1, emboss = 1)                          
                    col_fing_R_props.prop(arm_bones['properties_arm_R'], 'hinge_fing_all_R', "Hinge", toggle=True, icon_only = 1, emboss = 1)  

                    col_space = col_sliders_R.column()
                    col_space.scale_x = 2.5
                    col_space.scale_y = 4
                    col_space.alignment = 'CENTER'  
                    col_space.separator()  

                    col_leg_R_props = col_sliders_R.column()
                    col_leg_R_props.scale_x = 2.5
                    col_leg_R_props.scale_y = 0.75
                    col_leg_R_props.alignment = 'CENTER'   
                    col_leg_R_props.label("LEG_R")                                                                            
                    col_leg_R_props.prop(arm_bones['properties_leg_R'], 'ik_leg_R', "IK/FK", toggle=True, icon_only = 1, emboss = 1)                            
                    col_leg_R_props.prop(arm_bones['properties_leg_R'], 'hinge_leg_R', "Hinge", toggle=True, icon_only = 1, emboss = 1)  
                    col_leg_R_props.prop(arm_bones['properties_leg_R'], 'toon_leg_R', "Str IK", toggle=True, icon_only = 1, emboss = 1)  
                  
                    col_space = col_sliders_R.column()
                    col_space.scale_x = 2.5
                    col_space.scale_y = 3
                    col_space.alignment = 'CENTER'  
                    col_space.separator()  

                    col_foot_R_props = col_sliders_R.column()
                    col_foot_R_props.scale_x = 2.5
                    col_foot_R_props.scale_y = 0.75
                    col_foot_R_props.alignment = 'CENTER'   
                    col_foot_R_props.label("TOES_R")                                                                              
                    col_foot_R_props.prop(arm_bones['properties_leg_R'], 'ik_toes_all_R', "IK/FK", toggle=True, icon_only = 1, emboss = 1)   
                    col_foot_R_props.prop(arm_bones['properties_leg_R'], 'hinge_toes_all_R', "Hinge", toggle=True, icon_only = 1, emboss = 1)                          

                  # Sliders_L
              
                    col_sliders_L = box_L.column()  
                    col_sliders_L.scale_x = 1
                    col_sliders_L.scale_y = 1
                    col_sliders_L.alignment = 'CENTER'              

                    col_space = col_sliders_L.column()
                    col_space.scale_x = 2.5
                    col_space.scale_y = 36
                    col_space.alignment = 'CENTER'  
                    col_space.separator()
                                              
                    col_arm_L_props = col_sliders_L.column()
                    col_arm_L_props.scale_x = 2.5
                    col_arm_L_props.scale_y = 0.75
                    col_arm_L_props.alignment = 'CENTER'   
                    col_arm_L_props.label("ARM_L")                                                                            
                    col_arm_L_props.prop(arm_bones['properties_arm_L'], 'ik_arm_L', "IK/FK", toggle=True, icon_only = 1, emboss = 1)                            
                    col_arm_L_props.prop(arm_bones['properties_arm_L'], 'hinge_arm_L', "Hinge", toggle=True, icon_only = 1, emboss = 1)  
                    col_arm_L_props.prop(arm_bones['properties_arm_L'], 'toon_arm_L', "Str IK", toggle=True, icon_only = 1, emboss = 1)                               

                    col_space = col_sliders_L.column()
                    col_space.scale_x = 2.5
                    col_space.scale_y = 8
                    col_space.alignment = 'CENTER'  
                    col_space.separator()  

                    col_hand_L_props = col_sliders_L.column()
                    col_hand_L_props.scale_x = 2.5
                    col_hand_L_props.scale_y = 0.75
                    col_hand_L_props.alignment = 'CENTER'   
                    col_hand_L_props.label("HAND_L")                                                                              
                    col_hand_L_props.prop(arm_bones['properties_arm_L'], 'hinge_hand_L', "Hinge", toggle=True, icon_only = 1, emboss = 1)                           

                    col_space = col_sliders_L.column()
                    col_space.scale_x = 2.5
                    col_space.scale_y = 4
                    col_space.alignment = 'CENTER'  
                    col_space.separator()  

                    col_fing_L_props = col_sliders_L.column()
                    col_fing_L_props.scale_x = 2.5
                    col_fing_L_props.scale_y = 0.75
                    col_fing_L_props.alignment = 'CENTER'   
                    col_fing_L_props.label("FING_L")                                                                              
                    col_fing_L_props.prop(arm_bones['properties_arm_L'], 'ik_fing_all_L', "IK/FK", toggle=True, icon_only = 1, emboss = 1)                          
                    col_fing_L_props.prop(arm_bones['properties_arm_L'], 'hinge_fing_all_L', "Hinge", toggle=True, icon_only = 1, emboss = 1)  

                    col_space = col_sliders_L.column()
                    col_space.scale_x = 2.5
                    col_space.scale_y = 4
                    col_space.alignment = 'CENTER'  
                    col_space.separator()  

                    col_leg_L_props = col_sliders_L.column()
                    col_leg_L_props.scale_x = 2.5
                    col_leg_L_props.scale_y = 0.75
                    col_leg_L_props.alignment = 'CENTER'   
                    col_leg_L_props.label("LEG_L")                                                                            
                    col_leg_L_props.prop(arm_bones['properties_leg_L'], 'ik_leg_L', "IK/FK", toggle=True, icon_only = 1, emboss = 1)                            
                    col_leg_L_props.prop(arm_bones['properties_leg_L'], 'hinge_leg_L', "Hinge", toggle=True, icon_only = 1, emboss = 1)  
                    col_leg_L_props.prop(arm_bones['properties_leg_L'], 'toon_leg_L', "Str IK", toggle=True, icon_only = 1, emboss = 1)  
                  
                    col_space = col_sliders_L.column()
                    col_space.scale_x = 2.5
                    col_space.scale_y = 3
                    col_space.alignment = 'CENTER'  
                    col_space.separator()  

                    col_foot_L_props = col_sliders_L.column()
                    col_foot_L_props.scale_x = 2.5
                    col_foot_L_props.scale_y = 0.75
                    col_foot_L_props.alignment = 'CENTER'   
                    col_foot_L_props.label("TOES_L")                                                                              
                    col_foot_L_props.prop(arm_bones['properties_leg_L'], 'ik_toes_all_L', "IK/FK", toggle=True, icon_only = 1, emboss = 1)       
                    col_foot_L_props.prop(arm_bones['properties_leg_L'], 'hinge_toes_all_L', "Hinge", toggle=True, icon_only = 1, emboss = 1)                      

                col_snap = box.column()
                col_snap.alignment ='LEFT'
                col_snap.prop(props, "gui_snap", text="IK/FK SNAPPING")                
                
                if props.gui_snap:
                    col_snap.prop(props, "gui_snap_all", text="ALL")                      
                    
                    if is_selected(head) or props.gui_snap_all:

                        box = col_snap.column()    
                        box.label("SNAP HEAD")                      
                        col = box.column()
                        row = col.row() 
                        col2 = row.column()        
                        row.operator("head_snap.fk_ik", text="FK >> IK", icon="NONE")  
                        col2.operator("head_snap.ik_fk", text="IK >> FK", icon="NONE")  
                        
                    if is_selected(torso) or props.gui_snap_all:      
                        box = col_snap.column()    
                        box.label("SNAP TORSO")                      
                        col = box.column()
                        row = col.row() 
                        col2 = row.column()  
                        row.operator("torso_snap.fk_ik", text="FK >> IK", icon="NONE")  
                        col2.operator("torso_snap.ik_fk", text="IK >> FK", icon="NONE") 
                        row = col.row() 
                        col2 = row.column()             
                        row.operator("torso_snap.up_inv", text="UP >> INV", icon="NONE")  
                        col2.operator("torso_snap.inv_up", text="INV >> UP", icon="NONE") 
                                                                              
                    if is_selected(arm_l + hand_l) or props.gui_snap_all:  
                        box = col_snap.column()    
                        box.label("SNAP ARM LEFT")                    
                        col = col_snap.column()
                        row = col.row() 
                        col2 = row.column()          
                        row.operator("arm_l_snap.fk_ik", text="FK >> IK", icon="NONE")  
                        col2.operator("arm_l_snap.ik_fk", text="IK >> FK", icon="NONE")  
                        
                    if is_selected(arm_r + hand_r) or props.gui_snap_all:   
                        box = col_snap.column()    
                        box.label("SNAP ARM RIGHT")                      
                        col = col_snap.column()
                        row = col.row() 
                        col2 = row.column()        
                        row.operator("arm_r_snap.fk_ik", text="FK >> IK", icon="NONE")  
                        col2.operator("arm_r_snap.ik_fk", text="IK >> FK", icon="NONE")                     
                                    
                    if is_selected(leg_l + foot_l) or props.gui_snap_all:   
                        box = col_snap.column()    
                        box.label("SNAP LEG LEFT")                      
                        col = col_snap.column()
                        row = col.row() 
                        col2 = row.column()               
                        row.operator("leg_l_snap.fk_ik", text="FK >> IK", icon="NONE")  
                        col2.operator("leg_l_snap.ik_fk", text="IK >> FK", icon="NONE")                  
                                         
                    if is_selected(leg_r + foot_r) or props.gui_snap_all:  
                        box = col_snap.column()   
                        box.label("SNAP LEG RIGHT")                       
                        col = col_snap.column()
                        row = col.row() 
                        col2 = row.column()         
                        row.operator("leg_r_snap.fk_ik", text="FK >> IK", icon="NONE")  
                        col2.operator("leg_r_snap.ik_fk", text="IK >> FK", icon="NONE")    
                    
                col_snap.separator()   
                col_snap.separator()                                       
            # collapsed box        
            elif "gui_picker_body" in arm:
                row.operator("gui.blenrig_5_tabs", icon="RIGHTARROW", emboss = 0).tab = "gui_picker_body"
                row.label(text="BLENRIG PICKER", icon='MOD_ARMATURE')

                
################ FACE #######################################
            
        
            if "gui_picker_face" in arm:  
                box = layout.column()
                col = box.column()
                row = col.row() 
            # expanded box            
            if "gui_picker_face" in arm and arm["gui_picker_face"]:
                row.operator("gui.blenrig_5_tabs", icon="DOWNARROW_HLT", emboss = 0).tab = "gui_picker_face"
                row.label(text="FACE", icon='MONKEY')
                box.separator()
                col_smile = col.column()
                col_smile.label("Follow Smile")
                col_smile.prop(arm_bones['properties_head'], '["toon_teeth_up"]', "Teeth_Upper", slider=True)
                col_smile.prop(arm_bones['properties_head'], '["toon_teeth_low"]', "Teeth_Lower", slider=True)            
      
            # collapsed box 
          
            elif "gui_picker_face" in arm:
                row.operator("gui.blenrig_5_tabs", icon="RIGHTARROW", emboss = 0).tab = "gui_picker_face"
                row.label(text="FACE", icon='MOD_MASK')
          
########### Extra Properties
            if "gui_misc" in arm:
                box = layout.column()
                col = box.column()
                row = col.row()
            # expanded box
            if "gui_misc" in arm and arm["gui_misc"]:
                row.operator("gui.blenrig_5_tabs", icon="DOWNARROW_HLT", emboss = 0).tab = "gui_misc"
                row.label(text="EXTRA PROPERTIES", icon='SETTINGS')

                # Head Accessories
                col = box.column()
                row_rot = col.row()                               
                col_rot = row_rot.column()        
                if act_bone is not None:
                    for cust_prop in act_bone.keys():
                        if cust_prop == 'ROT_MODE':
                            col_rot.separator()                     
                            col_rot.label(text = 'ACTIVE BONE ROTATION ORDER', icon = "AXIS_TOP")    
                            box_rot = col_rot.box()                                                  
                            box_rot.prop(act_bone, '["ROT_MODE"]', toggle=True)   
                            col_rot.separator()      
                            col_rot.separator()                   

                row_props = col.row()  
                col_props = row_props.column()                 
                col_props.label(text ='CUSTOM PROPERTIES', icon = "BONE_DATA")                 
                row_all = col_props.row()
                row_all.alignment = "LEFT"
                row_all.prop(props, "gui_cust_props_all", text="All")    
                col_props.separator()               
                if not props.gui_cust_props_all:
                    if act_bone is not None:                    
                        for cust_prop in act_bone.keys():
                            excluded = ['_RNA_UI', 'ROT_MODE', 'model_res', 'muscle_system', 'muscle_res', 'deformation_extras', 'reproportion', 'rj_legs', 'rj_hands', 'rj_feet', 'rj_arms', 'hinge_head', 'hinge_neck', 'ik_head', 'look_switch', 'toon_head', 'toon_teeth_low', 'toon_teeth_up', 'hinge_arm_R', 'hinge_hand_R', 'ik_arm_R', 'toon_arm_R', 'hinge_arm_L', 'hinge_hand_L', 'ik_arm_L', 'toon_arm_L', 'inv_torso', 'ik_torso', 'toon_torso', 'ik_leg_L', 'ik_toes_all_L', 'hinge_leg_L', 'toon_leg_L', 'ik_leg_R', 'ik_toes_all_R', 'hinge_leg_R', 'toon_leg_R']
                            if (cust_prop not in excluded):
                                box_props = col_props.box()
                                box_props.prop(act_bone, '["{}"]'.format(cust_prop))                            
                if props.gui_cust_props_all:         
                    for b in arm_bones:
                        excluded_bones = ['properties', 'properties_leg_L', 'properties_leg_R', 'properties_torso', 'properties_arm_L', 'properties_arm_R', 'properties_head']
                        if (b.name not in excluded_bones):      
                            for cust_prop in b.keys():
                                if cust_prop != '_RNA_UI' and cust_prop != 'ROT_MODE':  
                                    box_props = col_props.box()                                                                
                                    box_props.prop(b, '["{}"]'.format(cust_prop), text = '["{} {}"]'.format(b.name, cust_prop))                      
                col_props.separator()

            # collapsed box
            elif "gui_misc" in arm:
                row.operator("gui.blenrig_5_tabs", icon="RIGHTARROW", emboss = 0).tab = "gui_misc"
                row.label(text="EXTRA PROPERTIES", icon='SETTINGS')

########### Muscle System box
            if "gui_muscle" in arm:
                box = layout.column()
                col = box.column()
                row = col.row()
            # expanded box
            if "gui_muscle" in arm and arm["gui_muscle"]:
                row.operator("gui.blenrig_5_tabs", icon="DOWNARROW_HLT", emboss = 0).tab = "gui_muscle"
                row.label("MUSCLE SYSTEM", icon = 'FORCE_LENNARDJONES')
                # System Toggle
                col = box.column()
                row = col.row()
                row.label("Off")
                row = row.row()
                row.alignment = "RIGHT"
                row.label("On")
                col.prop(arm_bones['properties'], '["muscle_system"]', "Muscles", toggle=True)

                box.separator()

                # Resolution
                col = box.column()
                col.prop(arm_bones['properties'], '["muscle_res"]', "Muscle Resolution", toggle=True)

                box.separator()

                # Extras Deformation
                col = box.column()
                col.prop(arm_bones['properties'], '["deformation_extras"]', "Deformation Extras", toggle=True)              

            # collapsed box
            elif "gui_muscle" in arm:
                row.operator("gui.blenrig_5_tabs", icon="RIGHTARROW", emboss = 0).tab = "gui_muscle"
                row.label("MUSCLE SYSTEM", icon = 'FORCE_LENNARDJONES')
                            
####### Rigging & Baking
            if "gui_bake" in arm:
                box = layout.column()
                col = box.column()
                row = col.row()
            # expanded box                
            if "gui_bake" in arm and arm["gui_bake"]:
                row.operator("gui.blenrig_5_tabs", icon="DOWNARROW_HLT", emboss = 0).tab = "gui_bake"                    
                row.label(text="RIGGING & BAKING", icon='SCRIPTWIN')
                col.separator
                col.prop(arm, 'reproportion', "Reproportion Mode", toggle=True, icon_only=True, icon='SCRIPTWIN')               
                col.separator()
                col.label("CHARACTER BAKING")
                row = col.row()
                row.operator("blenrig5.armature_baker", text="Bake Armature")                
                row.operator("blenrig5.mesh_pose_baker", text="Bake Mesh")
                row.prop(context.window_manager, "bake_to_shape") 
                row.operator("blenrig5.reset_hooks", text="Reset Hooks")                  
                row = col.row()
#                row.operator("armature.full_bake", text="Full Bake")
                col.separator()
                col.label("ARMATURE EXTRAS")
                split = col.split()
                row = split.row()
                row.operator("armature.reset_constraints")
                row.operator("blenrig5.reset_deformers", text="Reset Deformers")                 
                col.separator()
                col.label("REALISTIC JOINTS")           
                col.separator()
                if "rj_arms" in armobj and armobj["rj_arms"]:   
                    col.prop(armobj, '["rj_arms"]', "Arms", slider=True)    
                    col.prop(armobj, '["rj_hands"]', "Hands", slider=True)   
                    col.prop(armobj, '["rj_legs"]', "Legs", slider=True)   
                    col.prop(armobj, '["rj_feet"]', "Feet", slider=True)       
                    col.separator()
                if "rig_name" in arm and arm["rig_name"]:               
                    col.label("RIGGING LAYERS")
                    col.prop(context.active_object.data, "layers", index=15, toggle=True, text="WP Bones")
                    col.separator()
                    body = col.row()
                    body.prop(arm, "layers", index=7 , toggle=True, text="REPROPORTION")                                                 
                      
                
            else:
                row.operator("gui.blenrig_5_tabs", icon="RIGHTARROW", emboss = 0).tab = "gui_bake"
                row.label(text="RIGGING & BAKING", icon='SCRIPTWIN')
                
####### Rigging & Baking for MESH and 

        if blenrig_5 == False:
            box = layout.column()
            col = box.column()
            row = col.row()
        # expanded box                                
            row.label(text="RIGGING & BAKING", icon='SCRIPTWIN')
            col.separator()
            col.label("CHARACTER BAKING")
            row = col.row()
            row.operator("blenrig5.armature_baker", text="Bake Armature")            
            row.operator("blenrig5.mesh_pose_baker", text="Bake Mesh")
            row.prop(context.window_manager, "bake_to_shape")    
            row.operator("blenrig5.reset_hooks", text="Reset Hooks")            
            row = col.row()
#                row.operator("armature.full_bake", text="Full Bake")
            col.separator()
            col.label("ARMATURE EXTRAS")
            split = col.split()
            row = split.row()
            row.operator("armature.reset_constraints")    
            row.operator("blenrig5.reset_deformers", text="Reset Deformers")                                   


################################# BAKING OPERATORS ##########################################################


# Mesh Proportions Baker operator
class ARMATURE_OT_mesh_pose_baker(bpy.types.Operator):
    bl_label = "BlenRig 5 Mesh Baker"
    bl_idname = "blenrig5.mesh_pose_baker"
    bl_description = "Bake current pose to mesh"
    bl_options = {'REGISTER', 'UNDO'}       
        
    @classmethod
    def poll(cls, context):
        if not bpy.context.object:
            return False
        return (bpy.context.object.type == "MESH" and context.mode=='OBJECT')
   
    #Baking   
    def bake(self, context):
        if not bpy.context.object:
            return False        
        old_ob = bpy.context.active_object
        bake_meshes = [ob.name for ob in bpy.context.selected_objects if ob.type=="MESH"]

        for name in bake_meshes:
            if name in bpy.data.objects:
                ob = bpy.data.objects[name]
                
            bpy.context.scene.objects.active = ob
            
            # Turn off SUBSURF for baking
            for mod in ob.modifiers:
                if mod.type == 'SUBSURF':
                    old_state = mod.show_viewport
                    mod.show_viewport = False
            
            
            # --- get a mesh from the object ---
            apply_modifiers = True
            settings = 'PREVIEW'
            mesh = ob.to_mesh(bpy.context.scene, apply_modifiers, settings)            
            
            for mod in ob.modifiers:
                if mod.type == 'SUBSURF':
                    mod.show_viewport = old_state

            # If Bake to shape option is off                  
            if bpy.context.window_manager.bake_to_shape == False:  
                # Check if there are shapekeys in object  
                try:        
                    if ob.data.shape_keys.key_blocks:
                        key = ob.data.shape_keys
                        shapekeys = key.key_blocks                
                        # Transfer vertex locations to Basis key
                        for vert in ob.data.vertices:
                            shapekeys['Basis'].data[vert.index].co = mesh.vertices[vert.index].co 

                        # Make baked shape active
                        for i in range(len(shapekeys)):
                            shape = shapekeys[i]
                            if shape.name == 'Basis':
                                ob.active_shape_key_index = i
                except (AttributeError):
                    # Transfer vertex locations to Mesh                
                    for vert in ob.data.vertices:
                        vert.co = mesh.vertices[vert.index].co 

            # If Bake to shape option is on  
            else:   
                
                # Check if there are shapekeys in object
                try:
                    ob.data.shape_keys.key_blocks
                except (AttributeError):
                    Basis = ob.shape_key_add(from_mix=False)
                    Basis.name = 'Basis'
                    
                # Create new shape for storing the bake

                baked_shape = ob.shape_key_add(from_mix=False)
                baked_shape.name = 'Baked_shape'
                baked_shape.value = 1

                # Transfer vertex locations
                for vert in ob.data.vertices:
                    baked_shape.data[vert.index].co = mesh.vertices[vert.index].co 

                # Make baked shape active
                for i in range(len(ob.data.shape_keys.key_blocks)):
                    shape = ob.data.shape_keys.key_blocks[i]
                    if shape.name == baked_shape.name:
                        ob.active_shape_key_index = i
                   
                            
        # Remove unused baked mesh               
        bpy.data.meshes.remove(mesh)                         
        
        bpy.context.scene.objects.active = old_ob
               
        
    #Unbind Mdef modifier if object is bound    
    def mdef_unbind(self, context):
        if not bpy.context.object:
            return False        
        
        old_ob = bpy.context.active_object
        
        bake_meshes = [ob.name for ob in bpy.context.selected_objects if ob.type=="MESH"]
        for name in bake_meshes:
            if name in bpy.data.objects:
                ob = bpy.data.objects[name]
            bpy.context.scene.objects.active = ob
           
            # unbind mdef modifiers
            for i in range(len(ob.modifiers)):
                mod = ob.modifiers[i]
                if mod.type in ['MESH_DEFORM']:
                    if mod.is_bound == True:
                        bpy.ops.object.meshdeform_bind(modifier=mod.name)      
                             
        bpy.context.scene.objects.active = old_ob                           

    def execute(self, context):
        self.bake(context)     
        self.mdef_unbind(context)  
        self.report({'INFO'}, "Baking done")
        return{'FINISHED'}   

# Hook Reset operator
class ARMATURE_OT_reset_hooks(bpy.types.Operator):
    bl_label = "BlenRig 5 Reset Hooks"
    bl_idname = "blenrig5.reset_hooks"
    bl_description = "Reset Hooks on Lattices and Curves"
    bl_options = {'REGISTER', 'UNDO'}       

    @classmethod
    def poll(cls, context):
        if not bpy.context.object:
            return False
        return (bpy.context.object.type == "LATTICE", "CURVE" and context.mode=='OBJECT')
   
    def reset_hooks(self,context):
        
        selected_lattices = [ob.name for ob in bpy.context.selected_objects if ob.type=="LATTICE"]

        for name in selected_lattices:
            if name in bpy.data.objects:
                ob = bpy.data.objects[name]
                
            bpy.context.scene.objects.active = ob

            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.lattice.select_all(action='SELECT')
            for mod in ob.modifiers:
                if mod.type == 'HOOK':
                    bpy.ops.object.hook_reset(modifier=mod.name)
            bpy.ops.object.mode_set(mode='OBJECT')      

        selected_curves = [ob.name for ob in bpy.context.selected_objects if ob.type=="CURVE"]

        for name in selected_curves:
            if name in bpy.data.objects:
                ob = bpy.data.objects[name]
                
            bpy.context.scene.objects.active = ob

            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.curve.select_all(action='SELECT')
            for mod in ob.modifiers:
                if mod.type == 'HOOK':
                    bpy.ops.object.hook_reset(modifier=mod.name)
            bpy.ops.object.mode_set(mode='OBJECT')                         

    def execute(self, context):
        self.reset_hooks(context)     
        self.report({'INFO'}, "Hooks Reseted")
        return{'FINISHED'}   

# Reset Armature related Lattices and Curves operator
class ARMATURE_OT_reset_deformers(bpy.types.Operator):
    bl_label = "BlenRig 5 Reset Deformers"
    bl_idname = "blenrig5.reset_deformers"
    bl_description = "Reset Armature related Lattices and Curves"
    bl_options = {'REGISTER', 'UNDO'}       
    
    @classmethod
    def poll(cls, context):
        if not bpy.context.object:
            return False
        else:
            return (bpy.context.object.type == "ARMATURE")
    
    def reset_deformers(self, context):
 
        # preparing scene
        bpy.ops.object.mode_set(mode='OBJECT')
        old_active = bpy.context.active_object
        old_selected = bpy.context.selected_objects
        old_layers = [i for i in bpy.context.scene.layers]
        for ob in old_selected:
            ob.select = False
                            
        # Armature related lattices and curves
        
        selected_deformers = []
        
        for ob in bpy.data.objects:
            if ob.type in 'LATTICE' or 'CURVE':
                for mod in ob.modifiers:
                    if mod.type in 'HOOK':
                        if mod.object.name == bpy.context.object.name:
                            # Toggle on active layers
                            for i in range(len(ob.layers)):
                                layer = ob.layers[i]
                                if layer == True:
                                    bpy.context.scene.layers[i] = True                                    
                            ob.select = True
                            selected_deformers.append(ob.name)
                                 
        for name in selected_deformers:
            if name in bpy.data.objects:
                ob = bpy.data.objects[name]
                
            bpy.context.scene.objects.active = ob

        # Reset Hooks
        bpy.ops.blenrig5.reset_hooks()                               
                     
        #Back to Armature
        for ob in bpy.context.selected_objects:
            ob.select = False
        bpy.context.scene.layers = old_layers
        bpy.context.scene.objects.active = old_active
        for ob in old_selected:
            ob.select = True        
        bpy.ops.object.mode_set(mode='POSE')  
        #Hack for updating objects
        bpy.context.scene.frame_set(bpy.context.scene.frame_current)                                                   

    def execute(self, context):
        self.reset_deformers(context)
        self.report({'INFO'}, "Lattices and Curves Reset")
        return{'FINISHED'}
        


# Armature Baker operator
class ARMATURE_OT_armature_baker(bpy.types.Operator):
    bl_label = "BlenRig 5 Armature Baker"
    bl_idname = "blenrig5.armature_baker"
    bl_description = "Bake current pose to armature"
    bl_options = {'REGISTER', 'UNDO'}       
    
    @classmethod
    def poll(cls, context):
        if not bpy.context.object:
            return False
        else:
            return (bpy.context.object.type == "ARMATURE")
    
    def bake_armature(self, context):
 
        # preparing scene
        bpy.ops.object.mode_set(mode='OBJECT')
        old_active = bpy.context.active_object
        old_selected = bpy.context.selected_objects
        old_layers = [i for i in bpy.context.scene.layers]
        for ob in old_selected:
            ob.select = False

                
        # unparenting external objects related to the armature
        parent_pairs = []
        for ob in bpy.data.objects:
            if ob.parent is not None:
                if ob.parent.name == bpy.context.object.name:           
                    # Toggle on active layers
                    for i in range(len(ob.layers)):
                        layer = ob.layers[i]
                        if layer == True:
                            bpy.context.scene.layers[i] = True       
                    ob.select = True
                    parent_pairs.append([ob, ob.parent, ob.parent_bone])
                    bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
                    
        #Back to Armature
        for ob in bpy.context.selected_objects:
            ob.select = False
        bpy.context.scene.layers = old_layers
        bpy.context.scene.objects.active = old_active
        for ob in old_selected:
            ob.select = True                         
        
        bpy.ops.object.mode_set(mode='POSE')
        posebones = bpy.context.object.pose.bones
        
        # Bake Armature
        bpy.ops.pose.armature_apply()
        
        arm = bpy.context.object.data
        
        # Reset Constraints
        for b in posebones:
            for con in b.constraints:
                if con.type not in ['LIMIT_DISTANCE', 'STRETCH_TO', 'CHILD_OF']:
                    continue
                if con.type == 'LIMIT_DISTANCE':
                    con.distance = 0
                elif con.type == 'STRETCH_TO':
                    con.rest_length = 0
                elif con.type == 'CHILD_OF':
                    bpy.ops.object.mode_set(mode='EDIT')
                    arm.edit_bones.active = arm.edit_bones[b.name]
                    bpy.ops.object.mode_set(mode='POSE')
                    print ('"{}"'.format(con.name))
                    bpy.ops.constraint.childof_clear_inverse(constraint=con.name, owner='BONE')
                    bpy.ops.constraint.childof_set_inverse(constraint=con.name, owner='BONE')
                    # somehow it only works if you run it twice
                    bpy.ops.constraint.childof_set_inverse(constraint=con.name, owner='BONE')
                    bpy.ops.object.mode_set(mode='EDIT')
                    arm.edit_bones[b.name].select = False
        bpy.ops.object.mode_set(mode='OBJECT')
        for ob in bpy.context.selected_objects:
            ob.select = False        
        
        # re-parenting external objects related to the armature
        for pp in parent_pairs:
            ob, parent, bone = pp
            ob.parent = parent
            ob.parent_type = 'BONE'
            ob.parent_bone == bone 
            #Reseting Hooks
            ob.select = True  
            bpy.ops.blenrig5.reset_hooks()    
            
        #Back to Armature
        for ob in bpy.context.selected_objects:
            ob.select = False
        bpy.context.scene.layers = old_layers
        bpy.context.scene.objects.active = old_active
        for ob in old_selected:
            ob.select = True                         
        
        bpy.ops.object.mode_set(mode='POSE')                  
             
                       

    def execute(self, context):
        self.bake_armature(context)
        self.report({'INFO'}, "Baking done")
        return{'FINISHED'}



# Full Bake operator
class ARMATURE_OT_full_bake(bpy.types.Operator):
    bl_label = "Full Bake"
    bl_idname = "armature.full_bake"
    bl_description = "Full automatic proportion and armature baking"
    bl_options = {'REGISTER', 'UNDO'}        
    
    @classmethod
    def poll(cls, context):
        return bpy.context.active_object

    def full_bake(self, context):
        # preparing scene
        bpy.ops.object.mode_set(mode='OBJECT')
        old_active = bpy.context.active_object
        old_selected = bpy.context.selected_objects
        old_layers = [i for i in bpy.context.scene.layers]
        for ob in old_selected:
            ob.select = False
                            
        # Character Objects Lists

        mdef_cages = []
        armature_obj = []
        character_models = []

        # Armature objects
        for ob in bpy.data.objects:
            if ob.type in 'MESH':
                for mod in ob.modifiers:
                    if mod.type in 'ARMATURE':        
                        if mod.object.name == bpy.context.object.name:
                            armature_obj.append(ob.name)                 
        # Mesh Deform cages
        for name in armature_obj:
            if name in bpy.data.objects:
                ob = bpy.data.objects[name] 
                for mod in ob.modifiers:       
                    if mod.type in 'MESH_DEFORM':
                        mdef_cages.append(mod.object.name)

        # Character models
        # Mdef only models
        for ob in bpy.data.objects:
            if ob.type in 'MESH':
                for mod in ob.modifiers:
                    if mod.type in 'MESH_DEFORM':
                        if mod.object.name in mdef_cages:
                            if ob.name not in armature_obj:
                                character_models.append(ob.name)
        # Append models that have Armature Modifier                        
        for name in armature_obj:
            if name not in mdef_cages:
                character_models.append(name)
                                                                     
                        

        # Character model baking
        for name in character_models:
            if name in bpy.data.objects:
                ob = bpy.data.objects[name]
                # Toggle on active layers
                for i in range(len(ob.layers)):
                    layer = ob.layers[i]
                    if layer == True:
                        bpy.context.scene.layers[i] = True  
                ob.select = True
                
            bpy.context.scene.objects.active = ob

        bpy.ops.blenrig5.mesh_pose_baker()

        # Mesh Deform cages baking
        for ob in bpy.context.selected_objects:
            ob.select = False
        for name in mdef_cages:
            if name in bpy.data.objects:
                ob = bpy.data.objects[name]
                # Toggle on active layers
                for i in range(len(ob.layers)):
                    layer = ob.layers[i]
                    if layer == True:
                        bpy.context.scene.layers[i] = True  
                ob.select = True
                
            bpy.context.scene.objects.active = ob

        bpy.ops.blenrig5.mesh_pose_baker()

        #Back to Armature
        for ob in bpy.context.selected_objects:
            ob.select = False
        bpy.context.scene.layers = old_layers
        bpy.context.scene.objects.active = old_active
        for ob in old_selected:
            ob.select = True                         

        bpy.ops.object.mode_set(mode='POSE')

        # Bake Armature
        bpy.ops.blenrig5.armature_baker()

    def execute(self, context):
        self.full_bake(context)
        self.report({'INFO'}, "Full Baking done")
        return{'FINISHED'}

# Reset Constraints Operator
class ARMATURE_OT_reset_constraints(bpy.types.Operator):
    bl_label = "Reset Constraints"
    bl_idname = "armature.reset_constraints"
    bl_description = "Reset all posebone constraints"
    
    @classmethod
    def poll(cls, context):
        if not bpy.context.object:
            return False
        else:
            return (bpy.context.object.type=='ARMATURE' and \
                context.mode=='POSE')
    
    def invoke(self, context, event):
        pbones = context.active_object.pose.bones
        if len(pbones) < 1:
            self.report({'INFO'}, "No bones found")
            return{'FINISHED'}
        
        amount = 0
        for pbone in pbones:
            for con in pbone.constraints:
                if con.type == 'LIMIT_DISTANCE':
                    amount += 1
                    con.distance = 0
                elif con.type == 'STRETCH_TO':
                    amount += 1
                    con.rest_length = 0
#                elif con.type == 'CHILD_OF':
#                    bpy.ops.object.mode_set(mode='EDIT')
#                    arm.edit_bones.active = arm.edit_bones[b.name]
#                    bpy.ops.object.mode_set(mode='POSE')
#                    bpy.ops.constraint.childof_clear_inverse(constraint=con.name, owner='BONE')
#                    bpy.ops.constraint.childof_set_inverse(constraint=con.name, owner='BONE')
#                    # somehow it only works if you run it twice
#                    bpy.ops.constraint.childof_set_inverse(constraint=con.name, owner='BONE')
#                    bpy.ops.object.mode_set(mode='EDIT')
#                    arm.edit_bones[b.name].select = False       
#                    bpy.ops.object.mode_set(mode='POSE')                                 
        self.report({'INFO'}, str(amount) + " constraints reset")
        
        return{'FINISHED'}


##################################### Bone Alignment Operators #######################################

class Operator_BlenRig_Fix_Misaligned_Bones(bpy.types.Operator):    
    
    bl_idname = "blenrig_fix_misaligned.bones"   
    bl_label = "BlenRig Fix Misaligned Bones"   
    bl_description = "Fixes misaligned bones after baking"    
    bl_options = {'REGISTER', 'UNDO',}     

    @classmethod
    def poll(cls, context):
        if not bpy.context.object:
            return False
        else:
            return (bpy.context.object.type=='ARMATURE' and context.mode=='EDIT_ARMATURE')  
    
    active_layers = []
    
    def all_layers(self, context):
        arm = bpy.context.active_object
        arm_data = arm.data          
        for i in range(len(arm_data.layers)):
            layers_status = arm_data.layers[i]
            if layers_status.real == 1:
                self.active_layers.append(i)

            
        #Turn on all layers
        arm_data.layers = [(x in [x]) for x in range(32)]  
      
    def match_heads_tails(self, context):
        arm = bpy.context.active_object
        arm_data = arm.data        
        bones = arm_data.edit_bones
        bpy.ops.object.mode_set(mode='EDIT')        
        bpy.ops.armature.reveal()
        bpy.ops.armature.select_all(action='DESELECT')      
        #Match heads           
        for b in bones:
            if arm_data.use_mirror_x == True:
                if '_R' not in b.name:
                    if b['b_head']:
                        for t in bones:
                            if (t.name == b['b_head'][0]):
                                if b['b_head'][1] == 'head':
                                    b.head = t.head
                                if b['b_head'][1] == 'tail':
                                    b.head = t.tail      
        #Match tails   
                if '_R' not in b.name:                            
                    if b['b_tail']:
                        for t in bones:
                            if (t.name == b['b_tail'][0]):
                                if b['b_tail'][1] == 'head':
                                    b.tail = t.head
                                if b['b_tail'][1] == 'tail':
                                    b.tail = t.tail  
                #X-mirror                    
                if '_L' in b.name:
                    b.select = 1
                    b.select_head = 1
                    b.select_tail = 1
                    bpy.ops.armature.symmetrize(direction='NEGATIVE_X')  
                    bpy.ops.armature.select_all(action='DESELECT')                                                      
            else:
                if b['b_head']:
                    for t in bones:
                        if (t.name == b['b_head'][0]):
                            if b['b_head'][1] == 'head':
                                b.head = t.head
                            if b['b_head'][1] == 'tail':
                                b.head = t.tail                                                                            
        #Match tails                 
                if b['b_tail']:
                    for t in bones:
                        if (t.name == b['b_tail'][0]):
                            if b['b_tail'][1] == 'head':
                                b.tail = t.head
                            if b['b_tail'][1] == 'tail':
                                b.tail = t.tail     
                                
    def reset_layers(self, context):          
        arm = bpy.context.active_object
        arm_data = arm.data       
         
        arm_data.layers = [(x in self.active_layers) for x in range(32)]                           
                                
    def execute(self, context):
        self.all_layers(context)
        self.match_heads_tails(context)
        self.reset_layers(context)

                                                           

        return {'FINISHED'}  
                                
                            
class Operator_BlenRig_Auto_Bone_Roll(bpy.types.Operator):    
    
    bl_idname = "blenrig_auto_bone.roll"   
    bl_label = "BlenRig Auto Calulate Roll Angles"   
    bl_description = "Set roll angles to their predefined values"    
    bl_options = {'REGISTER', 'UNDO',}   
    
    @classmethod
    def poll(cls, context):
        if not bpy.context.object:
            return False
        else:
            return (bpy.context.object.type=='ARMATURE' and context.mode=='EDIT_ARMATURE')    
    
    active_layers = []
    
    def all_layers(self, context):
        arm = bpy.context.active_object
        arm_data = arm.data          
        for i in range(len(arm_data.layers)):
            layers_status = arm_data.layers[i]
            if layers_status.real == 1:
                self.active_layers.append(i)

            
        #Turn on all layers
        arm_data.layers = [(x in [x]) for x in range(32)]      
    
    def blenrig_update_mirrored(self, context):   
        arm = bpy.context.active_object
        arm_data = arm.data        
        bones = arm_data.edit_bones         
        if arm_data.use_mirror_x == True:
            for b in bones:
                if '_L' in b.name:
                    b.select = 1
                    b.select_head = 1
                    b.select_tail = 1
                    bpy.ops.armature.symmetrize(direction='NEGATIVE_X') 
                    bpy.ops.armature.select_all(action='DESELECT')    
        else:
            return False            

    def calc_roll(self, context, roll_type):
        bpy.ops.object.mode_set(mode='EDIT')
        arm = bpy.context.active_object
        arm_data = arm.data        
        bones = arm_data.edit_bones
        bpy.ops.armature.reveal()
        bpy.ops.armature.select_all(action='DESELECT')              
        
        for b in bones:
            if arm_data.use_mirror_x == True:
                if '_R' not in b.name:          
                    if b['b_roll'][0] == roll_type:
                        b.select = 1
                        bpy.ops.armature.calculate_roll(type=roll_type, axis_flip=False, axis_only=False)
                        b.select = 0    
            else:
                if b['b_roll']:        
                    if b['b_roll'][0] == roll_type:
                        b.select = 1
                        bpy.ops.armature.calculate_roll(type=roll_type, axis_flip=False, axis_only=False)
                        b.select = 0                           
    
    def blenrig_bone_auto_roll(self, context):
        self.calc_roll(context, 'GLOBAL_POS_Y')
        self.calc_roll(context, 'GLOBAL_POS_Z') 
        self.calc_roll(context, 'GLOBAL_POS_X') 
        self.calc_roll(context, 'GLOBAL_NEG_Y') 
        self.calc_roll(context, 'GLOBAL_NEG_Z') 
        self.calc_roll(context, 'GLOBAL_NEG_X')
        self.calc_roll(context, 'POS_Y')
        self.calc_roll(context, 'POS_Z')
        self.calc_roll(context, 'POS_X')
        self.calc_roll(context, 'NEG_Y')
        self.calc_roll(context, 'NEG_Z')
        self.calc_roll(context, 'NEG_X')
                                  
                
    def blenrig_bone_custom_roll(self, context):
        bpy.ops.object.mode_set(mode='EDIT')
        arm = bpy.context.active_object
        arm_data = arm.data        
        bones = arm_data.edit_bones
        bpy.ops.armature.reveal()
        bpy.ops.armature.select_all(action='DESELECT')    

        for b in bones:
            if arm_data.use_mirror_x == True:
                if '_R' not in b.name:               
                    if b['b_roll']:                            
                        if b['b_roll'][0] == 'ACTIVE':
                            for t in bones:
                                if (t.name == b['b_roll'][1]):
                                    arm.data.edit_bones.active = t
                                    b.select = 1
                                    bpy.ops.armature.calculate_roll(type='ACTIVE', axis_flip=False, axis_only=False)   
                                    b.select = 0  
                                    bpy.ops.armature.select_all(action='DESELECT') 
            else:       
                if b['b_roll']:                            
                    if b['b_roll'][0] == 'ACTIVE':
                        for t in bones:
                            if (t.name == b['b_roll'][1]):
                                arm.data.edit_bones.active = t
                                b.select = 1
                                bpy.ops.armature.calculate_roll(type='ACTIVE', axis_flip=False, axis_only=False)   
                                b.select = 0  
                                bpy.ops.armature.select_all(action='DESELECT')                                  

    def blenrig_bone_cursor_roll(self, context):
        bpy.ops.object.mode_set(mode='EDIT')
        arm = bpy.context.active_object
        arm_data = arm.data        
        bones = arm_data.edit_bones
        bpy.ops.armature.reveal()
        bpy.ops.armature.select_all(action='DESELECT')    
        #Enable cursor snapping context
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                c = bpy.context.copy()
                c['area'] = area
        else:
            print("No View3D, aborting.")
    

        for b in bones:
            if arm_data.use_mirror_x == True:
                if '_R' not in b.name:               
                    if b['b_roll']:                            
                        if b['b_roll'][0] == 'CURSOR':
                            for t in bones:
                                if (t.name == b['b_roll'][1]):
                                    arm.data.edit_bones.active = t
                                    bpy.ops.view3d.snap_cursor_to_active(c)
                                    b.select = 1
                                    bpy.ops.armature.calculate_roll(type='CURSOR', axis_flip=False, axis_only=False)   
                                    b.select = 0  
                                    bpy.ops.armature.select_all(action='DESELECT') 
            else:       
                if b['b_roll']:                            
                    if b['b_roll'][0] == 'CURSOR':
                        for t in bones:
                                if (t.name == b['b_roll'][1]):
                                    arm.data.edit_bones.active = t
                                    bpy.ops.view3d.snap_cursor_to_active(c)
                                    b.select = 1
                                    bpy.ops.armature.calculate_roll(type='CURSOR', axis_flip=False, axis_only=False)   
                                    b.select = 0  
                                    bpy.ops.armature.select_all(action='DESELECT') 

    def blenrig_bone_align(self, context):
        bpy.ops.object.mode_set(mode='EDIT')
        arm = bpy.context.active_object
        arm_data = arm.data        
        bones = arm_data.edit_bones
        bpy.ops.armature.reveal()
        bpy.ops.armature.select_all(action='DESELECT')        

        for b in bones:
            if arm_data.use_mirror_x == True:
                if '_R' not in b.name:               
                    if b['b_align']:
                        if b['b_align'][0] != "''":                             
                            for t in bones:
                                if (t.name == b['b_align'][0]):
                                    arm.data.edit_bones.active = t
                                    b.select = 1
                                    bpy.ops.armature.align()  
                                    bpy.ops.armature.calculate_roll(type='ACTIVE', axis_flip=False, axis_only=False)  
                                    b.select = 0  
                                    bpy.ops.armature.select_all(action='DESELECT') 
                                    for t2 in bones:
                                        if (b.name == t2['b_head'][0]):
                                            if t2['b_head'][1] == 'head':
                                                t2.head = b.head
                                            if t2['b_head'][1] == 'tail':
                                                t2.head = b.tail    
                                        if (b.name == t2['b_tail'][0]):
                                            if t2['b_tail'][1] == 'head':
                                                t2.tail = b.head
                                            if t2['b_head'][1] == 'tail':
                                                t2.tail = b.tail                                                                                           
                                                arm.data.edit_bones.active = t
                                                t2.select = 1
                                                bpy.ops.armature.calculate_roll(type='ACTIVE', axis_flip=False, axis_only=False)  
                                                t2.select = 0  
                                                bpy.ops.armature.select_all(action='DESELECT')                                      
            else:           
                if b['b_align']:
                    if b['b_align'][0] != "''":                             
                        for t in bones:
                            if (t.name == b['b_align'][0]):
                                arm.data.edit_bones.active = t
                                b.select = 1
                                bpy.ops.armature.align()  
                                bpy.ops.armature.calculate_roll(type='ACTIVE', axis_flip=False, axis_only=False)  
                                b.select = 0  
                                bpy.ops.armature.select_all(action='DESELECT') 
                                for t2 in bones:
                                    if (b.name == t2['b_head'][0]):
                                        if t2['b_head'][1] == 'head':
                                            t2.head = b.head
                                        if t2['b_head'][1] == 'tail':
                                            t2.head = b.tail    
                                    if (b.name == t2['b_tail'][0]):
                                        if t2['b_tail'][1] == 'head':
                                            t2.tail = b.head
                                        if t2['b_head'][1] == 'tail':
                                            t2.tail = b.tail                                                                                           
                                            arm.data.edit_bones.active = t
                                            t2.select = 1
                                            bpy.ops.armature.calculate_roll(type='ACTIVE', axis_flip=False, axis_only=False)  
                                            t2.select = 0  
                                            bpy.ops.armature.select_all(action='DESELECT')                                                                                                          

    def reset_layers(self, context):          
        arm = bpy.context.active_object
        arm_data = arm.data        
        arm_data.layers = [(x in self.active_layers) for x in range(32)]     

    def execute(self, context):
        self.all_layers(context)        
        self.blenrig_bone_auto_roll(context)
        self.blenrig_bone_custom_roll(context)
        self.blenrig_bone_cursor_roll(context)
        self.blenrig_bone_align(context)    
        self.blenrig_update_mirrored(context) 
        self.reset_layers(context)     
                                                                                                                                                                                                                                    

        return {'FINISHED'}  

class Operator_BlenRig_Custom_Bone_Roll(bpy.types.Operator):    
    
    bl_idname = "blenrig_custom_bone.roll"   
    bl_label = "BlenRig User Defined Roll Angles"   
    bl_description = "Calulate roll angles and aligns defined by user"    
    bl_options = {'REGISTER', 'UNDO',}       

    @classmethod
    def poll(cls, context):
        if not bpy.context.object:
            return False
        else:
            return (bpy.context.object.type=='ARMATURE' and context.mode=='EDIT_ARMATURE')  

    active_layers = []
    
    def all_layers(self, context):
        arm = bpy.context.active_object
        arm_data = arm.data          
        for i in range(len(arm_data.layers)):
            layers_status = arm_data.layers[i]
            if layers_status.real == 1:
                self.active_layers.append(i)

            
        #Turn on all layers
        arm_data.layers = [(x in [x]) for x in range(32)]  

    def blenrig_update_mirrored(self, context):   
        arm = bpy.context.active_object
        arm_data = arm.data        
        bones = arm_data.edit_bones         
        if arm_data.use_mirror_x == True:
            for b in bones:
                if '_L' in b.name:
                    b.select = 1
                    b.select_head = 1
                    b.select_tail = 1
                    bpy.ops.armature.symmetrize(direction='NEGATIVE_X')  
                    bpy.ops.armature.select_all(action='DESELECT')    
        else:
            return False  
                
    def blenrig_bone_custom_roll(self, context):
        bpy.ops.object.mode_set(mode='EDIT')
        arm = bpy.context.active_object
        arm_data = arm.data        
        bones = arm_data.edit_bones
        bpy.ops.armature.reveal()
        bpy.ops.armature.select_all(action='DESELECT')    

        for b in bones:
            if arm_data.use_mirror_x == True:
                if '_R' not in b.name:               
                    if b['b_roll']:                            
                        if b['b_roll'][0] == 'ACTIVE':
                            for t in bones:
                                if (t.name == b['b_roll'][1]):
                                    arm.data.edit_bones.active = t
                                    b.select = 1
                                    bpy.ops.armature.calculate_roll(type='ACTIVE', axis_flip=False, axis_only=False)   
                                    b.select = 0  
                                    bpy.ops.armature.select_all(action='DESELECT') 
            else:       
                if b['b_roll']:                            
                    if b['b_roll'][0] == 'ACTIVE':
                        for t in bones:
                            if (t.name == b['b_roll'][1]):
                                arm.data.edit_bones.active = t
                                b.select = 1
                                bpy.ops.armature.calculate_roll(type='ACTIVE', axis_flip=False, axis_only=False)   
                                b.select = 0  
                                bpy.ops.armature.select_all(action='DESELECT')                                  

    def blenrig_bone_align(self, context):
        bpy.ops.object.mode_set(mode='EDIT')
        arm = bpy.context.active_object
        arm_data = arm.data        
        bones = arm_data.edit_bones
        bpy.ops.armature.reveal()
        bpy.ops.armature.select_all(action='DESELECT')        

        for b in bones:
            if arm_data.use_mirror_x == True:
                if '_R' not in b.name:               
                    if b['b_align']:
                        if b['b_align'][0] != "''":                             
                            for t in bones:
                                if (t.name == b['b_align'][0]):
                                    arm.data.edit_bones.active = t
                                    b.select = 1
                                    bpy.ops.armature.align()  
                                    bpy.ops.armature.calculate_roll(type='ACTIVE', axis_flip=False, axis_only=False)  
                                    b.select = 0  
                                    bpy.ops.armature.select_all(action='DESELECT') 
                                    for t2 in bones:
                                        if (b.name == t2['b_head'][0]):
                                            if t2['b_head'][1] == 'head':
                                                t2.head = b.head
                                            if t2['b_head'][1] == 'tail':
                                                t2.head = b.tail    
                                        if (b.name == t2['b_tail'][0]):
                                            if t2['b_tail'][1] == 'head':
                                                t2.tail = b.head
                                            if t2['b_head'][1] == 'tail':
                                                t2.tail = b.tail                                                                                           
                                                arm.data.edit_bones.active = t
                                                t2.select = 1
                                                bpy.ops.armature.calculate_roll(type='ACTIVE', axis_flip=False, axis_only=False)  
                                                t2.select = 0  
                                                bpy.ops.armature.select_all(action='DESELECT')                                      
            else:           
                if b['b_align']:
                    if b['b_align'][0] != "''":                             
                        for t in bones:
                            if (t.name == b['b_align'][0]):
                                arm.data.edit_bones.active = t
                                b.select = 1
                                bpy.ops.armature.align()  
                                bpy.ops.armature.calculate_roll(type='ACTIVE', axis_flip=False, axis_only=False)  
                                b.select = 0  
                                bpy.ops.armature.select_all(action='DESELECT') 
                                for t2 in bones:
                                    if (b.name == t2['b_head'][0]):
                                        if t2['b_head'][1] == 'head':
                                            t2.head = b.head
                                        if t2['b_head'][1] == 'tail':
                                            t2.head = b.tail    
                                    if (b.name == t2['b_tail'][0]):
                                        if t2['b_tail'][1] == 'head':
                                            t2.tail = b.head
                                        if t2['b_head'][1] == 'tail':
                                            t2.tail = b.tail                                                                                           
                                            arm.data.edit_bones.active = t
                                            t2.select = 1
                                            bpy.ops.armature.calculate_roll(type='ACTIVE', axis_flip=False, axis_only=False)  
                                            t2.select = 0  
                                            bpy.ops.armature.select_all(action='DESELECT')                                                                                                          

    def reset_layers(self, context):          
        arm = bpy.context.active_object
        arm_data = arm.data        
        arm_data.layers = [(x in self.active_layers) for x in range(32)]     

    def execute(self, context):
        self.all_layers(context)         
        self.blenrig_bone_custom_roll(context)
        self.blenrig_bone_align(context)
        self.blenrig_update_mirrored(context)                 
        self.reset_layers(context)                                                                                                                                                                                                                                     

        return {'FINISHED'}    


################################# IK/FK SNAPPING OPERATORS ##########################################################

#Selected and Active Bones Transforms Copy Function

def sel_act_bones(b1, b2, copy_op): #args will be replaced by the actual bone names
    
    arm = bpy.context.active_object
    arm_data = arm.data
    p_bones = arm.pose.bones

    Bone1 = p_bones[b1]
    Bone2 = p_bones[b2]
    #set Bone2 as active
    arm.data.bones.active = Bone2.bone
    Bone1.bone.select = 1
    copy_operator = ['rot', 'loc', 'scale', 'loc_rot', 'loc_rot_scale']
    if copy_operator[0] == copy_op:
        bpy.ops.pose.copy_pose_vis_rot()
    elif copy_operator[1] == copy_op:
        bpy.ops.pose.copy_pose_vis_loc() 
    elif copy_operator[2] == copy_op:
        bpy.ops.pose.copy_pose_vis_sca()   
    elif copy_operator[3] == copy_op:
        bpy.ops.pose.copy_pose_vis_loc()   
        bpy.ops.pose.copy_pose_vis_rot()   
    elif copy_operator[4] == copy_op:
        bpy.ops.pose.copy_pose_vis_loc()   
        bpy.ops.pose.copy_pose_vis_rot()                           
        bpy.ops.pose.copy_pose_vis_sca()                                 
    Bone1.bone.select = 0
    Bone2.bone.select = 0

##### TORSO #####

class Operator_Torso_Snap_IK_FK(bpy.types.Operator):    
    
    bl_idname = "torso_snap.ik_fk"   
    bl_label = "BlenRig Torso Snap IK FK"   
    bl_description = "Prepare seamless switch to FK"    
    bl_options = {'REGISTER', 'UNDO',}      

    @classmethod
    def poll(cls, context):
        if not bpy.context.object:
            return False
        else:
            return (bpy.context.object.type=='ARMATURE' and context.mode=='POSE')
                    
    def execute(self, context):         
        arm = bpy.context.active_object
        arm_data = arm.data
        p_bones = arm.pose.bones
       
        for b in p_bones:
            if ('properties_torso' == b.name):
                prop = int(b.ik_torso)
                prop_inv = int(b.inv_torso)
                if prop != 0 or prop_inv != 0:
                    self.report({'ERROR'}, 'Only works in IK mode')  
                    return {"CANCELLED"}                  
                   
        check_bones = ['spine_1_fk', 'spine_1_ik', 'spine_2_fk', 'spine_2_ik', 'spine_3_fk', 'spine_3_ik', 'torso_fk_ctrl']
        
        for n in check_bones:
            if (n not in p_bones):
                self.report({'ERROR'}, 'Missing: ' + str(n))  
                return {"CANCELLED"} 
              
        for b in p_bones:
            b.bone.select = 0
            if (b.name in check_bones):
                b.bone.hide = False            
                       
        arm_data.layers[30] = True           
        sel_act_bones('spine_1_fk', 'spine_1_ik', 'loc_rot')         
        sel_act_bones('spine_2_fk', 'spine_2_ik', 'loc_rot')      
        sel_act_bones('spine_3_fk', 'spine_3_ik', 'loc_rot')                  
        p_bones['torso_fk_ctrl'].bone.select = 1
        bpy.ops.pose.rot_clear()               
                       
        for b in p_bones:        
            b.bone.select = 0
            select_bones = ['spine_1_fk', 'spine_2_fk', 'spine_3_fk', 'torso_fk_ctrl']
            if (b.name in select_bones):
                b.bone.select = 1                        
        arm_data.layers[30] = False            
           
        return {"FINISHED"}                

class Operator_Torso_Snap_FK_IK(bpy.types.Operator):    
    
    bl_idname = "torso_snap.fk_ik"   
    bl_label = "BlenRig Torso Snap FK IK"     
    bl_description = "Prepare seamless switch to IK"     
    bl_options = {'REGISTER', 'UNDO',}      

    @classmethod
    def poll(cls, context):
        if not bpy.context.object:
            return False
        else:
            return (bpy.context.object.type=='ARMATURE' and context.mode=='POSE')
                    
    def execute(self, context):         
        arm = bpy.context.active_object
        arm_data = arm.data
        p_bones = arm.pose.bones

        for b in p_bones:
            if ('properties_torso' == b.name):
                prop = int(b.ik_torso)
                prop_inv = int(b.inv_torso)
                if prop != 1 or prop_inv != 0:
                    self.report({'ERROR'}, 'Only works in FK mode')  
                    return {"CANCELLED"}   
        
        check_bones = ['torso_ik_ctrl', 'snap_torso_fk_pivot', 'spine_4_ik_ctrl', 'neck_1_fk', 'spine_3_ik_ctrl', 'spine_3_fk', 'spine_2_ik_ctrl', 'spine_2_fk', 'spine_1_ik_ctrl', 'spine_1_fk']
        
        for n in check_bones:
            if (n not in p_bones):
                self.report({'ERROR'}, 'Missing: ' + str(n))  
                return {"CANCELLED"} 
              
        for b in p_bones:
            b.bone.select = 0
            if (b.name in check_bones):
                b.bone.hide = False       
                            
        arm_data.layers[30] = True    
        sel_act_bones('torso_ik_ctrl', 'snap_torso_fk_pivot', 'loc_rot')         
        sel_act_bones('spine_4_ik_ctrl', 'neck_1_fk', 'loc')      
        sel_act_bones('spine_3_ik_ctrl', 'spine_3_fk', 'loc')  
        sel_act_bones('spine_2_ik_ctrl', 'spine_2_fk', 'loc_rot')           
        sel_act_bones('spine_1_ik_ctrl', 'spine_1_fk', 'rot')   
        p_bones['spine_4_ik_ctrl'].bone.select = 1
        bpy.ops.pose.rot_clear()    
        p_bones['spine_3_ik_ctrl'].bone.select = 1
        bpy.ops.pose.rot_clear()                                                            
                       
        for b in p_bones:        
            b.bone.select = 0
            select_bones = ['spine_1_ik_ctrl', 'spine_2_ik_ctrl', 'spine_3_ik_ctrl', 'spine_4_ik_ctrl', 'torso_ik_ctrl']
            if (b.name in select_bones):
                b.bone.select = 1                        
        arm_data.layers[30] = False            
           
        return {"FINISHED"}        

class Operator_Torso_Snap_INV_UP(bpy.types.Operator):   
    
    bl_idname = "torso_snap.inv_up"  
    bl_label = "BlenRig Torso Snap INV UP"    
    bl_description = "Prepare seamless switch to Invert torso"     
    bl_options = {'REGISTER', 'UNDO',}      

    @classmethod
    def poll(cls, context):
        if not bpy.context.object:
            return False
        else:
            return (bpy.context.object.type=='ARMATURE' and context.mode=='POSE')
                    
    def execute(self, context):         
        arm = bpy.context.active_object
        arm_data = arm.data
        p_bones = arm.pose.bones

        for b in p_bones:
            if ('properties_torso' == b.name):
                prop_inv = int(b.inv_torso)
                if prop_inv != 1:
                    self.report({'ERROR'}, 'Only works in FK/IK mode')  
                    return {"CANCELLED"}   
        
        check_bones = ['pelvis_ctrl', 'snap_pelvis_ctrl_inv', 'spine_1_fk', 'snap_spine_1_fk_inv', 'spine_2_fk', 'snap_spine_2_fk_inv', 'spine_3_fk', 'spine_3_inv', 'spine_2_ik_ctrl', 'spine_3_ik_ctrl', 'spine_4_ik_ctrl', 'torso_ik_ctrl', 'torso_fk_ctrl']
        
        for n in check_bones:
            if (n not in p_bones):
                self.report({'ERROR'}, 'Missing: ' + str(n))  
                return {"CANCELLED"} 
              
        for b in p_bones:
            b.bone.select = 0
            if (b.name in check_bones):
                b.bone.hide = False          
                         
        arm_data.layers[30] = True    
        sel_act_bones('pelvis_ctrl', 'snap_pelvis_ctrl_inv', 'loc_rot')         
        sel_act_bones('spine_1_fk', 'snap_spine_1_fk_inv', 'loc_rot')      
        sel_act_bones('spine_2_fk', 'snap_spine_2_fk_inv', 'loc_rot')  
        sel_act_bones('spine_3_fk', 'spine_3_inv', 'loc_rot')
        sel_act_bones('torso_ik_ctrl', 'snap_torso_fk_pivot', 'loc_rot')         
        sel_act_bones('spine_4_ik_ctrl', 'neck_1_fk', 'loc')      
        sel_act_bones('spine_3_ik_ctrl', 'spine_3_fk', 'loc')  
        sel_act_bones('spine_2_ik_ctrl', 'spine_2_fk', 'loc_rot')           
        sel_act_bones('spine_1_ik_ctrl', 'spine_1_fk', 'rot')   
        p_bones['spine_4_ik_ctrl'].bone.select = 1
        bpy.ops.pose.rot_clear()    
        p_bones['spine_3_ik_ctrl'].bone.select = 1
        bpy.ops.pose.rot_clear()         
        p_bones['torso_fk_ctrl'].bone.select = 1
        bpy.ops.pose.rot_clear()                                                              
                       
        for b in p_bones:        
            b.bone.select = 0
            select_bones = ['pelvis_ctrl', 'spine_1_fk', 'spine_2_fk', 'spine_3_fk','spine_2_ik_ctrl', 'spine_3_ik_ctrl', 'spine_4_ik_ctrl', 'torso_ik_ctrl', 'torso_fk_ctrl']
            if (b.name in select_bones):
                b.bone.select = 1                        
        arm_data.layers[30] = False            
           
        return {"FINISHED"}        


class Operator_Torso_Snap_UP_INV(bpy.types.Operator):   
    
    bl_idname = "torso_snap.up_inv"  
    bl_label = "BlenRig Torso Snap UP INV"    
    bl_description = "Prepare seamless switch to FK or IK Torso"      
    bl_options = {'REGISTER', 'UNDO',}      

    @classmethod
    def poll(cls, context):
        if not bpy.context.object:
            return False
        else:
            return (bpy.context.object.type=='ARMATURE' and context.mode=='POSE')
                    
    def execute(self, context):         
        arm = bpy.context.active_object
        arm_data = arm.data
        p_bones = arm.pose.bones

        for b in p_bones:
            if ('properties_torso' == b.name):
                prop = int(b.ik_torso)
                prop_inv = int(b.inv_torso)
                if prop_inv != 0:
                    self.report({'ERROR'}, 'Only works in invert mode')  
                    return {"CANCELLED"}   
        
        check_bones = ['spine_3_inv_ctrl', 'snap_torso_ctrl_inv_loc', 'spine_3_inv', 'spine_3_fk', 'spine_2_inv', 'snap_spine_2_inv_fk', 'spine_1_inv', 'snap_spine_1_inv_fk', 'pelvis_inv', 'pelvis', 'torso_inv_ctrl']
        
        for n in check_bones:
            if (n not in p_bones):
                self.report({'ERROR'}, 'Missing: ' + str(n))  
                return {"CANCELLED"} 
              
        for b in p_bones:
            b.bone.select = 0
            if (b.name in check_bones):
                b.bone.hide = False       
                            
        arm_data.layers[30] = True    
        sel_act_bones('spine_3_inv_ctrl', 'snap_torso_ctrl_inv_loc', 'loc_rot')         
        sel_act_bones('spine_3_inv', 'spine_3_fk', 'loc_rot')      
        sel_act_bones('spine_2_inv', 'snap_spine_2_inv_fk', 'loc_rot')  
        sel_act_bones('spine_1_inv', 'snap_spine_1_inv_fk', 'loc_rot')           
        sel_act_bones('pelvis_inv', 'pelvis', 'loc_rot')   
        p_bones['torso_inv_ctrl'].bone.select = 1
        bpy.ops.pose.rot_clear()                                                            
                       
        for b in p_bones:        
            b.bone.select = 0
            select_bones = ['pelvis_inv', 'spine_1_inv', 'spine_2_inv', 'spine_3_inv', 'torso_inv_ctrl']
            if (b.name in select_bones):
                b.bone.select = 1                        
        arm_data.layers[30] = False            
           
        return {"FINISHED"}    

##### HEAD #####
    

class Operator_Head_Snap_IK_FK(bpy.types.Operator): 
    
    bl_idname = "head_snap.ik_fk"    
    bl_label = "BlenRig Head Snap IK FK"     
    bl_description = "Prepare seamless switch to FK"     
    bl_options = {'REGISTER', 'UNDO',}      

    @classmethod
    def poll(cls, context):
        if not bpy.context.object:
            return False
        else:
            return (bpy.context.object.type=='ARMATURE' and context.mode=='POSE')
                    
    def execute(self, context):         
        arm = bpy.context.active_object
        arm_data = arm.data
        p_bones = arm.pose.bones
       
        for b in p_bones:
            if ('properties_head' == b.name):
                prop = int(b.ik_head)
                if prop != 0:
                    self.report({'ERROR'}, 'Only works in IK mode')  
                    return {"CANCELLED"}                  
                   
        check_bones = ['neck_1_fk', 'neck_1_ik', 'neck_2_fk', 'neck_2_ik', 'neck_3_fk', 'neck_3_ik', 'neck_fk_ctrl']
        
        for n in check_bones:
            if (n not in p_bones):
                self.report({'ERROR'}, 'Missing: ' + str(n))  
                return {"CANCELLED"} 
              
        for b in p_bones:
            b.bone.select = 0
            if (b.name in check_bones):
                b.bone.hide = False            
                       
        arm_data.layers[30] = True           
        sel_act_bones('neck_1_fk', 'neck_1_ik', 'loc_rot')         
        sel_act_bones('neck_2_fk', 'neck_2_ik', 'loc_rot')      
        sel_act_bones('neck_3_fk', 'neck_3_ik', 'loc_rot')                  
        p_bones['neck_fk_ctrl'].bone.select = 1
        bpy.ops.pose.rot_clear()               
                       
        for b in p_bones:        
            b.bone.select = 0
            select_bones = ['neck_1_fk', 'neck_2_fk', 'neck_3_fk', 'neck_fk_ctrl']
            if (b.name in select_bones):
                b.bone.select = 1                        
        arm_data.layers[30] = False            
           
        return {"FINISHED"}       

class Operator_Head_Snap_FK_IK(bpy.types.Operator): 
    
    bl_idname = "head_snap.fk_ik"    
    bl_label = "BlenRig Head Snap FK IK"      
    bl_description = "Prepare seamless switch to IK"    
    bl_options = {'REGISTER', 'UNDO',}      

    @classmethod
    def poll(cls, context):
        if not bpy.context.object:
            return False
        else:
            return (bpy.context.object.type=='ARMATURE' and context.mode=='POSE')
                    
    def execute(self, context):         
        arm = bpy.context.active_object
        arm_data = arm.data
        p_bones = arm.pose.bones

        for b in p_bones:
            if ('properties_head' == b.name):
                prop = int(b.ik_head)
                if prop != 1:
                    self.report({'ERROR'}, 'Only works in FK mode')  
                    return {"CANCELLED"}   
        
        check_bones = ['neck_ik_ctrl', 'snap_neck_fk_pivot', 'head_ik_ctrl', 'head_fk', 'neck_3_ik_ctrl', 'neck_3_fk', 'neck_2_ik_ctrl', 'neck_2_fk']
        
        for n in check_bones:
            if (n not in p_bones):
                self.report({'ERROR'}, 'Missing: ' + str(n))  
                return {"CANCELLED"} 
              
        for b in p_bones:
            b.bone.select = 0
            if (b.name in check_bones):
                b.bone.hide = False       
                            
        arm_data.layers[30] = True    
        sel_act_bones('neck_ik_ctrl', 'snap_neck_fk_pivot', 'loc_rot')         
        sel_act_bones('head_ik_ctrl', 'head_fk', 'loc')              
        sel_act_bones('neck_3_ik_ctrl', 'neck_3_fk', 'loc_rot')    
        sel_act_bones('neck_2_ik_ctrl', 'neck_2_fk', 'loc')          
        p_bones['neck_2_ik_ctrl'].bone.select = 1
        bpy.ops.pose.rot_clear()                                                                             
                       
        for b in p_bones:        
            b.bone.select = 0
            select_bones = ['neck_ik_ctrl', 'neck_3_ik_ctrl', 'neck_2_ik_ctrl']
            if (b.name in select_bones):
                b.bone.select = 1                        
        arm_data.layers[30] = False            
           
        return {"FINISHED"}        

##### ARM L #####


class Operator_Arm_L_Snap_IK_FK(bpy.types.Operator):    
    
    bl_idname = "arm_l_snap.ik_fk"   
    bl_label = "BlenRig Arm_L Snap IK FK"    
    bl_description = "Prepare seamless switch to FK"    
    bl_options = {'REGISTER', 'UNDO',}      

    @classmethod
    def poll(cls, context):
        if not bpy.context.object:
            return False
        else:
            return (bpy.context.object.type=='ARMATURE' and context.mode=='POSE')
                    
    def execute(self, context):         
        arm = bpy.context.active_object
        arm_data = arm.data
        p_bones = arm.pose.bones
       
        for b in p_bones:
            if ('properties_arm_L' == b.name):
                prop = int(b.ik_arm_L)
                if prop != 0:
                    self.report({'ERROR'}, 'Only works in IK mode')  
                    return {"CANCELLED"}                  
        
        # Biped
        if arm_data['rig_type'] == 'Biped':
                       
            check_bones = ['arm_fk_L', 'arm_ik_L', 'forearm_fk_L', 'forearm_ik_L', 'hand_fk_L', 'hand_ik_ctrl_L']
            
            for n in check_bones:
                if (n not in p_bones):
                    self.report({'ERROR'}, 'Missing: ' + str(n))  
                    return {"CANCELLED"} 
                  
            for b in p_bones:
                b.bone.select = 0
                if (b.name in check_bones):
                    b.bone.hide = False            
                           
            arm_data.layers[30] = True           
            sel_act_bones('arm_fk_L', 'arm_ik_L', 'rot')         
            sel_act_bones('forearm_fk_L', 'forearm_ik_L', 'rot')  
            for b in p_bones:
                if ('properties_arm_L' in b.name):
                    prop = int(b.hinge_hand_L)
                    if prop == 1:            
                        sel_act_bones('hand_fk_L', 'hand_ik_ctrl_L', 'rot')                                
                           
            for b in p_bones:        
                b.bone.select = 0
                select_bones = ['arm_fk_L', 'forearm_fk_L', 'hand_fk_L', 'hand_ik_ctrl_L']
                if (b.name in select_bones):
                    b.bone.select = 1                        
            arm_data.layers[30] = False       
        
        #Quadruped    
        if arm_data['rig_type'] == 'Quadruped':     
                
            check_bones = ['arm_fk_L', 'arm_ik_L', 'forearm_fk_L', 'forearm_ik_L', 'hand_fk_L', 'hand_ik_ctrl_L', 'carpal_fk_L', 'carpal_ik_L', 'fing_1_fk_L', 'fing_1_ik_L', 'fing_2_fk_L', 'fing_2_ik_L']
            
            for n in check_bones:
                if (n not in p_bones):
                    self.report({'ERROR'}, 'Missing: ' + str(n))  
                    return {"CANCELLED"} 
                  
            for b in p_bones:
                b.bone.select = 0
                if (b.name in check_bones):
                    b.bone.hide = False            
                           
            arm_data.layers[30] = True           
            sel_act_bones('arm_fk_L', 'arm_ik_L', 'rot')         
            sel_act_bones('forearm_fk_L', 'forearm_ik_L', 'rot')  
            sel_act_bones('carpal_fk_L', 'carpal_ik_L', 'rot')               
            sel_act_bones('hand_fk_L', 'hand_ik_ctrl_L', 'rot') 
            sel_act_bones('fing_1_fk_L', 'fing_1_ik_L', 'rot')  
            sel_act_bones('fing_2_fk_L', 'fing_2_ik_L', 'rot')                  
                                                                                      
            for b in p_bones:        
                b.bone.select = 0
                select_bones = ['arm_fk_L', 'forearm_fk_L', 'hand_fk_L', 'hand_ik_ctrl_L', 'carpal_fk_L', 'fing_1_fk_L', 'fing_2_fk_L']
                if (b.name in select_bones):
                    b.bone.select = 1                        
            arm_data.layers[30] = False                  
                                            
        return {"FINISHED"}    

class Operator_Arm_L_Snap_FK_IK(bpy.types.Operator):    
    
    bl_idname = "arm_l_snap.fk_ik"   
    bl_label = "BlenRig Arm_L Snap FK IK"    
    bl_description = "Prepare seamless switch to IK"   
    bl_options = {'REGISTER', 'UNDO',}      

    @classmethod
    def poll(cls, context):
        if not bpy.context.object:
            return False
        else:
            return (bpy.context.object.type=='ARMATURE' and context.mode=='POSE')
                    
    def execute(self, context):         
        arm = bpy.context.active_object
        arm_data = arm.data
        p_bones = arm.pose.bones
       
        for b in p_bones:
            if ('properties_arm_L' == b.name):
                prop = int(b.ik_arm_L)
                if prop != 1:
                    self.report({'ERROR'}, 'Only works in FK mode')  
                    return {"CANCELLED"}                  

        #Biped
        if arm_data['rig_type'] == 'Biped':
                   
            check_bones = ['hand_ik_ctrl_L', 'hand_fk_L', 'elbow_pole_L', 'snap_elbow_pole_fk_L', 'hand_fk_L', 'hand_ik_ctrl_L', 'hand_ik_pivot_point_L']
            
            for n in check_bones:
                if (n not in p_bones):
                    self.report({'ERROR'}, 'Missing: ' + str(n))  
                    return {"CANCELLED"} 
                  
            for b in p_bones:
                b.bone.select = 0
                if (b.name in check_bones):
                    b.bone.hide = False            
                           
            arm_data.layers[30] = True      
            p_bones['hand_ik_pivot_point_L'].bone.select = 1
            bpy.ops.pose.rot_clear()   
            bpy.ops.pose.loc_clear()    
            p_bones['hand_ik_pivot_point_L'].bone.select = 0                 
            sel_act_bones('hand_ik_ctrl_L', 'hand_fk_L', 'loc')         
            for b in p_bones:
                if ('properties_arm_L' in b.name):
                    prop = int(b.hinge_hand_L)
                    if prop == 0:            
                        sel_act_bones('hand_ik_ctrl_L', 'hand_fk_L', 'rot')                                                              
            sel_act_bones('elbow_pole_L', 'snap_elbow_pole_fk_L', 'loc')  
                           
            for b in p_bones:        
                b.bone.select = 0
                select_bones = ['hand_ik_ctrl_L', 'elbow_pole_L', 'hand_ik_pivot_point_L']
                if (b.name in select_bones):
                    b.bone.select = 1                        
            arm_data.layers[30] = False            
 
        #Quadruped   
        if arm_data['rig_type'] == 'Quadruped':        
            
            check_bones = ['hand_sole_ctrl_L', 'snap_hand_sole_ctrl_fk_L', 'hand_ik_ctrl_L', 'hand_fk_L', 'fings_ik_ctrl_L', 'snap_fings_ctrl_fk_L', 'fings_ik_ctrl_mid_L', 'snap_fing_ctrl_mid_fk_L', 'elbow_pole_L', 'snap_elbow_pole_fk_L', 'hand_sole_pivot_point_L', 'hand_roll_ctrl_L', 'fing_roll_1_L', 'fing_roll_2_L']
            
            for n in check_bones:
                if (n not in p_bones):
                    self.report({'ERROR'}, 'Missing: ' + str(n))  
                    return {"CANCELLED"} 
                  
            for b in p_bones:
                b.bone.select = 0
                if (b.name in check_bones):
                    b.bone.hide = False            
                           
            arm_data.layers[30] = True      
            p_bones['hand_sole_pivot_point_L'].bone.select = 1
            bpy.ops.pose.rot_clear()   
            bpy.ops.pose.loc_clear()    
            p_bones['hand_sole_pivot_point_L'].bone.select = 0  
            p_bones['hand_roll_ctrl_L'].bone.select = 1
            bpy.ops.pose.rot_clear()   
            bpy.ops.pose.loc_clear()    
            p_bones['hand_roll_ctrl_L'].bone.select = 0     
            p_bones['fing_roll_1_L'].bone.select = 1
            bpy.ops.pose.rot_clear()   
            bpy.ops.pose.loc_clear()    
            p_bones['fing_roll_1_L'].bone.select = 0     
            p_bones['fing_roll_2_L'].bone.select = 1
            bpy.ops.pose.rot_clear()   
            bpy.ops.pose.loc_clear()    
            p_bones['fing_roll_2_L'].bone.select = 0                                                                                                  
            sel_act_bones('hand_sole_ctrl_L', 'snap_hand_sole_ctrl_fk_L', 'loc_rot')  
            sel_act_bones('hand_ik_ctrl_L', 'hand_fk_L', 'loc_rot')  
            sel_act_bones('fings_ik_ctrl_L', 'snap_fings_ctrl_fk_L', 'loc_rot')  
            sel_act_bones('fings_ik_ctrl_mid_L', 'snap_fing_ctrl_mid_fk_L', 'loc_rot')       
            sel_act_bones('elbow_pole_L', 'snap_elbow_pole_fk_L', 'loc')                               
                           
            for b in p_bones:        
                b.bone.select = 0
                select_bones = ['hand_sole_ctrl_L', 'elbow_pole_L', 'fings_ik_ctrl_L', 'fings_ik_ctrl_mid_L', 'hand_ik_ctrl_L']
                if (b.name in select_bones):
                    b.bone.select = 1                        
            arm_data.layers[30] = False                  
           
        return {"FINISHED"}  

##### ARM R #####


class Operator_Arm_R_Snap_IK_FK(bpy.types.Operator):    
    
    bl_idname = "arm_r_snap.ik_fk"   
    bl_label = "BlenRig Arm_R Snap IK FK"    
    bl_description = "Prepare seamless switch to FK"       
    bl_options = {'REGISTER', 'UNDO',}      

    @classmethod
    def poll(cls, context):
        if not bpy.context.object:
            return False
        else:
            return (bpy.context.object.type=='ARMATURE' and context.mode=='POSE')
                    
    def execute(self, context):         
        arm = bpy.context.active_object
        arm_data = arm.data
        p_bones = arm.pose.bones
       
        for b in p_bones:
            if ('properties_arm_R' == b.name):
                prop = int(b.ik_arm_R)
                if prop != 0:
                    self.report({'ERROR'}, 'Only works in IK mode')  
                    return {"CANCELLED"}                  
                   
        # Biped
        if arm_data['rig_type'] == 'Biped':
                       
            check_bones = ['arm_fk_R', 'arm_ik_R', 'forearm_fk_R', 'forearm_ik_R', 'hand_fk_R', 'hand_ik_ctrl_R']
            
            for n in check_bones:
                if (n not in p_bones):
                    self.report({'ERROR'}, 'Missing: ' + str(n))  
                    return {"CANCELLED"} 
                  
            for b in p_bones:
                b.bone.select = 0
                if (b.name in check_bones):
                    b.bone.hide = False            
                           
            arm_data.layers[30] = True           
            sel_act_bones('arm_fk_R', 'arm_ik_R', 'rot')         
            sel_act_bones('forearm_fk_R', 'forearm_ik_R', 'rot')  
            for b in p_bones:
                if ('properties_arm_R' in b.name):
                    prop = int(b.hinge_hand_R)
                    if prop == 1:            
                        sel_act_bones('hand_fk_R', 'hand_ik_ctrl_R', 'rot')                                
                           
            for b in p_bones:        
                b.bone.select = 0
                select_bones = ['arm_fk_R', 'forearm_fk_R', 'hand_fk_R', 'hand_ik_ctrl_R']
                if (b.name in select_bones):
                    b.bone.select = 1                        
            arm_data.layers[30] = False       
        
        #Quadruped    
        if arm_data['rig_type'] == 'Quadruped':     
                
            check_bones = ['arm_fk_R', 'arm_ik_R', 'forearm_fk_R', 'forearm_ik_R', 'hand_fk_R', 'hand_ik_ctrl_R', 'carpal_fk_R', 'carpal_ik_R', 'fing_1_fk_R', 'fing_1_ik_R', 'fing_2_fk_R', 'fing_2_ik_R']
            
            for n in check_bones:
                if (n not in p_bones):
                    self.report({'ERROR'}, 'Missing: ' + str(n))  
                    return {"CANCELLED"} 
                  
            for b in p_bones:
                b.bone.select = 0
                if (b.name in check_bones):
                    b.bone.hide = False            
                           
            arm_data.layers[30] = True           
            sel_act_bones('arm_fk_R', 'arm_ik_R', 'rot')         
            sel_act_bones('forearm_fk_R', 'forearm_ik_R', 'rot')  
            sel_act_bones('carpal_fk_R', 'carpal_ik_R', 'rot')               
            sel_act_bones('hand_fk_R', 'hand_ik_ctrl_R', 'rot') 
            sel_act_bones('fing_1_fk_R', 'fing_1_ik_R', 'rot')  
            sel_act_bones('fing_2_fk_R', 'fing_2_ik_R', 'rot')                  
                                                                                      
            for b in p_bones:        
                b.bone.select = 0
                select_bones = ['arm_fk_R', 'forearm_fk_R', 'hand_fk_R', 'hand_ik_ctrl_R', 'carpal_fk_R', 'fing_1_fk_R', 'fing_2_fk_R']
                if (b.name in select_bones):
                    b.bone.select = 1                        
            arm_data.layers[30] = False                  
           
        return {"FINISHED"}    

class Operator_Arm_R_Snap_FK_IK(bpy.types.Operator):    
    
    bl_idname = "arm_r_snap.fk_ik"   
    bl_label = "BlenRig Arm_R Snap FK IK"    
    bl_description = "Prepare seamless switch to IK"   
    bl_options = {'REGISTER', 'UNDO',}      

    @classmethod
    def poll(cls, context):
        if not bpy.context.object:
            return False
        else:
            return (bpy.context.object.type=='ARMATURE' and context.mode=='POSE')
                    
    def execute(self, context):         
        arm = bpy.context.active_object
        arm_data = arm.data
        p_bones = arm.pose.bones
       
        for b in p_bones:
            if ('properties_arm_R' == b.name):
                prop = int(b.ik_arm_R)
                if prop != 1:
                    self.report({'ERROR'}, 'Only works in FK mode')  
                    return {"CANCELLED"}                  
                   
        #Biped
        if arm_data['rig_type'] == 'Biped':
                   
            check_bones = ['hand_ik_ctrl_R', 'hand_fk_R', 'elbow_pole_R', 'snap_elbow_pole_fk_R', 'hand_fk_R', 'hand_ik_ctrl_R', 'hand_ik_pivot_point_R']
            
            for n in check_bones:
                if (n not in p_bones):
                    self.report({'ERROR'}, 'Missing: ' + str(n))  
                    return {"CANCELLED"} 
                  
            for b in p_bones:
                b.bone.select = 0
                if (b.name in check_bones):
                    b.bone.hide = False            
                           
            arm_data.layers[30] = True      
            p_bones['hand_ik_pivot_point_R'].bone.select = 1
            bpy.ops.pose.rot_clear()   
            bpy.ops.pose.loc_clear()    
            p_bones['hand_ik_pivot_point_R'].bone.select = 0                 
            sel_act_bones('hand_ik_ctrl_R', 'hand_fk_R', 'loc')         
            for b in p_bones:
                if ('properties_arm_R' in b.name):
                    prop = int(b.hinge_hand_R)
                    if prop == 0:            
                        sel_act_bones('hand_ik_ctrl_R', 'hand_fk_R', 'rot')                                                              
            sel_act_bones('elbow_pole_R', 'snap_elbow_pole_fk_R', 'loc')  
                           
            for b in p_bones:        
                b.bone.select = 0
                select_bones = ['hand_ik_ctrl_R', 'elbow_pole_R', 'hand_ik_pivot_point_R']
                if (b.name in select_bones):
                    b.bone.select = 1                        
            arm_data.layers[30] = False            
 
        #Quadruped   
        if arm_data['rig_type'] == 'Quadruped':        
            
            check_bones = ['hand_sole_ctrl_R', 'snap_hand_sole_ctrl_fk_R', 'hand_ik_ctrl_R', 'hand_fk_R', 'fings_ik_ctrl_R', 'snap_fings_ctrl_fk_R', 'fings_ik_ctrl_mid_R', 'snap_fing_ctrl_mid_fk_R', 'elbow_pole_R', 'snap_elbow_pole_fk_R', 'hand_sole_pivot_point_R', 'hand_roll_ctrl_R', 'fing_roll_1_R', 'fing_roll_2_R']
            
            for n in check_bones:
                if (n not in p_bones):
                    self.report({'ERROR'}, 'Missing: ' + str(n))  
                    return {"CANCELLED"} 
                  
            for b in p_bones:
                b.bone.select = 0
                if (b.name in check_bones):
                    b.bone.hide = False            
                           
            arm_data.layers[30] = True      
            p_bones['hand_sole_pivot_point_R'].bone.select = 1
            bpy.ops.pose.rot_clear()   
            bpy.ops.pose.loc_clear()    
            p_bones['hand_sole_pivot_point_R'].bone.select = 0  
            p_bones['hand_roll_ctrl_R'].bone.select = 1
            bpy.ops.pose.rot_clear()   
            bpy.ops.pose.loc_clear()    
            p_bones['hand_roll_ctrl_R'].bone.select = 0     
            p_bones['fing_roll_1_R'].bone.select = 1
            bpy.ops.pose.rot_clear()   
            bpy.ops.pose.loc_clear()    
            p_bones['fing_roll_1_R'].bone.select = 0     
            p_bones['fing_roll_2_R'].bone.select = 1
            bpy.ops.pose.rot_clear()   
            bpy.ops.pose.loc_clear()    
            p_bones['fing_roll_2_R'].bone.select = 0                                                                                                  
            sel_act_bones('hand_sole_ctrl_R', 'snap_hand_sole_ctrl_fk_R', 'loc_rot')  
            sel_act_bones('hand_ik_ctrl_R', 'hand_fk_R', 'loc_rot')  
            sel_act_bones('fings_ik_ctrl_R', 'snap_fings_ctrl_fk_R', 'loc_rot')  
            sel_act_bones('fings_ik_ctrl_mid_R', 'snap_fing_ctrl_mid_fk_R', 'loc_rot')       
            sel_act_bones('elbow_pole_R', 'snap_elbow_pole_fk_R', 'loc')                               
                           
            for b in p_bones:        
                b.bone.select = 0
                select_bones = ['hand_sole_ctrl_R', 'elbow_pole_R', 'fings_ik_ctrl_R', 'fings_ik_ctrl_mid_R', 'hand_ik_ctrl_R']
                if (b.name in select_bones):
                    b.bone.select = 1                        
            arm_data.layers[30] = False              
               
        return {"FINISHED"}  

##### LEG L #####


class Operator_Leg_L_Snap_IK_FK(bpy.types.Operator):    
    
    bl_idname = "leg_l_snap.ik_fk"   
    bl_label = "BlenRig Leg_L Snap IK FK"     
    bl_description = "Prepare seamless switch to FK"    
    bl_options = {'REGISTER', 'UNDO',}      

    @classmethod
    def poll(cls, context):
        if not bpy.context.object:
            return False
        else:
            return (bpy.context.object.type=='ARMATURE' and context.mode=='POSE')
                    
    def execute(self, context):         
        arm = bpy.context.active_object
        arm_data = arm.data
        p_bones = arm.pose.bones
       
        for b in p_bones:
            if ('properties_leg_L' == b.name):
                prop = int(b.ik_leg_L)
                if prop != 0:
                    self.report({'ERROR'}, 'Only works in IK mode')  
                    return {"CANCELLED"}   
                
        #Biped
        if arm_data['rig_type'] == 'Biped':                               
                   
            check_bones = ['thigh_fk_L', 'thigh_ik_L', 'shin_fk_L', 'shin_ik_L', 'foot_fk_L', 'foot_ik_L', 'toe_1_fk_L', 'toe_1_ik_L', 'toe_2_fk_L', 'toe_2_ik_L' ]
            
            for n in check_bones:
                if (n not in p_bones):
                    self.report({'ERROR'}, 'Missing: ' + str(n))  
                    return {"CANCELLED"} 
                  
            for b in p_bones:
                b.bone.select = 0
                if (b.name in check_bones):
                    b.bone.hide = False            
                           
            arm_data.layers[30] = True           
            sel_act_bones('thigh_fk_L', 'thigh_ik_L', 'rot')         
            sel_act_bones('shin_fk_L', 'shin_ik_L', 'rot')  
            sel_act_bones('foot_fk_L', 'foot_ik_L', 'rot')    
            sel_act_bones('toe_1_fk_L', 'toe_1_ik_L', 'rot')  
            sel_act_bones('toe_2_fk_L', 'toe_2_ik_L', 'rot')                                           
                           
            for b in p_bones:        
                b.bone.select = 0
                select_bones = ['thigh_fk_L', 'shin_fk_L', 'foot_fk_L', 'toe_1_fk_L', 'toe_2_fk_L']
                if (b.name in select_bones):
                    b.bone.select = 1                        
            arm_data.layers[30] = False 
            
        #Quadruped
        if arm_data['rig_type'] == 'Quadruped':                               
                   
            check_bones = ['thigh_fk_L', 'thigh_ik_L', 'shin_fk_L', 'shin_ik_L', 'tarsal_fk_L', 'tarsal_ik_L', 'foot_fk_L', 'foot_ik_L', 'toe_1_fk_L', 'toe_1_ik_L', 'toe_2_fk_L', 'toe_2_ik_L' ]
            
            for n in check_bones:
                if (n not in p_bones):
                    self.report({'ERROR'}, 'Missing: ' + str(n))  
                    return {"CANCELLED"} 
                  
            for b in p_bones:
                b.bone.select = 0
                if (b.name in check_bones):
                    b.bone.hide = False            
                           
            arm_data.layers[30] = True           
            sel_act_bones('thigh_fk_L', 'thigh_ik_L', 'rot')         
            sel_act_bones('shin_fk_L', 'shin_ik_L', 'rot')  
            sel_act_bones('tarsal_fk_L', 'tarsal_ik_L', 'rot')              
            sel_act_bones('foot_fk_L', 'foot_ik_L', 'rot')    
            sel_act_bones('toe_1_fk_L', 'toe_1_ik_L', 'rot')  
            sel_act_bones('toe_2_fk_L', 'toe_2_ik_L', 'rot')                                           
                           
            for b in p_bones:        
                b.bone.select = 0
                select_bones = ['thigh_fk_L', 'shin_fk_L', 'tarsal_fk_L', 'foot_fk_L', 'toe_1_fk_L', 'toe_2_fk_L']
                if (b.name in select_bones):
                    b.bone.select = 1                        
            arm_data.layers[30] = False                                 
           
        return {"FINISHED"}        

class Operator_Leg_L_Snap_FK_IK(bpy.types.Operator):    
    
    bl_idname = "leg_l_snap.fk_ik"   
    bl_label = "BlenRig Leg_L Snap FK IK"  
    bl_description = "Prepare seamless switch to IK"   
    bl_options = {'REGISTER', 'UNDO',}      

    @classmethod
    def poll(cls, context):
        if not bpy.context.object:
            return False
        else:
            return (bpy.context.object.type=='ARMATURE' and context.mode=='POSE')
                    
    def execute(self, context):         
        arm = bpy.context.active_object
        arm_data = arm.data
        p_bones = arm.pose.bones
       
        for b in p_bones:
            if ('properties_leg_L' == b.name):
                prop = int(b.ik_leg_L)
                if prop != 1:
                    self.report({'ERROR'}, 'Only works in FK mode')  
                    return {"CANCELLED"}                  

        #Biped
        if arm_data['rig_type'] == 'Biped':  
                   
            check_bones = ['sole_ctrl_L', 'snap_sole_ctrl_fk_L', 'foot_ik_ctrl_L', 'foot_fk_L', 'toes_ik_ctrl_L', 'snap_toes_ctrl_fk_L', 'toes_ik_ctrl_mid_L', 'snap_toes_ctrl_mid_fk_L', 'knee_pole_L', 'snap_knee_fk_L', 'sole_pivot_point_L', 'foot_roll_ctrl_L', 'toe_roll_1_L', 'toe_roll_2_L']
            
            for n in check_bones:
                if (n not in p_bones):
                    self.report({'ERROR'}, 'Missing: ' + str(n))  
                    return {"CANCELLED"} 
                  
            for b in p_bones:
                b.bone.select = 0
                if (b.name in check_bones):
                    b.bone.hide = False            
                           
            arm_data.layers[30] = True      
            p_bones['sole_pivot_point_L'].bone.select = 1
            bpy.ops.pose.rot_clear()   
            bpy.ops.pose.loc_clear()    
            p_bones['sole_pivot_point_L'].bone.select = 0  
            p_bones['foot_roll_ctrl_L'].bone.select = 1
            bpy.ops.pose.rot_clear()   
            bpy.ops.pose.loc_clear()    
            p_bones['foot_roll_ctrl_L'].bone.select = 0     
            p_bones['toe_roll_1_L'].bone.select = 1
            bpy.ops.pose.rot_clear()   
            bpy.ops.pose.loc_clear()    
            p_bones['toe_roll_1_L'].bone.select = 0     
            p_bones['toe_roll_2_L'].bone.select = 1
            bpy.ops.pose.rot_clear()   
            bpy.ops.pose.loc_clear()    
            p_bones['toe_roll_2_L'].bone.select = 0                                                                                                  
            sel_act_bones('sole_ctrl_L', 'snap_sole_ctrl_fk_L', 'loc_rot')  
            sel_act_bones('foot_ik_ctrl_L', 'foot_fk_L', 'loc_rot')  
            sel_act_bones('toes_ik_ctrl_L', 'snap_toes_ctrl_fk_L', 'loc_rot')  
            sel_act_bones('toes_ik_ctrl_mid_L', 'snap_toes_ctrl_mid_fk_L', 'loc_rot')       
            sel_act_bones('knee_pole_L', 'snap_knee_fk_L', 'loc')                               
                           
            for b in p_bones:        
                b.bone.select = 0
                select_bones = ['sole_ctrl_L', 'knee_pole_L', 'toes_ik_ctrl_L', 'toes_ik_ctrl_mid_L', 'foot_ik_ctrl_L']
                if (b.name in select_bones):
                    b.bone.select = 1                        
            arm_data.layers[30] = False         
            
        #Quadruped
        if arm_data['rig_type'] == 'Quadruped':      
            
            check_bones = ['sole_ctrl_L', 'snap_sole_ctrl_fk_L', 'foot_ik_ctrl_L', 'foot_fk_L', 'toes_ik_ctrl_L', 'snap_toes_ctrl_fk_L', 'toes_ik_ctrl_mid_L', 'snap_toes_ctrl_mid_fk_L', 'thigh_fk_L', 'thigh_ik_L', 'knee_pole_L', 'snap_knee_fk_L', 'sole_pivot_point_L', 'foot_roll_ctrl_L', 'toe_roll_1_L', 'toe_roll_2_L']
            
            for n in check_bones:
                if (n not in p_bones):
                    self.report({'ERROR'}, 'Missing: ' + str(n))  
                    return {"CANCELLED"} 
                  
            for b in p_bones:
                b.bone.select = 0
                if (b.name in check_bones):
                    b.bone.hide = False            
                           
            arm_data.layers[30] = True      
            p_bones['sole_pivot_point_L'].bone.select = 1
            bpy.ops.pose.rot_clear()   
            bpy.ops.pose.loc_clear()    
            p_bones['sole_pivot_point_L'].bone.select = 0  
            p_bones['foot_roll_ctrl_L'].bone.select = 1
            bpy.ops.pose.rot_clear()   
            bpy.ops.pose.loc_clear()    
            p_bones['foot_roll_ctrl_L'].bone.select = 0     
            p_bones['toe_roll_1_L'].bone.select = 1
            bpy.ops.pose.rot_clear()   
            bpy.ops.pose.loc_clear()    
            p_bones['toe_roll_1_L'].bone.select = 0     
            p_bones['toe_roll_2_L'].bone.select = 1
            bpy.ops.pose.rot_clear()   
            bpy.ops.pose.loc_clear()    
            p_bones['toe_roll_2_L'].bone.select = 0         
            sel_act_bones('thigh_ik_L', 'thigh_fk_L', 'rot')                                                                                           
            sel_act_bones('sole_ctrl_L', 'snap_sole_ctrl_fk_L', 'loc_rot')  
            sel_act_bones('foot_ik_ctrl_L', 'foot_fk_L', 'loc_rot')  
            sel_act_bones('toes_ik_ctrl_L', 'snap_toes_ctrl_fk_L', 'loc_rot')  
            sel_act_bones('toes_ik_ctrl_mid_L', 'snap_toes_ctrl_mid_fk_L', 'loc_rot')       
            sel_act_bones('knee_pole_L', 'snap_knee_fk_L', 'loc')                               
                           
            for b in p_bones:        
                b.bone.select = 0
                select_bones = ['sole_ctrl_L', 'knee_pole_L', 'toes_ik_ctrl_L', 'toes_ik_ctrl_mid_L', 'foot_ik_ctrl_L']
                if (b.name in select_bones):
                    b.bone.select = 1                        
            arm_data.layers[30] = False                                       
           
        return {"FINISHED"}      

##### LEG R #####


class Operator_Leg_R_Snap_IK_FK(bpy.types.Operator):    
    
    bl_idname = "leg_r_snap.ik_fk"   
    bl_label = "BlenRig Leg_R Snap IK FK"     
    bl_description = "Prepare seamless switch to FK"    
    bl_options = {'REGISTER', 'UNDO',}      

    @classmethod
    def poll(cls, context):
        if not bpy.context.object:
            return False
        else:
            return (bpy.context.object.type=='ARMATURE' and context.mode=='POSE')
                    
    def execute(self, context):         
        arm = bpy.context.active_object
        arm_data = arm.data
        p_bones = arm.pose.bones
       
        for b in p_bones:
            if ('properties_Leg_R' == b.name):
                prop = int(b.ik_leg_R)
                if prop != 0:
                    self.report({'ERROR'}, 'Only works in IK mode')  
                    return {"CANCELLED"}                  
                   
        #Biped
        if arm_data['rig_type'] == 'Biped':                               
                   
            check_bones = ['thigh_fk_R', 'thigh_ik_R', 'shin_fk_R', 'shin_ik_R', 'foot_fk_R', 'foot_ik_R', 'toe_1_fk_R', 'toe_1_ik_R', 'toe_2_fk_R', 'toe_2_ik_R' ]
            
            for n in check_bones:
                if (n not in p_bones):
                    self.report({'ERROR'}, 'Missing: ' + str(n))  
                    return {"CANCELLED"} 
                  
            for b in p_bones:
                b.bone.select = 0
                if (b.name in check_bones):
                    b.bone.hide = False            
                           
            arm_data.layers[30] = True           
            sel_act_bones('thigh_fk_R', 'thigh_ik_R', 'rot')         
            sel_act_bones('shin_fk_R', 'shin_ik_R', 'rot')  
            sel_act_bones('foot_fk_R', 'foot_ik_R', 'rot')    
            sel_act_bones('toe_1_fk_R', 'toe_1_ik_R', 'rot')  
            sel_act_bones('toe_2_fk_R', 'toe_2_ik_R', 'rot')                                           
                           
            for b in p_bones:        
                b.bone.select = 0
                select_bones = ['thigh_fk_R', 'shin_fk_R', 'foot_fk_R', 'toe_1_fk_R', 'toe_2_fk_R']
                if (b.name in select_bones):
                    b.bone.select = 1                        
            arm_data.layers[30] = False 
            
        #Quadruped
        if arm_data['rig_type'] == 'Quadruped':                               
                   
            check_bones = ['thigh_fk_R', 'thigh_ik_R', 'shin_fk_R', 'shin_ik_R', 'tarsal_fk_R', 'tarsal_ik_R', 'foot_fk_R', 'foot_ik_R', 'toe_1_fk_R', 'toe_1_ik_R', 'toe_2_fk_R', 'toe_2_ik_R' ]
            
            for n in check_bones:
                if (n not in p_bones):
                    self.report({'ERROR'}, 'Missing: ' + str(n))  
                    return {"CANCELLED"} 
                  
            for b in p_bones:
                b.bone.select = 0
                if (b.name in check_bones):
                    b.bone.hide = False            
                           
            arm_data.layers[30] = True           
            sel_act_bones('thigh_fk_R', 'thigh_ik_R', 'rot')         
            sel_act_bones('shin_fk_R', 'shin_ik_R', 'rot')  
            sel_act_bones('tarsal_fk_R', 'tarsal_ik_R', 'rot')              
            sel_act_bones('foot_fk_R', 'foot_ik_R', 'rot')    
            sel_act_bones('toe_1_fk_R', 'toe_1_ik_R', 'rot')  
            sel_act_bones('toe_2_fk_R', 'toe_2_ik_R', 'rot')                                           
                           
            for b in p_bones:        
                b.bone.select = 0
                select_bones = ['thigh_fk_R', 'shin_fk_R', 'tarsal_fk_R', 'foot_fk_R', 'toe_1_fk_R', 'toe_2_fk_R']
                if (b.name in select_bones):
                    b.bone.select = 1                        
            arm_data.layers[30] = False           
           
        return {"FINISHED"}        

class Operator_Leg_R_Snap_FK_IK(bpy.types.Operator):    
    
    bl_idname = "leg_r_snap.fk_ik"   
    bl_label = "BlenRig Leg_R Snap FK IK"  
    bl_description = "Prepare seamless switch to IK"   
    bl_options = {'REGISTER', 'UNDO',}      

    @classmethod
    def poll(cls, context):
        if not bpy.context.object:
            return False
        else:
            return (bpy.context.object.type=='ARMATURE' and context.mode=='POSE')
                    
    def execute(self, context):         
        arm = bpy.context.active_object
        arm_data = arm.data
        p_bones = arm.pose.bones
       
        for b in p_bones:
            if ('properties_leg_R' == b.name):
                prop = int(b.ik_leg_R)
                if prop != 1:
                    self.report({'ERROR'}, 'Only works in FK mode')  
                    return {"CANCELLED"}                  
                   
        #Biped
        if arm_data['rig_type'] == 'Biped':  
                   
            check_bones = ['sole_ctrl_R', 'snap_sole_ctrl_fk_R', 'foot_ik_ctrl_R', 'foot_fk_R', 'toes_ik_ctrl_R', 'snap_toes_ctrl_fk_R', 'toes_ik_ctrl_mid_R', 'snap_toes_ctrl_mid_fk_R', 'knee_pole_R', 'snap_knee_fk_R', 'sole_pivot_point_R', 'foot_roll_ctrl_R', 'toe_roll_1_R', 'toe_roll_2_R']
            
            for n in check_bones:
                if (n not in p_bones):
                    self.report({'ERROR'}, 'Missing: ' + str(n))  
                    return {"CANCELLED"} 
                  
            for b in p_bones:
                b.bone.select = 0
                if (b.name in check_bones):
                    b.bone.hide = False            
                           
            arm_data.layers[30] = True      
            p_bones['sole_pivot_point_R'].bone.select = 1
            bpy.ops.pose.rot_clear()   
            bpy.ops.pose.loc_clear()    
            p_bones['sole_pivot_point_R'].bone.select = 0  
            p_bones['foot_roll_ctrl_R'].bone.select = 1
            bpy.ops.pose.rot_clear()   
            bpy.ops.pose.loc_clear()    
            p_bones['foot_roll_ctrl_R'].bone.select = 0     
            p_bones['toe_roll_1_R'].bone.select = 1
            bpy.ops.pose.rot_clear()   
            bpy.ops.pose.loc_clear()    
            p_bones['toe_roll_1_R'].bone.select = 0     
            p_bones['toe_roll_2_R'].bone.select = 1
            bpy.ops.pose.rot_clear()   
            bpy.ops.pose.loc_clear()    
            p_bones['toe_roll_2_R'].bone.select = 0                                                                                                  
            sel_act_bones('sole_ctrl_R', 'snap_sole_ctrl_fk_R', 'loc_rot')  
            sel_act_bones('foot_ik_ctrl_R', 'foot_fk_R', 'loc_rot')  
            sel_act_bones('toes_ik_ctrl_R', 'snap_toes_ctrl_fk_R', 'loc_rot')  
            sel_act_bones('toes_ik_ctrl_mid_R', 'snap_toes_ctrl_mid_fk_R', 'loc_rot')       
            sel_act_bones('knee_pole_R', 'snap_knee_fk_R', 'loc')                               
                           
            for b in p_bones:        
                b.bone.select = 0
                select_bones = ['sole_ctrl_R', 'knee_pole_R', 'toes_ik_ctrl_R', 'toes_ik_ctrl_mid_R', 'foot_ik_ctrl_R']
                if (b.name in select_bones):
                    b.bone.select = 1                        
            arm_data.layers[30] = False         
            
        #Quadruped
        if arm_data['rig_type'] == 'Quadruped':      
            
            check_bones = ['sole_ctrl_R', 'snap_sole_ctrl_fk_R', 'foot_ik_ctrl_R', 'foot_fk_R', 'toes_ik_ctrl_R', 'snap_toes_ctrl_fk_R', 'toes_ik_ctrl_mid_R', 'snap_toes_ctrl_mid_fk_R', 'thigh_fk_R', 'thigh_ik_R', 'knee_pole_R', 'snap_knee_fk_R', 'sole_pivot_point_R', 'foot_roll_ctrl_R', 'toe_roll_1_R', 'toe_roll_2_R']
            
            for n in check_bones:
                if (n not in p_bones):
                    self.report({'ERROR'}, 'Missing: ' + str(n))  
                    return {"CANCELLED"} 
                  
            for b in p_bones:
                b.bone.select = 0
                if (b.name in check_bones):
                    b.bone.hide = False            
                           
            arm_data.layers[30] = True      
            p_bones['sole_pivot_point_R'].bone.select = 1
            bpy.ops.pose.rot_clear()   
            bpy.ops.pose.loc_clear()    
            p_bones['sole_pivot_point_R'].bone.select = 0  
            p_bones['foot_roll_ctrl_R'].bone.select = 1
            bpy.ops.pose.rot_clear()   
            bpy.ops.pose.loc_clear()    
            p_bones['foot_roll_ctrl_R'].bone.select = 0     
            p_bones['toe_roll_1_R'].bone.select = 1
            bpy.ops.pose.rot_clear()   
            bpy.ops.pose.loc_clear()    
            p_bones['toe_roll_1_R'].bone.select = 0     
            p_bones['toe_roll_2_R'].bone.select = 1
            bpy.ops.pose.rot_clear()   
            bpy.ops.pose.loc_clear()    
            p_bones['toe_roll_2_R'].bone.select = 0         
            sel_act_bones('thigh_ik_R', 'thigh_fk_R', 'rot')                                                                                           
            sel_act_bones('sole_ctrl_R', 'snap_sole_ctrl_fk_R', 'loc_rot')  
            sel_act_bones('foot_ik_ctrl_R', 'foot_fk_R', 'loc_rot')  
            sel_act_bones('toes_ik_ctrl_R', 'snap_toes_ctrl_fk_R', 'loc_rot')  
            sel_act_bones('toes_ik_ctrl_mid_R', 'snap_toes_ctrl_mid_fk_R', 'loc_rot')       
            sel_act_bones('knee_pole_R', 'snap_knee_fk_R', 'loc')                               
                           
            for b in p_bones:        
                b.bone.select = 0
                select_bones = ['sole_ctrl_R', 'knee_pole_R', 'toes_ik_ctrl_R', 'toes_ik_ctrl_mid_R', 'foot_ik_ctrl_R']
                if (b.name in select_bones):
                    b.bone.select = 1                        
            arm_data.layers[30] = False               
           
        return {"FINISHED"}      


#################################### BLENRIG PICKER OPERATORS ####################################################

################### VIEW OPERATOR ##################################



class Operator_Zoom_Selected(bpy.types.Operator):    
    bl_idname = "operator.zoom"  
    bl_label = "BlenRig Zoom to Selected"   
    bl_description = "Zoom to selected / View All"  

    def invoke(self, context, event):     
        if event.ctrl == False and event.shift == False:
            bpy.ops.view3d.view_selected()
        else:
            bpy.ops.view3d.view_all()              
        return {"FINISHED"}
 
 
################### SELECTION OPERATORS ##################################

#Generic Selection Operator Structure

def select_op(self, context, event, b_name): #b_name will be replaced by the actual bone name
    armobj = bpy.context.active_object
    arm = bpy.context.active_object.data
    if (b_name in armobj.pose.bones):        # this line is replaced with actual bone name
        #Target Bone 
        Bone = armobj.pose.bones[b_name]    # this line is replaced with actual bone name             
        #Check if CTRL or SHIFT are pressed
        if event.ctrl == True or event.shift == True:
            #Get previously selected bones
            selected = [b.name for b in bpy.context.selected_pose_bones] 
            #Set target bone as active                  
            for b in armobj.pose.bones:
                b.bone.select = 0
            arm.bones.active = Bone.bone  
            #Reselect previously selected bones
            for b in armobj.pose.bones:
                if (b.name in selected):
                    b.bone.select = 1             
        else:
            for b in armobj.pose.bones:
                b.bone.select = 0
            arm.bones.active = Bone.bone 

######## BODY OPERATORS ########################################### 



#HEAD

class Operator_Head_Stretch(bpy.types.Operator):     
    bl_idname = "operator.head_stretch"  
    bl_label = "BlenRig Select head_stretch"     
    bl_description = "head_stretch"    
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def invoke(self, context, event):
        select_op(self, context, event, "head_stretch")                              
        return {"FINISHED"}    

class Operator_Head_Toon(bpy.types.Operator):    
    bl_idname = "operator.head_toon"     
    bl_label = "BlenRig Select head_toon"     
    bl_description = "head_toon"  
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}      
    
    def invoke(self, context, event):
        select_op(self, context, event, "head_toon")                              
        return {"FINISHED"}        

class Operator_Head_Top_Ctrl(bpy.types.Operator):    
    bl_idname = "operator.head_top_ctrl"     
    bl_label = "BlenRig Select head_top_ctrl"   
    bl_description = "head_top_ctrl" 
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}   
    
    def invoke(self, context, event):
        select_op(self, context, event, "head_top_ctrl")                              
        return {"FINISHED"}                  

class Operator_Head_Mid_Ctrl(bpy.types.Operator):    
    bl_idname = "operator.head_mid_ctrl"     
    bl_label = "BlenRigSelect head_mid_ctrl" 
    bl_description = "head_mid_ctrl"  
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}    

    def invoke(self, context, event):
        select_op(self, context, event, "head_mid_ctrl")                              
        return {"FINISHED"}        
    
class Operator_Head_Mid_Curve(bpy.types.Operator):   
    bl_idname = "operator.head_mid_curve"    
    bl_label = "BlenRig Select head_mid_curve"   
    bl_description = "head_mid_curve"    
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}   
    
    def invoke(self, context, event):
        select_op(self, context, event, "head_mid_curve")                              
        return {"FINISHED"}             
    
class Operator_Mouth_Str_Ctrl(bpy.types.Operator):   
    bl_idname = "operator.mouth_str_ctrl"    
    bl_label = "BlenRig Select mouth_str_ctrl"   
    bl_description = "mouth_str_ctrl"     
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}    
    
    def invoke(self, context, event):
        select_op(self, context, event, "mouth_str_ctrl")                              
        return {"FINISHED"}            

class Operator_Look_L(bpy.types.Operator):   
    bl_idname = "operator.look_l"    
    bl_label = "BlenRIg Select look_L" 
    bl_description = "look_L"         
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}    
    
    def invoke(self, context, event):
        select_op(self, context, event, "look_L")                              
        return {"FINISHED"}        

class Operator_Look_R(bpy.types.Operator):   
    bl_idname = "operator.look_r"    
    bl_label = "BlenRIg Select look_R"  
    bl_description = "look_R"    
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}         

    def invoke(self, context, event):
        select_op(self, context, event, "look_R")                              
        return {"FINISHED"}        

class Operator_Look(bpy.types.Operator):     
    bl_idname = "operator.look"  
    bl_label = "BlenRIg Select look"    
    bl_description = "look"     
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}    
    
    def invoke(self, context, event):
        select_op(self, context, event, "look")                              
        return {"FINISHED"}        

class Operator_Head_FK(bpy.types.Operator):  
    bl_idname = "operator.head_fk"   
    bl_label = "BlenRIg Select head_fk"   
    bl_description = "head_fk"  
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}         
    
    def invoke(self, context, event):
        select_op(self, context, event, "head_fk")                              
        return {"FINISHED"}        

class Operator_Head_IK(bpy.types.Operator):  
    bl_idname = "operator.head_ik_ctrl"  
    bl_label = "BlenRIg Select head_ik_ctrl"   
    bl_description = "head_ik_ctrl"     
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}           

    def invoke(self, context, event):
        armobj = bpy.context.active_object
        arm = bpy.context.active_object.data        
        prop = int(bpy.context.active_object.pose.bones['properties_head'].ik_head)  
        prop_hinge = int(bpy.context.active_object.pose.bones['properties_head'].hinge_head)           
        if ('head_fk' and 'head_ik_ctrl' in armobj.pose.bones):
            #Target Bone            
            if prop == 0 or prop_hinge == 1:
                Bone = armobj.pose.bones["head_ik_ctrl"]
            else:
                Bone = armobj.pose.bones["head_fk"]          
            #Check if CTRL or SHIFT are pressed
            if event.ctrl == True or event.shift == True:
                #Get previously selected bones
                selected = [b.name for b in bpy.context.selected_pose_bones] 
                #Set target bone as active     
                for b in armobj.pose.bones:
                    b.bone.select = 0
                arm.bones.active = Bone.bone  
                #Reselect previously selected bones
                for b in armobj.pose.bones:
                    if (b.name in selected):
                        b.bone.select = 1             
            else:        
                for b in armobj.pose.bones:
                    b.bone.select = 0
                arm.bones.active = Bone.bone                                    
        return {"FINISHED"}    

class Operator_Neck_4_Toon(bpy.types.Operator):  
    bl_idname = "operator.neck_4_toon"   
    bl_label = "BlenRig Select neck_4_toon" 
    bl_description = "neck_4_toon"      
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}    
    
    def invoke(self, context, event):
        select_op(self, context, event, "neck_4_toon")                              
        return {"FINISHED"}        
    
class Operator_Face_Toon_Up(bpy.types.Operator):     
    bl_idname = "operator.face_toon_up"  
    bl_label = "BlenRig Select face_toon_up"   
    bl_description = "face_toon_up"   
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}     
    
    def invoke(self, context, event):
        select_op(self, context, event, "face_toon_up")                              
        return {"FINISHED"}           
    
class Operator_Face_Toon_Mid(bpy.types.Operator):    
    bl_idname = "operator.face_toon_mid"     
    bl_label = "BlenRig Select face_toon_mid"   
    bl_description = "face_toon_mid"        
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}     
    
    def invoke(self, context, event):
        select_op(self, context, event, "face_toon_mid")                              
        return {"FINISHED"}        
    
class Operator_Face_Toon_Low(bpy.types.Operator):    
    bl_idname = "operator.face_toon_low"     
    bl_label = "BlenRig Select face_toon_low"     
    bl_description = "face_toon_low"   
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}   
    
    def invoke(self, context, event):
        select_op(self, context, event, "face_toon_low")                              
        return {"FINISHED"}                

#NECK

class Operator_Neck_3(bpy.types.Operator):   
    bl_idname = "operator.neck_3"    
    bl_label = "BlenRig Select neck_3"  
    bl_description = "neck_3_ik_ctrl / neck_3_fk"       
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}    

    def invoke(self, context, event):
        armobj = bpy.context.active_object
        arm = bpy.context.active_object.data
        prop = int(bpy.context.active_object.pose.bones['properties_head'].ik_head)        
        if ('neck_3_ik_ctrl' and 'neck_3_fk' in armobj.pose.bones):
            #Target Bone            
            if prop == 0:
                Bone = armobj.pose.bones["neck_3_ik_ctrl"]
            else:
                Bone = armobj.pose.bones["neck_3_fk"]            
            #Check if CTRL or SHIFT are pressed
            if event.ctrl == True or event.shift == True:
                #Get previously selected bones
                selected = [b.name for b in bpy.context.selected_pose_bones] 
                #Set target bone as active     
                for b in armobj.pose.bones:
                    b.bone.select = 0
                arm.bones.active = Bone.bone  
                #Reselect previously selected bones
                for b in armobj.pose.bones:
                    if (b.name in selected):
                        b.bone.select = 1             
            else:        
                for b in armobj.pose.bones:
                    b.bone.select = 0
                arm.bones.active = Bone.bone                                    
        return {"FINISHED"} 
    
class Operator_Neck_2(bpy.types.Operator):   
    bl_idname = "operator.neck_2"    
    bl_label = "BlenRig Select neck_2" 
    bl_description = "neck_2_ik_ctrl / neck_2_fk"       
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}                

    def invoke(self, context, event):
        armobj = bpy.context.active_object
        arm = bpy.context.active_object.data
        prop = int(bpy.context.active_object.pose.bones['properties_head'].ik_head)        
        if ('neck_2_ik_ctrl' and 'neck_2_fk' in armobj.pose.bones):
            #Target Bone            
            if prop == 0:
                Bone = armobj.pose.bones["neck_2_ik_ctrl"]
            else:
                Bone = armobj.pose.bones["neck_2_fk"]            
            #Check if CTRL or SHIFT are pressed
            if event.ctrl == True or event.shift == True:
                #Get previously selected bones
                selected = [b.name for b in bpy.context.selected_pose_bones] 
                #Set target bone as active     
                for b in armobj.pose.bones:
                    b.bone.select = 0
                arm.bones.active = Bone.bone  
                #Reselect previously selected bones
                for b in armobj.pose.bones:
                    if (b.name in selected):
                        b.bone.select = 1             
            else:        
                for b in armobj.pose.bones:
                    b.bone.select = 0
                arm.bones.active = Bone.bone                                    
        return {"FINISHED"}  

class Operator_Neck_1(bpy.types.Operator):   
    bl_idname = "operator.neck_1"    
    bl_label = "BlenRig Select neck_1"
    bl_description = "neck_1_fk"                
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}       
    
    def invoke(self, context, event):
        select_op(self, context, event, "neck_1_fk")                              
        return {"FINISHED"}            
    
class Operator_Neck_3_Toon(bpy.types.Operator):  
    bl_idname = "operator.neck_3_toon"   
    bl_label = "BlenRig Select neck_3_toon" 
    bl_description = "neck_3_toon"      
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}      
    
    def invoke(self, context, event):
        select_op(self, context, event, "neck_3_toon")                              
        return {"FINISHED"}         

class Operator_Neck_2_Toon(bpy.types.Operator):  
    bl_idname = "operator.neck_2_toon"   
    bl_label = "BlenRig Select neck_2_toon"  
    bl_description = "neck_2_toon"        
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}     
    
    def invoke(self, context, event):
        select_op(self, context, event, "neck_2_toon")                              
        return {"FINISHED"}          
    
class Operator_Neck_Ctrl(bpy.types.Operator):    
    bl_idname = "operator.neck_ctrl"     
    bl_label = "BlenRig Select neck_ctrl"  
    bl_description = "neck_ik_ctrl / neck_fk_ctrl"       
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}             

    def invoke(self, context, event):
        armobj = bpy.context.active_object
        arm = bpy.context.active_object.data
        prop = int(bpy.context.active_object.pose.bones['properties_head'].ik_head)        
        if ('neck_ik_ctrl' and 'neck_fk_ctrl' in armobj.pose.bones):
            #Target Bone            
            if prop == 0:
                Bone = armobj.pose.bones["neck_ik_ctrl"]
            else:
                Bone = armobj.pose.bones["neck_fk_ctrl"]             
            #Check if CTRL or SHIFT are pressed
            if event.ctrl == True or event.shift == True:
                #Get previously selected bones
                selected = [b.name for b in bpy.context.selected_pose_bones] 
                #Set target bone as active     
                for b in armobj.pose.bones:
                    b.bone.select = 0
                arm.bones.active = Bone.bone  
                #Reselect previously selected bones
                for b in armobj.pose.bones:
                    if (b.name in selected):
                        b.bone.select = 1             
            else:        
                for b in armobj.pose.bones:
                    b.bone.select = 0
                arm.bones.active = Bone.bone                                    
        return {"FINISHED"}     

#SHOULDERS

class Operator_Clavi_Toon_R(bpy.types.Operator):     
    bl_idname = "operator.clavi_toon_r"  
    bl_label = "BlenRig Select clavi_toon_R"     
    bl_description = "clavi_toon_R"    
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}    
    
    def invoke(self, context, event):
        select_op(self, context, event, "clavi_toon_R")                              
        return {"FINISHED"}           

class Operator_Shoulder_Rot_R(bpy.types.Operator):   
    bl_idname = "operator.shoulder_rot_r"    
    bl_label = "BlenRig Select shoulder_rot_R"   
    bl_description = "shoulder_rot_R"        
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}       
    
    def invoke(self, context, event):
        select_op(self, context, event, "shoulder_rot_R")                              
        return {"FINISHED"}        

class Operator_Shoulder_R(bpy.types.Operator):   
    bl_idname = "operator.shoulder_r"    
    bl_label = "BlenRig Select shoulder_R"  
    bl_description = "shoulder_R"         
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}       
    
    def invoke(self, context, event):
        select_op(self, context, event, "shoulder_R")                              
        return {"FINISHED"}        

class Operator_Head_Scale(bpy.types.Operator):   
    bl_idname = "operator.head_scale"    
    bl_label = "BlenRig Select head_scale"   
    bl_description = "head_scale"         
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'} 
    
    def invoke(self, context, event):
        select_op(self, context, event, "head_scale")                              
        return {"FINISHED"}              
    
class Operator_Shoulder_L(bpy.types.Operator):   
    bl_idname = "operator.shoulder_l"    
    bl_label = "BlenRig Select shoulder_L"  
    bl_description = "shoulder_L"        
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}   
    
    def invoke(self, context, event):
        select_op(self, context, event, "shoulder_L")                              
        return {"FINISHED"}            

class Operator_Shoulder_Rot_L(bpy.types.Operator):   
    bl_idname = "operator.shoulder_rot_l"    
    bl_label = "BlenRig Select shoulder_rot_L"   
    bl_description = "shoulder_rot_L"          
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}      
    
    def invoke(self, context, event):
        select_op(self, context, event, "shoulder_rot_L")                              
        return {"FINISHED"}         

class Operator_Clavi_Toon_L(bpy.types.Operator):     
    bl_idname = "operator.clavi_toon_l"  
    bl_label = "BlenRig Select clavi_toon_L"  
    bl_description = "clavi_toon_L"      
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}     
    
    def invoke(self, context, event):
        select_op(self, context, event, "clavi_toon_L")                              
        return {"FINISHED"}          
    
#ARM_R

class Operator_Arm_Toon_R(bpy.types.Operator):   
    bl_idname = "operator.arm_toon_r"    
    bl_label = "BlenRig Select arm_toon_R"  
    bl_description = "arm_toon_R"        
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}       
    
    def invoke(self, context, event):
        select_op(self, context, event, "arm_toon_R")                              
        return {"FINISHED"}        

class Operator_Elbow_Pole_R(bpy.types.Operator):     
    bl_idname = "operator.elbow_pole_r"  
    bl_label = "BlenRig Select elbow_pole_R"  
    bl_description = "elbow_pole_R"      
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}       
    
    def invoke(self, context, event):
        select_op(self, context, event, "elbow_pole_R")                              
        return {"FINISHED"}        

class Operator_Forearm_Toon_R(bpy.types.Operator):   
    bl_idname = "operator.forearm_toon_r"    
    bl_label = "BlenRig Select forearm_toon_R"  
    bl_description = "forearm_toon_R"        
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}       
    
    def invoke(self, context, event):
        select_op(self, context, event, "forearm_toon_R")                              
        return {"FINISHED"}        

class Operator_Arm_Scale_R(bpy.types.Operator):  
    bl_idname = "operator.arm_scale_r"   
    bl_label = "BlenRig Select arm_scale_R"  
    bl_description = "arm_scale_R"       
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}       
    
    def invoke(self, context, event):
        select_op(self, context, event, "arm_scale_R")                              
        return {"FINISHED"}        

class Operator_Arm_FK_R(bpy.types.Operator):     
    bl_idname = "operator.arm_fk_r"  
    bl_label = "BlenRig Select arm_fk_R"  
    bl_description = "arm_fk_R"      
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}      
    
    def invoke(self, context, event):
        select_op(self, context, event, "arm_fk_R")                              
        return {"FINISHED"}         

class Operator_Arm_IK_R(bpy.types.Operator):     
    bl_idname = "operator.arm_ik_r"  
    bl_label = "BlenRig Select arm_ik_R"  
    bl_description = "arm_ik_R"      
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}    
    
    def invoke(self, context, event):
        select_op(self, context, event, "arm_ik_R")                              
        return {"FINISHED"}           

class Operator_Elbow_Toon_R(bpy.types.Operator):     
    bl_idname = "operator.elbow_toon_r"  
    bl_label = "BlenRig Select elbow_toon_R"  
    bl_description = "elbow_toon_R"      
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}       
    
    def invoke(self, context, event):
        select_op(self, context, event, "elbow_toon_R")                              
        return {"FINISHED"}         
    
class Operator_Forearm_FK_R(bpy.types.Operator):     
    bl_idname = "operator.forearm_fk_r"  
    bl_label = "BlenRig Select forearm_fk_R"  
    bl_description = "forearm_fk_R"      
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}       
    
    def invoke(self, context, event):
        select_op(self, context, event, "forearm_fk_R")                              
        return {"FINISHED"}        

class Operator_Forearm_IK_R(bpy.types.Operator):     
    bl_idname = "operator.forearm_ik_r"  
    bl_label = "BlenRig Select forearm_ik_R"  
    bl_description = "forearm_ik_R"      
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}       
    
    def invoke(self, context, event):
        select_op(self, context, event, "forearm_ik_R")                              
        return {"FINISHED"}        

class Operator_Hand_Toon_R(bpy.types.Operator):  
    bl_idname = "operator.hand_toon_r"   
    bl_label = "BlenRig Select hand_toon_R"  
    bl_description = "hand_toon_R"       
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}       
    
    def invoke(self, context, event):
        select_op(self, context, event, "hand_toon_R")                              
        return {"FINISHED"}        

#ARM_L

class Operator_Arm_Toon_L(bpy.types.Operator):   
    bl_idname = "operator.arm_toon_l"    
    bl_label = "BlenRig Select arm_toon_L"  
    bl_description = "arm_toon_L"        
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}      
    
    def invoke(self, context, event):
        select_op(self, context, event, "arm_toon_L")                              
        return {"FINISHED"}         

class Operator_Elbow_Pole_L(bpy.types.Operator):     
    bl_idname = "operator.elbow_pole_l"  
    bl_label = "BlenRig Select elbow_pole_L"  
    bl_description = "elbow_pole_L"      
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}     
    
    def invoke(self, context, event):
        select_op(self, context, event, "elbow_pole_L")                              
        return {"FINISHED"}          

class Operator_Forearm_Toon_L(bpy.types.Operator):   
    bl_idname = "operator.forearm_toon_l"    
    bl_label = "BlenRig Select forearm_toon_L"  
    bl_description = "forearm_toon_L"        
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}       
    
    def invoke(self, context, event):
        select_op(self, context, event, "forearm_toon_L")                              
        return {"FINISHED"}        

class Operator_Arm_Scale_L(bpy.types.Operator):  
    bl_idname = "operator.arm_scale_l"   
    bl_label = "BlenRig Select arm_scale_L"  
    bl_description = "arm_scale_L"       
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}   
    
    def invoke(self, context, event):
        select_op(self, context, event, "arm_scale_L")                              
        return {"FINISHED"}            

class Operator_Arm_FK_L(bpy.types.Operator):     
    bl_idname = "operator.arm_fk_l"  
    bl_label = "BlenRig Select arm_fk_L"  
    bl_description = "arm_fk_L"      
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}    
    
    def invoke(self, context, event):
        select_op(self, context, event, "arm_fk_L")                              
        return {"FINISHED"}           

class Operator_Arm_IK_L(bpy.types.Operator):     
    bl_idname = "operator.arm_ik_l"  
    bl_label = "BlenRig Select arm_ik_L"  
    bl_description = "arm_ik_L"      
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}     
    
    def invoke(self, context, event):
        select_op(self, context, event, "arm_ik_L")                              
        return {"FINISHED"}          

class Operator_Elbow_Toon_L(bpy.types.Operator):     
    bl_idname = "operator.elbow_toon_l"  
    bl_label = "BlenRig Select elbow_toon_L"  
    bl_description = "elbow_toon_L"      
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}     
    
    def invoke(self, context, event):
        select_op(self, context, event, "elbow_toon_L")                              
        return {"FINISHED"}          
    
class Operator_Forearm_FK_L(bpy.types.Operator):     
    bl_idname = "operator.forearm_fk_l"  
    bl_label = "BlenRig Select forearm_fk_L"  
    bl_description = "forearm_fk_L"      
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}   
    
    def invoke(self, context, event):
        select_op(self, context, event, "forearm_fk_L")                              
        return {"FINISHED"}            

class Operator_Forearm_IK_L(bpy.types.Operator):     
    bl_idname = "operator.forearm_ik_l"  
    bl_label = "BlenRig Select forearm_ik_L"  
    bl_description = "forearm_ik_L"      
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}      
    
    def invoke(self, context, event):
        select_op(self, context, event, "forearm_ik_L")                              
        return {"FINISHED"}         

class Operator_Hand_Toon_L(bpy.types.Operator):  
    bl_idname = "operator.hand_toon_l"   
    bl_label = "BlenRig Select hand_toon_L"  
    bl_description = "hand_toon_L"       
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}     
    
    def invoke(self, context, event):
        select_op(self, context, event, "hand_toon_L")                              
        return {"FINISHED"}          

#SPINE  

class Operator_Torso_Ctrl(bpy.types.Operator):   
    bl_idname = "operator.torso_ctrl"    
    bl_label = "BlenRig Select torso_ctrl"  
    bl_description = "torso_ik_ctrl / torso_fk_ctrl / torso_inv_ctrl"    
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}       

    def invoke(self, context, event):
        armobj = bpy.context.active_object
        arm = bpy.context.active_object.data
        prop = int(bpy.context.active_object.pose.bones['properties_torso'].ik_torso)
        prop_inv = int(bpy.context.active_object.pose.bones['properties_torso'].inv_torso)                 
        if ('torso_ik_ctrl' and 'torso_fk_ctrl' and 'torso_inv_ctrl' in armobj.pose.bones):
            #Target Bone            
            if prop == 0 and prop_inv != 1:
                Bone = armobj.pose.bones["torso_ik_ctrl"]
            elif prop != 0 and prop_inv != 1:
                Bone = armobj.pose.bones["torso_fk_ctrl"]     
            else:
                Bone = armobj.pose.bones["torso_inv_ctrl"]          
            #Check if CTRL or SHIFT are pressed
            if event.ctrl == True or event.shift == True:
                #Get previously selected bones
                selected = [b.name for b in bpy.context.selected_pose_bones] 
                #Set target bone as active     
                for b in armobj.pose.bones:
                    b.bone.select = 0
                arm.bones.active = Bone.bone  
                #Reselect previously selected bones
                for b in armobj.pose.bones:
                    if (b.name in selected):
                        b.bone.select = 1             
            else:        
                for b in armobj.pose.bones:
                    b.bone.select = 0
                arm.bones.active = Bone.bone                                    
        return {"FINISHED"}    

class Operator_Spine_3(bpy.types.Operator):  
    bl_idname = "operator.spine_3"   
    bl_label = "BlenRig Select spine_3" 
    bl_description = "spine_4_ik_ctrl / spine_3_fk / spine_3_inv"     
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}      

    def invoke(self, context, event):
        armobj = bpy.context.active_object
        arm = bpy.context.active_object.data
        prop = int(bpy.context.active_object.pose.bones['properties_torso'].ik_torso)
        prop_inv = int(bpy.context.active_object.pose.bones['properties_torso'].inv_torso)                 
        if ('spine_4_ik_ctrl' and 'spine_3_fk' and 'spine_3_inv' in armobj.pose.bones):
            #Target Bone            
            if prop == 0 and prop_inv != 1:
                Bone = armobj.pose.bones["spine_4_ik_ctrl"]
            elif prop != 0 and prop_inv != 1:
                Bone = armobj.pose.bones["spine_3_fk"]    
            else:
                Bone = armobj.pose.bones["spine_3_inv"]         
            #Check if CTRL or SHIFT are pressed
            if event.ctrl == True or event.shift == True:
                #Get previously selected bones
                selected = [b.name for b in bpy.context.selected_pose_bones] 
                #Set target bone as active     
                for b in armobj.pose.bones:
                    b.bone.select = 0
                arm.bones.active = Bone.bone  
                #Reselect previously selected bones
                for b in armobj.pose.bones:
                    if (b.name in selected):
                        b.bone.select = 1             
            else:        
                for b in armobj.pose.bones:
                    b.bone.select = 0
                arm.bones.active = Bone.bone                                    
        return {"FINISHED"}     

class Operator_Spine_2(bpy.types.Operator):  
    bl_idname = "operator.spine_2"   
    bl_label = "BlenRig Select spine_2" 
    bl_description = "spine_3_ik_ctrl / spine_2_fk / spine_2_inv"      
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}     

    def invoke(self, context, event):
        armobj = bpy.context.active_object
        arm = bpy.context.active_object.data
        prop = int(bpy.context.active_object.pose.bones['properties_torso'].ik_torso)
        prop_inv = int(bpy.context.active_object.pose.bones['properties_torso'].inv_torso)                 
        if ('spine_3_ik_ctrl' and 'spine_2_fk' and 'spine_2_inv' in armobj.pose.bones):
            #Target Bone            
            if prop == 0 and prop_inv != 1:
                Bone = armobj.pose.bones["spine_3_ik_ctrl"]
            elif prop != 0 and prop_inv != 1:
                Bone = armobj.pose.bones["spine_2_fk"]    
            else:
                Bone = armobj.pose.bones["spine_2_inv"]         
            #Check if CTRL or SHIFT are pressed
            if event.ctrl == True or event.shift == True:
                #Get previously selected bones
                selected = [b.name for b in bpy.context.selected_pose_bones] 
                #Set target bone as active     
                for b in armobj.pose.bones:
                    b.bone.select = 0
                arm.bones.active = Bone.bone  
                #Reselect previously selected bones
                for b in armobj.pose.bones:
                    if (b.name in selected):
                        b.bone.select = 1             
            else:        
                for b in armobj.pose.bones:
                    b.bone.select = 0
                arm.bones.active = Bone.bone                                    
        return {"FINISHED"}   
    
class Operator_Spine_1(bpy.types.Operator):  
    bl_idname = "operator.spine_1"   
    bl_label = "BlenRig Select spine_1" 
    bl_description = "spine_2_ik_ctrl / spine_1_fk / spine_1_inv"      
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}     

    def invoke(self, context, event):
        armobj = bpy.context.active_object
        arm = bpy.context.active_object.data
        prop = int(bpy.context.active_object.pose.bones['properties_torso'].ik_torso)
        prop_inv = int(bpy.context.active_object.pose.bones['properties_torso'].inv_torso)                 
        if ('spine_2_ik_ctrl' and 'spine_1_fk' and 'spine_1_inv' in armobj.pose.bones):
            #Target Bone            
            if prop == 0 and prop_inv != 1:
                Bone = armobj.pose.bones["spine_2_ik_ctrl"]
            elif prop != 0 and prop_inv != 1:
                Bone = armobj.pose.bones["spine_1_fk"]    
            else:
                Bone = armobj.pose.bones["spine_1_inv"]         
            #Check if CTRL or SHIFT are pressed
            if event.ctrl == True or event.shift == True:
                #Get previously selected bones
                selected = [b.name for b in bpy.context.selected_pose_bones] 
                #Set target bone as active     
                for b in armobj.pose.bones:
                    b.bone.select = 0
                arm.bones.active = Bone.bone  
                #Reselect previously selected bones
                for b in armobj.pose.bones:
                    if (b.name in selected):
                        b.bone.select = 1             
            else:        
                for b in armobj.pose.bones:
                    b.bone.select = 0
                arm.bones.active = Bone.bone                                    
        return {"FINISHED"}          

class Operator_Spine_4_Toon(bpy.types.Operator):     
    bl_idname = "operator.spine_4_toon"  
    bl_label = "BlenRig Select spine_4_toon"  
    bl_description = "spine_4_toon"      
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}       
    
    def invoke(self, context, event):
        select_op(self, context, event, "spine_4_toon")                              
        return {"FINISHED"}        

class Operator_Spine_3_Toon(bpy.types.Operator):     
    bl_idname = "operator.spine_3_toon"  
    bl_label = "BlenRig Select spine_3_toon"  
    bl_description = "spine_3_toon"      
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}       
    
    def invoke(self, context, event):
        select_op(self, context, event, "spine_3_toon")                              
        return {"FINISHED"}        

class Operator_Spine_2_Toon(bpy.types.Operator):     
    bl_idname = "operator.spine_2_toon"  
    bl_label = "BlenRig Select spine_2_toon"  
    bl_description = "spine_2_toon"      
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}  
    
    def invoke(self, context, event):
        select_op(self, context, event, "spine_2_toon")                              
        return {"FINISHED"}             
    
class Operator_Spine_1_Toon(bpy.types.Operator):     
    bl_idname = "operator.spine_1_toon"  
    bl_label = "BlenRig Select spine_1_toon"  
    bl_description = "spine_1_toon"      
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}  
    
    def invoke(self, context, event):
        select_op(self, context, event, "spine_1_toon")                              
        return {"FINISHED"}             

class Operator_Spine_3_Inv_Ctrl(bpy.types.Operator):     
    bl_idname = "operator.spine_3_inv_ctrl"  
    bl_label = "BlenRig Select spine_3_inv_ctrl"  
    bl_description = "spine_3_inv_ctrl"      
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}    
    
    def invoke(self, context, event):
        select_op(self, context, event, "spine_3_inv_ctrl")                              
        return {"FINISHED"}           

class Operator_Pelvis_Toon(bpy.types.Operator):  
    bl_idname = "operator.pelvis_toon"   
    bl_label = "BlenRig Select pelvis_toon"  
    bl_description = "pelvis_toon"       
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}   
    
    def invoke(self, context, event):
        select_op(self, context, event, "pelvis_toon")                              
        return {"FINISHED"}            

class Operator_Pelvis_Ctrl(bpy.types.Operator):  
    bl_idname = "operator.pelvis_ctrl"   
    bl_label = "BlenRig Select spine_1" 
    bl_description = "pelvis_ctrl / pelvis_inv"     
    bl_options = {'INTERNAL'}

    def invoke(self, context, event):
        armobj = bpy.context.active_object
        arm = bpy.context.active_object.data
        prop = int(bpy.context.active_object.pose.bones['properties_torso'].ik_torso)
        prop_inv = int(bpy.context.active_object.pose.bones['properties_torso'].inv_torso)                 
        if ('pelvis_ctrl' and 'pelvis_inv' in armobj.pose.bones):
            #Target Bone            
            if prop_inv == 0:
                Bone = armobj.pose.bones["pelvis_ctrl"]
            else:
                Bone = armobj.pose.bones["pelvis_inv"]    
                       
            #Check if CTRL or SHIFT are pressed
            if event.ctrl == True or event.shift == True:
                #Get previously selected bones
                selected = [b.name for b in bpy.context.selected_pose_bones] 
                #Set target bone as active     
                for b in armobj.pose.bones:
                    b.bone.select = 0
                arm.bones.active = Bone.bone  
                #Reselect previously selected bones
                for b in armobj.pose.bones:
                    if (b.name in selected):
                        b.bone.select = 1             
            else:        
                for b in armobj.pose.bones:
                    b.bone.select = 0
                arm.bones.active = Bone.bone                                    
        return {"FINISHED"} 
    
class Operator_Master_Torso_Pivot_Point(bpy.types.Operator):     
    bl_idname = "operator.master_torso_pivot_point"  
    bl_label = "BlenRig Select master_torso_pivot_point"  
    bl_description = "master_torso_pivot_point"      
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'} 
    
    def invoke(self, context, event):
        select_op(self, context, event, "master_torso_pivot_point")                              
        return {"FINISHED"}              

class Operator_Master_Torso(bpy.types.Operator):     
    bl_idname = "operator.master_torso"  
    bl_label = "BlenRig Select master_torso"  
    bl_description = "master_torso"      
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}    
    
    def invoke(self, context, event):
        select_op(self, context, event, "master_torso")                              
        return {"FINISHED"}           

#HAND_R

class Operator_Hand_Roll_R(bpy.types.Operator):  
    bl_idname = "operator.hand_roll_r"   
    bl_label = "BlenRig Select hand_roll_R" 
    bl_description = "palm_bend_ik_ctrl_R / palm_bend_fk_ctrl_R"        
    bl_options = {'INTERNAL'}

    def invoke(self, context, event):
        armobj = bpy.context.active_object
        arm = bpy.context.active_object.data
        prop = int(bpy.context.active_object.pose.bones['properties_arm_R'].ik_arm_R)
        prop_hinge = int(bpy.context.active_object.pose.bones['properties_arm_R'].hinge_hand_R)    
        if ('palm_bend_ik_ctrl_R' and 'palm_bend_fk_ctrl_R' in armobj.pose.bones):
            #Target Bone            
            if prop == 1 or prop_hinge == 0:
                Bone = armobj.pose.bones["palm_bend_fk_ctrl_R"]
            else:
                Bone = armobj.pose.bones["palm_bend_ik_ctrl_R"]   
                       
            #Check if CTRL or SHIFT are pressed
            if event.ctrl == True or event.shift == True:
                #Get previously selected bones
                selected = [b.name for b in bpy.context.selected_pose_bones] 
                #Set target bone as active     
                for b in armobj.pose.bones:
                    b.bone.select = 0
                arm.bones.active = Bone.bone  
                #Reselect previously selected bones
                for b in armobj.pose.bones:
                    if (b.name in selected):
                        b.bone.select = 1             
            else:        
                for b in armobj.pose.bones:
                    b.bone.select = 0
                arm.bones.active = Bone.bone                                    
        return {"FINISHED"} 

class Operator_Hand_IK_Pivot_Point_R(bpy.types.Operator):    
    bl_idname = "operator.hand_ik_pivot_point_r"     
    bl_label = "BlenRig Select hand_ik_pivot_point_R"  
    bl_description = "hand_ik_pivot_point_R"         
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}   
    
    def invoke(self, context, event):
        select_op(self, context, event, "hand_ik_pivot_point_R")                              
        return {"FINISHED"}            
    
class Operator_Hand_IK_Ctrl_R(bpy.types.Operator):   
    bl_idname = "operator.hand_ik_ctrl_r"    
    bl_label = "BlenRig Select hand_ik_ctrl_R"  
    bl_description = "hand_ik_ctrl_R"        
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}      
    
    def invoke(self, context, event):
        select_op(self, context, event, "hand_ik_ctrl_R")                              
        return {"FINISHED"}         
    
class Operator_Hand_FK_R(bpy.types.Operator):    
    bl_idname = "operator.hand_fk_r"     
    bl_label = "BlenRig Select hand_fk_R"  
    bl_description = "hand_fk_R"         
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}       
    
    def invoke(self, context, event):
        select_op(self, context, event, "hand_fk_R")                              
        return {"FINISHED"}        

class Operator_Fing_Spread_R(bpy.types.Operator):    
    bl_idname = "operator.fing_spread_r"     
    bl_label = "BlenRig Select fing_spread_R"  
    bl_description = "fing_spread_R"         
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}  
    
    def invoke(self, context, event):
        select_op(self, context, event, "fing_spread_R")                              
        return {"FINISHED"}             
    
class Operator_Fing_Lit_Ctrl_R(bpy.types.Operator):  
    bl_idname = "operator.fing_lit_ctrl_r"   
    bl_label = "BlenRig Select fing_lit_ctrl_R"  
    bl_description = "fing_lit_ctrl_R"       
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}       
    
    def invoke(self, context, event):
        select_op(self, context, event, "fing_lit_ctrl_R")                              
        return {"FINISHED"}        
    
class Operator_Fing_Lit_2_R(bpy.types.Operator):     
    bl_idname = "operator.fing_lit_2_r"  
    bl_label = "BlenRig Select fing_lit_2_R"  
    bl_description = "fing_lit_2_R"      
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}       
    
    def invoke(self, context, event):
        select_op(self, context, event, "fing_lit_2_R")                              
        return {"FINISHED"}        
    
class Operator_Fing_Lit_3_R(bpy.types.Operator):     
    bl_idname = "operator.fing_lit_3_r"  
    bl_label = "BlenRig Select fing_lit_3_R"  
    bl_description = "fing_lit_3_R"      
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}  
    
    def invoke(self, context, event):
        select_op(self, context, event, "fing_lit_3_R")                              
        return {"FINISHED"}                 

class Operator_Fing_Lit_4_R(bpy.types.Operator):     
    bl_idname = "operator.fing_lit_4_r"  
    bl_label = "BlenRig Select fing_lit_4_R"  
    bl_description = "fing_lit_4_R"      
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}     
    
    def invoke(self, context, event):
        select_op(self, context, event, "fing_lit_4_R")                              
        return {"FINISHED"}          

class Operator_Fing_Ring_Ctrl_R(bpy.types.Operator):     
    bl_idname = "operator.fing_ring_ctrl_r"  
    bl_label = "BlenRig Select fing_ring_ctrl_R"  
    bl_description = "fing_ring_ctrl_R"      
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}    
    
    def invoke(self, context, event):
        select_op(self, context, event, "fing_ring_ctrl_R")                              
        return {"FINISHED"}           
    
class Operator_Fing_Ring_2_R(bpy.types.Operator):    
    bl_idname = "operator.fing_ring_2_r"     
    bl_label = "BlenRig Select fing_ring_2_R"  
    bl_description = "fing_ring_2_R"         
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}  
    
    def invoke(self, context, event):
        select_op(self, context, event, "fing_ring_2_R")                              
        return {"FINISHED"}             
    
class Operator_Fing_Ring_3_R(bpy.types.Operator):    
    bl_idname = "operator.fing_ring_3_r"     
    bl_label = "BlenRig Select fing_ring_3_R"  
    bl_description = "fing_ring_3_R"         
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}    
    
    def invoke(self, context, event):
        select_op(self, context, event, "fing_ring_3_R")                              
        return {"FINISHED"}                  

class Operator_Fing_Ring_4_R(bpy.types.Operator):    
    bl_idname = "operator.fing_ring_4_r"     
    bl_label = "BlenRig Select fing_ring_4_R"  
    bl_description = "fing_ring_4_R"         
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}  
    
    def invoke(self, context, event):
        select_op(self, context, event, "fing_ring_4_R")                              
        return {"FINISHED"}             

class Operator_Fing_Mid_Ctrl_R(bpy.types.Operator):  
    bl_idname = "operator.fing_mid_ctrl_r"   
    bl_label = "BlenRig Select fing_mid_ctrl_R"  
    bl_description = "fing_mid_ctrl_R"       
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}    
    
    def invoke(self, context, event):
        select_op(self, context, event, "fing_mid_ctrl_R")                              
        return {"FINISHED"}           
    
class Operator_Fing_Mid_2_R(bpy.types.Operator):     
    bl_idname = "operator.fing_mid_2_r"  
    bl_label = "BlenRig Select fing_mid_2_R"  
    bl_description = "fing_mid_2_R"      
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'} 
    
    def invoke(self, context, event):
        select_op(self, context, event, "fing_mid_2_R")                              
        return {"FINISHED"}              
    
class Operator_Fing_Mid_3_R(bpy.types.Operator):     
    bl_idname = "operator.fing_mid_3_r"  
    bl_label = "BlenRig Select fing_mid_3_R"  
    bl_description = "fing_mid_3_R"      
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}   
    
    def invoke(self, context, event):
        select_op(self, context, event, "fing_mid_3_R")                              
        return {"FINISHED"}                    

class Operator_Fing_Mid_4_R(bpy.types.Operator):     
    bl_idname = "operator.fing_mid_4_r"  
    bl_label = "BlenRig Select fing_mid_4_R"  
    bl_description = "fing_mid_4_R"      
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}     
    
    def invoke(self, context, event):
        select_op(self, context, event, "fing_mid_4_R")                              
        return {"FINISHED"}          

class Operator_Fing_Ind_Ctrl_R(bpy.types.Operator):  
    bl_idname = "operator.fing_ind_ctrl_r"   
    bl_label = "BlenRig Select fing_ind_ctrl_R"  
    bl_description = "fing_ind_ctrl_R"       
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}  
    
    def invoke(self, context, event):
        select_op(self, context, event, "fing_ind_ctrl_R")                              
        return {"FINISHED"}             
    
class Operator_Fing_Ind_2_R(bpy.types.Operator):     
    bl_idname = "operator.fing_ind_2_r"  
    bl_label = "BlenRig Select fing_ind_2_R"  
    bl_description = "fing_ind_2_R"      
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}       
    
    def invoke(self, context, event):
        select_op(self, context, event, "fing_ind_2_R")                              
        return {"FINISHED"}        
    
class Operator_Fing_Ind_3_R(bpy.types.Operator):     
    bl_idname = "operator.fing_ind_3_r"  
    bl_label = "BlenRig Select fing_ind_3_R"  
    bl_description = "fing_ind_3_R"      
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}      
    
    def invoke(self, context, event):
        select_op(self, context, event, "fing_ind_3_R")                              
        return {"FINISHED"}                  

class Operator_Fing_Ind_4_R(bpy.types.Operator):     
    bl_idname = "operator.fing_ind_4_r"  
    bl_label = "BlenRig Select fing_ind_4_R"  
    bl_description = "fing_ind_4_R"      
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}       
    
    def invoke(self, context, event):
        select_op(self, context, event, "fing_ind_4_R")                              
        return {"FINISHED"}        

class Operator_Fing_Thumb_Ctrl_R(bpy.types.Operator):    
    bl_idname = "operator.fing_thumb_ctrl_r"     
    bl_label = "BlenRig Select fing_thumb_ctrl_R"  
    bl_description = "fing_thumb_ctrl_R"         
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}       
    
    def invoke(self, context, event):
        select_op(self, context, event, "fing_thumb_ctrl_R")                              
        return {"FINISHED"}         

class Operator_Fing_Thumb_1_R(bpy.types.Operator):   
    bl_idname = "operator.fing_thumb_1_r"    
    bl_label = "BlenRig Select fing_thumb_1_R"  
    bl_description = "fing_thumb_1_R"        
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}    
    
    def invoke(self, context, event):
        select_op(self, context, event, "fing_thumb_1_R")                              
        return {"FINISHED"}           
    
class Operator_Fing_Thumb_2_R(bpy.types.Operator):   
    bl_idname = "operator.fing_thumb_2_r"    
    bl_label = "BlenRig Select fing_thumb_2_R"  
    bl_description = "fing_thumb_2_R"        
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}       
    
    def invoke(self, context, event):
        select_op(self, context, event, "fing_thumb_2_R")                              
        return {"FINISHED"}        
    
class Operator_Fing_Thumb_3_R(bpy.types.Operator):   
    bl_idname = "operator.fing_thumb_3_r"    
    bl_label = "BlenRig Select fing_thumb_3_R"  
    bl_description = "fing_thumb_3_R"        
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}     
    
    def invoke(self, context, event):
        select_op(self, context, event, "fing_thumb_3_R")                              
        return {"FINISHED"}                   

class Operator_Fing_Lit_IK_R(bpy.types.Operator):    
    bl_idname = "operator.fing_lit_ik_r"     
    bl_label = "BlenRig Select fing_lit_ik_R"  
    bl_description = "fing_lit_ik_R"         
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}       
    
    def invoke(self, context, event):
        select_op(self, context, event, "fing_lit_ik_R")                              
        return {"FINISHED"}        
    
class Operator_Fing_Ring_IK_R(bpy.types.Operator):   
    bl_idname = "operator.fing_ring_ik_r"    
    bl_label = "BlenRig Select fing_ring_ik_R"  
    bl_description = "fing_ring_ik_R"        
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}  
    
    def invoke(self, context, event):
        select_op(self, context, event, "fing_ring_ik_R")                              
        return {"FINISHED"}                    

class Operator_Fing_Mid_IK_R(bpy.types.Operator):    
    bl_idname = "operator.fing_mid_ik_r"     
    bl_label = "BlenRig Select fing_mid_ik_R"  
    bl_description = "fing_mid_ik_R"         
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}     
    
    def invoke(self, context, event):
        select_op(self, context, event, "fing_mid_ik_R")                              
        return {"FINISHED"}          
    
class Operator_Fing_Ind_IK_R(bpy.types.Operator):    
    bl_idname = "operator.fing_ind_ik_r"     
    bl_label = "BlenRig Select fing_ind_ik_R"  
    bl_description = "fing_ind_ik_R"         
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'} 
 
    def invoke(self, context, event):
        select_op(self, context, event, "fing_ind_ik_R")                              
        return {"FINISHED"}           

class Operator_Fing_Thumb_IK_R(bpy.types.Operator):  
    bl_idname = "operator.fing_thumb_ik_r"   
    bl_label = "BlenRig Select fing_thumb_ik_R"  
    bl_description = "fing_thumb_ik_R"       
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}    
    
    def invoke(self, context, event):
        select_op(self, context, event, "fing_thumb_ik_R")                              
        return {"FINISHED"}           

class Operator_Hand_Close_R(bpy.types.Operator):  
    bl_idname = "operator.hand_close_r"   
    bl_label = "BlenRig Select hand_close_R"  
    bl_description = "hand_close_R"       
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}       
    
    def invoke(self, context, event):
        select_op(self, context, event, "hand_close_R")                              
        return {"FINISHED"}            

#HAND_L

class Operator_Hand_Roll_L(bpy.types.Operator):  
    bl_idname = "operator.hand_roll_l"   
    bl_label = "BlenRig Select hand_roll_L" 
    bl_description = "palm_bend_ik_ctrl_L / palm_bend_fk_ctrl_L"        
    bl_options = {'INTERNAL'}

    def invoke(self, context, event):
        armobj = bpy.context.active_object
        arm = bpy.context.active_object.data
        prop = int(bpy.context.active_object.pose.bones['properties_arm_L'].ik_arm_L)
        prop_hinge = int(bpy.context.active_object.pose.bones['properties_arm_L'].hinge_hand_L)    
        if ('palm_bend_ik_ctrl_L' and 'palm_bend_fk_ctrl_L' in armobj.pose.bones):
            #Target Bone            
            if prop == 1 or prop_hinge == 0:
                Bone = armobj.pose.bones["palm_bend_fk_ctrl_L"]
            else:
                Bone = armobj.pose.bones["palm_bend_ik_ctrl_L"]   
                       
            #Check if CTRL or SHIFT are pressed
            if event.ctrl == True or event.shift == True:
                #Get previously selected bones
                selected = [b.name for b in bpy.context.selected_pose_bones] 
                #Set target bone as active     
                for b in armobj.pose.bones:
                    b.bone.select = 0
                arm.bones.active = Bone.bone  
                #Reselect previously selected bones
                for b in armobj.pose.bones:
                    if (b.name in selected):
                        b.bone.select = 1             
            else:        
                for b in armobj.pose.bones:
                    b.bone.select = 0
                arm.bones.active = Bone.bone                                    
        return {"FINISHED"} 

class Operator_Hand_IK_Pivot_Point_L(bpy.types.Operator):    
    bl_idname = "operator.hand_ik_pivot_point_l"     
    bl_label = "BlenRig Select hand_ik_pivot_point_L"  
    bl_description = "hand_ik_pivot_point_L"         
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}     
    
    def invoke(self, context, event):
        select_op(self, context, event, "hand_ik_pivot_point_L")                              
        return {"FINISHED"}          
    
class Operator_Hand_IK_Ctrl_L(bpy.types.Operator):   
    bl_idname = "operator.hand_ik_ctrl_l"    
    bl_label = "BlenRig Select hand_ik_ctrl_L"  
    bl_description = "hand_ik_ctrl_L"        
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}     
    
    def invoke(self, context, event):
        select_op(self, context, event, "hand_ik_ctrl_L")                              
        return {"FINISHED"}          
    
class Operator_Hand_FK_L(bpy.types.Operator):    
    bl_idname = "operator.hand_fk_l"     
    bl_label = "BlenRig Select hand_fk_L"  
    bl_description = "hand_fk_L"         
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}    
    
    def invoke(self, context, event):
        select_op(self, context, event, "hand_fk_L")                              
        return {"FINISHED"}           

class Operator_Fing_Spread_L(bpy.types.Operator):    
    bl_idname = "operator.fing_spread_l"     
    bl_label = "BlenRig Select fing_spread_L"  
    bl_description = "fing_spread_L"         
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}       
    
    def invoke(self, context, event):
        select_op(self, context, event, "fing_spread_L")                              
        return {"FINISHED"}         
    
class Operator_Fing_Lit_Ctrl_L(bpy.types.Operator):  
    bl_idname = "operator.fing_lit_ctrl_l"   
    bl_label = "BlenRig Select fing_lit_ctrl_L"  
    bl_description = "fing_lit_ctrl_L"       
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}     
    
    def invoke(self, context, event):
        select_op(self, context, event, "fing_lit_ctrl_L")                              
        return {"FINISHED"}          
    
class Operator_Fing_Lit_2_L(bpy.types.Operator):     
    bl_idname = "operator.fing_lit_2_l"  
    bl_label = "BlenRig Select fing_lit_2_L"  
    bl_description = "fing_lit_2_L"      
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}     
    
    def invoke(self, context, event):
        select_op(self, context, event, "fing_lit_2_L")                              
        return {"FINISHED"}          

class Operator_Fing_Lit_3_L(bpy.types.Operator):     
    bl_idname = "operator.fing_lit_3_l"  
    bl_label = "BlenRig Select fing_lit_3_L"  
    bl_description = "fing_lit_3_L"      
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}     
    
    def invoke(self, context, event):
        select_op(self, context, event, "fing_lit_3_L")                              
        return {"FINISHED"}                  

class Operator_Fing_Lit_4_L(bpy.types.Operator):     
    bl_idname = "operator.fing_lit_4_l"  
    bl_label = "BlenRig Select fing_lit_4_L"  
    bl_description = "fing_lit_4_L"      
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}   
    
    def invoke(self, context, event):
        select_op(self, context, event, "fing_lit_4_L")                              
        return {"FINISHED"}            

class Operator_Fing_Ring_Ctrl_L(bpy.types.Operator):     
    bl_idname = "operator.fing_ring_ctrl_l"  
    bl_label = "BlenRig Select fing_ring_ctrl_L"  
    bl_description = "fing_ring_ctrl_L"      
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}   
    
    def invoke(self, context, event):
        select_op(self, context, event, "fing_ring_ctrl_L")                              
        return {"FINISHED"}            
    
class Operator_Fing_Ring_2_L(bpy.types.Operator):    
    bl_idname = "operator.fing_ring_2_l"     
    bl_label = "BlenRig Select fing_ring_2_L"  
    bl_description = "fing_ring_2_L"         
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}       
    
    def invoke(self, context, event):
        select_op(self, context, event, "fing_ring_2_L")                              
        return {"FINISHED"}        
    
class Operator_Fing_Ring_3_L(bpy.types.Operator):    
    bl_idname = "operator.fing_ring_3_l"     
    bl_label = "BlenRig Select fing_ring_3_L"  
    bl_description = "fing_ring_3_L"         
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}    
    
    def invoke(self, context, event):
        select_op(self, context, event, "fing_ring_3_L")                              
        return {"FINISHED"}                     

class Operator_Fing_Ring_4_L(bpy.types.Operator):    
    bl_idname = "operator.fing_ring_4_l"     
    bl_label = "BlenRig Select fing_ring_4_L"  
    bl_description = "fing_ring_4_L"         
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}   
    
    def invoke(self, context, event):
        select_op(self, context, event, "fing_ring_4_L")                              
        return {"FINISHED"}            

class Operator_Fing_Mid_Ctrl_L(bpy.types.Operator):  
    bl_idname = "operator.fing_mid_ctrl_l"   
    bl_label = "BlenRig Select fing_mid_ctrl_L"  
    bl_description = "fing_mid_ctrl_L"       
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}   
    
    def invoke(self, context, event):
        select_op(self, context, event, "fing_mid_ctrl_L")                              
        return {"FINISHED"}            
    
class Operator_Fing_Mid_2_L(bpy.types.Operator):     
    bl_idname = "operator.fing_mid_2_l"  
    bl_label = "BlenRig Select fing_mid_2_L"  
    bl_description = "fing_mid_2_L"      
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}       
    
    def invoke(self, context, event):
        select_op(self, context, event, "fing_mid_2_L")                              
        return {"FINISHED"}        
    
class Operator_Fing_Mid_3_L(bpy.types.Operator):     
    bl_idname = "operator.fing_mid_3_l"  
    bl_label = "BlenRig Select fing_mid_3_L"  
    bl_description = "fing_mid_3_L"      
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}      
    
    def invoke(self, context, event):
        select_op(self, context, event, "fing_mid_3_L")                              
        return {"FINISHED"}             

class Operator_Fing_Mid_4_L(bpy.types.Operator):     
    bl_idname = "operator.fing_mid_4_l"  
    bl_label = "BlenRig Select fing_mid_4_L"  
    bl_description = "fing_mid_4_L"      
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'} 
    
    def invoke(self, context, event):
        select_op(self, context, event, "fing_mid_4_L")                              
        return {"FINISHED"}              

class Operator_Fing_Ind_Ctrl_L(bpy.types.Operator):  
    bl_idname = "operator.fing_ind_ctrl_l"   
    bl_label = "BlenRig Select fing_ind_ctrl_L"  
    bl_description = "fing_ind_ctrl_L"       
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}    
    
    def invoke(self, context, event):
        select_op(self, context, event, "fing_ind_ctrl_L")                              
        return {"FINISHED"}           
    
class Operator_Fing_Ind_2_L(bpy.types.Operator):     
    bl_idname = "operator.fing_ind_2_l"  
    bl_label = "BlenRig Select fing_ind_2_L"  
    bl_description = "fing_ind_2_L"      
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}   
    
    def invoke(self, context, event):
        select_op(self, context, event, "fing_ind_2_L")                              
        return {"FINISHED"}            
    
class Operator_Fing_Ind_3_L(bpy.types.Operator):     
    bl_idname = "operator.fing_ind_3_l"  
    bl_label = "BlenRig Select fing_ind_3_L"  
    bl_description = "fing_ind_3_L"      
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}     
    
    def invoke(self, context, event):
        select_op(self, context, event, "fing_ind_3_L")                              
        return {"FINISHED"}                    

class Operator_Fing_Ind_4_L(bpy.types.Operator):     
    bl_idname = "operator.fing_ind_4_l"  
    bl_label = "BlenRig Select fing_ind_4_L"  
    bl_description = "fing_ind_4_L"      
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}      
    
    def invoke(self, context, event):
        select_op(self, context, event, "fing_ind_4_L")                              
        return {"FINISHED"}         

class Operator_Fing_Thumb_Ctrl_L(bpy.types.Operator):    
    bl_idname = "operator.fing_thumb_ctrl_l"     
    bl_label = "BlenRig Select fing_thumb_ctrl_L"  
    bl_description = "fing_thumb_ctrl_L"         
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}  
    
    def invoke(self, context, event):
        select_op(self, context, event, "fing_thumb_ctrl_L")                              
        return {"FINISHED"}             

class Operator_Fing_Thumb_1_L(bpy.types.Operator):   
    bl_idname = "operator.fing_thumb_1_l"    
    bl_label = "BlenRig Select fing_thumb_1_L"  
    bl_description = "fing_thumb_1_L"        
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'} 
    
    def invoke(self, context, event):
        select_op(self, context, event, "fing_thumb_1_L")                              
        return {"FINISHED"}              
    
class Operator_Fing_Thumb_2_L(bpy.types.Operator):   
    bl_idname = "operator.fing_thumb_2_l"    
    bl_label = "BlenRig Select fing_thumb_2_L"  
    bl_description = "fing_thumb_2_L"        
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}   
    
    def invoke(self, context, event):
        select_op(self, context, event, "fing_thumb_2_L")                              
        return {"FINISHED"}            
    
class Operator_Fing_Thumb_3_L(bpy.types.Operator):   
    bl_idname = "operator.fing_thumb_3_l"    
    bl_label = "BlenRig Select fing_thumb_3_L"  
    bl_description = "fing_thumb_3_L"        
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'} 
    
    def invoke(self, context, event):
        select_op(self, context, event, "fing_thumb_3_L")                              
        return {"FINISHED"}                      

class Operator_Fing_Lit_IK_L(bpy.types.Operator):    
    bl_idname = "operator.fing_lit_ik_l"     
    bl_label = "BlenRig Select fing_lit_ik_L"  
    bl_description = "fing_lit_ik_L"         
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}       
    
    def invoke(self, context, event):
        select_op(self, context, event, "fing_lit_ik_L")                              
        return {"FINISHED"}        
    
class Operator_Fing_Ring_IK_L(bpy.types.Operator):   
    bl_idname = "operator.fing_ring_ik_l"    
    bl_label = "BlenRig Select fing_ring_ik_L"  
    bl_description = "fing_ring_ik_L"        
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}      
    
    def invoke(self, context, event):
        select_op(self, context, event, "fing_ring_ik_L")                              
        return {"FINISHED"}                    

class Operator_Fing_Mid_IK_L(bpy.types.Operator):    
    bl_idname = "operator.fing_mid_ik_l"     
    bl_label = "BlenRig Select fing_mid_ik_L"  
    bl_description = "fing_mid_ik_L"         
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}    
    
    def invoke(self, context, event):
        select_op(self, context, event, "fing_mid_ik_L")                              
        return {"FINISHED"}           
    
class Operator_Fing_Ind_IK_L(bpy.types.Operator):    
    bl_idname = "operator.fing_ind_ik_l"     
    bl_label = "BlenRig Select fing_ind_ik_L"  
    bl_description = "fing_ind_ik_L"         
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}       
    
    def invoke(self, context, event):
        select_op(self, context, event, "fing_ind_ik_L")                              
        return {"FINISHED"}        
    
class Operator_Fing_Thumb_IK_L(bpy.types.Operator):  
    bl_idname = "operator.fing_thumb_ik_l"   
    bl_label = "BlenRig Select fing_thumb_ik_L"  
    bl_description = "fing_thumb_ik_L"       
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}   
    
    def invoke(self, context, event):
        select_op(self, context, event, "fing_thumb_ik_L")                              
        return {"FINISHED"}            

class Operator_Hand_Close_L(bpy.types.Operator):  
    bl_idname = "operator.hand_close_l"   
    bl_label = "BlenRig Select hand_close_L"  
    bl_description = "hand_close_L"       
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}       
    
    def invoke(self, context, event):
        select_op(self, context, event, "hand_close_L")                              
        return {"FINISHED"}           
    
#LEG_R  

class Operator_Thigh_Toon_R(bpy.types.Operator):     
    bl_idname = "operator.thigh_toon_r"  
    bl_label = "BlenRig Select thigh_toon_R"  
    bl_description = "thigh_toon_R"      
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}    
    
    def invoke(self, context, event):
        select_op(self, context, event, "thigh_toon_R")                              
        return {"FINISHED"}                

class Operator_Knee_Pole_R(bpy.types.Operator):  
    bl_idname = "operator.knee_pole_r"   
    bl_label = "BlenRig Select knee_pole_R"  
    bl_description = "knee_pole_R"       
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}  
    
    def invoke(self, context, event):
        select_op(self, context, event, "knee_pole_R")                              
        return {"FINISHED"}           

class Operator_Shin_Toon_R(bpy.types.Operator):  
    bl_idname = "operator.shin_toon_r"   
    bl_label = "BlenRig Select shin_toon_R"  
    bl_description = "shin_toon_R"       
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}       
    
    def invoke(self, context, event):
        select_op(self, context, event, "shin_toon_R")                              
        return {"FINISHED"}         

class Operator_Pelvis_Toon_R(bpy.types.Operator):    
    bl_idname = "operator.pelvis_toon_r"     
    bl_label = "BlenRig Select pelvis_toon_R"  
    bl_description = "pelvis_toon_R"         
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}     
    
    def invoke(self, context, event):
        select_op(self, context, event, "pelvis_toon_R")                              
        return {"FINISHED"}          

class Operator_Leg_Scale_R(bpy.types.Operator):  
    bl_idname = "operator.leg_scale_r"   
    bl_label = "BlenRig Select leg_scale_R"  
    bl_description = "leg_scale_R"       
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}   
    
    def invoke(self, context, event):
        select_op(self, context, event, "leg_scale_R")                              
        return {"FINISHED"}            

class Operator_Thigh_FK_R(bpy.types.Operator):   
    bl_idname = "operator.thigh_fk_r"    
    bl_label = "BlenRig Select thigh_fk_R"  
    bl_description = "thigh_fk_R"        
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}   
    
    def invoke(self, context, event):
        select_op(self, context, event, "thigh_fk_R")                              
        return {"FINISHED"}            

class Operator_Thigh_IK_R(bpy.types.Operator):   
    bl_idname = "operator.thigh_ik_r"    
    bl_label = "BlenRig Select thigh_ik_R"  
    bl_description = "thigh_ik_R"        
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}      
    
    def invoke(self, context, event):
        select_op(self, context, event, "thigh_ik_R")                              
        return {"FINISHED"}          
    
class Operator_Knee_Toon_R(bpy.types.Operator):  
    bl_idname = "operator.knee_toon_r"   
    bl_label = "BlenRig Select knee_toon_R"  
    bl_description = "knee_toon_R"       
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}      
    
    def invoke(self, context, event):
        select_op(self, context, event, "knee_toon_R")                              
        return {"FINISHED"}          
    
class Operator_Shin_FK_R(bpy.types.Operator):    
    bl_idname = "operator.shin_fk_r"     
    bl_label = "BlenRig Select shin_fk_R"  
    bl_description = "shin_fk_R"         
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}       
    
    def invoke(self, context, event):
        select_op(self, context, event, "shin_fk_R")                              
        return {"FINISHED"}        
    
class Operator_Shin_IK_R(bpy.types.Operator):    
    bl_idname = "operator.shin_ik_r"     
    bl_label = "BlenRig Select shin_ik_R"  
    bl_description = "shin_ik_R"         
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}     
    
    def invoke(self, context, event):
        select_op(self, context, event, "shin_ik_R")                              
        return {"FINISHED"}           
    
class Operator_Foot_Toon_R(bpy.types.Operator):  
    bl_idname = "operator.foot_toon_r"   
    bl_label = "BlenRig Select foot_toon_R"  
    bl_description = "foot_toon_R"       
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}      
    
    def invoke(self, context, event):
        select_op(self, context, event, "foot_toon_R")                              
        return {"FINISHED"}             

#LEG_L  

class Operator_Thigh_Toon_L(bpy.types.Operator):     
    bl_idname = "operator.thigh_toon_l"  
    bl_label = "BlenRig Select thigh_toon_L"  
    bl_description = "thigh_toon_L"      
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}   
    
    def invoke(self, context, event):
        select_op(self, context, event, "thigh_toon_L")                              
        return {"FINISHED"}               

class Operator_Knee_Pole_L(bpy.types.Operator):  
    bl_idname = "operator.knee_pole_l"   
    bl_label = "BlenRig Select knee_pole_L"  
    bl_description = "knee_pole_L"       
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}   
    
    def invoke(self, context, event):
        select_op(self, context, event, "knee_pole_L")                              
        return {"FINISHED"}            

class Operator_Shin_Toon_L(bpy.types.Operator):  
    bl_idname = "operator.shin_toon_l"   
    bl_label = "BlenRig Select shin_toon_L"  
    bl_description = "shin_toon_L"       
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}  
    
    def invoke(self, context, event):
        select_op(self, context, event, "shin_toon_L")                              
        return {"FINISHED"}             

class Operator_Pelvis_Toon_L(bpy.types.Operator):    
    bl_idname = "operator.pelvis_toon_l"     
    bl_label = "BlenRig Select pelvis_toon_L"  
    bl_description = "pelvis_toon_L"         
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}      
    
    def invoke(self, context, event):
        select_op(self, context, event, "pelvis_toon_L")                              
        return {"FINISHED"}         

class Operator_Leg_Scale_L(bpy.types.Operator):  
    bl_idname = "operator.leg_scale_l"   
    bl_label = "BlenRig Select leg_scale_L"  
    bl_description = "leg_scale_L"       
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}       
    
    def invoke(self, context, event):
        select_op(self, context, event, "leg_scale_L")                              
        return {"FINISHED"}        

class Operator_Thigh_FK_L(bpy.types.Operator):   
    bl_idname = "operator.thigh_fk_l"    
    bl_label = "BlenRig Select thigh_fk_L"  
    bl_description = "thigh_fk_L"        
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}     
    
    def invoke(self, context, event):
        select_op(self, context, event, "thigh_fk_L")                              
        return {"FINISHED"}          

class Operator_Thigh_IK_L(bpy.types.Operator):   
    bl_idname = "operator.thigh_ik_l"    
    bl_label = "BlenRig Select thigh_ik_L"  
    bl_description = "thigh_ik_L"        
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}       
    
    def invoke(self, context, event):
        select_op(self, context, event, "thigh_ik_L")                              
        return {"FINISHED"}        
    
class Operator_Knee_Toon_L(bpy.types.Operator):  
    bl_idname = "operator.knee_toon_l"   
    bl_label = "BlenRig Select knee_toon_L"  
    bl_description = "knee_toon_L"       
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}   
    
    def invoke(self, context, event):
        select_op(self, context, event, "knee_toon_L")                              
        return {"FINISHED"}            
    
class Operator_Shin_FK_L(bpy.types.Operator):    
    bl_idname = "operator.shin_fk_l"     
    bl_label = "BlenRig Select shin_fk_L"  
    bl_description = "shin_fk_L"         
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}   
    
    def invoke(self, context, event):
        select_op(self, context, event, "shin_fk_L")                              
        return {"FINISHED"}            
    
class Operator_Shin_IK_L(bpy.types.Operator):    
    bl_idname = "operator.shin_ik_l"     
    bl_label = "BlenRig Select shin_ik_L"  
    bl_description = "shin_ik_L"         
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}       
    
    def invoke(self, context, event):
        select_op(self, context, event, "shin_ik_L")                              
        return {"FINISHED"}        
    
class Operator_Foot_Toon_L(bpy.types.Operator):  
    bl_idname = "operator.foot_toon_l"   
    bl_label = "BlenRig Select foot_toon_L"  
    bl_description = "foot_toon_L"       
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}    
    
    def invoke(self, context, event):
        select_op(self, context, event, "foot_toon_L")                              
        return {"FINISHED"}             

#FOOT_R

class Operator_Toe_2_FK_R(bpy.types.Operator):   
    bl_idname = "operator.toe_2_fk_r"    
    bl_label = "BlenRig Select toe_2_fk_R"  
    bl_description = "toe_2_fk_R"        
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}     
    
    def invoke(self, context, event):
        select_op(self, context, event, "toe_2_fk_R")                              
        return {"FINISHED"}          

class Operator_Toe_Roll_2_R(bpy.types.Operator):     
    bl_idname = "operator.toe_roll_2_r"  
    bl_label = "BlenRig Select toe_roll_2_R"  
    bl_description = "toe_roll_2_R"      
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}     
    
    def invoke(self, context, event):
        select_op(self, context, event, "toe_roll_2_R")                              
        return {"FINISHED"}          

class Operator_Toe_1_FK_R(bpy.types.Operator):   
    bl_idname = "operator.toe_1_fk_r"    
    bl_label = "BlenRig Select toe_1_fk_R"  
    bl_description = "toe_1_fk_R"        
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}     
    
    def invoke(self, context, event):
        select_op(self, context, event, "toe_1_fk_R")                              
        return {"FINISHED"}          

class Operator_Toe_Roll_1_R(bpy.types.Operator):     
    bl_idname = "operator.toe_roll_1_r"  
    bl_label = "BlenRig Select toe_roll_1_R"  
    bl_description = "toe_roll_1_R"      
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}     
    
    def invoke(self, context, event):
        select_op(self, context, event, "toe_roll_1_R")                              
        return {"FINISHED"}          

class Operator_Foot_R(bpy.types.Operator):   
    bl_idname = "operator.foot_r"    
    bl_label = "BlenRig Select foot_R"  
    bl_description = "foot_ik_ctrl_R / foot_fk_R"         
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}       

    def invoke(self, context, event):
        armobj = bpy.context.active_object
        arm = bpy.context.active_object.data
        prop = int(bpy.context.active_object.pose.bones['properties_leg_R'].ik_leg_R)       
        if ('foot_ik_ctrl_R' and 'foot_fk_R' in armobj.pose.bones):
            #Target Bone            
            if prop == 0:
                Bone = armobj.pose.bones["foot_ik_ctrl_R"]
            else:
                Bone = armobj.pose.bones["foot_fk_R"]            
            #Check if CTRL or SHIFT are pressed
            if event.ctrl == True or event.shift == True:
                #Get previously selected bones
                selected = [b.name for b in bpy.context.selected_pose_bones] 
                #Set target bone as active     
                for b in armobj.pose.bones:
                    b.bone.select = 0
                arm.bones.active = Bone.bone  
                #Reselect previously selected bones
                for b in armobj.pose.bones:
                    if (b.name in selected):
                        b.bone.select = 1             
            else:        
                for b in armobj.pose.bones:
                    b.bone.select = 0
                arm.bones.active = Bone.bone                                    
        return {"FINISHED"} 

class Operator_Foot_Roll_Ctrl_R(bpy.types.Operator):     
    bl_idname = "operator.foot_roll_ctrl_r"  
    bl_label = "BlenRig Select foot_roll_ctrl_R"  
    bl_description = "foot_roll_ctrl_R"      
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}       
    
    def invoke(self, context, event):
        select_op(self, context, event, "foot_roll_ctrl_R")                              
        return {"FINISHED"}        

class Operator_Sole_Ctrl_R(bpy.types.Operator):  
    bl_idname = "operator.sole_ctrl_r"   
    bl_label = "BlenRig Select sole_ctrl_R"  
    bl_description = "sole_ctrl_R"       
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}      
    
    def invoke(self, context, event):
        select_op(self, context, event, "sole_ctrl_R")                              
        return {"FINISHED"}         

class Operator_Sole_Pivot_Point_R(bpy.types.Operator):   
    bl_idname = "operator.sole_pivot_point_r"    
    bl_label = "BlenRig Select sole_pivot_point_R"  
    bl_description = "sole_pivot_point_R"        
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}    
    
    def invoke(self, context, event):
        select_op(self, context, event, "sole_pivot_point_R")                              
        return {"FINISHED"}           
      
#FOOT_L

class Operator_Toe_2_FK_L(bpy.types.Operator):   
    bl_idname = "operator.toe_2_fk_l"    
    bl_label = "BlenRig Select toe_2_fk_L"  
    bl_description = "toe_2_fk_L"        
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}   
    
    def invoke(self, context, event):
        select_op(self, context, event, "toe_2_fk_L")                              
        return {"FINISHED"}            

class Operator_Toe_Roll_2_L(bpy.types.Operator):     
    bl_idname = "operator.toe_roll_2_l"  
    bl_label = "BlenRig Select toe_roll_2_L"  
    bl_description = "toe_roll_2_L"      
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}      
    
    def invoke(self, context, event):
        select_op(self, context, event, "toe_roll_2_L")                              
        return {"FINISHED"}         

class Operator_Toe_1_FK_L(bpy.types.Operator):   
    bl_idname = "operator.toe_1_fk_l"    
    bl_label = "BlenRig Select toe_1_fk_L"  
    bl_description = "toe_1_fk_L"        
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}    
    
    def invoke(self, context, event):
        select_op(self, context, event, "toe_1_fk_L")                              
        return {"FINISHED"}           

class Operator_Toe_Roll_1_L(bpy.types.Operator):     
    bl_idname = "operator.toe_roll_1_l"  
    bl_label = "BlenRig Select toe_roll_1_L"  
    bl_description = "toe_roll_1_L"      
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}       

    def invoke(self, context, event):
        select_op(self, context, event, "toe_roll_1_L")                              
        return {"FINISHED"}    

class Operator_Foot_L(bpy.types.Operator):   
    bl_idname = "operator.foot_l"    
    bl_label = "BlenRig Select foot_L"  
    bl_description = "foot_ik_ctrl_L / foot_fk_L"         
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}       

    def invoke(self, context, event):
        armobj = bpy.context.active_object
        arm = bpy.context.active_object.data
        prop = int(bpy.context.active_object.pose.bones['properties_leg_L'].ik_leg_L)       
        if ('foot_ik_ctrl_L' and 'foot_fk_L' in armobj.pose.bones):
            #Target Bone            
            if prop == 0:
                Bone = armobj.pose.bones["foot_ik_ctrl_L"]
            else:
                Bone = armobj.pose.bones["foot_fk_L"]            
            #Check if CTRL or SHIFT are pressed
            if event.ctrl == True or event.shift == True:
                #Get previously selected bones
                selected = [b.name for b in bpy.context.selected_pose_bones] 
                #Set target bone as active     
                for b in armobj.pose.bones:
                    b.bone.select = 0
                arm.bones.active = Bone.bone  
                #Reselect previously selected bones
                for b in armobj.pose.bones:
                    if (b.name in selected):
                        b.bone.select = 1             
            else:        
                for b in armobj.pose.bones:
                    b.bone.select = 0
                arm.bones.active = Bone.bone                                    
        return {"FINISHED"} 

class Operator_Foot_Roll_Ctrl_L(bpy.types.Operator):     
    bl_idname = "operator.foot_roll_ctrl_l"  
    bl_label = "BlenRig Select foot_roll_ctrl_L"  
    bl_description = "foot_roll_ctrl_L"      
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}   
    
    def invoke(self, context, event):
        select_op(self, context, event, "foot_roll_ctrl_L")                              
        return {"FINISHED"}            

class Operator_Sole_Ctrl_L(bpy.types.Operator):  
    bl_idname = "operator.sole_ctrl_l"   
    bl_label = "BlenRig Select sole_ctrl_L"  
    bl_description = "sole_ctrl_L"       
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}    
    
    def invoke(self, context, event):
        select_op(self, context, event, "sole_ctrl_L")                              
        return {"FINISHED"}               

class Operator_Sole_Pivot_Point_L(bpy.types.Operator):   
    bl_idname = "operator.sole_pivot_point_l"    
    bl_label = "BlenRig Select sole_pivot_point_L"  
    bl_description = "sole_pivot_point_L"        
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}       
    
    def invoke(self, context, event):
        select_op(self, context, event, "sole_pivot_point_L")                              
        return {"FINISHED"}        

#MASTER

class Operator_Master(bpy.types.Operator):   
    bl_idname = "operator.master"    
    bl_label = "BlenRig Select master"  
    bl_description = "master"        
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}    
    
    def invoke(self, context, event):
        select_op(self, context, event, "master")                              
        return {"FINISHED"}           

######### QUADRUPED #######################################

#ARM_L

class Operator_Ankle_Toon_L(bpy.types.Operator):     
    bl_idname = "operator.ankle_toon_l"  
    bl_label = "BlenRig Select ankle_toon_L"  
    bl_description = "ankle_toon_L"      
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}       
    
    def invoke(self, context, event):
        select_op(self, context, event, "ankle_toon_L")                              
        return {"FINISHED"}           
    
class Operator_Carpal_FK_L(bpy.types.Operator):     
    bl_idname = "operator.carpal_fk_l"  
    bl_label = "BlenRig Select carpal_fk_L"  
    bl_description = "carpal_fk_L"      
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}   
    
    def invoke(self, context, event):
        select_op(self, context, event, "carpal_fk_L")                              
        return {"FINISHED"}            

class Operator_Carpal_IK_L(bpy.types.Operator):     
    bl_idname = "operator.carpal_ik_l"  
    bl_label = "BlenRig Select carpal_ik_L"  
    bl_description = "carpal_ik_L"      
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}   
    
    def invoke(self, context, event):
        select_op(self, context, event, "carpal_ik_L")                              
        return {"FINISHED"}            

class Operator_Carpal_Toon_L(bpy.types.Operator):     
    bl_idname = "operator.carpal_toon_l"  
    bl_label = "BlenRig Select carpal_toon_L"  
    bl_description = "carpal_toon_L"      
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}  
    
    def invoke(self, context, event):
        select_op(self, context, event, "carpal_toon_L")                              
        return {"FINISHED"}              

#ARM_R

class Operator_Ankle_Toon_R(bpy.types.Operator):     
    bl_idname = "operator.ankle_toon_r"  
    bl_label = "BlenRig Select ankle_toon_R"  
    bl_description = "ankle_toon_R"      
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}      
    
    def invoke(self, context, event):
        select_op(self, context, event, "ankle_toon_R")                              
        return {"FINISHED"}         
    
class Operator_Carpal_FK_R(bpy.types.Operator):     
    bl_idname = "operator.carpal_fk_r"  
    bl_label = "BlenRig Select carpal_fk_R"  
    bl_description = "carpal_fk_R"      
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}      
    
    def invoke(self, context, event):
        select_op(self, context, event, "carpal_fk_R")                              
        return {"FINISHED"}         

class Operator_Carpal_IK_R(bpy.types.Operator):     
    bl_idname = "operator.carpal_ik_r"  
    bl_label = "BlenRig Select carpal_ik_R"  
    bl_description = "carpal_ik_R"      
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}   
    
    def invoke(self, context, event):
        select_op(self, context, event, "carpal_ik_R")                              
        return {"FINISHED"}            

class Operator_Carpal_Toon_R(bpy.types.Operator):     
    bl_idname = "operator.carpal_toon_r"  
    bl_label = "BlenRig Select carpal_toon_R"  
    bl_description = "carpal_toon_R"      
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}   
    
    def invoke(self, context, event):
        select_op(self, context, event, "carpal_toon_R")                              
        return {"FINISHED"}            

#LEG_L

class Operator_Hock_Toon_L(bpy.types.Operator):     
    bl_idname = "operator.hock_toon_l"  
    bl_label = "BlenRig Select hock_toon_L"  
    bl_description = "hock_toon_L"      
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}     
    
    def invoke(self, context, event):
        select_op(self, context, event, "hock_toon_L")                              
        return {"FINISHED"}          
    
class Operator_Tarsal_FK_L(bpy.types.Operator):     
    bl_idname = "operator.tarsal_fk_l"  
    bl_label = "BlenRig Select tarsal_fk_L"  
    bl_description = "tarsal_fk_L"      
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}     
    
    def invoke(self, context, event):
        select_op(self, context, event, "tarsal_fk_L")                              
        return {"FINISHED"}           

class Operator_Tarsal_IK_L(bpy.types.Operator):     
    bl_idname = "operator.tarsal_ik_l"  
    bl_label = "BlenRig Select tarsal_ik_L"  
    bl_description = "tarsal_ik_L"      
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}     
    
    def invoke(self, context, event):
        select_op(self, context, event, "tarsal_ik_L")                              
        return {"FINISHED"}          

class Operator_Tarsal_Toon_L(bpy.types.Operator):     
    bl_idname = "operator.tarsal_toon_l"  
    bl_label = "BlenRig Select tarsal_toon_L"  
    bl_description = "tarsal_toon_L"      
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}  
    
    def invoke(self, context, event):
        select_op(self, context, event, "tarsal_toon_L")                              
        return {"FINISHED"}              

#LEG_R

class Operator_Hock_Toon_R(bpy.types.Operator):     
    bl_idname = "operator.hock_toon_r"  
    bl_label = "BlenRig Select hock_toon_R"  
    bl_description = "hock_toon_R"      
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}  
    
    def invoke(self, context, event):
        select_op(self, context, event, "hock_toon_R")                              
        return {"FINISHED"}             
    
class Operator_Tarsal_FK_R(bpy.types.Operator):     
    bl_idname = "operator.tarsal_fk_r"  
    bl_label = "BlenRig Select tarsal_fk_R"  
    bl_description = "tarsal_fk_R"      
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}   
    
    def invoke(self, context, event):
        select_op(self, context, event, "tarsal_fk_R")                              
        return {"FINISHED"}            

class Operator_Tarsal_IK_R(bpy.types.Operator):     
    bl_idname = "operator.tarsal_ik_r"  
    bl_label = "BlenRig Select tarsal_ik_R"  
    bl_description = "tarsal_ik_R"      
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}      
    
    def invoke(self, context, event):
        select_op(self, context, event, "tarsal_ik_R")                              
        return {"FINISHED"}         
    
class Operator_Tarsal_Toon_R(bpy.types.Operator):     
    bl_idname = "operator.tarsal_toon_r"  
    bl_label = "BlenRig Select tarsal_toon_R"  
    bl_description = "tarsal_toon_R"      
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}     
    
    def invoke(self, context, event):
        select_op(self, context, event, "tarsal_toon_R")                              
        return {"FINISHED"}          

#HAND_L

class Operator_Fing_2_FK_L(bpy.types.Operator):     
    bl_idname = "operator.fing_2_fk_l"  
    bl_label = "BlenRig Select fing_2_fk_L"  
    bl_description = "fing_2_fk_L"      
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}     
    
    def invoke(self, context, event):
        select_op(self, context, event, "fing_2_fk_L")                              
        return {"FINISHED"}          

class Operator_Fing_Roll_2_L(bpy.types.Operator):     
    bl_idname = "operator.fing_roll_2_l"  
    bl_label = "BlenRig Select fing_roll_2_L"  
    bl_description = "fing_roll_2_L"      
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'} 
    
    def invoke(self, context, event):
        select_op(self, context, event, "fing_roll_2_L")                              
        return {"FINISHED"}              

class Operator_Fing_1_FK_L(bpy.types.Operator):   
    bl_idname = "operator.fing_1_fk_l"    
    bl_label = "BlenRig Select fing_1_fk_L"  
    bl_description = "fing_1_fk_L"        
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'} 
    
    def invoke(self, context, event):
        select_op(self, context, event, "fing_1_fk_L")                              
        return {"FINISHED"}              

class Operator_Fing_Roll_1_L(bpy.types.Operator):     
    bl_idname = "operator.fing_roll_1_l"  
    bl_label = "BlenRig Select fing_roll_1_L"  
    bl_description = "fing_roll_1_L"      
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}  
    
    def invoke(self, context, event):
        select_op(self, context, event, "fing_roll_1_L")                              
        return {"FINISHED"}             

class Operator_Hand_L(bpy.types.Operator):   
    bl_idname = "operator.hand_l"    
    bl_label = "BlenRig Select hand_L"  
    bl_description = "hand_ik_ctrl_L / hand_fk_L"         
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}       

    def invoke(self, context, event):
        armobj = bpy.context.active_object
        arm = bpy.context.active_object.data
        prop = int(bpy.context.active_object.pose.bones['properties_arm_L'].ik_arm_L)       
        if ('hand_ik_ctrl_L' and 'hand_fk_L' in armobj.pose.bones):
            #Target Bone            
            if prop == 0:
                Bone = armobj.pose.bones["hand_ik_ctrl_L"]
            else:
                Bone = armobj.pose.bones["hand_fk_L"]            
            #Check if CTRL or SHIFT are pressed
            if event.ctrl == True or event.shift == True:
                #Get previously selected bones
                selected = [b.name for b in bpy.context.selected_pose_bones] 
                #Set target bone as active     
                for b in armobj.pose.bones:
                    b.bone.select = 0
                arm.bones.active = Bone.bone  
                #Reselect previously selected bones
                for b in armobj.pose.bones:
                    if (b.name in selected):
                        b.bone.select = 1             
            else:        
                for b in armobj.pose.bones:
                    b.bone.select = 0
                arm.bones.active = Bone.bone                                    
        return {"FINISHED"} 

class Operator_Hand_Roll_Ctrl_L(bpy.types.Operator):     
    bl_idname = "operator.hand_roll_ctrl_l"  
    bl_label = "BlenRig Select hand_roll_ctrl_L"  
    bl_description = "hand_roll_ctrl_L"      
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}  
    
    def invoke(self, context, event):
        select_op(self, context, event, "hand_roll_ctrl_L")                              
        return {"FINISHED"}             

class Operator_Hand_Sole_Ctrl_L(bpy.types.Operator):  
    bl_idname = "operator.hand_sole_ctrl_l"   
    bl_label = "BlenRig Select hand_sole_ctrl_L"  
    bl_description = "hand_sole_ctrl_L"       
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}     
    
    def invoke(self, context, event):
        select_op(self, context, event, "hand_sole_ctrl_L")                              
        return {"FINISHED"}          

class Operator_Hand_Sole_Pivot_Point_L(bpy.types.Operator):   
    bl_idname = "operator.hand_sole_pivot_point_l"    
    bl_label = "BlenRig Select hand_sole_pivot_point_L"  
    bl_description = "hand_sole_pivot_point_L"        
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}    
    
    def invoke(self, context, event):
        select_op(self, context, event, "hand_sole_pivot_point_L")                              
        return {"FINISHED"}           

#HAND_R

class Operator_Fing_2_FK_R(bpy.types.Operator):     
    bl_idname = "operator.fing_2_fk_r"  
    bl_label = "BlenRig Select fing_2_fk_R"  
    bl_description = "fing_2_fk_R"      
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}      
    
    def invoke(self, context, event):
        select_op(self, context, event, "fing_2_fk_R")                              
        return {"FINISHED"}            

class Operator_Fing_Roll_2_R(bpy.types.Operator):     
    bl_idname = "operator.fing_roll_2_r"  
    bl_label = "BlenRig Select fing_roll_2_R"  
    bl_description = "fing_roll_2_R"      
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}   
    
    def invoke(self, context, event):
        select_op(self, context, event, "fing_roll_2_R")                              
        return {"FINISHED"}            

class Operator_Fing_1_FK_R(bpy.types.Operator):   
    bl_idname = "operator.fing_1_fk_r"    
    bl_label = "BlenRig Select fing_1_fk_R"  
    bl_description = "fing_1_fk_R"        
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}      
    
    def invoke(self, context, event):
        select_op(self, context, event, "fing_1_fk_R")                              
        return {"FINISHED"}         

class Operator_Fing_Roll_1_R(bpy.types.Operator):     
    bl_idname = "operator.fing_roll_1_r"  
    bl_label = "BlenRig Select fing_roll_1_R"  
    bl_description = "fing_roll_1_R"      
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}    
    
    def invoke(self, context, event):
        select_op(self, context, event, "fing_roll_1_R")                              
        return {"FINISHED"}       

class Operator_Hand_R(bpy.types.Operator):   
    bl_idname = "operator.hand_r"    
    bl_label = "BlenRig Select hand_R"  
    bl_description = "hand_ik_ctrl_R / hand_fk_R"         
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}      
    
    def invoke(self, context, event):
        select_op(self, context, event, "ankle_toon_L")                              
        return {"FINISHED"}         

    def invoke(self, context, event):
        armobj = bpy.context.active_object
        arm = bpy.context.active_object.data
        prop = int(bpy.context.active_object.pose.bones['properties_arm_R'].ik_arm_R)       
        if ('hand_ik_ctrl_R' and 'hand_fk_R' in armobj.pose.bones):
            #Target Bone            
            if prop == 0:
                Bone = armobj.pose.bones["hand_ik_ctrl_R"]
            else:
                Bone = armobj.pose.bones["hand_fk_R"]            
            #Check if CTRL or SHIFT are pressed
            if event.ctrl == True or event.shift == True:
                #Get previously selected bones
                selected = [b.name for b in bpy.context.selected_pose_bones] 
                #Set target bone as active     
                for b in armobj.pose.bones:
                    b.bone.select = 0
                arm.bones.active = Bone.bone  
                #Reselect previously selected bones
                for b in armobj.pose.bones:
                    if (b.name in selected):
                        b.bone.select = 1             
            else:        
                for b in armobj.pose.bones:
                    b.bone.select = 0
                arm.bones.active = Bone.bone                                    
        return {"FINISHED"} 

class Operator_Hand_Roll_Ctrl_R(bpy.types.Operator):     
    bl_idname = "operator.hand_roll_ctrl_r"  
    bl_label = "BlenRig Select hand_roll_ctrl_R"  
    bl_description = "hand_roll_ctrl_R"      
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}   
    
    def invoke(self, context, event):
        select_op(self, context, event, "hand_roll_ctrl_R")                              
        return {"FINISHED"}            

class Operator_Hand_Sole_Ctrl_R(bpy.types.Operator):  
    bl_idname = "operator.hand_sole_ctrl_r"   
    bl_label = "BlenRig Select hand_sole_ctrl_R"  
    bl_description = "hand_sole_ctrl_R"       
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}       
    
    def invoke(self, context, event):
        select_op(self, context, event, "hand_sole_ctrl_R")                              
        return {"FINISHED"}        

class Operator_Hand_Sole_Pivot_Point_R(bpy.types.Operator):   
    bl_idname = "operator.hand_sole_pivot_point_r"    
    bl_label = "BlenRig Select hand_sole_pivot_point_R"  
    bl_description = "hand_sole_pivot_point_R"        
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}   
    
    def invoke(self, context, event):
        select_op(self, context, event, "hand_sole_pivot_point_R")                              
        return {"FINISHED"}            
 
######### FACE OPERATORS ###########################################


######### GUI OPERATORS ########################################### 

# Display or hide tabs (sets the appropriate id-property)
class ARMATURE_OT_blenrig_5_gui(bpy.types.Operator):
    "Display tab"
    bl_label = ""
    bl_idname = "gui.blenrig_5_tabs"

    tab = bpy.props.StringProperty(name="Tab", description="Tab of the gui to expand")
    
    def invoke(self, context, event):
        arm = bpy.context.active_object.data
        if self.properties.tab in arm:
            arm[self.properties.tab] = not arm[self.properties.tab]
        return{'FINISHED'}

####### RGISTRATION ###############################################

# Needed for property registration
class Blenrig_5_Props(bpy.types.PropertyGroup):
    gui_picker_body_props = bpy.props.BoolProperty(default=True, description="Toggle properties display")
    gui_snap_all = bpy.props.BoolProperty(default=False, description="Display ALL Snapping Buttons")    
    gui_snap = bpy.props.BoolProperty(default=False, description="Display Snapping Buttons") 
    gui_cust_props_all = bpy.props.BoolProperty(default=False, description="Show ALL Custom Properties") 

classes = [ARMATURE_OT_reset_constraints,
    ARMATURE_OT_full_bake,
    ARMATURE_OT_armature_baker,
    ARMATURE_OT_mesh_pose_baker,
    ARMATURE_OT_reset_hooks,
    ARMATURE_OT_reset_deformers,
    ARMATURE_OT_blenrig_5_gui,
    BlenRig_5_Interface,
    Blenrig_5_Props
    ]


def register():
    for c in classes:
        bpy.utils.register_class(c)
    bpy.types.WindowManager.blenrig_5_props = bpy.props.PointerProperty(type = Blenrig_5_Props)
    bpy.types.WindowManager.bake_to_shape = bpy.props.BoolProperty(name="Bake to Shape Key", default=False, description="Bake the mesh in a separate Shape Key")   

    # BlenRig IK/FK Snapping Operators     
    bpy.utils.register_class(Operator_Torso_Snap_FK_IK)
    bpy.utils.register_class(Operator_Torso_Snap_IK_FK) 
    bpy.utils.register_class(Operator_Head_Snap_FK_IK)  
    bpy.utils.register_class(Operator_Head_Snap_IK_FK)  
    bpy.utils.register_class(Operator_Torso_Snap_UP_INV)            
    bpy.utils.register_class(Operator_Torso_Snap_INV_UP)  
    bpy.utils.register_class(Operator_Arm_L_Snap_FK_IK)  
    bpy.utils.register_class(Operator_Arm_L_Snap_IK_FK)   
    bpy.utils.register_class(Operator_Arm_R_Snap_FK_IK)  
    bpy.utils.register_class(Operator_Arm_R_Snap_IK_FK)   
    bpy.utils.register_class(Operator_Leg_L_Snap_FK_IK)  
    bpy.utils.register_class(Operator_Leg_L_Snap_IK_FK)
    bpy.utils.register_class(Operator_Leg_R_Snap_FK_IK)  
    bpy.utils.register_class(Operator_Leg_R_Snap_IK_FK)                              
    # BlenRig Picker Operators
    bpy.utils.register_class(Operator_Head_Stretch)
    bpy.utils.register_class(Operator_Head_Toon)   
    bpy.utils.register_class(Operator_Head_Top_Ctrl)  
    bpy.utils.register_class(Operator_Head_Mid_Ctrl)          
    bpy.utils.register_class(Operator_Head_Mid_Curve) 
    bpy.utils.register_class(Operator_Mouth_Str_Ctrl)        
    bpy.utils.register_class(Operator_Head_FK) 
    bpy.utils.register_class(Operator_Head_IK)   
    bpy.utils.register_class(Operator_Neck_4_Toon) 
    bpy.utils.register_class(Operator_Face_Toon_Up)      
    bpy.utils.register_class(Operator_Face_Toon_Mid) 
    bpy.utils.register_class(Operator_Face_Toon_Low)  
    bpy.utils.register_class(Operator_Neck_3) 
    bpy.utils.register_class(Operator_Neck_2)
    bpy.utils.register_class(Operator_Neck_1)    
    bpy.utils.register_class(Operator_Neck_3_Toon)  
    bpy.utils.register_class(Operator_Neck_2_Toon) 
    bpy.utils.register_class(Operator_Neck_Ctrl)  
    bpy.utils.register_class(Operator_Shoulder_L) 
    bpy.utils.register_class(Operator_Shoulder_R) 
    bpy.utils.register_class(Operator_Shoulder_Rot_L) 
    bpy.utils.register_class(Operator_Shoulder_Rot_R) 
    bpy.utils.register_class(Operator_Clavi_Toon_L) 
    bpy.utils.register_class(Operator_Clavi_Toon_R) 
    bpy.utils.register_class(Operator_Head_Scale) 
    bpy.utils.register_class(Operator_Arm_Toon_L) 
    bpy.utils.register_class(Operator_Elbow_Pole_L) 
    bpy.utils.register_class(Operator_Forearm_Toon_L) 
    bpy.utils.register_class(Operator_Arm_Scale_L) 
    bpy.utils.register_class(Operator_Arm_FK_L) 
    bpy.utils.register_class(Operator_Arm_IK_L) 
    bpy.utils.register_class(Operator_Elbow_Toon_L) 
    bpy.utils.register_class(Operator_Forearm_FK_L) 
    bpy.utils.register_class(Operator_Forearm_IK_L) 
    bpy.utils.register_class(Operator_Hand_Toon_L)    
    bpy.utils.register_class(Operator_Arm_Toon_R) 
    bpy.utils.register_class(Operator_Elbow_Pole_R) 
    bpy.utils.register_class(Operator_Forearm_Toon_R) 
    bpy.utils.register_class(Operator_Arm_Scale_R) 
    bpy.utils.register_class(Operator_Arm_FK_R) 
    bpy.utils.register_class(Operator_Arm_IK_R) 
    bpy.utils.register_class(Operator_Elbow_Toon_R) 
    bpy.utils.register_class(Operator_Forearm_FK_R) 
    bpy.utils.register_class(Operator_Forearm_IK_R) 
    bpy.utils.register_class(Operator_Hand_Toon_R)  
    bpy.utils.register_class(Operator_Torso_Ctrl) 
    bpy.utils.register_class(Operator_Spine_3)   
    bpy.utils.register_class(Operator_Spine_2)  
    bpy.utils.register_class(Operator_Spine_1)  
    bpy.utils.register_class(Operator_Master_Torso_Pivot_Point)   
    bpy.utils.register_class(Operator_Master_Torso)   
    bpy.utils.register_class(Operator_Pelvis_Ctrl)                               
    bpy.utils.register_class(Operator_Spine_4_Toon)                                         
    bpy.utils.register_class(Operator_Spine_3_Toon)   
    bpy.utils.register_class(Operator_Spine_2_Toon)   
    bpy.utils.register_class(Operator_Spine_1_Toon)   
    bpy.utils.register_class(Operator_Pelvis_Toon)   
    bpy.utils.register_class(Operator_Spine_3_Inv_Ctrl)  
    bpy.utils.register_class(Operator_Hand_Roll_L) 
    bpy.utils.register_class(Operator_Fing_Spread_L)  
    bpy.utils.register_class(Operator_Hand_IK_Pivot_Point_L)     
    bpy.utils.register_class(Operator_Hand_IK_Ctrl_L)   
    bpy.utils.register_class(Operator_Hand_FK_L)                                                   
    bpy.utils.register_class(Operator_Fing_Lit_Ctrl_L)  
    bpy.utils.register_class(Operator_Fing_Lit_2_L) 
    bpy.utils.register_class(Operator_Fing_Lit_3_L)  
    bpy.utils.register_class(Operator_Fing_Lit_4_L)  
    bpy.utils.register_class(Operator_Fing_Ring_Ctrl_L)  
    bpy.utils.register_class(Operator_Fing_Ring_2_L) 
    bpy.utils.register_class(Operator_Fing_Ring_3_L)  
    bpy.utils.register_class(Operator_Fing_Ring_4_L)   
    bpy.utils.register_class(Operator_Fing_Mid_Ctrl_L)  
    bpy.utils.register_class(Operator_Fing_Mid_2_L) 
    bpy.utils.register_class(Operator_Fing_Mid_3_L)  
    bpy.utils.register_class(Operator_Fing_Mid_4_L)  
    bpy.utils.register_class(Operator_Fing_Ind_Ctrl_L)  
    bpy.utils.register_class(Operator_Fing_Ind_2_L) 
    bpy.utils.register_class(Operator_Fing_Ind_3_L)  
    bpy.utils.register_class(Operator_Fing_Ind_4_L)  
    bpy.utils.register_class(Operator_Fing_Thumb_Ctrl_L)  
    bpy.utils.register_class(Operator_Fing_Thumb_2_L) 
    bpy.utils.register_class(Operator_Fing_Thumb_3_L)  
    bpy.utils.register_class(Operator_Fing_Thumb_1_L)   
    bpy.utils.register_class(Operator_Fing_Lit_IK_L)  
    bpy.utils.register_class(Operator_Fing_Ring_IK_L) 
    bpy.utils.register_class(Operator_Fing_Mid_IK_L) 
    bpy.utils.register_class(Operator_Fing_Ind_IK_L) 
    bpy.utils.register_class(Operator_Fing_Thumb_IK_L)   
    bpy.utils.register_class(Operator_Hand_Close_L)        
    bpy.utils.register_class(Operator_Hand_Roll_R) 
    bpy.utils.register_class(Operator_Fing_Spread_R)  
    bpy.utils.register_class(Operator_Hand_IK_Pivot_Point_R)     
    bpy.utils.register_class(Operator_Hand_IK_Ctrl_R)   
    bpy.utils.register_class(Operator_Hand_FK_R)                                                   
    bpy.utils.register_class(Operator_Fing_Lit_Ctrl_R)  
    bpy.utils.register_class(Operator_Fing_Lit_2_R) 
    bpy.utils.register_class(Operator_Fing_Lit_3_R)  
    bpy.utils.register_class(Operator_Fing_Lit_4_R)  
    bpy.utils.register_class(Operator_Fing_Ring_Ctrl_R)  
    bpy.utils.register_class(Operator_Fing_Ring_2_R) 
    bpy.utils.register_class(Operator_Fing_Ring_3_R)  
    bpy.utils.register_class(Operator_Fing_Ring_4_R)   
    bpy.utils.register_class(Operator_Fing_Mid_Ctrl_R)  
    bpy.utils.register_class(Operator_Fing_Mid_2_R) 
    bpy.utils.register_class(Operator_Fing_Mid_3_R)  
    bpy.utils.register_class(Operator_Fing_Mid_4_R)  
    bpy.utils.register_class(Operator_Fing_Ind_Ctrl_R)  
    bpy.utils.register_class(Operator_Fing_Ind_2_R) 
    bpy.utils.register_class(Operator_Fing_Ind_3_R)  
    bpy.utils.register_class(Operator_Fing_Ind_4_R)  
    bpy.utils.register_class(Operator_Fing_Thumb_Ctrl_R)  
    bpy.utils.register_class(Operator_Fing_Thumb_2_R) 
    bpy.utils.register_class(Operator_Fing_Thumb_3_R)  
    bpy.utils.register_class(Operator_Fing_Thumb_1_R)   
    bpy.utils.register_class(Operator_Fing_Lit_IK_R)  
    bpy.utils.register_class(Operator_Fing_Ring_IK_R) 
    bpy.utils.register_class(Operator_Fing_Mid_IK_R) 
    bpy.utils.register_class(Operator_Fing_Ind_IK_R) 
    bpy.utils.register_class(Operator_Fing_Thumb_IK_R)  
    bpy.utils.register_class(Operator_Hand_Close_R)        
    bpy.utils.register_class(Operator_Thigh_Toon_L)   
    bpy.utils.register_class(Operator_Knee_Pole_L)  
    bpy.utils.register_class(Operator_Shin_Toon_L)  
    bpy.utils.register_class(Operator_Pelvis_Toon_L)  
    bpy.utils.register_class(Operator_Leg_Scale_L)    
    bpy.utils.register_class(Operator_Thigh_FK_L)  
    bpy.utils.register_class(Operator_Thigh_IK_L)  
    bpy.utils.register_class(Operator_Knee_Toon_L)  
    bpy.utils.register_class(Operator_Shin_FK_L)  
    bpy.utils.register_class(Operator_Shin_IK_L)  
    bpy.utils.register_class(Operator_Foot_Toon_L)    
    bpy.utils.register_class(Operator_Thigh_Toon_R)   
    bpy.utils.register_class(Operator_Knee_Pole_R)  
    bpy.utils.register_class(Operator_Shin_Toon_R)  
    bpy.utils.register_class(Operator_Pelvis_Toon_R)  
    bpy.utils.register_class(Operator_Leg_Scale_R)    
    bpy.utils.register_class(Operator_Thigh_FK_R)  
    bpy.utils.register_class(Operator_Thigh_IK_R)  
    bpy.utils.register_class(Operator_Knee_Toon_R)  
    bpy.utils.register_class(Operator_Shin_FK_R)  
    bpy.utils.register_class(Operator_Shin_IK_R)  
    bpy.utils.register_class(Operator_Foot_Toon_R)  
    bpy.utils.register_class(Operator_Toe_2_FK_L)  
    bpy.utils.register_class(Operator_Toe_Roll_1_L)   
    bpy.utils.register_class(Operator_Toe_1_FK_L)   
    bpy.utils.register_class(Operator_Toe_Roll_2_L)   
    bpy.utils.register_class(Operator_Foot_L)   
    bpy.utils.register_class(Operator_Foot_Roll_Ctrl_L)   
    bpy.utils.register_class(Operator_Sole_Ctrl_L)   
    bpy.utils.register_class(Operator_Sole_Pivot_Point_L)      
    bpy.utils.register_class(Operator_Toe_2_FK_R)  
    bpy.utils.register_class(Operator_Toe_Roll_1_R)   
    bpy.utils.register_class(Operator_Toe_1_FK_R)   
    bpy.utils.register_class(Operator_Toe_Roll_2_R)   
    bpy.utils.register_class(Operator_Foot_R)   
    bpy.utils.register_class(Operator_Foot_Roll_Ctrl_R)   
    bpy.utils.register_class(Operator_Sole_Ctrl_R)   
    bpy.utils.register_class(Operator_Sole_Pivot_Point_R)    
    bpy.utils.register_class(Operator_Master)                                     
    bpy.utils.register_class(Operator_Look) 
    bpy.utils.register_class(Operator_Look_L) 
    bpy.utils.register_class(Operator_Look_R)        
    bpy.utils.register_class(Operator_Zoom_Selected)
    #Quadruped
    bpy.utils.register_class(Operator_Ankle_Toon_L) 
    bpy.utils.register_class(Operator_Carpal_FK_L) 
    bpy.utils.register_class(Operator_Carpal_IK_L)  
    bpy.utils.register_class(Operator_Carpal_Toon_L)      
    bpy.utils.register_class(Operator_Ankle_Toon_R) 
    bpy.utils.register_class(Operator_Carpal_FK_R) 
    bpy.utils.register_class(Operator_Carpal_IK_R) 
    bpy.utils.register_class(Operator_Carpal_Toon_R)      
    bpy.utils.register_class(Operator_Hock_Toon_L) 
    bpy.utils.register_class(Operator_Tarsal_FK_L) 
    bpy.utils.register_class(Operator_Tarsal_IK_L) 
    bpy.utils.register_class(Operator_Tarsal_Toon_L)        
    bpy.utils.register_class(Operator_Hock_Toon_R) 
    bpy.utils.register_class(Operator_Tarsal_FK_R) 
    bpy.utils.register_class(Operator_Tarsal_IK_R)
    bpy.utils.register_class(Operator_Tarsal_Toon_R)  
    bpy.utils.register_class(Operator_Fing_2_FK_L)     
    bpy.utils.register_class(Operator_Fing_1_FK_L)   
    bpy.utils.register_class(Operator_Fing_Roll_2_L)    
    bpy.utils.register_class(Operator_Fing_Roll_1_L)      
    bpy.utils.register_class(Operator_Hand_L)    
    bpy.utils.register_class(Operator_Hand_Roll_Ctrl_L)    
    bpy.utils.register_class(Operator_Hand_Sole_Ctrl_L)    
    bpy.utils.register_class(Operator_Hand_Sole_Pivot_Point_L)     
    bpy.utils.register_class(Operator_Fing_2_FK_R)     
    bpy.utils.register_class(Operator_Fing_1_FK_R)   
    bpy.utils.register_class(Operator_Fing_Roll_2_R)    
    bpy.utils.register_class(Operator_Fing_Roll_1_R)      
    bpy.utils.register_class(Operator_Hand_R)    
    bpy.utils.register_class(Operator_Hand_Roll_Ctrl_R)    
    bpy.utils.register_class(Operator_Hand_Sole_Ctrl_R)    
    bpy.utils.register_class(Operator_Hand_Sole_Pivot_Point_R)   
    #Align Operators
    bpy.utils.register_class(Operator_BlenRig_Fix_Misaligned_Bones)
    bpy.utils.register_class(Operator_BlenRig_Auto_Bone_Roll)    
    bpy.utils.register_class(Operator_BlenRig_Custom_Bone_Roll)      
                                                               

def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)
    del bpy.types.WindowManager.bake_to_shape          
    # BlenRig IK/FK Snapping Operators      
    bpy.utils.unregister_class(Operator_Torso_Snap_FK_IK)
    bpy.utils.unregister_class(Operator_Torso_Snap_IK_FK) 
    bpy.utils.unregister_class(Operator_Head_Snap_FK_IK)  
    bpy.utils.unregister_class(Operator_Head_Snap_IK_FK)    
    bpy.utils.unregister_class(Operator_Torso_Snap_UP_INV)          
    bpy.utils.unregister_class(Operator_Torso_Snap_INV_UP)  
    bpy.utils.unregister_class(Operator_Arm_L_Snap_FK_IK)    
    bpy.utils.unregister_class(Operator_Arm_L_Snap_IK_FK)   
    bpy.utils.unregister_class(Operator_Arm_R_Snap_FK_IK)    
    bpy.utils.unregister_class(Operator_Arm_R_Snap_IK_FK)   
    bpy.utils.unregister_class(Operator_Leg_L_Snap_FK_IK)  
    bpy.utils.unregister_class(Operator_Leg_L_Snap_IK_FK)
    bpy.utils.unregister_class(Operator_Leg_R_Snap_FK_IK)  
    bpy.utils.unregister_class(Operator_Leg_R_Snap_IK_FK)   
    # BlenRig Picker Operators
    bpy.utils.unregister_class(Operator_Head_Stretch)   
    bpy.utils.unregister_class(Operator_Head_Toon)  
    bpy.utils.unregister_class(Operator_Head_Top_Ctrl)  
    bpy.utils.unregister_class(Operator_Head_Mid_Ctrl)        
    bpy.utils.unregister_class(Operator_Head_Mid_Curve) 
    bpy.utils.unregister_class(Operator_Mouth_Str_Ctrl)             
    bpy.utils.unregister_class(Operator_Head_FK) 
    bpy.utils.unregister_class(Operator_Head_IK)   
    bpy.utils.unregister_class(Operator_Neck_4_Toon) 
    bpy.utils.unregister_class(Operator_Face_Toon_Up)        
    bpy.utils.unregister_class(Operator_Face_Toon_Mid) 
    bpy.utils.unregister_class(Operator_Face_Toon_Low)  
    bpy.utils.unregister_class(Operator_Neck_3) 
    bpy.utils.unregister_class(Operator_Neck_2)
    bpy.utils.unregister_class(Operator_Neck_1)  
    bpy.utils.unregister_class(Operator_Neck_3_Toon)    
    bpy.utils.unregister_class(Operator_Neck_2_Toon) 
    bpy.utils.unregister_class(Operator_Neck_Ctrl)              
    bpy.utils.unregister_class(Operator_Shoulder_L) 
    bpy.utils.unregister_class(Operator_Shoulder_R) 
    bpy.utils.unregister_class(Operator_Shoulder_Rot_L) 
    bpy.utils.unregister_class(Operator_Shoulder_Rot_R) 
    bpy.utils.unregister_class(Operator_Clavi_Toon_L) 
    bpy.utils.unregister_class(Operator_Clavi_Toon_R) 
    bpy.utils.unregister_class(Operator_Head_Scale)
    bpy.utils.unregister_class(Operator_Arm_Toon_L) 
    bpy.utils.unregister_class(Operator_Elbow_Pole_L) 
    bpy.utils.unregister_class(Operator_Forearm_Toon_L) 
    bpy.utils.unregister_class(Operator_Arm_Scale_L) 
    bpy.utils.unregister_class(Operator_Arm_FK_L) 
    bpy.utils.unregister_class(Operator_Arm_IK_L) 
    bpy.utils.unregister_class(Operator_Elbow_Toon_L) 
    bpy.utils.unregister_class(Operator_Forearm_FK_L) 
    bpy.utils.unregister_class(Operator_Forearm_IK_L) 
    bpy.utils.unregister_class(Operator_Hand_Toon_L)      
    bpy.utils.unregister_class(Operator_Arm_Toon_R) 
    bpy.utils.unregister_class(Operator_Elbow_Pole_R) 
    bpy.utils.unregister_class(Operator_Forearm_Toon_R) 
    bpy.utils.unregister_class(Operator_Arm_Scale_R) 
    bpy.utils.unregister_class(Operator_Arm_FK_R) 
    bpy.utils.unregister_class(Operator_Arm_IK_R) 
    bpy.utils.unregister_class(Operator_Elbow_Toon_R) 
    bpy.utils.unregister_class(Operator_Forearm_FK_R) 
    bpy.utils.unregister_class(Operator_Forearm_IK_R) 
    bpy.utils.unregister_class(Operator_Hand_Toon_R)      
    bpy.utils.unregister_class(Operator_Torso_Ctrl)          
    bpy.utils.unregister_class(Operator_Spine_3)   
    bpy.utils.unregister_class(Operator_Spine_2)    
    bpy.utils.unregister_class(Operator_Spine_1)    
    bpy.utils.unregister_class(Operator_Master_Torso_Pivot_Point)   
    bpy.utils.unregister_class(Operator_Master_Torso)   
    bpy.utils.unregister_class(Operator_Pelvis_Ctrl)   
    bpy.utils.unregister_class(Operator_Spine_4_Toon)                                           
    bpy.utils.unregister_class(Operator_Spine_3_Toon)   
    bpy.utils.unregister_class(Operator_Spine_2_Toon)   
    bpy.utils.unregister_class(Operator_Spine_1_Toon)   
    bpy.utils.unregister_class(Operator_Pelvis_Toon)     
    bpy.utils.unregister_class(Operator_Spine_3_Inv_Ctrl)    
    bpy.utils.unregister_class(Operator_Hand_Roll_L) 
    bpy.utils.unregister_class(Operator_Fing_Spread_L)  
    bpy.utils.unregister_class(Operator_Hand_IK_Pivot_Point_L)   
    bpy.utils.unregister_class(Operator_Hand_IK_Ctrl_L)   
    bpy.utils.unregister_class(Operator_Hand_FK_L)                                                 
    bpy.utils.unregister_class(Operator_Fing_Lit_Ctrl_L)  
    bpy.utils.unregister_class(Operator_Fing_Lit_2_L) 
    bpy.utils.unregister_class(Operator_Fing_Lit_3_L)  
    bpy.utils.unregister_class(Operator_Fing_Lit_4_L)  
    bpy.utils.unregister_class(Operator_Fing_Ring_Ctrl_L)  
    bpy.utils.unregister_class(Operator_Fing_Ring_2_L) 
    bpy.utils.unregister_class(Operator_Fing_Ring_3_L)  
    bpy.utils.unregister_class(Operator_Fing_Ring_4_L)   
    bpy.utils.unregister_class(Operator_Fing_Mid_Ctrl_L)  
    bpy.utils.unregister_class(Operator_Fing_Mid_2_L) 
    bpy.utils.unregister_class(Operator_Fing_Mid_3_L)  
    bpy.utils.unregister_class(Operator_Fing_Mid_4_L)  
    bpy.utils.unregister_class(Operator_Fing_Ind_Ctrl_L)  
    bpy.utils.unregister_class(Operator_Fing_Ind_2_L) 
    bpy.utils.unregister_class(Operator_Fing_Ind_3_L)  
    bpy.utils.unregister_class(Operator_Fing_Ind_4_L)  
    bpy.utils.unregister_class(Operator_Fing_Thumb_Ctrl_L)  
    bpy.utils.unregister_class(Operator_Fing_Thumb_2_L) 
    bpy.utils.unregister_class(Operator_Fing_Thumb_3_L)  
    bpy.utils.unregister_class(Operator_Fing_Thumb_1_L) 
    bpy.utils.unregister_class(Operator_Fing_Lit_IK_L)  
    bpy.utils.unregister_class(Operator_Fing_Ring_IK_L) 
    bpy.utils.unregister_class(Operator_Fing_Mid_IK_L) 
    bpy.utils.unregister_class(Operator_Fing_Ind_IK_L) 
    bpy.utils.unregister_class(Operator_Fing_Thumb_IK_L)   
    bpy.utils.unregister_class(Operator_Hand_Close_L)          
    bpy.utils.unregister_class(Operator_Hand_Roll_R) 
    bpy.utils.unregister_class(Operator_Fing_Spread_R)  
    bpy.utils.unregister_class(Operator_Hand_IK_Pivot_Point_R)   
    bpy.utils.unregister_class(Operator_Hand_IK_Ctrl_R)   
    bpy.utils.unregister_class(Operator_Hand_FK_R)                                                 
    bpy.utils.unregister_class(Operator_Fing_Lit_Ctrl_R)  
    bpy.utils.unregister_class(Operator_Fing_Lit_2_R) 
    bpy.utils.unregister_class(Operator_Fing_Lit_3_R)  
    bpy.utils.unregister_class(Operator_Fing_Lit_4_R)  
    bpy.utils.unregister_class(Operator_Fing_Ring_Ctrl_R)  
    bpy.utils.unregister_class(Operator_Fing_Ring_2_R) 
    bpy.utils.unregister_class(Operator_Fing_Ring_3_R)  
    bpy.utils.unregister_class(Operator_Fing_Ring_4_R)   
    bpy.utils.unregister_class(Operator_Fing_Mid_Ctrl_R)  
    bpy.utils.unregister_class(Operator_Fing_Mid_2_R) 
    bpy.utils.unregister_class(Operator_Fing_Mid_3_R)  
    bpy.utils.unregister_class(Operator_Fing_Mid_4_R)  
    bpy.utils.unregister_class(Operator_Fing_Ind_Ctrl_R)  
    bpy.utils.unregister_class(Operator_Fing_Ind_2_R) 
    bpy.utils.unregister_class(Operator_Fing_Ind_3_R)  
    bpy.utils.unregister_class(Operator_Fing_Ind_4_R)  
    bpy.utils.unregister_class(Operator_Fing_Thumb_Ctrl_R)  
    bpy.utils.unregister_class(Operator_Fing_Thumb_2_R) 
    bpy.utils.unregister_class(Operator_Fing_Thumb_3_R)  
    bpy.utils.unregister_class(Operator_Fing_Thumb_1_R) 
    bpy.utils.unregister_class(Operator_Fing_Lit_IK_R)  
    bpy.utils.unregister_class(Operator_Fing_Ring_IK_R) 
    bpy.utils.unregister_class(Operator_Fing_Mid_IK_R) 
    bpy.utils.unregister_class(Operator_Fing_Ind_IK_R) 
    bpy.utils.unregister_class(Operator_Fing_Thumb_IK_R)   
    bpy.utils.unregister_class(Operator_Hand_Close_R)       
    bpy.utils.unregister_class(Operator_Thigh_Toon_L)   
    bpy.utils.unregister_class(Operator_Knee_Pole_L)  
    bpy.utils.unregister_class(Operator_Shin_Toon_L)  
    bpy.utils.unregister_class(Operator_Pelvis_Toon_L)  
    bpy.utils.unregister_class(Operator_Leg_Scale_L)      
    bpy.utils.unregister_class(Operator_Thigh_FK_L)  
    bpy.utils.unregister_class(Operator_Thigh_IK_L)  
    bpy.utils.unregister_class(Operator_Knee_Toon_L)  
    bpy.utils.unregister_class(Operator_Shin_FK_L)  
    bpy.utils.unregister_class(Operator_Shin_IK_L)  
    bpy.utils.unregister_class(Operator_Foot_Toon_L)      
    bpy.utils.unregister_class(Operator_Thigh_Toon_R)   
    bpy.utils.unregister_class(Operator_Knee_Pole_R)  
    bpy.utils.unregister_class(Operator_Shin_Toon_R)  
    bpy.utils.unregister_class(Operator_Pelvis_Toon_R)  
    bpy.utils.unregister_class(Operator_Leg_Scale_R)      
    bpy.utils.unregister_class(Operator_Thigh_FK_R)  
    bpy.utils.unregister_class(Operator_Thigh_IK_R)  
    bpy.utils.unregister_class(Operator_Knee_Toon_R)  
    bpy.utils.unregister_class(Operator_Shin_FK_R)  
    bpy.utils.unregister_class(Operator_Shin_IK_R)  
    bpy.utils.unregister_class(Operator_Foot_Toon_R) 
    bpy.utils.unregister_class(Operator_Toe_2_FK_L)  
    bpy.utils.unregister_class(Operator_Toe_Roll_1_L)   
    bpy.utils.unregister_class(Operator_Toe_1_FK_L)   
    bpy.utils.unregister_class(Operator_Toe_Roll_2_L)   
    bpy.utils.unregister_class(Operator_Foot_L)   
    bpy.utils.unregister_class(Operator_Foot_Roll_Ctrl_L)   
    bpy.utils.unregister_class(Operator_Sole_Ctrl_L)   
    bpy.utils.unregister_class(Operator_Sole_Pivot_Point_L)    
    bpy.utils.unregister_class(Operator_Toe_2_FK_R)  
    bpy.utils.unregister_class(Operator_Toe_Roll_1_R)   
    bpy.utils.unregister_class(Operator_Toe_1_FK_R)   
    bpy.utils.unregister_class(Operator_Toe_Roll_2_R)   
    bpy.utils.unregister_class(Operator_Foot_R)   
    bpy.utils.unregister_class(Operator_Foot_Roll_Ctrl_R)   
    bpy.utils.unregister_class(Operator_Sole_Ctrl_R)   
    bpy.utils.unregister_class(Operator_Sole_Pivot_Point_R) 
    bpy.utils.unregister_class(Operator_Master)                                 
    bpy.utils.unregister_class(Operator_Look) 
    bpy.utils.unregister_class(Operator_Look_L) 
    bpy.utils.unregister_class(Operator_Look_R)      
    bpy.utils.unregister_class(Operator_Zoom_Selected)
    #Quadruped
    bpy.utils.unregister_class(Operator_Ankle_Toon_L) 
    bpy.utils.unregister_class(Operator_Carpal_FK_L) 
    bpy.utils.unregister_class(Operator_Carpal_IK_L)  
    bpy.utils.unregister_class(Operator_Carpal_Toon_L)      
    bpy.utils.unregister_class(Operator_Ankle_Toon_R) 
    bpy.utils.unregister_class(Operator_Carpal_FK_R) 
    bpy.utils.unregister_class(Operator_Carpal_IK_R) 
    bpy.utils.unregister_class(Operator_Carpal_Toon_R)      
    bpy.utils.unregister_class(Operator_Hock_Toon_L) 
    bpy.utils.unregister_class(Operator_Tarsal_FK_L) 
    bpy.utils.unregister_class(Operator_Tarsal_IK_L) 
    bpy.utils.unregister_class(Operator_Tarsal_Toon_L)        
    bpy.utils.unregister_class(Operator_Hock_Toon_R) 
    bpy.utils.unregister_class(Operator_Tarsal_FK_R) 
    bpy.utils.unregister_class(Operator_Tarsal_IK_R)
    bpy.utils.unregister_class(Operator_Tarsal_Toon_R)     
    bpy.utils.unregister_class(Operator_Fing_2_FK_L)     
    bpy.utils.unregister_class(Operator_Fing_1_FK_L)   
    bpy.utils.unregister_class(Operator_Fing_Roll_2_L)    
    bpy.utils.unregister_class(Operator_Fing_Roll_1_L)      
    bpy.utils.unregister_class(Operator_Hand_L)    
    bpy.utils.unregister_class(Operator_Hand_Roll_Ctrl_L)    
    bpy.utils.unregister_class(Operator_Hand_Sole_Ctrl_L)    
    bpy.utils.unregister_class(Operator_Hand_Sole_Pivot_Point_L)     
    bpy.utils.unregister_class(Operator_Fing_2_FK_R)     
    bpy.utils.unregister_class(Operator_Fing_1_FK_R)   
    bpy.utils.unregister_class(Operator_Fing_Roll_2_R)    
    bpy.utils.unregister_class(Operator_Fing_Roll_1_R)      
    bpy.utils.unregister_class(Operator_Hand_R)    
    bpy.utils.unregister_class(Operator_Hand_Roll_Ctrl_R)    
    bpy.utils.unregister_class(Operator_Hand_Sole_Ctrl_R)    
    bpy.utils.unregister_class(Operator_Hand_Sole_Pivot_Point_R)        
    #Align Operators
    bpy.utils.unregister_class(Operator_BlenRig_Fix_Misaligned_Bones)    
    bpy.utils.unregister_class(Operator_BlenRig_Auto_Bone_Roll)    
    bpy.utils.unregister_class(Operator_BlenRig_Custom_Bone_Roll)           
                                            

if __name__ == "__main__":
    register()