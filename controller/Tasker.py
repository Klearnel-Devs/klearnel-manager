__author__ = 'antoine'
from controller.Networker import Networker
from model.ScanElem import ScanElem
from model.QrElem import QrElem
from model.Exceptions import *
from controller import Active

KL_EXIT = -1
QR_ADD = 1
QR_RM = 2
QR_REST = 3
QR_LIST = 4
QR_INFO = 5
QR_RM_ALL = 6
QR_REST_ALL = 7
QR_LIST_RECALL = 8
SCAN_ADD = 10
SCAN_RM = 11
SCAN_LIST = 12
SCAN_MOD = 13
CONF_LIST = 20
CONF_MOD = 21
NET_CONNEC = 30


class Tasker:
    def send_credentials(self, net, client):
        net.send_val(client.token)
        if net.get_ack() != net.SOCK_ACK:
            raise ConnectionRefusedError("Error on token negociation")
        net.send_val(client.password)

        if net.get_ack() != net.SOCK_ACK:
            raise ConnectionRefusedError("Error on root password negociation")


class TaskGlobal(Tasker):
    def get_monitor_info(self):
        pass

    def stop_klearnel(self):
        pass

    def restart_klearnel(self):
        pass


class TaskScan(Tasker):
    def add_to_scan(self, client, new_elem):
        net = Networker()
        try:
            net.connect_to(client.name)
        except NoConnectivity:
            raise ScanException("Unable to connect to " + client.name)
        try:
            self.send_credentials(net, client)
        except ConnectionRefusedError:
            raise ScanException("Unable to authentify with " + client.name)
            net.s.close()
        try:
            net.send_val(str(SCAN_ADD) + ":" + str(len(new_elem.path)))
            net.send_val(new_elem.path)
            net.send_val(new_elem.get_options())
            net.send_val(str(len(str(new_elem.back_limit_size))))
            print(str(len(str(new_elem.back_limit_size))))
            net.send_val(new_elem.back_limit_size)
            print(str(new_elem.back_limit_size))
            net.send_val(len(str(new_elem.del_limit_size)))
            print(str(len(str(new_elem.del_limit_size))))
            net.send_val(new_elem.del_limit_size)
            print(str(new_elem.del_limit_size))
            net.send_val(new_elem.is_temp)
            net.send_val(len(str(new_elem.max_age)))
            print(str(len(str(new_elem.max_age))))
            net.send_val(new_elem.max_age)
            print(str(new_elem.max_age))
        except ConnectionError:
            raise ScanException("Unable to add " + new_elem.path + "\nto scanner on " + client.name)
        finally:
            net.s.close()

    def mod_from_scan(self, client, path, options):
        net = Networker()
        try:
            net.connect_to(client.name)
        except NoConnectivity:
            raise ScanException("Unable to connect to " + client.name)
        try:
            self.send_credentials(net, client)
        except ConnectionRefusedError:
            raise ScanException("Unable to authentify with " + client.name)
            net.s.close()
        try:
            net.send_val(str(SCAN_MOD) + ":" + str(len(new_elem.path)))
            net.send_val(new_elem.path)
            net.send_val(new_elem.get_options())
            net.send_val(new_elem.is_temp)
        except ConnectionError:
            raise ScanException("Unable to change options for " + path +
                            "\n from scanner on " + client.name)
        finally:
            net.s.close()


    def rm_from_scan(self, client, path):
        net = Networker()
        try:
            net.connect_to(client.name)
        except NoConnectivity:
            raise ScanException("Unable to connect to " + client.name)
        try:
            self.send_credentials(net, client)
        except ConnectionRefusedError:
            raise ScanException("Unable to authentify with " + client.name)
            net.s.close()
        try:
            net.send_val(str(SCAN_RM) + ":" + str(len(path)))
            net.send_val(path)
        except ConnectionError:
            raise ScanException("Unable to remove " + path + " from scanner on " + client.name)
        finally:
            net.s.close()

    def get_scan_list(self, client):
        print("Getting scan list")
        net = Networker()
        print("1")
        try:
            net.connect_to(client.name)
            print("2")
        except NoConnectivity:
            raise ScanException("Unable to connect to " + client.name)
        try:
            self.send_credentials(net, client)
            print("3")
        except ConnectionRefusedError:
            raise ScanException("Unable to authentify with " + client.name)
            net.s.close()
        print("4")
        scan_list = list()
        try:
            print(str(SCAN_LIST) + ":0")
            net.send_val(str(SCAN_LIST) + ":0")
            print(str(SCAN_LIST) + ":0")
            print("5")
            result = None
            i = 0
            while result != "EOF":
                print("6")
                size = net.get_data(20)
                net.send_ack(net.SOCK_ACK)
                if size == "EOF":
                    break
                print("7")
                result = net.get_data(int(size))
                scan_elem = ScanElem(result)
                print("8")
                net.send_ack(net.SOCK_ACK)
                print("Getting Options")
                size = net.get_data(20)
                net.send_ack(net.SOCK_ACK)
                result = net.get_data(int(size))
                scan_elem.set_options(result)
                net.send_ack(net.SOCK_ACK)
                print("Got Options : " + str(result))
                size = net.get_data(20)
                net.send_ack(net.SOCK_ACK)
                result = net.get_data(int(size))
                scan_elem.back_limit_size = result
                print(str(result))
                net.send_ack(net.SOCK_ACK)

                size = net.get_data(20)
                net.send_ack(net.SOCK_ACK)
                result = net.get_data(int(size))
                scan_elem.del_limit_size = result
                print(str(result))
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
                print(str(result))
                net.send_ack(net.SOCK_ACK)

                scan_list.append(scan_elem)
                i += 1

        except ConnectionError:
            raise ScanException("Unable to get list from scanner on " + client.name)
        finally:
            net.s.close()
        print("Got scan list")
        return scan_list


