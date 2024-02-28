def ppm_calculator(mz:float, ppm_error):

    mz_error = ((ppm_error/1000000)*mz)

    return mz_error