from  __future__ import  print_function

import os
import sys
import re
import string

from scriptCommon import catchPath

versionParser = re.compile( r'(\s*static\sVersion\sversion)\s*\(\s*(.*)\s*,\s*(.*)\s*,\s*(.*)\s*,\s*\"(.*)\"\s*,\s*(.*)\s*\).*' )
rootPath = os.path.join( catchPath, 'include/' )
versionPath = os.path.join( rootPath, "internal/catch_version.cpp" )
definePath = os.path.join(rootPath, 'catch.hpp')
readmePath = os.path.join( catchPath, "README.md" )
cmakePath = os.path.join(catchPath, 'CMakeLists.txt')

class Version:
    def __init__(self):
        with open( versionPath, 'r' ) as f:
            for line in f:
                if m := versionParser.match(line):
                    self.variableDecl = m.group(1)
                    self.majorVersion = int(m.group(2))
                    self.minorVersion = int(m.group(3))
                    self.patchNumber = int(m.group(4))
                    self.branchName = m.group(5)
                    self.buildNumber = int(m.group(6))

    def nonDevelopRelease(self):
        if self.branchName != "":
            self.branchName = ""
            self.buildNumber = 0
    def developBuild(self):
        if self.branchName == "":
            self.branchName = "develop"
            self.buildNumber = 0

    def incrementBuildNumber(self):
        self.developBuild()
        self.buildNumber = self.buildNumber+1

    def incrementPatchNumber(self):
        self.nonDevelopRelease()
        self.patchNumber = self.patchNumber+1

    def incrementMinorVersion(self):
        self.nonDevelopRelease()
        self.patchNumber = 0
        self.minorVersion = self.minorVersion+1

    def incrementMajorVersion(self):
        self.nonDevelopRelease()
        self.patchNumber = 0
        self.minorVersion = 0
        self.majorVersion = self.majorVersion+1

    def getVersionString(self):
        versionString = '{0}.{1}.{2}'.format( self.majorVersion, self.minorVersion, self.patchNumber )
        if self.branchName != "":
            versionString += '-{0}.{1}'.format( self.branchName, self.buildNumber )
        return versionString

    def updateVersionFile(self):
        with open( versionPath, 'r' ) as f:
            lines = []
            for line in f:
                m = versionParser.match( line )
                if m:
                    lines.append( '{0}( {1}, {2}, {3}, "{4}", {5} );'.format( self.variableDecl, self.majorVersion, self.minorVersion, self.patchNumber, self.branchName, self.buildNumber ) )
                else:
                    lines.append( line.rstrip() )
        f = open( versionPath, 'w' )
        for line in lines:
            f.write( line + "\n" )

def updateReadmeFile(version):
    import updateWandbox

    downloadParser = re.compile( r'<a href=\"https://github.com/catchorg/Catch2/releases/download/v\d+\.\d+\.\d+/catch.hpp\">' )
    success, wandboxLink = updateWandbox.uploadFiles()
    if not success:
        print(f'Error when uploading to wandbox: {wandboxLink}')
        exit(1)
    with open( readmePath, 'r' ) as f:
        lines = [line.rstrip() for line in f]
    f = open( readmePath, 'w' )
    for line in lines:
        line = downloadParser.sub( r'<a href="https://github.com/catchorg/Catch2/releases/download/v{0}/catch.hpp">'.format(version.getVersionString()) , line)
        if '[![Try online](https://img.shields.io/badge/try-online-blue.svg)]' in line:
            line = '[![Try online](https://img.shields.io/badge/try-online-blue.svg)]({0})'.format(wandboxLink)
        f.write( line + "\n" )


def updateCmakeFile(version):
    with open(cmakePath, 'r') as file:
        lines = file.readlines()
    with open(cmakePath, 'w') as file:
        for line in lines:
            if 'project(Catch2 LANGUAGES CXX VERSION ' in line:
                file.write('project(Catch2 LANGUAGES CXX VERSION {0})\n'.format(version.getVersionString()))
            else:
                file.write(line)


def updateVersionDefine(version):
    with open(definePath, 'r') as file:
        lines = file.readlines()
    with open(definePath, 'w') as file:
        for line in lines:
            if '#define CATCH_VERSION_MAJOR' in line:
                file.write(f'#define CATCH_VERSION_MAJOR {version.majorVersion}\n')
            elif '#define CATCH_VERSION_MINOR' in line:
                file.write(f'#define CATCH_VERSION_MINOR {version.minorVersion}\n')
            elif '#define CATCH_VERSION_PATCH' in line:
                file.write(f'#define CATCH_VERSION_PATCH {version.patchNumber}\n')
            else:
                file.write(line)


def performUpdates(version):
    # First update version file, so we can regenerate single header and
    # have it ready for upload to wandbox, when updating readme
    version.updateVersionFile()
    updateVersionDefine(version)

    import generateSingleHeader
    generateSingleHeader.generate(version)

    # Then copy the reporters to single include folder to keep them in sync
    # We probably should have some kind of convention to select which reporters need to be copied automagically,
    # but this works for now
    import shutil
    for rep in ('automake', 'tap', 'teamcity'):
        sourceFile = os.path.join(
            catchPath, f'include/reporters/catch_reporter_{rep}.hpp'
        )
        destFile = os.path.join(
            catchPath, 'single_include', 'catch2', f'catch_reporter_{rep}.hpp'
        )
        shutil.copyfile(sourceFile, destFile)

    updateReadmeFile(version)
    updateCmakeFile(version)