class TaskQR(Tasker):
    def add_to_qr(self, client, path):
        net = Networker()
        try:
            net.connect_to(client.name)
        except NoConnectivity:
            raise QrException("Unable to connect to " + client.name)
        try:
            self.send_credentials(net, client)
        except ConnectionRefusedError:
            raise QrException("Unable to authentify with " + client.name)
            net.s.close()
        try:
            net.send_val(str(QR_ADD) + ":" + str(len(path)))
            net.send_val(path)
        except ConnectionError:
            # net.s.close()
            raise QrException("Unable to add " + path + " to quarantine on " + client.name)
        finally:
            net.s.close()

    def rm_from_qr(self, client, filename):
        net = Networker()
        try:
            net.connect_to(client.name)
        except NoConnectivity:
            raise QrException("Unable to connect to " + client.name)
        try:
            self.send_credentials(net, client)
        except ConnectionRefusedError:
            raise QrException("Unable to authentify with " + client.name)
            net.s.close()
        try:
            net.send_val(str(QR_RM) + ":" + str(len(filename)))
            net.send_val(filename)
        except ConnectionError:
            raise QrException("Unable to remove " + filename + " from quarantine on " + client.name)
        finally:
            net.s.close()

    def restore_from_qr(self, client, filename):
        net = Networker()
        try:
            net.connect_to(client.name)
        except NoConnectivity:
            raise QrException("Unable to connect to " + client.name)
        try:
            self.send_credentials(net, client)
        except ConnectionRefusedError:
            raise QrException("Unable to authentify with " + client.name)
            net.s.close()
        try:
            net.send_val(str(QR_REST) + ":" + str(len(filename)))
            net.send_val(filename)
        except ConnectionError:
            raise QrException("Unable to restore " + filename + " from quarantine on " + client.name)
        finally:
            net.s.close()

    def get_qr_list(self, client):
        net = Networker()
        try:
            net.connect_to(client.name)
        except NoConnectivity:
            raise QrException("Unable to connect to " + client.name)
        try:
            self.send_credentials(net, client)
        except ConnectionRefusedError:
            raise QrException("Unable to authentify with " + client.name)
            net.s.close()
        qr_list = list()
        try:
            net.send_val(str(QR_LIST) + ":0")
            result = None
            i = 0
            while result != "EOF":
                size = net.get_data(20)
                net.send_ack(net.SOCK_ACK)
                if size == "EOF":
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

        except ConnectionError:
            raise QrException("Unable to get list from quarantine on " + client.name)
        finally:
            net.s.close()

        return qr_list

    def get_qr_info(self):
        pass

    def rm_all_from_qr(self, client):
        net = Networker()
        try:
            net.connect_to(client.name)
        except NoConnectivity:
            raise QrException("Unable to connect to " + client.name)
        try:
            self.send_credentials(net, client)
        except ConnectionRefusedError:
            raise QrException("Unable to authentify with " + client.name)
            net.s.close()
        try:
            net.send_val(str(QR_RM_ALL) + ":0")
        except ConnectionError:
            raise Exception("Unable to remove all elements in the quarantine on " + client.name)
        finally:
            net.s.close()

    def restore_all_from_qr(self, client):
        net = Networker()
        try:
            net.connect_to(client.name)
        except NoConnectivity:
            raise QrException("Unable to connect to " + client.name)
        try:
            self.send_credentials(net, client)
        except ConnectionRefusedError:
            raise QrException("Unable to authentify with " + client.name)
            net.s.close()
        try:
            net.send_val(str(QR_REST_ALL) + ":0")
        except ConnectionError:
            raise Exception("Unable to restore all elements from the quarantine on " + client.name)
        finally:
            net.s.close()


