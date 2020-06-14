"""
replica_exchange.py
written in Python3
author: C. Lockhart <chris@lockhartlab.org>

Terminology --
1. Replica
3. System
"""

import copy
import numpy as np


class ReplicaExchange:
    """
    Run replica exchange simulations.

    Examples
    --------
    >>> re = ReplicaExchange()
    >>> re += Replica(index=0)
    >>> re += Replica(index=1)
    >>> re += Exchange(mode='adjacent')
    >>> re.start(2000)
    """

    def __init__(self):
        self._replicas = {}
        self._exchanges = []

    def __add__(self, other):
        """
        Add Replica or Exchange to ReplicaExchange system.

        Parameters
        ----------
        other : Replica or Exchange
            Instance of Replica or Exchange to add.

        Returns
        -------
        ReplicaExchange
            A new instance of ReplicaExchange.
        """

        obj = copy.deepcopy(self)
        obj.add(other)
        return obj

    def add(self, other):
        """
        Add Replica or Exchange to ReplicaExchange.

        Parameters
        ----------
        other : Replica or Exchange
            Instance of Replica or Exchange.
        """

        if isinstance(other, Replica):
            self.add_replica(other)
        elif isinstance(other, Exchange):
            self.add_exchange(other)

    def add_exchange(self, exchange):
        """
        Add Exchange to ReplicaExchange.

        Parameters
        ----------
        exchange : Exchange
            Instance of Exchange
        """

        if not isinstance(exchange, Exchange):
            raise AttributeError('must be instance of Exchange')

        self._exchanges.append(exchange)

    def add_replica(self, replica):
        """
        Add Replica to ReplicaExchange.

        Parameters
        ----------
        replica : Replica
            Instance of Replica.
        """

        if not isinstance(replica, Replica):
            raise AttributeError('must be instance of Replica')

        self._replicas[replica.index] = replica

    def start(self, n_steps):
        # Determine

        #
        # for step in range(n_steps):
        #     pass

        step = np.zeros(len())
        pass

class Exchange:
    """
    Exchange dictate which replicas exchange and how.
    """

    def __init__(self):
        pass


class Replica:
    def __init__(self, index):
        self._index = index

    @property
    def index(self):
        return self._index
