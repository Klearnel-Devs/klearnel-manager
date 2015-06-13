## @package model
#   Defines classes to be displayed by the GUI and handled by Controller
#
# @author Antoine Ceyssens <a.ceyssens@nukama.be> & Derek Van Hove <d.vanhove@nukama.be>

## Class representing Klearnel's configuration options
class Config:
    ## Dictionary containing global values
    gbl = dict(log_age=0, small=0, medium=0, large=0)
    ## Dictionary containing definitions for small files
    sma = dict(exp_def=0, backup=0, location='')
    ## Dictionary containing definitions for medium files
    med = dict(exp_def=0, backup=0, location='')
    ## Dictionary containing definitions for large files
    lrg = dict(exp_def=0, backup=0, location='')

    ## Sets the maximum log age in seconds
    # @param new The inputted log age in days
    def set_log_age(self, new):
        self.gbl['log_age'] = round(new * 86400)

    ## GETTER
    # @return  The maximum log age in days
    def get_log_age(self):
        return self.gbl['log_age'] // 86400

    ## Sets the expiration definition of a given file size in seconds
    # @param section The section in which to change the definition
    # @param new The new value in days
    def set_exp_def(self, section, new):
        if section == 'sma':
            self.sma['exp_def'] = new * 86400
        if section == 'med':
            self.med['exp_def'] = new * 86400
        if section == 'lrg':
            self.lrg['exp_def'] = new * 86400

    ## GETTER
    # @param section The section for which to get the definition
    # @return The expiration definition of a given file size in days
    def get_exp_def(self, section):
        if section == 'sma':
            return self.sma['exp_def'] // 86400
        if section == 'med':
            return self.med['exp_def'] // 86400
        if section == 'lrg':
            return self.lrg['exp_def'] // 86400

    ## Sets the size definition of a given file size in seconds
    # @param key The section in which to change the definition
    # @param value The new value in bytes
    def set_size_def(self, key, value):
        self.gbl[key] = value * pow(1024, 2)

    ## GETTER
    # @param key The key for which to get the definition
    # @return The size definition of a given file size in MB
    def get_size_def(self, key):
        return self.gbl[key] // pow(1024, 2)

    ## GETTER
    # @param section The section for which to get the definition
    # @param key The key of the key=>value pair
    # @return The formatted value requested
    def get_value(self, section, key):
        if key == 'exp_def':
            return str(self.get_exp_def(section))
        if section == 'gbl':
            if key == 'log_age':
                return str(self.get_log_age())
            else:
                return str(self.get_size_def(key))
        if section == 'sma':
            if key == 'backup':
                return bool(self.sma[key])
            return str(self.sma[key])
        if section == 'med':
            if key == 'backup':
                return bool(self.med[key])
            return str(self.med[key])
        if section == 'lrg':
            if key == 'backup':
                return bool(self.lrg[key])
            return str(self.lrg[key])

    ## GETTER
    # @param section The section for which to get the definition
    # @param key The key of the key=>value pair
    # @return The config value in bytes for Klearnel
    def get_value_res(self, section, key):
        if section == 'gbl':
            return str(self.gbl[key])
        if section == 'sma':
            return str(self.sma[key])
        if section == 'med':
            return str(self.med[key])
        if section == 'lrg':
            return str(self.lrg[key])

    ## Sets a configuration setting
    # @param section The section in which to change the definition
    # @param key The key of the key=>value pair
    # @param value The new value
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
