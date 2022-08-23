import re

from anadet.dataSearcher import DataSearcher
from anadet.detector import Detector, DetectorProps, SourceProps
import yaml

class DetectorManager:
    def __init__(self):
        self.detectors = dict()
        self.state = {}
        self.dataSearcher = DataSearcher()
        self.meta_info = dict()


    def appendResults(self, filename):
        """
        filename the name of the file with legit .csv results data from Geant4
        """
        # looking for energy info in full filename
        src_props = None
        energy_list = self.dataSearcher.lookingForEnergyInfo(filename)
        # preority to the last found energy info (closer to the file by the dir tree)
        if energy_list:
            energy = energy_list[-1]['energy']
            energy_unit = energy_list[-1]['energy_unit']
            src_props = SourceProps(energy, energy_unit)
        else:
            pass # TODO - try to find info in meta file
        if not src_props:
            print(f"WARNING: can't find energy for filename {filename}")
            # TODO - scenario with unknown source energy

        # looking for num of histories
        nhists = self.dataSearcher.lookingForNhists(filename)
        if not nhists:
            pass # TODO - no nhists in filename, maybe search in meta of doesn't matter
        # looking for det params
        det_name, hist_type, det_type, det_quantity, det_num = self.dataSearcher.lookingForDetNameInfo(filename)
        det_props = DetectorProps(src_props)
        det_props.quantity = det_quantity
        det_props.num = str(det_num)
        det_props.tags.extend([det_type]) # tags is an array

        key_name = Detector.createName(det_props)
        if key_name not in self.detectors:
            self.detectors[key_name] = Detector(det_props)
        
        # Now we have detector in the self.detectors list
        self.detectors[key_name].appendResult(filename)

    def readMeta(self, meta_filename):
        loaded_data = None
        with open(meta_filename, 'r') as stream:
            loaded_data = yaml.safe_load(stream)
        return {}
