from emulators.Device import Device
from emulators.Medium import Medium
from emulators.MessageStub import MessageStub
import numpy as np


class GossipMessage(MessageStub):

    def __init__(self, sender: int, destination: int, secrets):
        super().__init__(sender, destination)
        # we use a set to keep the "secrets" here
        self.secrets = secrets

    def __str__(self):
        return f'{self.source} -> {self.destination} : {self.secrets}'


class Gossip1(Device):

    def __init__(self, index: int, number_of_devices: int, medium: Medium):
        super().__init__(index, number_of_devices, medium)
        # for this exercise we use the index as the "secret", but it could have been a new routing-table (for instance)
        # or sharing of all the public keys in a cryptographic system
        self._secrets = set([index])

    def run(self):

        number_of_devices = self.number_of_devices()

        for i in range(number_of_devices + 1):

            if (i == self.index()):
                continue

            message = GossipMessage(self.index(), i, self._secrets)
            self.medium().send(message)

            while True:
                ingoing = self.medium().receive()

                if ingoing is None:
                    break

                if len(self._secrets) == number_of_devices:
                    print(f'{self.index()} is done!')
                    return

                self._secrets.update(ingoing.secrets)

    def print_result(self):
        print(f'\tDevice {self.index()} got secrets: {self._secrets}')


"""Implement the following gossiping problem in `exercises/exercise1.py`.

A number of persons initially know one distinct secret each.

In each message, a person discloses all their secrets to the recipient.

These individuals can communicate only in pairs (no conference calls) but it is possible that different pairs of people talk concurrently. For all the tasks below you should consider the following two scenarios:

 - Scenario 1: a person may call any other person, thus the network is a total graph,
 - Scenario 2: the persons are organized in a bi-directional circle, where the each person can only pass messages to the left and the right (use the modulo operator).

In both scenarios you should use the `async` network, details of the differences between `sync` and `async` will be given in the third lecture.

Your tasks are as follows:

 - implement the above behaviour - however, with the freedom to pick which person to talk to, when to send a message, etc. 
 - Try to minimize the number of messages.
 - How few messages are enough?
 - Is your solution optimal? And in what sense?"""