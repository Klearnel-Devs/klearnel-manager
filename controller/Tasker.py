__author__ = 'antoine'
from controller.Networker import Networker
from model.Client import ClientList
from model.ScanElem import ScanElem
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
    net = Networker()

    def send_credentials(self, client):
        self.net.send_val(client.token)
        if self.net.get_ack() != self.net.SOCK_ACK:
            raise ConnectionRefusedError("Error on token negociation")
        self.net.send_val(client.password)

        if self.net.get_ack() != self.net.SOCK_ACK:
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
        self.net.connect_to(client.name)
        self.send_credentials(client)
        try:
            self.net.send_val(str(SCAN_ADD)+":"+str(len(new_elem.path)))
            self.net.send_val(new_elem.path)
            self.net.send_val(new_elem.options)
            self.net.send_val(str(len(new_elem.back_limit_size)))
            self.net.send_val(new_elem.back_limit_size)
            self.net.send_val(str(len(new_elem.del_limit_size)))
            self.net.send_val(new_elem.del_limit_size)
            self.net.send_val(new_elem.is_temp)
            self.net.send_val(str(len(new_elem.max_age)))
            self.net.send_val(new_elem.max_age)
        except ConnectionError:
            self.net.s.close()
            raise Exception("Unable to add "+new_elem.path+" to scanner on "+client.name)
        self.net.s.close()

    def rm_from_scan(self, client, path):
        self.net.connect_to(client.name)
        self.send_credentials(client)
        try:
            self.net.send_val(str(SCAN_RM)+":"+str(len(path)))
            self.net.send_val(path)
        except ConnectionError:
            self.net.s.close()
            raise Exception("Unable to remove "+path+" from scanner on "+client.name)
        self.net.s.close()

    def get_scan_list(self, client):
        self.net.connect_to(client.name)
        self.send_credentials(client)
        scan_list = list()
        try:
            self.net.send_val(str(SCAN_LIST)+":0")
            result = None
            i = 0
            while result != "EOF":
                size = self.net.get_data(20)
                self.net.send_ack(self.net.SOCK_ACK)
                if size == "EOF":
                    break
                result = self.net.get_data(int(size))
                scan_elem = ScanElem(result)
                self.net.send_ack(self.net.SOCK_ACK)

                size = self.net.get_data(20)
                self.net.send_ack(self.net.SOCK_ACK)
                result = self.net.get_data(int(size))
                scan_elem.options = result
                self.net.send_ack(self.net.SOCK_ACK)

                size = self.net.get_data(20)
                self.net.send_ack(self.net.SOCK_ACK)
                result = self.net.get_data(int(size))
                scan_elem.back_limit_size = result
                self.net.send_ack(self.net.SOCK_ACK)

                size = self.net.get_data(20)
                self.net.send_ack(self.net.SOCK_ACK)
                result = self.net.get_data(int(size))
                scan_elem.del_limit_size = result
                self.net.send_ack(self.net.SOCK_ACK)

                size = self.net.get_data(20)
                self.net.send_ack(self.net.SOCK_ACK)
                result = self.net.get_data(int(size))
                scan_elem.is_temp = result
                self.net.send_ack(self.net.SOCK_ACK)

                size = self.net.get_data(20)
                self.net.send_ack(self.net.SOCK_ACK)
                result = self.net.get_data(int(size))
                scan_elem.max_age = result
                self.net.send_ack(self.net.SOCK_ACK)

                scan_list.append(scan_elem)
                i += 1

        except ConnectionError:
            self.net.s.close()
            raise Exception("Unable to get list from scanner on "+client.name)
        self.net.send_ack(self.net.SOCK_ACK)
        self.net.s.close()
        return scan_list


class TaskQR(Tasker):

    def add_to_qr(self, client, path):
        self.net.connect_to(client.name)
        self.send_credentials(client)
        try:
            self.net.send_val(str(QR_ADD)+":"+str(len(path)))
            self.net.send_val(path)
        except ConnectionError:
            self.net.s.close()
            raise Exception("Unable to add "+path+" to quarantine on "+client.name)
        self.net.s.close()

    def rm_from_qr(self, client, filename):
        self.net.connect_to(client.name)
        self.send_credentials(client)
        try:
            self.net.send_val(str(QR_RM)+":"+str(len(filename)))
            self.net.send_val(filename)
        except ConnectionError:
            self.net.s.close()
            raise Exception("Unable to remove "+filename+" from quarantine on "+client.name)
        self.net.s.close()

    def restore_from_qr(self, client, filename):
        self.net.connect_to(client.name)
        self.send_credentials(client)
        try:
            self.net.send_val(str(QR_REST)+":"+str(len(filename)))
            self.net.send_val(filename)
        except ConnectionError:
            self.net.s.close()
            raise Exception("Unable to restore "+filename+" from quarantine on "+client.name)
        self.net.s.close()

    def get_qr_list(self):
        pass

    def get_qr_info(self):
        pass

    def rm_all_from_qr(self):
        pass

    def restore_all_from_qr(self):
        pass

if __name__ == "__main__":
    cl = ClientList()
    cl.load_list()
    qr_task = TaskScan()
    scan_e = ScanElem("/home/antoine/Images")
    scan_e.options = "1011000000"
    scan_e.back_limit_size = "150.0"
    scan_e.del_limit_size = "0.0"
    scan_e.is_temp = "0"
    scan_e.max_age = "15"
    # qr_task.add_to_scan(cl.c_list[0], scan_e)
    # qr_task.rm_from_scan(cl.c_list[0], "/home/antoine/Documents")
    scanList = qr_task.get_scan_list(cl.c_list[0])
    for scan_elem in scanList:
        print("Elem "+scan_elem.path)
        print(" - Options: "+scan_elem.options)
        print(" - Back limit size: "+scan_elem.back_limit_size)
        print(" - Del limit size: "+scan_elem.del_limit_size)
        print(" - Temp folder ? "+("true" if (scan_elem.is_temp == 1) else "false"))
        print(" - Max Age: "+scan_elem.max_age)

