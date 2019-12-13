import numpy as np
from itertools import combinations
import copy
# print list(combinations([1,2,3,4,5], 3))
# class Simplex:
#     def __init__(self, A, b, c):
#         self.A = A
#         self.b = b
#         self.c = c
#         self.x = np.array([0 for _ in range(self.A.shape[1])])

#     def __updateX(self, index, xb):
#         for i in range(len(index)):
#             self.x[index[i]] = xb[i]

#     def Compute(self):
#         A_column = self.A.shape[1]
#         B_column = self.b.shape[0]
        
#         index = np.array([i for i in range(A_column - B_column, A_column)])
#         B = A[:, index]
#         while (np.linalg.matrix_rank(B) != B_column):
#             index = np.sort(np.random.choice(A_column, B_column, replace=False))
#             B = A[:, index]
#         print(B)
#         zindex = []
#         for i in range(A_column):
#             if i not in index:
#                 zindex.append(i)
#         zindex = np.array(zindex)

#         cb = self.c[index].reshape(1, B_column)
#         z = np.array([1])
#         while(max(z) > 0):
#             B_inv = np.linalg.inv(B)
#             xb = B_inv.dot(self.b)
#             self.__updateX(index, xb)
#             print("f={0}".format(self.c.T.dot(self.x)))
#             w = cb.dot(B_inv)
#             z = []
#             for i in range(len(zindex)):
#                 zi = w.dot(self.A[:, zindex[i]])
#                 zi -= self.c[zindex[i]]
#                 z.append(zi)
#             print(z)
#             z = np.array(z)
#             maxzindex = z.argmax()
#             y = B_inv.dot(self.A[:, zindex[maxzindex]])
#             b_bar = xb
#             bdy = []
#             for i in range(len(y)):
#                 if y[i] > 0:
#                     bdy.append(b_bar[i] / y[i])
#                 else:
#                     bdy.append(1e4)
#             bdy = np.array(bdy)
#             outindex = bdy.argmin()
#             self.x[maxzindex] = outindex
#             B[:, outindex] = self.A[:, maxzindex]
#             cb[0, outindex] = self.c[maxzindex]
#             zindex[zindex == maxzindex] = index[outindex]
#             index[outindex] = maxzindex
#             print(B)

class Simplex:
    def __init__(self, A, b, C):
        # 构造单纯性表
        self.table = []
        for i in range(A.shape[0]):
            row = np.array(np.append(A[i, :], b[i]))
            self.table.append(row)
        
        # 选取一个可行解
        # comb = list(combinations(range(A.shape[1]), A.shape[0]))
        # for i in comb:
        #     B = A[:, i]
        #     if (np.linalg.matrix_rank(B) == A.shape[0]):
        #         self.B = B
        #         self.Cb = C[list(i)]
        #         self.base = list(i)
        #         break
        i = [0, 3, 5]        
        B = A[:, i]
        self.B = B
        self.Cb = C[list(i)]
        self.base = list(i)

        self.invB = np.linalg.inv(self.B)
        omega = (self.Cb.dot(self.invB)).dot(A) - C
        f0 = (self.Cb.dot(self.invB)).dot(b)
        omega = np.append(omega, f0)
        self.table.append(omega)
        self.table = np.array(self.table)

        self.echo()

    def Compute(self):
        while (True):
            omega = copy.deepcopy(self.table[self.table.shape[0] - 1, 0:self.table.shape[1] - 1])
            for i in self.base:
                omega[i] = 0
            l = omega.argmax()
            if (omega[l] <= 0):
                b = self.table[0:self.table.shape[0]-1, self.table.shape[1] - 1]
                X = np.array([0 for _ in range(self.table.shape[1] - 1)])
                for i in range(len(self.base)):
                    X[self.base[i]] = b[i]
                print(X)
                print("最优值", self.table[self.table.shape[0] - 1, self.table.shape[1] - 1])
                break
            else:
                Pl = copy.deepcopy(self.table[0:self.table.shape[0]-1, l])
                if Pl.max() <= 0:
                    print("无最优解")
                else:
                    b = copy.deepcopy(self.table[0:self.table.shape[0]-1, self.table.shape[1] - 1])
                    for i in range(len(Pl)):
                        if Pl[i] <= 0:
                            Pl[i] = 1e4
                        else:
                            Pl[i] = b[i] / Pl[i]
                    k = Pl.argmin()
                    self.base[k] = l

                    akl = self.table[k, l]
                    omegakl = copy.deepcopy(self.table[self.table.shape[0] - 1, l])
                    self.table[self.table.shape[0] - 1, :] -= (self.table[k, :] / akl) * omegakl

                    self.table[k, :] /= akl
                    for r in range(len(self.table)):
                        if r != k and r != self.table.shape[0] - 1:
                            a = self.table[r, l] / self.table[k, l]
                            self.table[r, :] -= a * self.table[k, :]

            self.echo()
        # while (True)
    
    def echo(self):
        for i in self.table:
            print(i)
        print("\n")

if __name__ == "__main__":
    A = np.array([[1, 3, -1, 0, 2, 0], [0, -2, 4, 1, 0, 0], [0, -4, 3, 0, 8, 1]])
    b = np.array([7, 12, 10])
    C = np.array([0, 1, -3, 0, 2, 0])
    simplex = Simplex(A, b, C)
    simplex.Compute()
