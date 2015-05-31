__author__ = 'Derek'
from kivy.properties import NumericProperty, StringProperty, BooleanProperty,\
    ListProperty

class Config:
    gbl = dict(log_age=30, small=1, medium=10, large=100)
    sma = dict(exp_def=30, backup=1, location='/home/nuccah/Documents/Backup')
    med = dict(exp_def=30, backup=0, location='No Location Specified')
    lrg = dict(exp_def=30, backup=1, location='/home/nuccah/Documents/Backup')

    def get_log_age(self, new):
        self.gbl['log_age'] = round(new * 86400)

    def set_log_age(self):
        return self.gbl['log_age'] // 86400

    def set_exp_def(self, section, new):
        if section == 'sma':
            return self.sma['exp_def'] // 86400
        if section == 'med':
            return self.med['exp_def'] // 86400
        if section == 'lrg':
            return self.lrg['exp_def'] // 86400

    def get_exp_def(self, section):
        if section == 'sma':
            return self.sma['exp_def'] * 86400
        if section == 'med':
            return self.med['exp_def'] * 86400
        if section == 'lrg':
            return self.lrg['exp_def'] * 86400

    def set_size_def(self, key):
        return self.gbl[key] // 1024

    def get_size_def(self, key):
        return self.gbl[key] * 1024

    def get_value(self, section, entry):
        if section == 'gbl':
            return format(self.gbl[entry])
        if section == 'sma':
            if entry == 'backup':
                return bool(self.sma[entry])
            return format(self.sma[entry])
        if section == 'med':
            if entry == 'backup':
                return bool(self.med[entry])
            return format(self.med[entry])
        if section == 'lrg':
            if entry == 'backup':
                return bool(self.lrg[entry])
            return format(self.lrg[entry])

if __name__ == '__main__':
    cfg = Config()
    print(cfg.gbl['log_age'])