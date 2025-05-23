#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5 import uic,QtCore,QtGui,QtWidgets
from PyQt5.QtWidgets import QApplication,QMessageBox,QMainWindow,QWidget, QTreeView
from PyQt5.QtWidgets import QFileSystemModel,QPushButton, QLineEdit
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt
import sys
import math
import numpy as np
import matplotlib.pyplot as plt
import os, sqlite3
import pandas as pd

        
class materialLabUI(QMainWindow):
    #初始化主页面
    def __init__(self):
        # 从文件中加载UI定义
        super().__init__()
        uic.loadUi("materialLab.ui",self)
        self.setWindowTitle("材料库管理")
        self.modelTreeCreate()          #建立材料库的模型树
        
        
        #为matID的combox添加1-20个列表
        for i in range(1,21):
            self.toMatID.addItem(str(i))
            
        #定义各个按钮的点击连接功能
        self.clearData.clicked.connect(self.clearDisplayData)
        self.addMaterial.clicked.connect(self.addtoMaterialLab)
        self.deleteMaterialButton.clicked.connect(self.deleteMaterial)
        self.updateMaterialButton.clicked.connect(self.updateMaterialData)
        
    def modelTreeCreate(self):
        self.tree_view = self.findChild(QTreeView, 'materialNameTree')  # 确保treeView是QTreeView的对象名
        

        # 创建模型
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['Material Labrary'])  # 设置表头

        # 添加根节点(各种fiber)
        self.carbon_fiber = QStandardItem("Carbon Fiber")
        self.glass_fiber = QStandardItem("Glass Fiber")
        self.other_fiber = QStandardItem("Other Fiber")
        self.user_fiber = QStandardItem("User")
        self.model.appendRow(self.carbon_fiber)
        self.model.appendRow(self.glass_fiber)
        self.model.appendRow(self.other_fiber)
        self.model.appendRow(self.user_fiber)
        
        #手动添加模型树，但是在界面中新增相关的数据后，再打开软件时模型树就没有显示了
        #所以需要使用材料库，每次打开软件时调取材料库中的数据来生成模型树
        '''
        # 为carboon fiber添加对应的材料
        carboon_item = ["T300/5208 (Carbon/Epoxy)","T300/934 (Carbon/Epoxy)","T300/976 (Carbon/Epoxy)",
                        "AS/3501 (Carbon/Epoxy)","AS4/3501-6 (Carbon/Epoxy)","AS4/3502 (Carbon/Epoxy)",
                        "GY70/934 (Carbon/Epoxy)","AS4/APC2 (Carbon/PEEK)","AS4/5250-3 (Carbon/Bismaleimide)",
                        "Generic (IM6/Epoxy)", "IM6/APC2 (Carbon/PEEK)"]
                        
        for item in carboon_item:
            self.carboon_fiber.appendRow(QStandardItem(item))
        # chapter1 = QStandardItem("T300/5208 (carboon/Epoxy)")
        # carboon_fiber.appendRow(chapter1)
        
        #为glass_fiber添加对应的目录
        glass_item = ["Generic (E-Glass/Epoxy)","Generic (S-Glass/Epoxy)","S2-449/SP (S-Glass/Epoxy)"]
        for item in glass_item:
            self.glass_fiber.appendRow(QStandardItem(item))

        other_item = ["Generic (Kevlar 149/Epoxy)"]
        for item in other_item:
            self.other_fiber.appendRow(QStandardItem(item))
        '''
        try:
            conn = sqlite3.connect("material.db")
            cursor = conn.cursor()
            # Carbon Fiber的目录表
            cursor.execute('select name from materialLab where classify=?', ("Carbon Fiber",))
            rows = cursor.fetchall()
            for row in rows:
                self.carbon_fiber.appendRow(QStandardItem(row[0]))
            
            # Glass Fiber的目录表
            cursor.execute('select name from materialLab where classify=?', ("Glass Fiber",))
            rows = cursor.fetchall()
            for row in rows:
                self.glass_fiber.appendRow(QStandardItem(row[0]))
             
            # Other Fiber的目录表
            cursor.execute('select name from materialLab where classify=?', ("Other Fiber",))
            rows = cursor.fetchall()
            for row in rows:
                self.other_fiber.appendRow(QStandardItem(row[0]))
                
            # User的目录表
            cursor.execute('select name from materialLab where classify=?', ("User",))
            rows = cursor.fetchall()
            for row in rows:
                self.user_fiber.appendRow(QStandardItem(row[0]))
                
        except sqlite3.Error as e:
            print(f"An error occurred:{e}")
    
        finally:
            if conn:
                conn.close()
        # 设置模型
        self.tree_view.setModel(self.model)
        self.disable_editing(self.carbon_fiber)
        self.disable_editing(self.glass_fiber)
        self.disable_editing(self.other_fiber)

        # 展开所有节点
        self.tree_view.clicked.connect(self.item_clicked)
        self.tree_view.expandAll()
        self.tree_view.setStyleSheet("""
            QTreeView::item {
                padding: 5px;  /* 设置节点间距 */
            }
        """)


    def disable_editing(self, item):
        """
        递归设置节点及其所有子节点不可编辑
        """
        # 设置当前节点不可编辑
        item.setFlags(item.flags() & ~Qt.ItemIsEditable)

        # 递归处理子节点
        for row in range(item.rowCount()):
            child_item = item.child(row)
            if child_item:
                self.disable_editing(child_item)
                
    # 定义模型树上的点击操作
    def item_clicked(self,index):
        root_item = ["Carbon Fiber","Glass Fiber","Other Fiber","User"]
        item = self.model.itemFromIndex(index)
        if item is None:
            return
        item_text = item.text()
        if item_text not in root_item:
            self.materialName.setText(item_text)
            self.read_material(item_text)
             
    def read_material(self,name):
        try:
            conn = sqlite3.connect("material.db")
            cursor = conn.cursor()
            cursor.execute('select value,description from materialLab where name=?', (name,))
            rows = cursor.fetchall()
            for row in rows:
                values_json,desc = row
            #使用pd.read_json命令将json数据转换为series数据时，如果数据类型有很多种
            #最好指定dtype，不然转换出来的数据可能有问题(比如是时间序列）
            # print(values_json)
            values_float = pd.read_json(values_json,typ = "series",dtype=float)
            values = values_float.apply(self.fomat_value)
            # values = values_int.apply(lambda x: "{:.4e}".format(x))

            self.E1.setText(values[1])
            self.E2.setText(values[2])
            self.G12.setText(values[3])
            if isinstance(values_float[4],str):
                self.v12.setText(values_float[4])
            else:
                self.v12.setText(str(round(values_float[4],3)))
            self.CTE1.setText(values[5])
            self.CTE2.setText(values[6])
            if isinstance(values_float[7],str):
                self.CME1.setText(values_float[7])
            else:
                self.CME1.setText(str(round(values_float[7],3)))
            if isinstance(values_float[8],str):
                self.CME2.setText(values_float[8])
            else:
                self.CME2.setText(str(round(values_float[8],3)))
            self.Xt.setText(values[9])
            self.Xc.setText(values[10])
            self.Yt.setText(values[11])
            self.Yc.setText(values[12])
            self.S.setText(values[13])
            self.description.setText(desc)
            
        except sqlite3.Error as e:
            print(f"An error occurred:{e}")
    
        finally:
            if conn:
                conn.close()
    
    #对导入的数据进行格式转换
    def fomat_value(self,value):
        if pd.isna(value) or (isinstance(value, str) and value.strip() == ''):
            return "  "
            # print(value,type(value))            
        return "{:.4e}".format(float(value))

    def clearDisplayData(self):
        line_edits = self.findChildren(QLineEdit)
        for line_edit in line_edits:
            line_edit.clear()

    def addtoMaterialLab(self):
        #先对输入的lineEdits中所有的内容合理性进行判断
        line_edits = self.findChildren(QLineEdit)
        for line_edit in line_edits:
            if line_edit not in [self.materialName,self.description]:
                text = line_edit.text().strip() #去除输入数据的首尾空格
                if text == "":
                    continue
                try:
                    float(text)
                except ValueError:
                    QMessageBox.warning(self, "Invalid Input", f"Please enter a valid number in {line_edit.objectName()}.")
                    line_edit.setFocus()
                    return
                    
        #获取各个QlineEdit中的数据
        name_data = self.materialName.text()
        material_data = pd.Series(np.nan,index = range(1,14))
        material_data[1] = self.E1.text()
        material_data[2] = self.E2.text()
        material_data[3] = self.G12.text()
        material_data[4] = self.v12.text()
        material_data[5] = self.CTE1.text()
        material_data[6] = self.CTE2.text()
        material_data[7] = self.CME1.text()
        material_data[8] = self.CME2.text()
        material_data[9] = self.Xt.text()
        material_data[10] = self.Xc.text()
        material_data[11] = self.Yt.text()
        material_data[12] = self.Yc.text()
        material_data[13] = self.S.text()
        material_data_json = material_data.to_json()
        description_data = self.description.text()
        itemToAdd = self.rootItemAdd.currentText()
        
        #打开数据库并将数据插入到数据库中
        try:
            conn = sqlite3.connect("material.db")
            cursor = conn.cursor()
            cursor.execute('select * from materialLab where name=?', (name_data,))
            existing_data = cursor.fetchone()
            #判断name是否存在数据库中
            if existing_data:
                reply = QMessageBox.question(self, '更新确认',
                                     "当前材料库中存在该材料，是否更新？", QMessageBox.Yes | 
                                     QMessageBox.No, QMessageBox.No)
                if reply == QMessageBox.Yes:
                    cursor.execute("""UPDATE materialLab SET value=?,description=?
                                WHERE name=?""",(material_data_json,description_data,name_data))
            else:
                #name不存在时插入数据
                cursor.execute("INSERT INTO materialLab (name,value,description,classify) VALUES(?,?,?,?)",(name_data,material_data_json,description_data,itemToAdd))
                if itemToAdd == "Carbon Fiber":
                    self.carbon_fiber.appendRow(QStandardItem(name_data))
                    self.disable_editing(self.carbon_fiber)
                elif itemToAdd == "Glass Fiber": 
                    self.glass_fiber.appendRow(QStandardItem(name_data))
                    self.disable_editing(self.glass_fiber)
                elif itemToAdd == "Other Fiber": 
                    self.other_fiber.appendRow(QStandardItem(name_data))
                    self.disable_editing(self.other_fiber)
                elif itemToAdd == "User": 
                    self.user_fiber.appendRow(QStandardItem(name_data))
                    self.disable_editing(self.user_fiber)
                
            conn.commit()
                                
        except sqlite3.Error as e:
            print(f"An error occurred:{e}")
    
        finally:
            if conn:
                conn.close()


    def deleteMaterial(self):
        name_data = self.materialName.text()
        #打开数据库删除掉指定的数据
        try:
            conn = sqlite3.connect("material.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM materialLab WHERE name=?",(name_data,))
            conn.commit()
            self.clearDisplayData()
            #删除模型树上对应的目录
            root_item = self.model.invisibleRootItem()
            # 遍历所有父项
            for parent_row in range(root_item.rowCount()):
                parent = root_item.child(parent_row)
                if parent:
                    # 遍历父项的所有子项
                    for child_row in range(parent.rowCount()):
                        child = parent.child(child_row)
                        if child and child.text() == name_data:
                            parent.removeRow(child_row)
                            return  # 找到并删除后退出)                    
                    
        except sqlite3.Error as e:
            print(f"An error occurred:{e}")
    
        finally:
            if conn:
                conn.close()

    def updateMaterialData(self):
        #先对输入的lineEdits中所有的内容合理性进行判断
        line_edits = self.findChildren(QLineEdit)
        for line_edit in line_edits:
            if line_edit not in [self.materialName,self.description]:
                text = line_edit.text().strip() #去除输入数据的首尾空格
                if text == "":
                    continue
                try:
                    float(text)
                except ValueError:
                    QMessageBox.warning(self, "Invalid Input", f"Please enter a valid number in {line_edit.objectName()}.")
                    line_edit.setFocus()
                    return
                    
        #获取各个QlineEdit中的数据
        name_data = self.materialName.text()
        material_data = pd.Series(np.nan,index = range(1,14))
        material_data[1] = self.E1.text()
        material_data[2] = self.E2.text()
        material_data[3] = self.G12.text()
        material_data[4] = self.v12.text()
        material_data[5] = self.CTE1.text()
        material_data[6] = self.CTE2.text()
        material_data[7] = self.CME1.text()
        material_data[8] = self.CME2.text()
        material_data[9] = self.Xt.text()
        material_data[10] = self.Xc.text()
        material_data[11] = self.Yt.text()
        material_data[12] = self.Yc.text()
        material_data[13] = self.S.text()
        material_data_json = material_data.to_json()
        description_data = self.description.text()
        itemToAdd = self.rootItemAdd.currentText()
        
        #打开数据库并将数据插入到数据库中
        try:
            conn = sqlite3.connect("material.db")
            cursor = conn.cursor()
            cursor.execute('select * from materialLab where name=?', (name_data,))
            existing_data = cursor.fetchone()
            #判断name是否存在数据库中
            if existing_data:
                reply = QMessageBox.question(self, '更新确认',
                                     "是否进行更新？", QMessageBox.Yes | 
                                     QMessageBox.No, QMessageBox.No)
                if reply == QMessageBox.Yes:
                    cursor.execute("""UPDATE materialLab SET value=?,description=?
                                WHERE name=?""",(material_data_json,description_data,name_data))
            else:
                #name不存在时插入数据
                reply = QMessageBox.question(self, '新建材料确认',
                                     "当前材料库中不存在该材料，是否新建", QMessageBox.Yes | 
                                     QMessageBox.No, QMessageBox.No)
                if reply == QMessageBox.Yes:
                    cursor.execute("INSERT INTO materialLab (name,value,description,classify) VALUES(?,?,?,?)",(name_data,material_data_json,description_data,itemToAdd))
                    if itemToAdd == "Carbon Fiber":
                        self.carbon_fiber.appendRow(QStandardItem(name_data))
                        self.disable_editing(self.carbon_fiber)
                    elif itemToAdd == "Glass Fiber": 
                        self.glass_fiber.appendRow(QStandardItem(name_data))
                        self.disable_editing(self.glass_fiber)
                    elif itemToAdd == "Other Fiber": 
                        self.other_fiber.appendRow(QStandardItem(name_data))
                        self.disable_editing(self.other_fiber)
                    elif itemToAdd == "User": 
                        self.user_fiber.appendRow(QStandardItem(name_data))
                        self.disable_editing(self.user_fiber)
                
            conn.commit()
                                
        except sqlite3.Error as e:
            print(f"An error occurred:{e}")
    
        finally:
            if conn:
                conn.close()
        
if __name__ == "__main__":
    app = QApplication([])
    myMainw = materialLabUI()
    myMainw.show()
    app.exec_()