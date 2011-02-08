##################################################
#
# Eutelescope module
#
# Author: Jan Engels, DESY
# Date: Jan, 2007
#
##################################################
                                                                                                                                                            
# custom imports
from marlinpkg import MarlinPKG
from util import *

class Eutelescope(MarlinPKG):
    """ Responsible for the Eutelescope installation process. """
    
    def __init__(self, userInput):
        MarlinPKG.__init__(self, "Eutelescope", userInput )

        # required modules
        self.reqmodules = [ "Marlin",  "LCIO" ]

        # optional modules
        self.optmodules = [ "GEAR", "AIDA" , "MarlinUtil", "CLHEP", "GSL", "CED", "ROOT" ]

        # cvs root
        self.download.root = "eutelescope"


    def compile(self):
        """ compile Eutelescope """


        # ----- BUILD EUTELESCOPE ----------------------------
        os.chdir( self.installPath+"/build" )

        if( self.rebuild ):
            tryunlink( "CMakeCache.txt" )

        if( os.system( self.genCMakeCmd() + " 2>&1 | tee -a " + self.logfile ) != 0 ):
            self.abort( "failed to configure!!" )

        if( os.system( "make install 2>&1 | tee -a " + self.logfile ) != 0 ):
            self.abort( "failed to install!!" )

        os.chdir( self.installPath )


        if self.env.get( "EUDAQ_VERSION", "" ):

            # ----- BUILD EUDAQ ---------------------------------
            os.system( "svn co http://svn.hepforge.org/eudaq/%s eudaq/%s" % (self.env["EUDAQ_VERSION"], self.env["EUDAQ_VERSION"]) )

            os.chdir( self.env[ "EUDAQ" ] ) # needs to be defined in preCheckDeps (so it is written to build_env.sh)

            if( self.rebuild ):
                os.system( "make clean" )

            os.system( "make USE_LCIO=1 USE_EUTELESCOPE=1 main" )

            # ----- RE-BUILD EUTELESCOPE ---------------------------
            os.chdir( self.installPath + "/build" )

            os.system( self.genCMakeCmd() + " -DEUDAQ_DIR="+self.env[ "EUDAQ" ] )
            os.system( "make install" )


    def preCheckDeps(self):
        MarlinPKG.preCheckDeps(self)

        if self.env.get( "EUDAQ_VERSION", "" ):
            self.env[ "EUDAQ" ] = self.installPath + "/eudaq/" + self.env["EUDAQ_VERSION"]



    def postCheckDeps(self):
        MarlinPKG.postCheckDeps(self)

        self.env["EUTELESCOPE"] = self.installPath
        self.envpath["PATH"].append( '$EUTELESCOPE/bin' )
        self.envpath["LD_LIBRARY_PATH"].append( '$EUTELESCOPE/lib' )

