import sys
from PySide import QtGui, QtCore
import MySQLdb

class Example(QtGui.QDialog):
    
    def __init__(self):
        super(Example, self).__init__()
        self.conn()
        self.initUI()
        
    def conn(self):
        conn = MySQLdb.connect(host="localhost", user="root", passwd="lozinka", db="istrazivac")
        cursor = conn.cursor()

        cursor.execute("SELECT xkoord, ykoord, d_tezina FROM polje;")
        lista = cursor.fetchall()
        nova = []
        xlista = []
        ylista = []
        self.zadnja = []


        for el in lista:
            ylista.append(int(el[1]))
            xlista.append(int(el[0]))

        self.maxX = max(xlista)
        self.maxY = max(ylista)

        i = 0
        for el in lista:
            if int(el[0]) >= 0 \
             and int(el[1]) >= 0 \
             and int(el[0]) < self.maxX \
             and int(el[1]) < self.maxY:
             nova.append([int(el[0]), int(el[1]), int(el[2])])

        yIshodiste = max(ylista) * 50 + 50

        for el in nova:
            if el[2] == 1: 
                boja = "prolaz"
            else: 
                boja = "zid"
            self.zadnja.append([el[0], yIshodiste - (abs(el[1])*50+50), boja])

    def initUI(self):      
        self.setGeometry(300, 300, self.maxX * 100, self.maxY * 100)
        self.setWindowTitle('Colors')
        self.show()

    def paintEvent(self, e):

        qp = QtGui.QPainter()
        qp.begin(self)
        self.crtajSvijet(qp)
        qp.end()
        
    def crtajSvijet(self, qp):
      
        color = QtGui.QColor(0, 0, 0)
        color.setNamedColor('#d4d4d4')
        qp.setPen(color)

        for el in self.zadnja:
            if el[2] == "zid":
                qp.setBrush(QtGui.QColor(188, 32, 199))
            else:
                qp.setBrush(QtGui.QColor(255, 255, 200))
            qp.drawRect(el[0]*50+50, el[1], 50, 50)

              
        
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
