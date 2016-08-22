# -------------------------------------------------------------------------
# Name:        Water Balance module
# Purpose:		1.) check if water balnace per time step is ok ( = 0)
#               2.) produce an annual overview - income, outcome storage 
# Author:      PB
#
# Created:     22/08/2016
# Copyright:   (c) PB 2016
# -------------------------------------------------------------------------

from management_modules.data_handling import *


class waterbalance(object):

    """
    # ************************************************************
    # ***** WATER BALANCE ****************************************
    # ************************************************************

	# 1.) check if water balnace per time step is ok ( = 0)
    # 2.) produce an annual overview - income, outcome storage 
    """

    def __init__(self, waterbalance_variable):
        self.var = waterbalance_variable

# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

    def initial(self):
        """ initial part of the water balance module
        """
        if option['calcWaterBalance']:
            i = 1

        """ store the initial storage volume of snow, soil etc.
        """
        if option['sumWaterBalance']:
            # variables of storage
            self.var.sum_balanceStore = ['SnowCover','sum_interceptStor','sum_topWaterLayer','sum_storUpp000005','sum_storUpp005030','sum_storLow030150']

            # variable of fluxes
            self.var.sum_balanceFlux = ['Precipitation','SnowMelt','Rain','sum_interceptEvap','actualET']

            #for variable in self.var.sum_balanceStore:
                # vars(self.var)["sumup_" + variable] =  vars(self.var)[variable]
            for variable in self.var.sum_balanceFlux:
                vars(self.var)["sumup_" + variable] =  globals.inZero.copy()
            i =1


# --------------------------------------------------------------------------
# --------------------------------------------------------------------------


    """
    def getMinMaxMean(mapFile):
        mn = pcr.cellvalue(pcr.mapminimum(mapFile), 1)[0]
        mx = pcr.cellvalue(pcr.mapmaximum(mapFile), 1)[0]
        nrValues = pcr.cellvalue(pcr.maptotal(pcr.scalar(pcr.defined(mapFile))), 1)[
                0]  # / getNumNonMissingValues(mapFile)
        return mn, mx, (getMapTotal(mapFile) / nrValues)
    """

    def waterBalanceCheck(self, fluxesIn, fluxesOut, preStorages, endStorages, processName, printTrue=False):
        """ dynamic part of the water balance module
        Returns the water balance for a list of input, output, and storage map files
        """

        income =  globals.inZero.copy()
        out = globals.inZero.copy()
        store =  globals.inZero.copy()

        for fluxIn in fluxesIn:   income += fluxIn
        for fluxOut in fluxesOut: out += fluxOut
        for preStorage in preStorages: store += preStorage
        for endStorage in endStorages: store -= endStorage
        balance =  income + store - out
        #balance = endStorages
        minB = np.amin(balance)
        maxB = np.amax(balance)
        #meanB = np.average(balance, axis=0)
        meanB = 0.0

        if printTrue:
            print "     %s %10.8f %10.8f %10.8f" % (processName, minB,maxB, meanB),
        j = 0

# ----------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------


def dynamic(self):
    """ dynamic part of the water balance module
    """
    if option['sumWaterBalance']:
        i = 1

        # sum up storage variables
        #for variable in self.var.sum_balanceStore:
         #   vars(self.var)["sumup_" + variable] =  vars(self.var)[variable].copy()


        # sum up fluxes variables
        for variable in self.var.sum_balanceFlux:
            vars(self.var)["sumup_" + variable] = vars(self.var)["sumup_" + variable] + vars(self.var)[variable]