class TaskConfig(Tasker):
    def get_config(self, client):
        net = Networker()
        net.connect_to(client.name)
        self.send_credentials(net, client)
        try:
            net.send_val(str(CONF_LIST) + ":0")

            size = net.get_data(20)
            net.send_ack(net.SOCK_ACK)
            result = net.get_data(int(size))
            Active.confList.set_log_age(int(result))
            net.send_ack(net.SOCK_ACK)

            size = net.get_data(20)
            net.send_ack(net.SOCK_ACK)
            result = net.get_data(int(size))
            Active.confList.set_size_def("small", int(result))
            net.send_ack(net.SOCK_ACK)

            size = net.get_data(20)
            net.send_ack(net.SOCK_ACK)
            result = net.get_data(int(size))
            Active.confList.set_size_def("medium", int(result))
            net.send_ack(net.SOCK_ACK)

            size = net.get_data(20)
            net.send_ack(net.SOCK_ACK)
            result = net.get_data(int(size))
            Active.confList.set_size_def("large", int(result))
            net.send_ack(net.SOCK_ACK)

            size = net.get_data(20)
            net.send_ack(net.SOCK_ACK)
            result = net.get_data(int(size))
            Active.confList.set_exp_def("sma", int(result))
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
            Active.confList.set_exp_def("med", int(result))
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
            Active.confList.set_exp_def("lrg", int(result))
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

        except ConnectionError:
            raise ConfigException("Unable to get configurations from " + client.name)
        finally:
            net.s.close()

    def send_conf_mod(self, client, section, key, new_value):
        net = Networker()
        try:
            net.connect_to(client.name)
        except NoConnectivity:
            raise ConfigException("Unable to connect to " + client.name)
        try:
            self.send_credentials(net, client)
        except ConnectionRefusedError:
            raise ConfigException("Unable to authentify with " + client.name)
            net.s.close()
        try:
            net.send_val(str(CONF_MOD) + ":0")
            net.send_val(str(len(section)))
            net.send_val(section)
            net.send_val(str(len(key)))
            net.send_val(key)
            net.send_val(str(len(new_value)))
            net.send_val(new_value)
            if net.get_ack() != net.SOCK_ACK:
                raise ConnectionError("Operation canceled")
        except ConnectionError:
            raise ConfigException("Unable to modify "+key+" with: "+new_value)
        finally:
            net.s.close()

if __name__ == "__main__":
    from model.Client import Client, ClientList
    from model.Config import Config
    from controller import Active
    Active.cl = ClientList()
    Active.confList = Config()
    Active.cl.load_list()
    conf_task = TaskConfig()
    conf_task.get_config(Active.cl.c_list[0])
    print("Value of SMALL -> Location: "+Active.confList.sma['location'])
