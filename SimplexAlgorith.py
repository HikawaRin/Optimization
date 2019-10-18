import numpy as np

class Simplex:
    def __init__(self, A, b, c):
        self.A = A
        self.b = b
        self.c = c
        self.x = np.array([0 for _ in range(self.A.shape[1])])

    def __updateX(self, index, xb):
        for i in range(len(index)):
            self.x[index[i]] = xb[i]

    def Compute(self):
        A_column = self.A.shape[1]
        B_column = self.b.shape[0]
        
        index = np.array([i for i in range(A_column - B_column, A_column)])
        B = A[:, index]
        while (np.linalg.matrix_rank(B) != B_column):
            index = np.sort(np.random.choice(A_column, B_column, replace=False))
            B = A[:, index]
        print(B)
        zindex = []
        for i in range(A_column):
            if i not in index:
                zindex.append(i)
        zindex = np.array(zindex)

        cb = self.c[index].reshape(1, B_column)
        z = np.array([1])
        while(max(z) > 0):
            B_inv = np.linalg.inv(B)
            xb = B_inv.dot(self.b)
            self.__updateX(index, xb)
            print("f={0}".format(self.c.T.dot(self.x)))
            w = cb.dot(B_inv)
            z = []
            for i in range(len(zindex)):
                zi = w.dot(self.A[:, zindex[i]])
                zi -= self.c[zindex[i]]
                z.append(zi)
            print(z)
            z = np.array(z)
            maxzindex = z.argmax()
            y = B_inv.dot(self.A[:, zindex[maxzindex]])
            b_bar = xb
            bdy = []
            for i in range(len(y)):
                if y[i] > 0:
                    bdy.append(b_bar[i] / y[i])
                else:
                    bdy.append(1e4)
            bdy = np.array(bdy)
            outindex = bdy.argmin()
            self.x[maxzindex] = outindex
            B[:, outindex] = self.A[:, maxzindex]
            cb[0, outindex] = self.c[maxzindex]
            zindex[zindex == maxzindex] = index[outindex]
            index[outindex] = maxzindex
            print(B)
        

if __name__ == "__main__":
    A = np.array([[-1, 2, 1, 0, 0], [2, 3, 0, 1, 0], [1, -1, 0, 0, 1]])
    b = np.array([4, 12, 3])
    c = np.array([-4, -1, 0, 0, 0])
    simplex = Simplex(A, b, c)
    simplex.Compute()
