import numpy as np
from itertools import combinations

class RevisedSimplex:
    def __init__(self, A, b, C):
        self.A = A
        self.b = b
        self.C = C
    
    def Compute(self):
        # 选取基底
        # comb = list(combinations(range(A.shape[1]), A.shape[0]))
        # for i in comb:
        #     B = self.A[:, i]
        #     if (np.linalg.matrix_rank(B) == A.shape[0]):
        #         self.B = np.array(B)
        #         self.Cb = self.C[list(i)]
        #         self.base = list(i)
        #         break
        self.base = [3, 4]
        self.B = np.array(self.A[:, self.base])
        self.Cb = self.C[self.base]

        self.invB = np.linalg.inv(self.B)
        while (True):
            pi = self.Cb.dot(self.invB)
            omega = pi.dot(self.A) - self.C
            if (omega.max() <= 0):
                f = self.Cb.dot(self.b.T)
                print("最优解", f)
                break
            
            l = 0
            for i in range(len(omega)):
                if (omega[i] > 0):
                    l = i
                    break
            Xb = self.invB.dot(self.A[:, l])
            if (Xb.max() <= 0):
                print("无最优解")
                break
            self.A[:, l] = Xb.T
            theta = self.b / Xb
            k = 0
            for i in range(len(theta)):
                if (Xb[i] > 0 and theta[i] < theta[k]):
                    k = i
            
            Ekl = np.eye(self.A.shape[0])
            Ekl[:, k] = -1 * self.A[:, l] / self.A[k, l]
            Ekl[k, k] = 1 / self.A[k, l]

            self.invB = Ekl.dot(self.invB)
            self.base[k] = l
            self.Cb = self.C[self.base]
            self.b = self.invB.dot(self.b)
        # while (True)

if __name__ == "__main__":
    A = np.array([[3, 2, 3, 1, 0], [2, 2, 3, 0, 1]]).astype(np.double)
    b = np.array([30, 40]).astype(np.double)
    C = np.array([-4, -3, -6, 0, 0]).astype(np.double)
    r = RevisedSimplex(A, b, C)
    r.Compute()