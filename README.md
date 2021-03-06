# Molecular Blender [![Build Status](https://travis-ci.org/smparker/molecular-blender.svg?branch=master)](https://travis-ci.org/smparker/molecular-blender)
An import plugin specialized for .xyz files of molecules used in, for example,
quantum chemistry

## Capabilities

- imports using linked objects making rapid changes to the aesthetics feasible
- basic styling (stick model, VDW, ball and stick, wireframe) and sensible
  defaults
- support for animations (input as multiframe .xyz files) including dynamically
  drawing bonds
- find and fill in aromatic rings
- draw spheres sitting on atoms to represent atomic charges and dynamically
  scale them during an animation
- draw molecular orbital isosurfaces with .cube files or .molden files

## Installation
There are two basic ways to install Molecular Blender, either through
the Blender interface or directly adding it to Blender's internal list of addons.

### Through Blender
The simplest way to install would be to download this repository as a zip file.
Then, navigate to `User Preferences` in Blender and select the `Add-ons` pane.
Click the `Install from File...` button at the bottom of the panel and select
the .zip file of the repository. Then activate it in the `Add-ons` window (and
hit `Save User Settings` for good measure).

### Manual
You can also add a directory or a symlink directly to the addons folder.
The recommended way for developers to install Molecular Blender is with a symlink:

    ln -s /path/to/molecular/blender/repo /path/to/blender/scripts/addons/

and then it should appear in the list of Import-Export addons that can be
activated like any other addon.

On Mac OS X, the path for a user supplied addon is

    /Users/<username>/Library/Application\ Support/Blender/<version>/scripts/addons

where `<username>` and `<version>` should be replaced with your username and the
Blender version you are using.

## Design

The only guiding design principle so far has been to try and separate the molecular
data structures (Molecule, Bond, Atom) from the Blender manipulations. This is
subject to change.
