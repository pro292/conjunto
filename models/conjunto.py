from random import sample, randint, choice


class conjunto:

    def __init__(self, cant_elementos = None, elementos = None):
        if cant_elementos and elementos is None:
            self.cant_elementos = cant_elementos
            self.elementos = [None] * self.cant_elementos
            self.__elementos_random(self.cant_elementos)
            self.__ordenar_conjunto()
        elif cant_elementos and elementos is not None:
            if len(elementos) == cant_elementos:
                self.cant_elementos = cant_elementos
                self.elementos = elementos
                self.__eliminar_repetidos()
                self.__ordenar_conjunto()
            else:
                raise ValueError("La cantidad de elementos no coincide con 'cant_elementos'")
        elif (cant_elementos is None and elementos is None) or (cant_elementos == 0 and elementos == [] or elementos == [None]):# si no se pasa nada por parametro se crea un conjunto vacio
            self.cant_elementos = 0
            self.elementos = []
        elif cant_elementos is None and elementos is not None:
            self.elementos = elementos
            self.cant_elementos = len(elementos)

    # para cargarlo en un json, pasa los atributos de conjunto para cargarlos despues en el html
    def to_dict(self):
        return {
            'elementos': self.elementos,
            'cant_elementos': self.cant_elementos
        }
            
    def conjunto_vacio(self):
        if self.cant_elementos == 0 or self.cant_elementos == None:
            return True
        else:
            return False   

    ##### Metodos publicos

    # adicina un elemento al conjunto, si el elemento ya existe no lo agrega
    def adicionar_elemento(self, elem):
        if self.conjunto_vacio():
            self.elementos = [elem]
            self.cant_elementos = 1
        else:
            if not self.pertenece(elem):
                self.elementos = self.elementos + [elem]
                self.cant_elementos += 1
                self.__ordenar_conjunto()
            else:
                print("El elemento ya existe en el conjunto")

    # elimina el primer elemento del conjunto pasado por parametro
    def eliminar_elemento(self, elem):
        encontrado = False
        if not self.conjunto_vacio():
            if self.pertenece(elem):
                nueva_lista = [None] * (self.cant_elementos - 1)
                i = 0
                j = 0
                while i < self.cant_elementos:
                    if self.elementos[i] != elem and not encontrado:
                        nueva_lista[j] = self.elementos[i]
                        j += 1
                    elif self.elementos[i] != elem and encontrado:
                        nueva_lista[j] = self.elementos[i]
                        j += 1
                    elif self.elementos[i] == elem and not encontrado:
                        encontrado = True
                    elif self.elementos[i] == elem and encontrado:
                        nueva_lista[j] = self.elementos[i]
                        j += 1
                    i += 1
                self.cant_elementos = len(nueva_lista)
                self.elementos = nueva_lista
            else:
                print("Elemento no encontrado")
        else:
            print("El conjunto está vacío")                     

    def pertenece(self, elem):
        if self.conjunto_vacio():
            #print("El conjunto está vacío")
            return False
        else:
            for i in range(0, self.cant_elementos):
                if self.elementos[i] == elem:
                    return True
                    break
            return False

    # devuelve true si el conjunto pasado por parametro contiene otros conjuntos
    # si este no cotiene ni un conjunto dentro de el devuelve false
    # si esta mezclado devuelve los subindices de los que no son conjuntos. ej: [1, 2, 3, [4, 5], 6] -> [0, 1, 2, 4]
    def conjunto_de_conjuntos(self):
        if self.conjunto_vacio():
            #print("El conjunto está vacío")
            return False
        else:
            subindices = []
            k = 0
            for i in range(0, self.cant_elementos):
                if type(self.elementos[i]) == list:
                    k += 1
                elif type(self.elementos[i]) != list:
                    subindices = subindices + [i]
            if k == self.cant_elementos:
                return True
            elif k == 0:
                return False
            else:
                return subindices

    # devuelve true si es un conjunto de numeros o letras
    def es_conjunto(self):
        if self.conjunto_vacio():
            return True
        subindices = []           
        i = 0
        for i in range(0, self.cant_elementos):
            if type(self.elementos[i]) == int or type(self.elementos[i]) in range(65, 91) or type(self.elementos[i]) in range(97, 123):
                subindices = subindices + [i]
        if len(subindices) == self.cant_elementos:
            return True
        else:
            return False

    def union(self, conjunto2):
        if self.conjunto_de_conjuntos() == True or conjunto2.conjunto_de_conjuntos() == True:
            return None
        elif self.conjunto_de_conjuntos() == False and conjunto2.conjunto_de_conjuntos() == False:
            conjunto_union = conjunto()
            if self.conjunto_vacio() and conjunto2.conjunto_vacio():
                return conjunto_union
            for elementos in self.elementos:
                conjunto_union.adicionar_elemento(elementos)
            for elementos in conjunto2.elementos:
                conjunto_union.adicionar_elemento(elementos)
            return conjunto_union

    def interseccion(self, conjunto2):
        if self.conjunto_de_conjuntos() == True or conjunto2.conjunto_de_conjuntos() == True:
            return None
        if self.conjunto_de_conjuntos() == False:           
            conjunto_interseccion = conjunto()
            if self.cant_elementos >= conjunto2.cant_elementos:
                for elementos in self.elementos:
                    if conjunto2.pertenece(elementos):
                        conjunto_interseccion.adicionar_elemento(elementos)
                return conjunto_interseccion # o self.elementos = conjunto_union.elementos y self.cant_elementos = conjunto_union.cant_elementos
            else:
                for elementos in conjunto2.elementos:
                    if self.pertenece(elementos):
                        conjunto_interseccion.adicionar_elemento(elementos)
                return conjunto_interseccion
        else:
            return None
    
    def diferencia(self, conjunto2):
        if self.conjunto_de_conjuntos() == True or conjunto2.conjunto_de_conjuntos() == True:
            return None
        elif self.conjunto_de_conjuntos() == False and conjunto2.conjunto_de_conjuntos() == False:
            conjunto_diferencia = conjunto()
            for elementos in self.elementos:
                if elementos not in conjunto2.elementos:
                    conjunto_diferencia.adicionar_elemento(elementos)
            return conjunto_diferencia
        else:
            return None

    def diferencia_simetrica(self, conjunto2):
        if self.conjunto_de_conjuntos() == True or conjunto2.conjunto_de_conjuntos() == True:
            return None
        elif self.conjunto_de_conjuntos() == False and conjunto2.conjunto_de_conjuntos() == False:
            diferencia_conj1 = conjunto()
            diferencia_conj2 = conjunto()
            diferencia_conj1 = self.diferencia(conjunto2)
            diferencia_conj2 = conjunto2.diferencia(self)
            return diferencia_conj1.union(diferencia_conj2)

    # devuelve true si self es subconjunto de conjunto2
    def subconjunto(self, conjunto2):
        if self.conjunto_de_conjuntos() == True or conjunto2.conjunto_de_conjuntos() == True:
            return None
        elif self.conjunto_de_conjuntos() == False and conjunto2.conjunto_de_conjuntos() == False:
            if self.conjunto_vacio() and conjunto2.conjunto_vacio():
                return True
            elif self.cant_elementos > conjunto2.cant_elementos:
                return False
            else:
                i = 0
                for elementos in self.elementos:
                    if elementos in conjunto2.elementos:
                        i += 1
                if i == self.cant_elementos:
                    return True
                else:
                    return False

    def superconjunto(self,conjunto2):
        if self.conjunto_de_conjuntos() == True or conjunto2.conjunto_de_conjuntos() == True:
            return None
        elif self.conjunto_de_conjuntos() == False and conjunto2.conjunto_de_conjuntos() == False:
            if self.conjunto_vacio() and conjunto2.conjunto_vacio():
                return True
            elif self.cant_elementos < conjunto2.cant_elementos:
                return False
            else:
                return conjunto2.subconjunto(self)


    ##### Metodos privados

    # genera de manera aleatoria los elementos del conjunto, que pueden ser enteros o letras
    # estos mismo no se repetiran
    def __elementos_random(self, n):
        tipo = ["entero", "letra"]
        rango_num = range(0, 1000)
        rango_letra = range(97, 123)
        length = randint(1, 26)   # longitud maxima, dado que el maximo de letras es 26, aunque es posible hacerlo mas grande para los numeros
        aleatorio = choice(tipo)
        #aleatorio =    tipo[randint(0, 1)]
        if aleatorio == "entero":
            self.elementos = sample(rango_num, length)
            self.cant_elementos = len(self.elementos)
        elif aleatorio == "letra":
            self.elementos = [chr(x) for x in sample(rango_letra, length)]
            self.cant_elementos = len(self.elementos)

    # elimina los elementos repetidos del conjunto, ya que un conjunto no puede tener elementos repetidos
    def __eliminar_repetidos(self):
        if not self.conjunto_vacio():
            if self.__elemento_repetido():
                lista_aux = self.__elementos_repetidos()
                nueva_lista = []
                i = 0
                repetidor = 0
                for elements in self.elementos:
                    if elements not in nueva_lista:
                        nueva_lista = nueva_lista + [elements]
            
                self.elementos = nueva_lista[:]
                self.cant_elementos = len(nueva_lista)
            
    # identifica si hay por lo menos un elemento repetido
    def __elemento_repetido(self):
        if self.conjunto_vacio():
            return False
            #print("El conjunto está vacío")
        else:
            nueva_lista = self.elementos[:]
            rep = 0
            i = 0
            j = 0
            for j in range(0, self.cant_elementos):
                for i in range(0, self.cant_elementos):
                    if nueva_lista[j] == self.elementos[i]:
                        rep += 1
                        if rep > 1:
                            return True
                            break  # se detiene cuando se encuentra al menos un elemento repetido 
                rep = 0
            if rep == 0:
                return False
            

    # devuelve los elementos repetidos del conjunto en formato de lista de listas
    # la clave es el elemento y el valor es la cantidad de veces que se repite
    # ej: [1, 2, 2, 1, 2] -> [[1, 2], [2, 3]]
    def __elementos_repetidos(self):
        if self.conjunto_vacio():
            print("El conjunto está vacío")
            return None
        else:
            nueva_lista = self.elementos[:]
            lista_aux = []
            elem_rep = []
            key = None
            value = 0
            i = 0
            j = 0
            m = 0
            for j in range(0, self.cant_elementos):
                for i in range(0, self.cant_elementos):
                    key = nueva_lista[j]
                    if nueva_lista[j] == self.elementos[i]:
                        value += 1
                if value > 1:
                    lista_aux = [key, value]
                    if lista_aux not in elem_rep and (m < 1 or not (lista_aux in elem_rep)):
                        elem_rep = elem_rep + [lista_aux]
                lista_aux = []
                value = 0
                key = None
        if elem_rep:
            return elem_rep
        else:
            print("No hay elementos repetidos")
            return None
            
    def __ordenar_conjunto(self):
        if not self.conjunto_vacio():
            if self.__elemento_repetido():
                self.__eliminar_repetidos()
            numeros = []
            letras = []
            for elem in self.elementos:
                if type(elem) == int:
                    numeros = numeros + [elem]
                elif type(elem) == str and len(elem) == 1:
                    letras = letras + [elem]
            numeros.sort()
            letras.sort()
            self.elementos = numeros[:] + letras[:]

h = conjunto(4, ['a','b','c','d'])
k = conjunto(2, ['c','z'])
print(h.interseccion(k).elementos)
# recordatorio: en el fronted, mas especificamente en los input, no permitir que se ingresen palabras
# ni combinacion de letras con numero o letras con letras, etc, solo numeros o letras