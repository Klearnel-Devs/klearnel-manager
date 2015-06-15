## @package controller
#   Handles communication between Klearnel & Klearnel Manager
#
# @author Antoine Ceyssens <a.ceyssens@nukama.be> & Derek Van Hove <d.vanhove@nukama.be>
from controller.Networker import Networker
from model.ScanElem import ScanElem
from model.QrElem import QrElem
from model.Exceptions import *
from controller import Active
from socket import SHUT_RDWR
import socket

## DEFINES CODE FOR KLEARNEL EXIT
KL_EXIT = -1
## DEFINES CODE FOR ADDING ITEM TO KLEARNEL'S QUARANTINE
QR_ADD = 1
## DEFINES CODE FOR REMOVING ITEM FROM KLEARNEL'S QUARANTINE
QR_RM = 2
## DEFINES CODE FOR RESTORING ITEM FROM KLEARNEL'S QUARANTINE
QR_REST = 3
## DEFINES CODE FOR RETRIEVING KLEARNEL'S QUARANTINE LIST
QR_LIST = 4
## DEFINES CODE FOR GETTING KLEARNEL'S QUARANTINE INFO
QR_INFO = 5
## DEFINES CODE FOR REMOVING ALL ITEMS IN KLEARNEL'S QUARANTINE
QR_RM_ALL = 6
## DEFINES CODE FOR RESTORING ALL ITEMS IN KLEARNEL'S QUARANTINE
QR_REST_ALL = 7
## DEFINES CODE FOR ADDING ITEM TO KLEARNEL'S SCANNER
SCAN_ADD = 10
## DEFINES CODE FOR REMOVING ITEM FROM KLEARNEL'S SCANNER
SCAN_RM = 11
## DEFINES CODE FOR GETTING KLEARNEL'S SCANNER LIST
SCAN_LIST = 12
## DEFINES CODE FOR MODIFYING AN ELEMENT'S SCAN OPTIONS
SCAN_MOD = 13
## DEFINES CODE FOR GETTING KLEARNEL'S CONFIGURATION SETTINGS
CONF_LIST = 20
## DEFINES CODE FOR MODIFYING KLEARNEL'S CONFIGURATION SETTINGS
CONF_MOD = 21
## DEFINES CODE FOR AUTHENTIFYING WITH KLEARNEL
NET_CONNEC = 30

## Superclass that handles data between Klearnel & Klearnel Manager
class Tasker:
    ## Method that sends identifying credentials to Klearnel
    # @param net Networker instance
    # @param client The client concerning communication
    # @throws ConnectionRefusedError
    def send_credentials(self, net, client):
        net.send_val(client.token)
        if net.get_ack() != net.SOCK_ACK:
            raise ConnectionRefusedError("Error on token negociation")
        net.send_val(client.password)

        if net.get_ack() != net.SOCK_ACK:
            raise ConnectionRefusedError("Error on root password negociation")

## Subclass of Tasker for Klearnel host control
class TaskGlobal(Tasker):

    ## NOT YET IMPLEMENTED
    def get_monitor_info(self):
        pass

    ## NOT YET IMPLEMENTED
    def stop_klearnel(self):
        pass

    ## NOT YET IMPLEMENTED
    def restart_klearnel(self):
        pass

