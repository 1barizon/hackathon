# app do funcionario
import pandas as pd
import flet as ft
import asyncio
import os
import time
    

def get_problems():
    path = "assets\\problemas.xlsx"
    df = pd.read_excel(path)
    return df

def problema_resolvido(problema, existing_df, page):

    path = "assets\\problemas.xlsx"
    existing_df = pd.read_excel(path)
 
    for index, row in existing_df.iterrows():
        if row["tipo"] == problema["tipo"] and row["gravidade"] == problema["gravidade"] and row["rua"] == problema["rua"] and row["bairro"] == problema["bairro"] and row["numero"] == problema["numero"] and row["complemento"] == problema["complemento"]:
           
            existing_df["status"] = "Resolvido"
            
            existing_df.to_excel(path)
            update(existing_df, page)
            
    


    

def update(existing_df,page):
    lista_demandas = []
    path = "assets\\problemas.xlsx"

    
    
    if os.path.exists(path):
        
        new_df = pd.read_excel(path)
       
      
        if not new_df.equals(existing_df):
            
            existing_df = new_df.copy()
        else:
            existing_df = existing_df.copy()     
    else:
        print(f"O arquivo {path} não existe.")
    
    for control in page.controls[:]:
            if isinstance(control, ft.Card):
                page.controls.remove(control)
    for index, row in existing_df.iterrows():

        
        
        if row["status"] == "Pendente":
            
            card = ft.Card(content=ft.Container(content=ft.Column([
                ft.ListTile(
                    leading=ft.Icon(ft.icons.WARNING_AMBER_SHARP),
                    title=ft.Text(row["tipo"], size=22),
                    subtitle=ft.Text(row["gravidade"], size=18),
                    
                ),
                ft.Divider(),
            
                ft.Text("Endereço: " + str(row["rua"]) + ", " + str(row["bairro"]) + "\n" + str(row["numero"])+ ", " + str(row["complemento"]), size=18),
                ft.ElevatedButton("Problema resolvido", 
                style=ft.ButtonStyle(text_style=ft.TextStyle(size=10, weight="bold")), 
                width=300, height=40, bgcolor=ft.colors.GREEN, 
                color=ft.colors.WHITE, on_click=lambda e, row=row: problema_resolvido(row, existing_df,page)),
            ]),padding=20, width=400))
            page.add(card)
        else: 
            pass
    
    page.update()
        




def main(page: ft.Page):
    df = get_problems()
    page.add(ft.SafeArea(ft.Row([ ft.Text("Demandas", size=30), ft.Icon(ft.icons.WARNING_ROUNDED)])))
    page.add(ft.Divider())
    page.scroll = "always"
    
    current_time = time.strftime("%H:%M:%S")
    
    page.update()
    
   
   

    button = ft.ElevatedButton(
    style=ft.ButtonStyle(text_style=ft.TextStyle(size=26, weight="bold")),
    text="Atualizar", width=400,                  
    height=50,bgcolor=ft.colors.BLUE, color=ft.colors.WHITE, 
    on_click=lambda e: update(df, page),
    )
    
    page.add(button)

  





ft.app(main)