#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import random

"""
1: Each individual has equal probability of having two or three links (that is, transmitting the
infection to one or two individuals).
2: Each individual has equal probability (equal to 1⁄4) of having one, two, three, or four links (that is,
of no transmitting the infection or transmitting it to one, two, or three individuals)
"""
case = 1
max_generation = 15


class Individual(object):
    """
    Clase para la creación de los objetos que modelan los individuos e la población

    :type infected: bool
    :type childs: list[Individual]
    """

    def __init__(self, infected=None):
        self.childs = []
        self.infected = infected

    def get_childs(self):
        """
        Método para generar la siguiente generación del individuo

        :return: Una lista con los descendientes del individuo
        :rtype: list[Individual]
        """
        number_childs = get_number_childs()

        for count in range(0, number_childs):
            self.childs.append(Individual(False))

        for count in range(0, get_number_childs_infecteds(number_childs)):
            self.childs[count].infected = True

        return self.childs


class Generation(object):
    """
    Clase para modelar la genración creada en cada iteración y que contendrá una lista de individuos

    :type individuals: list[Individual]
    """

    def __init__(self):
        self.individuals = []

    def get_new_generation(self):
        """
        Método que permite obtener una nueva generación a partir de la existente

        :return: Un nuevo objeto generación con la lista de los individuos.
        :rtype: Generation
        """
        new_generation = Generation()
        for individual in self.individuals:
            new_generation.individuals.extend(individual.get_childs())
        return new_generation

    def get_total_individuals(self):
        return len(self.individuals)

    def get_total_infected(self):
        total = 0
        for individual in self.individuals:
            if individual.infected:
                total = total + 1
        return total


class Population(object):
    """
    :type generations: list[Generation]
    """

    def __init__(self):
        self.generations = []

    def update(self):

        if self.get_generation_number() == -1:
            generation = Generation()
            generation.individuals.append(Individual(True))
            self.generations.append(generation)
            return

        current_generation = self.get_current_generation()
        new_generation = current_generation.get_new_generation()

        self.generations.append(new_generation)

    def get_generation_number(self):
        return len(self.generations) - 1

    def get_current_generation(self):
        return self.generations[self.get_generation_number()]

    def get_total_individuals(self):
        total = 0
        for generation in self.generations:
            total = total + generation.get_total_individuals()
        return total

    def get_total_infected(self):
        total = 0
        for generation in self.generations:
            total = total + generation.get_total_infected()
        return total


def get_number_childs():
    if case == 1:
        return random.randint(1, 3)
    else:
        return random.randint(0, 4)


def get_number_childs_infecteds(childs):
    return random.randint(0, childs)


def main():
    population = Population()
    while population.get_generation_number() < max_generation:
        population.update()
        partial_output(population)
    total_output(population)


def partial_output(population):
    print str(
        "Generación: {generation}\tIndividuos: {total_persons}\tInfectados: {infecteds}\t({ratio}%)".format(
            generation=population.get_generation_number(),
            total_persons=population.get_current_generation().get_total_individuals(),
            infecteds=population.get_current_generation().get_total_infected(),
            ratio=int(100 * population.get_current_generation().get_total_infected() /
                      population.get_current_generation().get_total_individuals())
        )
    )


def total_output(population):
    print "============================================================================="
    print str(
        "Total de individuos: {total_persons} - Total de infectados: {total_infected}".format(
            total_persons=population.get_total_individuals(),
            total_infected=population.get_total_infected()
        )
    )

    print
    print ("Run <python Infection.py --help> para más ayuda")


def get_system_arguments():
    parser = argparse.ArgumentParser(prog='Infection.py',
                                     usage='Programa para simulacion de infecciones',
                                     description=str('Este programa corre un algoritmo para simular la propagación de '
                                                     'un virus.'),
                                     )
    parser.add_argument('--version', action='version', version='infection 1.0',
                        help='Muestra la version del programa y sale.')
    parser.add_argument('--max-gen', type=int, default=15,
                        help='El número de iteraciones (generaciones) del simulador (default: 1)')
    parser.add_argument('--case', type=int, default=1,
                        help='El número de caso contemplado. (default: 1)')
    args = parser.parse_args()

    return vars(args)


if __name__ == "__main__":
    options_dict = get_system_arguments()
    case = options_dict.get('case')
    max_generation = options_dict.get('max_gen')
    main()
