import flet as ft
import requests
import pandas as pd

def get_address_by_cep(cep, rua, bairro,problema_df):
    # Remove any non-numeric characters from the CEP
    cep = ''.join(filter(str.isdigit, cep))
    
    # Make a request to the ViaCEP API
    response = requests.get(f"https://viacep.com.br/ws/{cep}/json/")
    
    # Check if the request was successful
    if response.status_code == 200:
        address_data = response.json()
        
        if 'erro' not in address_data:
            
            rua.value = address_data['logradouro']
            bairro.value = address_data['bairro']

            problema_df["cep"] = cep
            problema_df["rua"] = rua.value
            problema_df["bairro"] = bairro.value
           
           
            bairro.update()
            rua.update()
            
            
        else:
            return f"CEP {cep} not found."
    else:
        return "Failed to connect to the API."

def tipo_problema(x, problema_df):
    value = x.value
    
    if value == "1":
        problema_df["tipo"] = "Vazamento"    
    if value == "2":
        problema_df["tipo"] = "Desabastecimento"
    if value == "3":
        problema_df["tipo"] = "Esgoto"
    if value == "4":
        problema_df["tipo"] = "Bueiro"
   
    
def tipo_de_graviade(x, problema_df):
    value = x.value
    if value == "1":
        problema_df["gravidade"] = "Muito Grave"    
    if value == "2":
        problema_df["gravidade"] = "Grave"
    if value == "3":
        problema_df["gravidade"] = "Moderado"
    if value == "4":
        problema_df["gravidade"] = "Leve"
    

def enviar(problema_df, page, dlg_modal):
    path = "app\\assets\\problemas.xlsx"
    existing_df = pd.read_excel(path)
    new_df  = pd.DataFrame([problema_df])
    updated_df = pd.concat([existing_df, new_df], ignore_index=True)
    
    updated_df.to_excel(path, index=False)
   
    page.close(dlg_modal)
    
    
def pop_up(dlg_modal, page, problema_df, numero, complemento):
    problema_df["numero"] = numero.value
    problema_df["complemento"] = complemento.value
    dlg_modal.content = ft.Text(
        "Problema: " + problema_df["tipo"] + "\n" + 
        "Rua: " + problema_df["rua"] + "\n" +
        "Bairro: " + problema_df["bairro"] + "\n" +
        "CEP: " + problema_df["cep"] + "\n" +
        "Número: " + problema_df["numero"] + "\n" +
        "Complemento: " + problema_df["complemento"] + "\n" +
        "Gravidade: " + problema_df["gravidade"] + "\n")
    
    page.open(dlg_modal)
    


