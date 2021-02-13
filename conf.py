import re
import os
import copy

class Config:
    def __init__(self):
        f = open('/home/pi/PiMule/data/menu.conf')
        conf = self.load_conf(f.readlines())
        conf = self.fix_dirs(conf)
        conf = self.fix_missing(conf)
        self.conf = self.fix_empty(conf)
        f.close()

    def load_conf(self, lines):
        conf = {}
        current_conf = {}
        current_system = ''
        for line in lines:
            if(line.startswith('[')):
                if current_system != '':
                    conf[current_system] = current_conf
                    conf[current_system]['inherited'] = False
                current_conf = {}
                current_system = self.clean_label_string(line)

            if line.startswith('#') or line.find('=') == -1:
                continue
                
            line = self.clean_string(line)
            conf_line = line.split('=')
            try:
                current_conf[conf_line[0]] = int(conf_line[1])
            except ValueError:
                if conf_line[1].startswith('('):
                    current_conf[conf_line[0]] = self.get_color_tuple(conf_line[1])
                elif conf_line[1].startswith('['):
                    current_conf[conf_line[0]] = self.get_command_list(conf_line[1])
                else:
                    current_conf[conf_line[0]] = conf_line[1]
        conf[current_system] = current_conf
        conf[current_system]['inherited'] = False
        return conf

    def fix_dirs(self, conf):
        root_dir = conf['root']['dir']
        for key in conf:
            if key == 'root':
                continue
            
            print(conf[key])
            conf[key]['dir'] = os.path.join(root_dir, conf[key]['dir'])
        return conf
            
    def fix_missing(self, conf):
        mall = conf['root']
        for key in conf:
            if key == 'root':
                continue
            for inner_key in mall:
                if inner_key not in conf[key]:
                    conf[key][inner_key] = mall[inner_key]
        return conf
    
    # If all folders but one are empty, the one that isn't empty becomes the root folder
    def fix_empty(self, conf):
        print('fixing empty!')
        tmp_conf = {}
        for key in conf:
            print('checking ' + key)
            if key == 'root':
                print('skipping')
                continue
            nr_of_files = 0
            print('traversing ' + conf[key]['dir'])
            for dir, dirnames, filenames in os.walk(conf[key]['dir']):
                print('found ' + str(len(filenames)) + ' files in ' + key)
                nr_of_files += len(filenames)
            print('found ' + str(nr_of_files) + ' files')
            if nr_of_files > 0:
                tmp_conf[key] = conf[key]
        
        new_conf = {}
        if len(tmp_conf) == 1:
            new_conf['root'] = tmp_conf[next(iter(tmp_conf))]
        else:
            new_conf = conf
            
        return new_conf
            
    def clean_string(self, str):
        return re.sub('[\r\n]', '', str)
        
    def clean_label_string(self, str):
        return re.sub('[\[\]\r\n]', '', str)
        
    def get_color_tuple(self, str):
        str = str.replace('(', '').replace(')', '')
        parts = str.split(',')
        tuple = (int(parts[0]), int(parts[1]), int(parts[2]))
        return tuple
    
    def get_command_list(self, str):
        str = str.replace('[', '').replace(']', '')
        if str == '':
            return []
        parts = str.split(',')
	
        return parts
        
    def get_conf_for_dir(self, dir):
        for key in self.conf:
            if self.conf[key]['dir'] == dir:
                return self.conf[key]
        
        ret = copy.deepcopy(self.get_conf_for_dir(os.path.abspath(os.path.dirname(dir))))
        if ret['dir'] != dir:
            ret['dir'] = dir
            ret['inherited'] = True
        return ret
    
    def get_conf_for_label(self, label):
        if label in self.conf:
            return self.conf[label]
        else:
            return self.conf['root']
        
if __name__ == "__main__":
    c = Config()