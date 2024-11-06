from typing import List

import requests


class Item:
    def __init__(self, descricao: str, qtde: float, vlr_unit: float, codigo: str = None):
        self.descricao = descricao
        self.qtde = qtde
        self.vlr_unit = vlr_unit
        self.codigo = codigo

    def to_xml(self):
        codigo_xml = f"<codigo>{self.codigo}</codigo>" if self.codigo else ""
        return f"""
            <item>
                {codigo_xml}
                <descricao>{self.descricao}</descricao>
                <qtde>{self.qtde}</qtde>
                <vlr_unit>{self.vlr_unit}</vlr_unit>
            </item>
        """


class NFCe:
    def __init__(self, numero: str, itens: List[Item]):
        self.numero = numero
        self.itens = itens

    def to_xml(self):
        itens_xml = "".join(item.to_xml() for item in self.itens)
        return f"""
            <pedido>
                <numero>{self.numero}</numero>
                <cliente>
                    <nome>Consumidor final</nome>
                </cliente>
                <itens>
                    {itens_xml}
                </itens>
            </pedido>
        """


class NFCeService:
    def __init__(self, nfce: NFCe, api_key: str):
        self.nfce = nfce
        self.api_key = api_key

    def enviar_nota(self):
        url = "https://bling.com.br/Api/v2/nfce/json/"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        xml_payload = self.nfce.to_xml()
        data = {"apikey": self.api_key, "xml": xml_payload}

        response = requests.post(url, data=data, headers=headers)

        if response.status_code == 200:
            print("NFC-e enviada com sucesso:", response.json())
        else:
            print("Erro ao enviar NFC-e:", response.text)


# Exemplo de uso
itens = [Item(descricao="Produto A", qtde=1, vlr_unit=10.0)]
nova_nfce = NFCe(numero="1001", itens=itens)

api_key = "3b7ea79b51e0eb05db6e801aab074f79ed060684b8857e1efd1fdec571c1"
service = NFCeService(nova_nfce, api_key)
service.enviar_nota()
