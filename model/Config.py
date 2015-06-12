__author__ = 'Derek'

class Config:
    gbl = dict(log_age=0, small=0, medium=0, large=0)
    sma = dict(exp_def=0, backup=0, location='')
    med = dict(exp_def=0, backup=0, location='')
    lrg = dict(exp_def=0, backup=0, location='')

    def set_log_age(self, new):
        self.gbl['log_age'] = round(new * 86400)

    def get_log_age(self):
        return self.gbl['log_age'] // 86400

    def set_exp_def(self, section, new):
        if section == 'sma':
            self.sma['exp_def'] = new * 86400
        if section == 'med':
            self.med['exp_def'] = new * 86400
        if section == 'lrg':
            self.lrg['exp_def'] = new * 86400

    def get_exp_def(self, section):
        if section == 'sma':
            return self.sma['exp_def'] // 86400
        if section == 'med':
            return self.med['exp_def'] // 86400
        if section == 'lrg':
            return self.lrg['exp_def'] // 86400

    def set_size_def(self, key, value):
        self.gbl[key] = value * pow(1024, 2)

    def get_size_def(self, key):
        return self.gbl[key] // pow(1024, 2)

    def get_value(self, section, entry):
        if entry == 'exp_def':
            return str(self.get_exp_def(section))
        if section == 'gbl':
            if entry == 'log_age':
                return str(self.get_log_age())
            else:
                return str(self.get_size_def(entry))
        if section == 'sma':
            if entry == 'backup':
                return bool(self.sma[entry])
            return str(self.sma[entry])
        if section == 'med':
            if entry == 'backup':
                return bool(self.med[entry])
            return str(self.med[entry])
        if section == 'lrg':
            if entry == 'backup':
                return bool(self.lrg[entry])
            return str(self.lrg[entry])

    def get_value_res(self, section, entry):
        if section == 'gbl':
            return str(self.gbl[entry])
        if section == 'sma':
            return str(self.sma[entry])
        if section == 'med':
            return str(self.med[entry])
        if section == 'lrg':
            return str(self.lrg[entry])

    def set_config(self, section, key, value):
        if key == 'exp_def':
            self.set_exp_def(section, int(value))
        if section == 'gbl':
            if key == 'log_age':
                self.set_log_age(int(value))
            else:
                self.set_size_def(key, int(value))
        if section == 'sma':
            if key == 'backup':
                self.sma[key] = value
            else:
                self.sma[key] = str(value)
        if section == 'med':
            if key == 'backup':
                self.med[key] = value
            else:
                self.med[key] = str(value)
        if section == 'lrg':
            if key == 'backup':
                self.lrg[key] = value
            else:
                self.lrg[key] = str(value)

if __name__ == '__main__':
    cfg = Config()
    print(cfg.gbl['log_age'])