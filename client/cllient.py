import random
import socket
import pickle
import string
import uuid
import json
from entidades import *
import threading

class Cliente:
    def __init__(self, port, host) -> None:
        self._port = port
        self._host = host
        self._s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    def start_client(self):
        self._s.connect((self._host, self._port))
        self._login()
        
    def __request(self, typeOperation, data):
        data_serialized = pickle.dumps((typeOperation, data))
        self._s.send(data_serialized)


        response = self._s.recv(4096)
        if not response:
            return False

        try:
            # Tenta desserializar os dados
            deserialized_data = pickle.loads(response)
            return deserialized_data
        except pickle.UnpicklingError:
            print("Erro ao desserializar os dados recebidos.")
            return None
        
    def _login(self):
        print("Bem-vindo ao VENDEPASS, sua plataforma de reserva.")
        email = input("Informe seu email: \n")
        password = input("Informe sua senha: \n")
        user = self.__request(100, {'username': email, 'password_user': password})
        
        if user:
            print(f"Bem-vindo, {user.username}!")
            self._selecionar_voo(user)
        else:
            print("Login falhou. Verifique suas credenciais e tente novamente.")
    
             
    def _listar_voos(self, voos, destino_selecionado):
            for voo in voos:
                if voo.destino == destino_selecionado:
                    self._mostrar_detalhes_voo(voo)
            print("-" * 40)

            for voo in voos:
                if voo.destino != destino_selecionado:
                    self._mostrar_detalhes_voo(voo)
    
    def _selecionar_voo(self, user: User):
        all_trechos = self.__request(201, "")
        for num, capital in enumerate(all_trechos):
            print(f"[{num}] - {capital}")
        
        origem = input("Digite de onde você quer partir: \n")
        
        for num in range(len(all_trechos[origem])):
            print(f'[{num}] - {all_trechos[origem][num].destino}')
        destino = input("Digite para onde você quer ir: \n")

        print(f'\nVoos a partir de [{origem}]:')
        self._listar_voos(all_trechos[origem], destino)

        id_voo = input('Selecione o ID do voo: \n')
        self._confirmar_compra(user, all_trechos[origem], id_voo)

        def _listar_voos(self, voos, destino_selecionado):
            for voo in voos:
                if voo.destino == destino_selecionado:
                    self._mostrar_detalhes_voo(voo)
            print("-" * 40)

            for voo in voos:
                if voo.destino != destino_selecionado:
                    self._mostrar_detalhes_voo(voo)
                    
    def _mostrar_detalhes_voo(self, voo):
        print(f'ID: {voo.id}')
        print(f'Origem: {voo.origem}')
        print(f'Destino: {voo.destino}')
        print(f'Vagas disponíveis: {voo.vagas}')
        print("-" * 40)
    
    def _confirmar_compra(self, user, voos, id_voo_selecionado):
        for voo in voos:
            if voo.id == id_voo_selecionado:
                passagem = user.comprar_passagem(voo, 'A1', '78')
                if passagem:
                    print(f"ID do Voo: {passagem.id_voo}")
                    print(f"ID do Passageiro: {passagem.id_passageiro}")
                    print(f"CPF: {passagem.cpf}")
                    print(f"Assento(s): {', '.join(passagem.assento) if passagem.assento else 'Nenhum assento alocado'}")
                else:
                    print('Voo lotado')
    
        #  def verification(self):
    #     while True:
    #         try:
    #             # Recebe dados do servidor
    #             data = self._s.recv(1024)
    #             if not data:
    #                 print("Conexão perdida com o servidor.")
    #                 break
    #             else:
    #                 print("Recebido do servidor:", data.decode())
    #         except Exception as e:
    #             print(f"Erro ao receber dados do servidor: {e}")
    #             break
    #         self._s.send(pickle.dump(''))