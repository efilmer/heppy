'''Compute the event variable M3'''

from heppy.framework.analyzer import Analyzer
from heppy.particles.tlv.resonance import Resonance 

import pprint 
import itertools

class M3Builder(Analyzer):
    '''Computes the event variable M3
    
    Example::
    
      m3builder = cfg.Analyzer(
         M3Builder,
         instance_label = 'm3'
         jets = 'jets'
      )
    
    All combinations of 3 jets are tested to retain
    the one with highest pT (transverse momentum of the 3-jet system).
    This combination of three jets is used to build an "M3" particle,
    with the pdgid of the top quark. 
    
    @param jets: input collection of jets.
    @param instance_label: label for a particular instance of the m3builder.
      used as a name to store in the event the output M3 particle.
    '''
    
    def process(self, event):
        '''Process the event.
        
        The event must contain:
         - self.cfg_ana.jets : the input collection of jets
         
        This method creates:
         - event.<self.instance_label> : output M3 particle
        '''
        jets = getattr(event, self.cfg_ana.jets)

        m3 = None
        pt3max=0
        seljets=None
        #print jets

        if len(jets)>=3:
            for l in list(itertools.permutations(jets,3)):
                #ntag=sum([l[0].tags['b'],l[1].tags['b'],l[2].tags['b']])
                pt3=(l[0].p4()+l[1].p4()+l[2].p4()).Pt()
                if pt3>pt3max:
                    ptmax=pt3
                    seljets=l

            top_pdgid = 6
            m3 = Resonance(seljets, top_pdgid)
        setattr(event, self.instance_label, m3)



