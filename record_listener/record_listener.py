import random
import copy
import math
import numpy as np
import scipy as sp
import cyclus
from cyclus.agents import Agent, Facility
from cyclus import lib
import cyclus.typesystem as ts


class record_listener(Facility):
    f33_file = ts.String(
        doc="f33_filename",
        tooltip="tooltip",
        uilabel='label')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def enter_notify(self):
        super().enter_notify()
        lib.TIME_SERIES_LISTENERS['depletion_history'].append(self.listen)
        self.depl_history = []

    def tick(self):
        print('TICK', self.context.time)
        t = [ 1, 2, 3, 4, 5, 6, 7, 5, 9, 10]
        p = [ 11, 12, 13, 14, 15, 16, 17, 15, 19 , 20]
        t_ = t[self.context.time]
        p_ = p[self.context.time]
        begin_comp = {'u235': t_, 'u238': 100-t_}
        print(t_, p_)

        end_comp = self.check_existing_history(t_, p_, begin_comp)
        if end_comp == 0:
            print('Do depletion')
            end_comp = {'cs137': t_, 'u238': 100-t_}
            self.record(t[self.context.time], p[self.context.time],
                        begin_comp, end_comp)

        print('TICK END\n\n')



    def check_existing_history(self, t_, p_, begin_comp):
        print('Checking existing history for time', self.context.time)
        for i in self.depl_history:
            q = i.split(',')
            print(q)
            entry_dict = {'f33_file': q[0],
                          't': int(q[1]),
                          'p': float(q[2]),
                          'begin_comp': self.comp_entry_to_dict(q[3]),
                          'end_comp': self.comp_entry_to_dict(q[4])
                          }
            print(entry_dict)
            print(t_, p_, begin_comp)
            cat1 = (entry_dict['f33_file'] == self.f33_file)
            cat2 = (entry_dict['t'] == t_)
            cat3 = (entry_dict['p'] == p_)
            cat4 = (entry_dict['begin_comp'] == begin_comp)

            if cat1 and cat2 and cat3 and cat4:
                # already exists
                print('=====================')
                print('=====================')
                print('=====================')
                print('Already Exists!')
                print('=====================')
                print('=====================')
                print('=====================')

                end_comp = entry_dict['end_comp']

                return end_comp

        # if nothing is found:
        return 0



    def comp_entry_to_dict(self, s):
        """ Converts entery iso1:frac1;iso2:frac2;iso3:frac3...
            to dict
        """
        x = s.split(';')
        iso = [q.split(':')[0] for q in x]
        val = [q.split(':')[1] for q in x]
        return {k:float(v) for k,v in zip(iso, val)}

    def listen(self, agent, time, value, commod):
        print('Agent')
        print(agent)
        print('time')
        print(time)
        print('value')
        print(value)
        self.depl_history.append(value)


    def record(self, time, power, begin_comp, end_comp):
        # records hash of [f33_file, begincomphash, time, power, endcomphas]
        l = [self.f33_file, str(time), str(power)]
        
        # boc:
        """
        boc = l + ['boc']
        print(boc)
        for iso, frac in begin_comp.items():
            row = boc + [str(iso), str(frac)]
            lib.record_time_series('depletion_history', self, ','.join(row))
        eoc = l + ['eoc']
        print(eoc)
        for iso, frac in end_comp.items():
            row = eoc + [str(iso), str(frac)]
            lib.record_time_series('depletion_history', self, ','.join(row))
        """
        s = ','.join(l) + ','
        for iso, frac in begin_comp.items():
            s += str(iso) + ':' + str(frac) + ';'
        s = s[:-1] + ','
        for iso, frac in end_comp.items():
            s += str(iso) + ':' + str(frac) + ';'
        s = s[:-1]
        print(s)
        lib.record_time_series('depletion_history', self, s)
         
        print('done')