## Subclass of Tasker to handle all Scanner related communication
class TaskScan(Tasker):
    ## Adds an element to Klearnel's scanner list
    # @param client The host on which to connect
    # @param new_elem The new scanner item
    # @exception ConnectionRefusedError
    # @exception ConnectionError
    # @exception NoConnectivity
    # @throws ScanException
    def add_to_scan(self, client, new_elem):
        net = Networker()
        try:
            net.connect_to(client.name)
            self.send_credentials(net, client)
            net.send_val(str(SCAN_ADD) + ":" + str(len(new_elem.path)))
            net.send_val(new_elem.path)
            net.send_val(new_elem.get_options())

            net.send_val(str(len(str(new_elem.back_limit_size))))
            net.send_val(str(new_elem.back_limit_size))

            net.send_val(str(len(str(new_elem.del_limit_size))))
            net.send_val(str(new_elem.del_limit_size))

            net.send_val(str(new_elem.is_temp))

            net.send_val(str(len(str(new_elem.max_age))))
            net.send_val(str(new_elem.max_age))

        except ConnectionRefusedError:
            raise ScanException("Unable to authentify with " + client.name)
        except ConnectionError:
            raise ScanException("Unable to add " + new_elem.path + "\nto scanner on " + client.name)
        except NoConnectivity:
            raise ScanException("Unable to connect to " + client.name)
        finally:
            try:
                net.s.shutdown(SHUT_RDWR)
                net.s.close()
            except socket.error:
                pass

    ## Modifies a scanner element in Klearnel's Scanner Watchlist
    # @param client The client on which to connect
    # @param path The path of the scanner element
    # @param options The modified options
    # @param tmp Boolean determining whether item is a temp folder
    # @exception ConnectionRefusedError
    # @exception ConnectionError
    # @exception NoConnectivity
    # @throws ScanException
    def mod_from_scan(self, client, path, options, tmp):
        net = Networker()
        try:
            net.connect_to(client.name)
            self.send_credentials(net, client)
            net.send_val(str(SCAN_MOD) + ":" + str(len(path)))
            net.send_val(path)
            net.send_val(options)
            net.send_val(str(tmp))
        except ConnectionRefusedError:
            raise ScanException("Unable to authentify with " + client.name)
        except ConnectionError:
            raise ScanException("Unable to change options for " + path +
                                "\n from scanner on " + client.name)
        except NoConnectivity:
            raise ScanException("Unable to connect to " + client.name)
        finally:
            try:
                net.s.shutdown(SHUT_RDWR)
                net.s.close()
            except socket.error:
                pass

    ## Removes an item from Klearnels scanner watchlist
    # @param client The client on which to connect
    # @param path The scanner elements path
    # @exception ConnectionRefusedError
    # @exception ConnectionError
    # @exception NoConnectivity
    # @throws ScanException
    def rm_from_scan(self, client, path):
        net = Networker()
        try:
            net.connect_to(client.name)
            self.send_credentials(net, client)
            net.send_val(str(SCAN_RM) + ":" + str(len(path)))
            net.send_val(path)
        except ConnectionRefusedError:
            raise ScanException("Unable to authentify with " + client.name)
        except ConnectionError:
            raise ScanException("Unable to remove " + path + " from scanner on " + client.name)
        except NoConnectivity:
            raise ScanException("Unable to connect to " + client.name)
        finally:
            try:
                net.s.shutdown(SHUT_RDWR)
                net.s.close()
            except socket.error:
                pass

    ## Asks and receives the Scanner Watchlist from Klearnel
    # @param client The client on which to connect
    # @exception ConnectionRefusedError
    # @exception ConnectionError
    # @exception NoConnectivity
    # @exception EmptyListException Raised if received list is empty
    # @throws ScanException
    # @return scan_list The new scanner list from Klearnel
    def get_scan_list(self, client):
        net = Networker()
        scan_list = list()
        try:
            net.connect_to(client.name)
            self.send_credentials(net, client)
            net.send_val(str(SCAN_LIST) + ":0")
            result = None
            i = 0
            while result != "EOF":
                size = net.get_data(20)
                net.send_ack(net.SOCK_ACK)
                if size == "EOF":
                    if i is 0:
                        raise EmptyListException("Scanner List is Empty")
                    else:
                        break
                result = net.get_data(int(size))
                scan_elem = ScanElem(result)
                net.send_ack(net.SOCK_ACK)
                size = net.get_data(20)
                net.send_ack(net.SOCK_ACK)
                result = net.get_data(int(size))
                scan_elem.set_options(result)
                net.send_ack(net.SOCK_ACK)
                size = net.get_data(20)
                net.send_ack(net.SOCK_ACK)
                result = net.get_data(int(size))
                scan_elem.back_limit_size = result
                net.send_ack(net.SOCK_ACK)

                size = net.get_data(20)
                net.send_ack(net.SOCK_ACK)
                result = net.get_data(int(size))
                scan_elem.del_limit_size = result
                net.send_ack(net.SOCK_ACK)

                size = net.get_data(20)
                net.send_ack(net.SOCK_ACK)
                result = net.get_data(int(size))
                scan_elem.is_temp = result
                net.send_ack(net.SOCK_ACK)

                size = net.get_data(20)
                net.send_ack(net.SOCK_ACK)
                result = net.get_data(int(size))
                scan_elem.max_age = result
                net.send_ack(net.SOCK_ACK)

                scan_list.append(scan_elem)
                i += 1
        except ConnectionRefusedError:
            raise ScanException("Unable to authentify with " + client.name)
        except NoConnectivity:
            raise ScanException("Unable to connect to " + client.name)
        except ConnectionError:
            raise ScanException("Unable to get list from scanner on " + client.name)
        finally:
            try:
                net.s.shutdown(SHUT_RDWR)
                net.s.close()
            except socket.error:
                pass
        return scan_list

