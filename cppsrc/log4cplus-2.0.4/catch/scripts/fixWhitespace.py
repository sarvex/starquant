#!/usr/bin/env python

from  __future__ import  print_function
import os
from scriptCommon import catchPath

def isSourceFile( path ):
    return path.endswith( ".cpp" ) or path.endswith( ".h" ) or path.endswith( ".hpp" )

def fixAllFilesInDir( dir ):
    changedFiles = 0
    for f in os.listdir( dir ):
        path = os.path.join( dir,f )
        if os.path.isfile( path ):
            if isSourceFile( path ):
                if fixFile( path ):
                    changedFiles += 1
        else:
            fixAllFilesInDir( path )
    return changedFiles

def fixFile( path ):
    with open( path, 'r' ) as f:
        lines = []
        changed = 0
        for line in f:
            trimmed = line.rstrip() + "\n"
            trimmed = trimmed.replace('\t', '    ')
            if trimmed != line:
                changed = changed +1
            lines.append( trimmed )
    if changed > 0:
        global changedFiles
        changedFiles = changedFiles + 1
        print(f"{path}:")
        print(f" - fixed {str(changed)} line(s)")
        altPath = f"{path}.backup"
        os.rename( path, altPath )
        with open( path, 'w' ) as f2:
            for line in lines:
                f2.write( line )
        os.remove( altPath )
        return True
    return False

changedFiles = fixAllFilesInDir(catchPath)
if changedFiles > 0:
    print(f"Fixed {str(changedFiles)} file(s)")
else:
    print( "No trailing whitespace found" )
