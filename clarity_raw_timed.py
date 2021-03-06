import numpy as np
import clarity_libraw
from os.path import expanduser
from PyDAQmx import *

# Options
SaveEachData2CSV = False
SaveEachData2NPY = True

# Set folder and file names
home = expanduser("~") + '\\Dropbox (Clarity Movement)\\Hardware R&D\\'
filefolder = home + 'Sensirion\\MVP test\\2017_03_09 MVPx4\\'

# Declaration of variable passed by reference
nChan = 2
nSample = 15000000
fSample = 50000
nAcquisition = 1

taskHandle = TaskHandle()
read = int32()
data = np.zeros((nChan * nSample,), dtype=np.float64)

try:

    # DAQmx Configure Code
    DAQmxCreateTask("", byref(taskHandle))
    DAQmxCreateAIVoltageChan(taskHandle, b'Dev5/ai0:1',
                             "", DAQmx_Val_Diff, 0, 5, DAQmx_Val_Volts, None)
    DAQmxCfgSampClkTiming(taskHandle, "", fSample,
                          DAQmx_Val_Rising, DAQmx_Val_FiniteSamps, nSample)

    for ii in range(nAcquisition):

        print('Taking data: ', ii + 1, ' of ', nAcquisition)

        # DAQmx Start Code
        DAQmxStartTask(taskHandle)
        DAQmxReadAnalogF64(taskHandle, nSample, nSample / fSample + 1,
                           DAQmx_Val_GroupByChannel, data, nSample * nChan, byref(read), None)
        DAQmxStopTask(taskHandle)

        data2 = data.reshape((nChan, nSample)).T

        if SaveEachData2CSV:
            np.savetxt(filefolder + 'raw data\\' +
                       clarity_libraw.str5(ii) + '.csv', data2, delimiter=',')

        if SaveEachData2NPY:
            np.save(filefolder + 'raw data\\' +
                    clarity_libraw.str5(ii) + '.npy', data2)

except DAQError as err:
    print("DAQmx Error Code: ", err.error)

finally:
    if taskHandle:
        # DAQmx Stop Code
        DAQmxClearTask(taskHandle)
