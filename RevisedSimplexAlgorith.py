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
                self.b = self.invB.dot(self.b)
                # f = self.Cb.T.dot(self.b)
                X = np.array([0 for _ in range(self.A.shape[1])])
                for i in range(len(self.base)):
                    X[self.base[i]] = self.b[i]
                f = self.C.T.dot(X)
                print("最优解", X)
                print("最优值", f)
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
            theta = self.b / (Xb + 1e-8)
            k = 0
            for i in range(len(theta)):
                if (Xb[i] > 0 and theta[i] < theta[k]):
                    k = i
            
            # 使用计算出的Xb计算Ekl
            Ekl = np.eye(self.A.shape[0]).astype(np.double)
            Ekl[:, k] = -1 * Xb / Xb[k]
            Ekl[k, k] = 1 / Xb[k]

            # 不更新A及b
            self.invB = Ekl.dot(self.invB)
            self.base[k] = l
            self.Cb = self.C[self.base]
        # while (True)

if __name__ == "__main__":
    A = np.array([[3, 2, 3, 1, 0], [2, 2, 3, 0, 1]]).astype(np.double)
    b = np.array([30, 40]).astype(np.double)
    C = np.array([-4, -3, -6, 0, 0]).astype(np.double)
    r = RevisedSimplex(A, b, C)
    r.Compute()