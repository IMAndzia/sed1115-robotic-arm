# sed1115-robotic-arm

## Project Overview
This repository contains the embedded software design and source data for an inspired by the mechanical "Etch A Sketch" toy, this system runs on a Raspberry Pi Pico using MicroPython. It reads continuous horizontal (X) and vertical (Y) coordinate inputs from two analog potentiometers and pen elevation commands from a toggle switch, processes the data through trigonometric inverse kinematics, and drives three independent PWM servos to actuate the shoulder joint, elbow joint and pen mechanism.

## Module Responsibilities
1. Anna Rogowsla - Inverse kinematics math (Kinematics.py)
                 - Joint movement routines (Arm_control.py)
                 - Unit test developement (test_kinematics.py)
                 - Main program loop for the Raspberry Pi Pico brachiograph (main.py)
   
2. Alena Romaniuk - Unit tests for angle-to-duty conversion and servo movement (test_arm_control.py)
                  - Main program loop for the Raspberry Pi Pico brachiograph (main.py)
                  - Joint movement routines (Arm_control.py)
                  - Stores GPIO pin numbers, arm lengths, and safe servo limits (config.py)

3. Alex Rabinow - Reads X and Y potentiometers and pen button, converts dial readings into (x, y) coordinates. (Inputs.py)

## Workflow & Project Management
- Version Control: All development follows a feature-branch workflow. Team members push modular changes to dedicated feature branches and merge into "main" via Pull Requests (PRs)
- Issue Tracking: GitHub Issues are actively used for bug tracking, task management, and assigning specific skeletal function deliverables to team members
