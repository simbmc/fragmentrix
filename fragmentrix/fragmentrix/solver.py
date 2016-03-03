'''
Created on 26.02.2016

@author: Yingxiong
'''

def brent(f, xa, xb, ftol=1e-6, xtol=1e-8, max_iter=500, *args,  **kwargs):

    #check that the bracket's interval is sufficiently big.
    if abs(xb - xa) < xtol:
        raise ValueError

    # check lower bound
    fa = f(xa, *args, **kwargs)               # first function call
    if abs(fa) < ftol:
        return xa

    # check upper bound
    fb = f(xb, *args, **kwargs)               # second function call
    if abs(fb) < ftol:
        return xb

    # check if the root is bracketed.
    if fa * fb > 0.0:
        raise ValueError

    #xblk, fblk = 0, 0
    #spre, scur = 0, 0

    for i in range(max_iter):
        if (fa * fb) < 0:
            xblk, fblk = xa, fa
            spre = scur = xb - xa

        if abs(fblk) < abs(fb):
            xa, fa = xb, fb
            xb, fb = xblk, fblk
            xblk, fblk = xa, fa

        # Scipy's line 63.is missing.
        #tol = xtol + rtol * fabs(xb)

        sbis = (xblk - xb) / 2

        if abs(fb) < ftol:
            return xb

        if abs(sbis) < xtol:
            raise ValueError

        if abs(spre) > xtol and abs(fb) < abs(fa):
            if xa == xblk:
                # interpolate
                stry = -fb * (xb - xa) / (fb - fa)
            else:
                # extrapolate
                dpre = (fa - fb) / (xa - xb)
                dblk = (fblk - fb) / (xblk - xb)
                stry = -fb * (fblk * dblk - fa * dpre) / (dblk * dpre * (fblk - fa))
            if ((2 * abs(stry)) < min(abs(spre), 3 * abs(sbis) - xtol)):
                # good short step
                spre, scur = scur, stry
            else:
                #bisect
                spre, scur = sbis, sbis
        else:
            # bisect
            spre, scur = sbis, sbis

        xa, fa = xb, fb
        if (abs(scur) > xtol):
            xb += scur
        else:
            xb += xtol if sbis > 0 else -xtol

        fb = f(xb, *args, **kwargs)

    raise RuntimeError

if __name__ == '__main__':

    def f(x):
        '''
        here solve x for ...
        3*x**5 - 2*x**3 + 1*x - 37 = 0
        '''
        return 3*x**5 - 2*x**3 + 1*x - 37
    
    
    x_approx = 1  # rough guess
    # f refers to the function f(x)
    x = brent(f, x_approx, 100)
    print x