## Subclass of Tasker for Quarantine operations
class TaskQR(Tasker):
    ## Adds an element to Klearnel's QR List
    # @param client The host on which to connect
    # @param path The new quarantine file path
    # @exception ConnectionRefusedError
    # @exception ConnectionError
    # @exception NoConnectivity
    # @throws QrException
    def add_to_qr(self, client, path):
        net = Networker()
        try:
            net.connect_to(client.name)
            self.send_credentials(net, client)
            net.send_val(str(QR_ADD) + ":" + str(len(path)))
            net.send_val(path)
        except NoConnectivity:
            raise QrException("Unable to connect to " + client.name)
        except ConnectionRefusedError:
            raise QrException("Unable to authentify with " + client.name)
        except ConnectionError:
            raise QrException("Unable to add " + path + " to quarantine on " + client.name)
        finally:
            try:
                net.s.shutdown(SHUT_RDWR)
                net.s.close()
            except socket.error:
                pass

    ## Removes an item from Klearnels quarantine list
    # @param client The client on which to connect
    # @param filename The file to remove
    # @exception ConnectionRefusedError
    # @exception ConnectionError
    # @exception NoConnectivity
    # @throws QrException
    def rm_from_qr(self, client, filename):
        net = Networker()
        try:
            net.connect_to(client.name)
            self.send_credentials(net, client)
            net.send_val(str(QR_RM) + ":" + str(len(filename)))
            net.send_val(filename)
        except NoConnectivity:
            raise QrException("Unable to connect to " + client.name)
        except ConnectionRefusedError:
            raise QrException("Unable to authentify with " + client.name)
        except ConnectionError:
            raise QrException("Unable to remove " + filename + " from quarantine on " + client.name)
        finally:
            try:
                net.s.shutdown(SHUT_RDWR)
                net.s.close()
            except socket.error:
                pass

    ## Restores an item from Klearnels quarantine list
    # @param client The client on which to connect
    # @param filename The file to restore
    # @exception ConnectionRefusedError
    # @exception ConnectionError
    # @exception NoConnectivity
    # @throws QrException
    def restore_from_qr(self, client, filename):
        net = Networker()
        try:
            net.connect_to(client.name)
            self.send_credentials(net, client)
            net.send_val(str(QR_REST) + ":" + str(len(filename)))
            net.send_val(filename)
        except NoConnectivity:
            raise QrException("Unable to connect to " + client.name)
        except ConnectionRefusedError:
            raise QrException("Unable to authentify with " + client.name)
        except ConnectionError:
            raise QrException("Unable to restore " + filename + " from quarantine on " + client.name)
        finally:
            try:
                net.s.shutdown(SHUT_RDWR)
                net.s.close()
            except socket.error:
                pass

    ## Asks and receives the Quarantine list from Klearnel
    # @param client The client on which to connect
    # @exception ConnectionRefusedError
    # @exception ConnectionError
    # @exception NoConnectivity
    # @exception EmptyListException Raised if received list is empty
    # @throws QrException
    # @return qr_list The new quarantine list
    def get_qr_list(self, client):
        net = Networker()
        qr_list = list()
        try:
            net.connect_to(client.name)
            self.send_credentials(net, client)
            net.send_val(str(QR_LIST) + ":0")
            result = None
            i = 0
            while result != "EOF":
                size = net.get_data(20)
                net.send_ack(net.SOCK_ACK)
                if size == "EOF":
                    if i is 0:
                        raise EmptyListException("Quarantine List is Empty")
                    else:
                        break
                result = net.get_data(int(size))
                qr_elem = QrElem(result)
                net.send_ack(net.SOCK_ACK)

                size = net.get_data(20)
                net.send_ack(net.SOCK_ACK)
                result = net.get_data(int(size))
                qr_elem.o_path = result
                net.send_ack(net.SOCK_ACK)

                size = net.get_data(20)
                net.send_ack(net.SOCK_ACK)
                result = net.get_data(int(size))
                qr_elem.d_begin = result
                net.send_ack(net.SOCK_ACK)

                size = net.get_data(20)
                net.send_ack(net.SOCK_ACK)
                result = net.get_data(int(size))
                qr_elem.d_expire = result
                net.send_ack(net.SOCK_ACK)

                qr_list.append(qr_elem)
                i += 1

        except NoConnectivity:
            raise QrException("Unable to connect to " + client.name)
        except ConnectionRefusedError:
            raise QrException("Unable to authentify with " + client.name)
        except ConnectionError:
            raise QrException("Unable to get list from quarantine on " + client.name)
        finally:
            try:
                net.s.shutdown(SHUT_RDWR)
                net.s.close()
            except socket.error:
                pass

        return qr_list

    ## NOT YET IMPLEMENTED
    def get_qr_info(self):
        pass

    ## Removes all items from Klearnel's Quarantine List
    # @param client The client on which to connect
    # @exception ConnectionRefusedError
    # @exception ConnectionError
    # @exception NoConnectivity
    # @throws QrException
    def rm_all_from_qr(self, client):
        net = Networker()
        try:
            net.connect_to(client.name)
            self.send_credentials(net, client)
            net.send_val(str(QR_RM_ALL) + ":0")
        except ConnectionError:
            raise Exception("Unable to remove all elements in the quarantine on " + client.name)
        except ConnectionRefusedError:
            raise QrException("Unable to authentify with " + client.name)
        except NoConnectivity:
            raise QrException("Unable to connect to " + client.name)
        finally:
            try:
                net.s.shutdown(SHUT_RDWR)
                net.s.close()
            except socket.error:
                pass

    ## Restores all files in Klearnel's Quarantine list
    # @param client The client on which to connect
    # @exception ConnectionRefusedError
    # @exception ConnectionError
    # @exception NoConnectivity
    # @throws QrException
    def restore_all_from_qr(self, client):
        net = Networker()
        try:
            net.connect_to(client.name)
            self.send_credentials(net, client)
            net.send_val(str(QR_REST_ALL) + ":0")
        except NoConnectivity:
            raise QrException("Unable to connect to " + client.name)
        except ConnectionRefusedError:
            raise QrException("Unable to authentify with " + client.name)
        except ConnectionError:
            raise Exception("Unable to restore all elements from the quarantine on " + client.name)
        finally:
            try:
                net.s.shutdown(SHUT_RDWR)
                net.s.close()
            except socket.error:
                pass

