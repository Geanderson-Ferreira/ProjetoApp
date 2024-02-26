import subprocess


def getIp():

    def obter_enderecos_ip_linux():
        try:
            # Executa o comando 'hostname -I' no terminal
            resultado = subprocess.check_output(['hostname', '-I'], universal_newlines=True)
            
            # Converte a saída em uma lista de endereços IP
            enderecos_ip = resultado.strip().split()
            
            return enderecos_ip
        except Exception as e:
            print(f"Erro ao obter endereços IP: {e}")
            return None


    # Chama a função e imprime os endereços IP no Linux
    enderecos_ip_linux = obter_enderecos_ip_linux()

    if enderecos_ip_linux:
        if len(enderecos_ip_linux) >= 1:
            return enderecos_ip_linux[0]
