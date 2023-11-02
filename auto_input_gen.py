# -*- coding: utf-8 -*-
"""
This is a auto-generate Gaussian input file machine
Created on Thu Nov  2 10:18:55 2023
@author: Lian-Wei Ye
"""
import os

Lanthanide = "Ce"                                 
Halogen    = "F"                                  
PP         = "SPP"                                
Molecule   = Lanthanide + Halogen + "3"

file_path = r"D:\G16W\auto_input_gen"              # 想要文件存储的位置

# =============================================================================
# Head
# Define calculation parameters
# =============================================================================                                               
Head = """%chk={}.chk                            
%nproc=24
%mem=80GB
# HF/genecp opt freq

Title

0 1
""".format(Molecule)
# =============================================================================
# XYZ
# Obtain coordination information 需要手动输入坐标文件
# =============================================================================
XYZ = """ {}                -0.52935042   -0.54232675    0.00000000
 {}                 0.30399733    0.63617370    2.04124183
 {}                -3.02935042   -0.54229594    0.00000000
 {}                 0.30395431   -2.89935946    0.00000000
""".format(Lanthanide,Halogen,Halogen,Halogen)




# =============================================================================
# ###以上为需要修改的部分
# ###以下为代码部分
# =============================================================================




# =============================================================================
# Tail
# Defin the pseudopotential and basis_set information
# =============================================================================
# 读取基组文件
basis_set_file_path = r"D:\G16W\auto_input_gen"
basis_set_file = basis_set_file_path + r"\basis_set_{}.txt".format(PP)
with open(basis_set_file,'r') as bs_file:
    basis_set_data = bs_file.read()
# 读取赝势文件
pseudopotential_file_path = r"D:\G16W\auto_input_gen"
pseudopotential_file = pseudopotential_file_path + r"\pseudopotential_{}.txt".format(PP)
with open(pseudopotential_file,'r') as pp_file:
    pseudopotential_data = pp_file.read()


# 读取xyz文件中的元素信息
molecule_elements = set([line.split()[0] for line in XYZ.split('\n') if line.strip()])
# 基组与元素匹配
selected_basis_set = ""
found_element = False
for element in molecule_elements:
    for line in basis_set_data.split('\n'):
        parts = line.split()
        if len(parts) >= 1 and parts[0] in element:
            found_element = True
        if found_element:
            if line.strip()!="****":
                selected_basis_set += line + '\n'
            if line.strip()=="****":
                selected_basis_set += line + '\n'
                found_element = False
                break
# 赝势与元素匹配
selected_pseudopotentials = ""
found_element = False
for element in molecule_elements:
    for line in pseudopotential_data.split('\n'):
        parts = line.split()
        if len(parts) >= 1 and parts[0] in element:
            found_element = True
        if found_element:
            if line.strip():
                selected_pseudopotentials += line + '\n'
            if not line.strip():
                selected_pseudopotentials += line
                found_element = False
                break
# =============================================================================
# Save
# Save in specific directory
# =============================================================================
input_file_content = Head + XYZ + '\n' + selected_basis_set + '\n' + selected_pseudopotentials + '\n\n'

if PP == "SPP":
    orbital = 'valence'
elif PP == "LPP":
    orbital = 'core'
file_name = r"\{}\{}\{}.gjf".format(Molecule,orbital,Molecule)
file_path_name = file_path + file_name

#创建一个文件夹保存gjf文件
os.makedirs(os.path.dirname(file_path_name),exist_ok=True)
with open(file_path_name, "w") as f:
    f.write(input_file_content)