## Subclass of Tasker for handling configuration communications
class TaskConfig(Tasker):
    ## Asks & Receives Klearnel's configuration parameters
    # @param client The client on which to connect
    # @exception ConnectionRefusedError
    # @exception ConnectionError
    # @exception NoConnectivity
    # @throws ConfigException
    def get_config(self, client):
        net = Networker()
        try:
            net.connect_to(client.name)
            self.send_credentials(net, client)
            net.send_val(str(CONF_LIST) + ":0")

            size = net.get_data(20)
            net.send_ack(net.SOCK_ACK)
            result = net.get_data(int(size))
            Active.confList.gbl['log_age'] = int(result)
            net.send_ack(net.SOCK_ACK)

            size = net.get_data(20)
            net.send_ack(net.SOCK_ACK)
            result = net.get_data(int(size))
            Active.confList.gbl['small'] = int(result)
            net.send_ack(net.SOCK_ACK)

            size = net.get_data(20)
            net.send_ack(net.SOCK_ACK)
            result = net.get_data(int(size))
            Active.confList.gbl['medium'] = int(result)
            net.send_ack(net.SOCK_ACK)

            size = net.get_data(20)
            net.send_ack(net.SOCK_ACK)
            result = net.get_data(int(size))
            Active.confList.gbl['large'] = int(result)
            net.send_ack(net.SOCK_ACK)

            size = net.get_data(20)
            net.send_ack(net.SOCK_ACK)
            result = net.get_data(int(size))
            Active.confList.sma['exp_def'] = int(result)
            net.send_ack(net.SOCK_ACK)

            size = net.get_data(20)
            net.send_ack(net.SOCK_ACK)
            result = net.get_data(int(size))
            Active.confList.sma['backup'] = int(result)
            net.send_ack(net.SOCK_ACK)

            size = net.get_data(20)
            net.send_ack(net.SOCK_ACK)
            result = net.get_data(int(size))
            Active.confList.sma['location'] = result
            net.send_ack(net.SOCK_ACK)

            size = net.get_data(20)
            net.send_ack(net.SOCK_ACK)
            result = net.get_data(int(size))
            Active.confList.med['exp_def'] = int(result)
            net.send_ack(net.SOCK_ACK)

            size = net.get_data(20)
            net.send_ack(net.SOCK_ACK)
            result = net.get_data(int(size))
            Active.confList.med['backup'] = int(result)
            net.send_ack(net.SOCK_ACK)

            size = net.get_data(20)
            net.send_ack(net.SOCK_ACK)
            result = net.get_data(int(size))
            Active.confList.med['location'] = result
            net.send_ack(net.SOCK_ACK)

            size = net.get_data(20)
            net.send_ack(net.SOCK_ACK)
            result = net.get_data(int(size))
            Active.confList.lrg['exp_def'] = int(result)
            net.send_ack(net.SOCK_ACK)

            size = net.get_data(20)
            net.send_ack(net.SOCK_ACK)
            result = net.get_data(int(size))
            Active.confList.lrg['backup'] = int(result)
            net.send_ack(net.SOCK_ACK)

            size = net.get_data(20)
            net.send_ack(net.SOCK_ACK)
            result = net.get_data(int(size))
            Active.confList.lrg['location'] = result
            net.send_ack(net.SOCK_ACK)
        except NoConnectivity:
            raise ConfigException("Unable to connect to " + client.name)
        except ConnectionRefusedError:
            raise ConfigException("Unable to authentify with " + client.name)
        except ConnectionError:
            raise ConfigException("Unable to get configurations from " + client.name)
        finally:
            try:
                net.s.shutdown(SHUT_RDWR)
                net.s.close()
            except socket.error:
                pass

    ## Sends modifications of Klearnel's configuration settings
    # @param client The client on which to connect
    # @param section The section in which the key value pair are contained
    # @param key The key on which to change its value
    # @param new_value The new setting
    # @exception ConnectionRefusedError
    # @exception ConnectionError
    # @exception NoConnectivity
    # @throws ConfigException
    def send_conf_mod(self, client, section, key, new_value):
        net = Networker()
        try:
            net.connect_to(client.name)
            self.send_credentials(net, client)
            if section is 'gbl':
                section = 'global'
            elif section is 'sma':
                section = 'small'
            elif section is 'med':
                section = 'medium'
            elif section is 'lrg':
                section = 'large'
            net.send_val(str(CONF_MOD) + ":0")
            net.send_val(str(len(section)))
            net.send_val(section)
            net.send_val(str(len(key)))
            net.send_val(key)
            net.send_val(str(len(new_value)))
            net.send_val(new_value)
            if net.get_ack() != net.SOCK_ACK:
                raise ConnectionError("Operation canceled")
        except ConnectionRefusedError:
            raise ConfigException("Unable to authentify with " + client.name)
        except NoConnectivity:
            raise ConfigException("Unable to connect to " + client.name)
        except ConnectionError:
            raise ConfigException("Unable to modify "+key+" with: "+new_value)
        finally:
            try:
                net.s.shutdown(SHUT_RDWR)
                net.s.close()
            except socket.error:
                pass

