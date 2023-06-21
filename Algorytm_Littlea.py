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

        self.numer_podproblemu = 0 # potrzebny do identyfikacji podproblemów


    def matrix_redux(self, macierz):
        lower_bound = 0

        for row in range(len(macierz)):
            #zredukuj wiersze
            min_element_row = min(macierz[row])
            if min_element_row == float("inf"):
                continue
            macierz[row] = macierz[row] - min_element_row
            lower_bound += min_element_row

        #zredukuj kolumny
        for col in range(len(macierz)):
            min_element_col = min(macierz[:, col])
            if min_element_col == float("inf"):
                continue
            macierz[:, col] = macierz[:, col] - min_element_col
            lower_bound += min_element_col

        return macierz, lower_bound


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


    def zabron_podcykli(self, macierz, do_wykreslenia, poprzednia_scierzka):
        flaga_zmiany = 1
        lancuch = [do_wykreslenia]

        while flaga_zmiany:
            flaga_zmiany = 0
            # kazdy element wystepuje tylko raz w lancuchu, wystarczy zate
            # sprawdzic czy da sie zwiekszyc lancuch z elementem ij
            # jezeli nie, oznacza to ze zablokowaliśmy wszystkie podcykle
            for element_dolaczany in poprzednia_scierzka:

                #dolacz na poczatek
                if lancuch[0][0] == element_dolaczany[1]:
                    flaga_zmiany = 1
                    macierz[lancuch[-1][1]][element_dolaczany[0]] = float("inf")  # zabron przejscia z konca lancucha do poczatku
                    lancuch.insert(0, element_dolaczany)

                #dolacz na koniec
                elif lancuch[-1][1] == element_dolaczany[0]:
                    flaga_zmiany = 1
                    macierz[element_dolaczany[1]][lancuch[0][0]] = float("inf")  # zabron przejscia z konca lancucha do poczatku
                    lancuch.append(element_dolaczany)

        return macierz



    def stworz_podproblem1(self, macierz, do_wykreslenia, LB, poprzednia_sciezka = None):
        wiersz_do_wykreslenia = do_wykreslenia[0]
        kolumna_do_wykreslenia = do_wykreslenia[1]

        # wykresl wiersz
        macierz[wiersz_do_wykreslenia] = [float("inf") for _ in range(len(macierz))]
        # wykresl kolumne
        macierz[:, kolumna_do_wykreslenia] = [float("inf") for _ in range(len(macierz))]
        # wykresl potencjalne podcykle
        macierz[kolumna_do_wykreslenia, wiersz_do_wykreslenia] = float("inf")
        macierz = self.zabron_podcykli(macierz, do_wykreslenia, poprzednia_sciezka)

        # zredukuj macierz, okresl nowe dolne ograniczenie, dodaj wierzcholek do sciezki
        macierz, new_LB = self.matrix_redux(macierz)
        new_LB += LB
        poprzednia_sciezka.append(do_wykreslenia)

        podproblem = PodProblem(self.numer_podproblemu, macierz, new_LB, poprzednia_sciezka)

        # zaktualizuj identyfikator podproblemow
        self.numer_podproblemu += 1

        return podproblem


    def stworz_podproblem2(self, macierz, do_wykreslenia, LB, poprzednia_sciezka = None):
        wiersz_do_wykreslenia = do_wykreslenia[0]
        kolumna_do_wykreslenia = do_wykreslenia[1]

        # zabraniamy <i*j*>
        macierz[kolumna_do_wykreslenia, wiersz_do_wykreslenia] = float("inf")

        # zredukuj macierz, okresl nowe dolne ograniczenie
        macierz, new_LB = self.matrix_redux(macierz)
        new_LB += LB

        podproblem = PodProblem(self.numer_podproblemu, macierz, new_LB, poprzednia_sciezka)
        self.numer_podproblemu += 1

        return podproblem


    def analiza(self, podproblem):

        # kryterium 1

        # kryterium 2
        if podproblem.lower_bound >= self.lower_bound_main:
            return None

        # kryterium 3
        if len(podproblem.poprzednia_scierzka) == len(self.macierz):
            # stworz rozwiazanie
            self.rozwiazanie = list({tuple(x) for x in podproblem.poprzednia_scierzka})
            self.lower_bound_main = podproblem.lower_bound
            return None

        self.lista_kandydatow.append(podproblem)


    def rozwiazanie_algorytmu(self):

        # 1) Redukcja macierzy
        self.macierz, LB = self.matrix_redux(self.macierz)

        # 2) Wyznaczenie odcinka o maksymalnym koszcie (optymistycznym) wylaczenia
        #    pozbywamy sie najmniej optymalnych wierszy i kolumn

        do_wykreslenia = self.max_cost_vertex(self.macierz)

        # 3) Podzial problemu na dwa pod problemy (PP)
        # (1) zawierajacy wybrany wierzcholek
        # (2) nie zawierajacy
        macierz1 =  self.macierz.copy()
        macierz2 =  self.macierz.copy()
        pod_probpem1 = self.stworz_podproblem1(macierz1, do_wykreslenia, LB, [])
        pod_probpem2 = self.stworz_podproblem2(macierz2, do_wykreslenia, LB, [])

        # 4) Analiza PP
        self.analiza(pod_probpem1)
        self.analiza(pod_probpem2)

        # class PodProblem:
        #     def __init__(self, identyfikator, macierz, lower_bound, poprzednia_scierzka):
        #         self.identyfikator = identyfikator
        #         self.macierz = macierz
        #         self.lower_bound = lower_bound
        #         self.poprzednia_scierzka = poprzednia_scierzka

        while self.lista_kandydatow:

            # wybiez podproblem o najmniejszej dolnej granicy
            podproblem = self.lista_kandydatow[0]
            index = 0

            for kandydat_index in range(1, len(self.lista_kandydatow)):
                if self.lista_kandydatow[kandydat_index].lower_bound < podproblem.lower_bound:
                    podproblem = self.lista_kandydatow[kandydat_index]
                    index = kandydat_index
            self.lista_kandydatow.pop(index)

            #powtarzaj algorytm
            do_wykreslenia = self.max_cost_vertex(podproblem.macierz)

            macierz1 =  podproblem.macierz.copy()
            macierz2 =  podproblem.macierz.copy()
            pod_probpem1 = self.stworz_podproblem1(macierz1, do_wykreslenia, podproblem.lower_bound, podproblem.poprzednia_scierzka)
            pod_probpem2 = self.stworz_podproblem2(macierz2, do_wykreslenia, podproblem.lower_bound, podproblem.poprzednia_scierzka)

            self.analiza(pod_probpem1)
            self.analiza(pod_probpem2)

        print(self.rozwiazanie)

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
    A = np.array([[inf, 5,    4,   6,   6,  12],
                  [8,   inf,  5,   3,   4,  5],
                  [4,   9,    inf, 3,   1,  7],
                  [9,   2,    5,   inf, 6,  3],
                  [8,   2,    7,   7,  inf, 9],
                  [2,   2,    7,   3,  13, inf]])

    
    Test = AlgorytmLittlea(A)
    Test.rozwiazanie_algorytmu()


if __name__ == '__main__':
    main()







