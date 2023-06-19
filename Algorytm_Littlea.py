#Algorytm wegierski

import numpy as np


class PodProblem:
    def __init__(self, identyfikator, macierz, lower_bound, poprzednia_scierzka):
        self.identyfikator = identyfikator
        self.macierz = macierz
        self.lower_bound = lower_bound
        self.poprzednia_scierzka = poprzednia_scierzka


class AlgorytmLittlea:
    def __init__(self, macierz):
        self.macierz = macierz

        self.lower_bound_main = float("inf") # pierwsze rozwiazanie wyznacza wartosc LB
        self.lista_kandydatow = []
        self.rozwiazanie = []

    def matrix_redux(self):
        for row in range(len(self.macierz)):
            #zredukuj wiersze
            min_element_row = min(self.macierz[row])
            self.macierz[row] = self.macierz[row] - min_element_row
            self.lower_bound_main += min_element_row

        #zredukuj kolumny
        for col in range(len(self.macierz)):
            min_element_col = min(self.macierz[:, col])
            self.macierz[:, col] = self.macierz[:, col] - min_element_col
            self.lower_bound_main += min_element_col


    def max_cost_vertex(self, macierz):
        wierzcholek_ij = [None, None] #[row, col]
        max_cost = -1

        # sprawdz wszystkie wieszchoki dla ktorych koszt przejscia = 0
        for row_index, row in enumerate(macierz):
            for col_index, element in enumerate(row):

                if element == 0:
                    copy_row = macierz[row_index].copy()
                    copy_col = macierz[:, col_index].copy()
                    min_row = np.delete(copy_row, col_index)
                    min_col = np.delete(copy_col, row_index)

                    new_cost = min(min_row) + min(min_col)
                    if new_cost > max_cost:
                        wierzcholek_ij = [row_index, col_index]
                        max_cost = new_cost

        return wierzcholek_ij


    def rozwiazanieAlgorytmu(self):

        # 1) Redukcja macierzy i wyznaczenie LB
        self.matrix_redux()

        # 2) Wyznaczenie odcinka o maksymalnym koszcie (optymistycznym) wylaczenia
        #    pozbywamy sie najmniej optymalnych wierszy i kolumn
        do_wykreslenia = self.max_cost_vertex(self.macierz)

        # 3) Podzial problemu na dwa pod problemy (PP)
        # 3.1 zawierajacy wybrany wierzcholek
        # 3.2 nie zawierajacy



        # while True:



def main():
    # A = np.array([[5, 2, 3, 2, 7],
    #               [6, 8, 4, 2, 5],
    #               [6, 4, 3, 7, 2],
    #               [6, 9, 0, 4, 0],
    #               [4, 1, 2, 4, 0]])
    # A = np.array([[3, 1, 3, 3, 3, 6],
    #             [6, 2, 2, 3, 2, 4],
    #             [7, 8, 9, 5, 6, 1],
    #             [3, 8, 5, 8, 7, 2],
    #             [9, 6, 1, 1, 6, 5],
    #             [9, 6, 1, 8, 9, 6]])

    inf = float("inf")
    A = np.array([[inf, 5,    4,   6,   6],
                  [8,   inf,  5,   3,   4],
                  [4,   3,    inf, 3,   1],
                  [8,   2,    5,   inf, 6],
                  [2,   2,    7,   0,  inf]])

    
    Test = AlgorytmLittlea(A)
    Test.rozwiazanieAlgorytmu()


if __name__ == '__main__':
    main()