def main(page: ft.Page):
    
    page.scroll = "always"
    
  

    page.update()


    def switch_page(e):
        page.clean()
        if e.control.data == "home":
           
            page.add(home_page())
        elif e.control.data == "about":
            
            page.add(problema_page())
      

    def problema_page():


        df = pd.DataFrame(columns=["tipo", "rua", "bairro", "cep", "numero", "complemento", "gravidade", "status"]) 
        problema_df = {
            "tipo": "",
            "rua": "",
            "bairro": "",
            "cep": "",
            "numero": "",
            "complemento": "",
            "gravidade": "",
            "status": "Pendente"
        }

        rua = ft.TextField(
            label="Nome da rua:",
            value="",
            autofocus=True,                            
            )
    

        bairro = ft.TextField(
        label="Bairro:",
        value="",
        autofocus=True,
        )
        
        

        numero = ft.TextField(
        label="Número:",
        value="",
        autofocus=True,                
        )
        
        complemento = ft.TextField(
        label="Complemento:",
        value="",
        autofocus=True,
                            
        )

        cep = ft.TextField(
        label="CEP:",
        value="",
        autofocus=True,
        on_blur = lambda e: get_address_by_cep(cep.value, rua, bairro, problema_df),                   
        )


        

        radio_group = ft.RadioGroup(
        content=ft.Column(
            [
                ft.Radio(value=1, label="Vazamento"),
                ft.Radio(value=2, label="Desabastecimento"),
                ft.Radio(value=3, label="Esgoto"),
                ft.Radio(value=4, label="Bueiro")
            ]
        ),
        on_change= lambda e: tipo_problema(radio_group, problema_df) 
        )           
        gravidade_radio_button = ft.RadioGroup(
        content=ft.Column(
            [
                ft.Radio(value="1", label="Muito Grave"),
                ft.Radio(value="2", label="Grave"),
                ft.Radio(value="3", label="Moderado"),
                ft.Radio(value="4", label="Leve")
            ]
        ),
        on_change= lambda e: tipo_de_graviade(gravidade_radio_button, problema_df))                    
    
        
        dlg_modal = ft.AlertDialog(
            modal = True,
            title=ft.Text("Confirmar Informações"),
            
            actions=[
                ft.TextButton("Enviar", on_click=lambda e:enviar(problema_df, page, dlg_modal)),
                ft.TextButton("Cancelar", on_click=lambda e: page.close(dlg_modal)),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            
        )




        return ft.Column([
            ft.SafeArea(ft.Row([ ft.Text("Relatar um problema", size=30), ft.Icon(ft.icons.WARNING_ROUNDED)])),
            ft.Divider(),
            ft.ElevatedButton("Voltar para pagina inicial", data="home", on_click= switch_page),
            ft.ListTile(
                leading=ft.Icon(ft.icons.WATER_DROP),
                title=ft.Text("Detalhes do problema:", size=22),
        ),
            ft.Card(
                content=ft.Container(  
                    content=ft.Column(
                        [
                            ft.ListTile(
                                leading=ft.Icon(ft.icons.HANDYMAN),
                                title=ft.Text("Tipo de problema:"),
                            ),
                            radio_group
                        ]
                    ),
                    width=400,
                    padding=10,
                    
                    
                ),
                
            ),
            ft.Card(
                content=ft.Container(
                    content=ft.Column(
                        [
                            ft.ListTile(
                                leading=ft.Icon(ft.icons.GPS_FIXED),
                                title=ft.Text("Local:"),                    
                            ),
                            cep,
                            rua,

                            numero,
                            complemento,
                        
                            bairro,
                        ]
                    ),
                    width=400,
                    padding=10,
                    
                ),
                
            ),
            ft.Card(
                content=ft.Container(
                    content=ft.Column(
                        [
                            ft.ListTile(


                                leading=ft.Icon(ft.icons.WARNING_AMBER),
                                title=ft.Text("Gravidade:"),
                            ),
                            gravidade_radio_button
                        ]
                    ),
                    width=400,
                    padding=10,        
                    
                ),
                
            ),
            ft.ElevatedButton(
            style=ft.ButtonStyle(text_style=ft.TextStyle(size=26, weight="bold")),
            text="Enviar", width=400,                  
            height=50,bgcolor=ft.colors.BLUE, color=ft.colors.WHITE, 
            on_click=lambda e: pop_up(dlg_modal, page, problema_df, numero, complemento),
            ),

  
        ])



    
    def home_page():
        
       
        image = ft.Image(src="app\\assets\\logo-canf.png", width=300, height=200, fit=ft.ImageFit.CONTAIN)
        return ft.Column([
            image,
            ft.Text("Olá, João!", style="headlineMedium"),
            ft.Text("Bem vindo à Águas de Nova Friburgo"),
            ft.Text("Grupo Águas do Brasil"),
            ft.Divider(),
            
            
            


            ft.Container(
            ft.ElevatedButton("Relatar Problema", data="about", 
                            style=ft.ButtonStyle(text_style=ft.TextStyle(size=26, weight="bold")),
                            on_click=switch_page,
            ),
                        width=400,
                        height=80,
                        border_radius=20,
                        padding=10,
                        alignment=ft.alignment.center
            ),
             ft.Text(
            "INFORMAÇÕES",
            size=30,
            spans=[
                ft.TextSpan(
                    "\nUso Consciente da Água: Responsabilidade de Todos",
                    ft.TextStyle(italic=True, size=20, color=ft.colors.BLUE),
                    spans=[
                        ft.TextSpan(
                            spans=[
                                ft.TextSpan("\nA água é um recurso essencial para a vida e para o desenvolvimento sustentável, mas sua disponibilidade tem sido ameaçada devido ao aumento do consumo, ao desperdício e às mudanças climáticas. Em um cenário onde a escassez de água afeta milhões de pessoas em todo o mundo, o uso consciente da água se torna uma responsabilidade de cada cidadão.", ft.TextStyle(size=15)),
                                ft.TextSpan("\n", ft.TextStyle(size=15)),
                                ft.TextSpan("\nPor Que Usar a Água Conscientemente?", ft.TextStyle(size=15)),
                                ft.TextSpan("\n", ft.TextStyle(size=15)),
                                ft.TextSpan("\nO uso consciente da água é essencial para garantir que esse recurso esteja disponível não apenas para as necessidades atuais, mas também para as futuras gerações. Reduzir o consumo de água ajuda a preservar os mananciais e reduz a pressão sobre o sistema de tratamento e distribuição, diminuindo os impactos ambientais e econômicos.", ft.TextStyle(size=15)),
                            ],
                        ),
                    ],
                )
            ],
        )
            
        ]                     
    )

        


   

    
    page.add(home_page())
  



ft.app(main)
