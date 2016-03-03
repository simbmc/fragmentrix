'''
Created on 26.02.2016

@author: Yingxiong
'''
import numpy as np
from solver import brent

class SCTT:
    
    Em = 25e3 #matrix modulus 
    Ef = 180e3 #fiber modulus
    vf = 0.01 #reinforcement ratio
    T = 12. #bond intensity
    sig_cu = 18. #[MPa]
    x = np.linspace(0, 1000, 1000) #specimen discretization
    sig_mu_x = np.linspace(3.0, 4.5, 1000) #matrix strength field
                            
    def cb(self, z, sig_c): #Eq.(3) and Eq. (9)
        sig_m = np.minimum(z * self.T * self.vf / (1 - self.vf), self.Em*sig_c/(self.vf*self.Ef + (1-self.vf)*self.Em)) #matrix stress
        esp_f = (sig_c-sig_m) / self.vf / self.Ef #reinforcement strain
        return  sig_m, esp_f
    
    @staticmethod
    def get_z_x(x, XK): #Eq.(5)
        z_grid = np.abs(x[:, np.newaxis] - np.array(XK)[np.newaxis, :])
        return np.amin(z_grid, axis=1)
    
    def get_lambda_z(self, sig_mu, z):
        fun = lambda sig_c: sig_mu - self.cb(z, sig_c)[0]
        try: # search for the local crack load level 
            return brent(fun, 0, self.sig_cu)
        except: # solution not found (shielded zone) return the ultimate composite stress
            return self.sig_cu
    
    def get_sig_c_K(self, z_x):
        get_lambda_x = np.vectorize(self.get_lambda_z)
        lambda_x = get_lambda_x(self.sig_mu_x, z_x) #Eq. (6)
        y_idx = np.argmin(lambda_x) #Eq. (7) and Eq.(8)
        return lambda_x[y_idx], self.x[y_idx]
    
    cracking_history = [0, 0, 0]

    def get_cracking_history(self):
        XK = [0.] #position of the first crack
        sig_c_K = [0., 3.0]
        eps_c_K = [0., 3.0/(self.vf*self.Ef + (1-self.vf)*self.Em)]
        sig_m_K = []
        sig_c_k = 0.
        while sig_c_k < self.sig_cu:
            z_x = self.get_z_x(self.x, XK)
            sig_c_k, y_i = self.get_sig_c_K(z_x)
            #if sig_c_k == self.sig_cu: break
            XK.append(y_i)
            sig_c_K.append(sig_c_k)
            sig_m, eps_f = self.cb(self.get_z_x(self.x, XK), sig_c_k)
            sig_m_K.append(sig_m)
            eps_c_K.append(np.trapz(eps_f, self.x)/1000.) #Eq. (10)
        #sig_c_K.append(self.sig_cu)
        #eps_c_K.append(np.trapz(self.cb(self.get_z_x(self.x, XK), self.sig_cu)[1], self.x)/1000.)
        self.cracking_history = [sig_c_K, eps_c_K, sig_m_K]
    
    @property
    def sig_m_K(self):
        return self.cracking_history[2]
    
    @property
    def sig_c_K(self):
        return self.cracking_history[0]

    @property
    def eps_c_K(self):
        return self.cracking_history[1]
        
    # for visualization of the crack bridge
    z = np.linspace(-50, 50, 201)
    sig_m_cb = None
    def get_sig_m_cb(self):
        self.sig_m_cb = self.cb(np.abs(self.z), 100.)[0]
        
if __name__ == '__main__':
    
    s = SCTT()
    s.get_cracking_history()
    print s.sig_c_K
