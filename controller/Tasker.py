__author__ = 'antoine'
from controller.Networker import Networker
from model.Client import ClientList
from model.ScanElem import ScanElem
from model.QrElem import QrElem
from model.Exceptions import ScanException, QrException

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
SCAN_OPTIONS = 11


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
        net.connect_to(client.name)
        self.send_credentials(net, client)
        try:
            net.send_val(str(SCAN_ADD) + ":" + str(len(new_elem.path)))
            net.send_val(new_elem.path)
            net.send_val(new_elem.get_options())
            net.send_val(str(len(new_elem.back_limit_size)))
            net.send_val(new_elem.back_limit_size)
            net.send_val(str(len(new_elem.del_limit_size)))
            net.send_val(new_elem.del_limit_size)
            net.send_val(new_elem.is_temp)
            net.send_val(str(len(new_elem.max_age)))
            net.send_val(new_elem.max_age)
        except ConnectionError:
            raise ScanException("Unable to add " + new_elem.path + " to scanner on " + client.name)
        finally:
            net.s.close()

    def rm_from_scan(self, client, path):
        net = Networker()
        net.connect_to(client.name)
        self.send_credentials(net, client)
        try:
            net.send_val(str(SCAN_RM) + ":" + str(len(path)))
            net.send_val(path)
        except ConnectionError:
            raise Exception("Unable to remove " + path + " from scanner on " + client.name)
        finally:
            net.s.close()

    def get_scan_list(self, client):
        net = Networker()
        net.connect_to(client.name)
        self.send_credentials(net, client)
        scan_list = list()
        try:
            net.send_val(str(SCAN_LIST) + ":0")
            result = None
            i = 0
            while result != "EOF":
                size = net.get_data(20)
                net.send_ack(net.SOCK_ACK)
                if size == "EOF":
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

        except ConnectionError:
            raise ScanException("Unable to get list from scanner on " + client.name)
        finally:
            net.s.close()
        return scan_list


class TaskQR(Tasker):
    def add_to_qr(self, client, path):
        net = Networker()
        net.connect_to(client.name)
        self.send_credentials(net, client)
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
        net.connect_to(client.name)
        self.send_credentials(net, client)
        try:
            net.send_val(str(QR_RM) + ":" + str(len(filename)))
            net.send_val(filename)
        except ConnectionError:
            raise Exception("Unable to remove " + filename + " from quarantine on " + client.name)
        finally:
            net.s.close()

    def restore_from_qr(self, client, filename):
        net = Networker()
        net.connect_to(client.name)
        self.send_credentials(net, client)
        try:
            net.send_val(str(QR_REST) + ":" + str(len(filename)))
            net.send_val(filename)
        except ConnectionError:
            raise Exception("Unable to restore " + filename + " from quarantine on " + client.name)
        finally:
            net.s.close()

    def get_qr_list(self, client):
        net = Networker()
        net.connect_to(client.name)
        self.send_credentials(net, client)
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
            raise Exception("Unable to get list from quarantine on " + client.name)
        finally:
            net.s.close()

        return qr_list

    def get_qr_info(self):
        pass

    def rm_all_from_qr(self, client):
        net = Networker()
        net.connect_to(client.name)
        self.send_credentials(net, client)
        try:
            net.send_val(str(QR_RM_ALL) + ":0")
        except ConnectionError:
            raise Exception("Unable to remove all elements in the quarantine on " + client.name)
        finally:
            net.s.close()

    def restore_all_from_qr(self, client):
        net = Networker()
        net.connect_to(client.name)
        self.send_credentials(net, client)
        try:
            net.send_val(str(QR_REST_ALL) + ":0")
        except ConnectionError:
            raise Exception("Unable to restore all elements from the quarantine on " + client.name)
        finally:
            net.s.close()


class TaskConfig(Tasker):
    def get_config(self, client):
        pass

    def send_conf_mod(self, client, section, key, new_value):
        pass

if __name__ == "__main__":
    cl = ClientList()
    cl.load_list()
    qr_task = TaskQR()
    scan_task = TaskScan()
    scan_e = ScanElem("/home/antoine/Images")
    scan_e.options = "1011000000"
    scan_e.back_limit_size = "150.0"
    scan_e.del_limit_size = "0.0"
    scan_e.is_temp = "0"
    scan_e.max_age = "15"
    # scan_task.add_to_scan(cl.c_list[0], scan_e)
    # scan_task.rm_from_scan(cl.c_list[0], "/home/antoine/Documents")
    """scanList = scan_task.get_scan_list(cl.c_list[0])
    for scan_elem in scanList:
        print("Elem "+scan_elem.path)
        print(" - Options: "+scan_elem.options)
        print(" - Back limit size: "+scan_elem.back_limit_size)
        print(" - Del limit size: "+scan_elem.del_limit_size)
        print(" - Temp folder ? "+("true" if (scan_elem.is_temp == 1) else "false"))
        print(" - Max Age: "+scan_elem.max_age)"""
    """qrList = qr_task.get_qr_list(cl.c_list[0])
    for qrElem in qrList:
        print("Elem "+qrElem.f_name)
        print(" - Old path: "+qrElem.o_path)
        print(" - Entry date: "+qrElem.d_begin)
        print(" - Expire date: "+qrElem.d_expire)"""
    # qr_task.restore_from_qr(cl.c_list[0], "toto.txt")
    """qr_task.add_to_qr(cl.c_list[0], "/home/antoine/Documents/toto.txt")
    qr_task.add_to_qr(cl.c_list[0], "/home/antoine/Documents/tata.txt")
    qr_task.add_to_qr(cl.c_list[0], "/home/antoine/Documents/trololo.txt")"""
    # qr_task.rm_all_from_qr(cl.c_list[0])
    qr_task.restore_all_from_qr(cl.c_list[0])
