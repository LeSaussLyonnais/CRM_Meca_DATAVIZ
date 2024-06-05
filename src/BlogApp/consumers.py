import json
from channels.generic.websocket import AsyncWebsocketConsumer
 

class WeatherConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add('weathers', self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard('weathers', self.channel_name)

    async def send_new_data(self, event):
        new_data = event['text']
        await self.send(json.dumps(new_data))


class PlanChargeConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        #Cette méthode est appelée lorsque le client WebSocket se connecte au serveur.
        #Elle ajoute le canal (channel) de la connexion à un groupe spécifique nommé 'charge'. Cela permet de regrouper plusieurs connexions WebSocket pour un traitement groupé. Le nom du groupe est arbitraire et peut être défini selon les besoins de votre application.
        #Enfin, elle accepte la connexion WebSocket.
        site = self.scope.get("url_route").get("kwargs").get("nom_site")
        atelier = self.scope.get("url_route").get("kwargs").get("nom_atelier")
        annee = self.scope.get("url_route").get("kwargs").get("num_annee")
        semaine = self.scope.get("url_route").get("kwargs").get("num_semaine")
        await self.channel_layer.group_add(
            "charge_"+site+"_"+atelier+"_"+str(annee)+"_"+str(semaine), 
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, code):
        #Cette méthode est appelée lorsque le client se déconnecte du serveur WebSocket, soit volontairement soit suite à une erreur.
        #Elle retire le canal de la connexion du groupe 'charge'.
        site = self.scope.get("url_route").get("kwargs").get("nom_site")
        atelier = self.scope.get("url_route").get("kwargs").get("nom_atelier")
        annee = self.scope.get("url_route").get("kwargs").get("num_annee")
        semaine = self.scope.get("url_route").get("kwargs").get("num_semaine")
        await self.channel_layer.group_discard(
            "charge_"+site+"_"+atelier+"_"+str(annee)+"_"+str(semaine), 
            self.channel_name
        )

    async def send_new_data(self, event):
        #Cette méthode est utilisée pour envoyer de nouvelles données à tous les clients connectés au groupe 'charge'.
        #Elle est généralement appelée lorsque de nouvelles données sont disponibles et doivent être diffusées à tous les clients.
        #L'argument event contient les données envoyées par l'événement déclencheur. Dans ce cas, l'événement est un simple texte.
        #La méthode récupère les nouvelles données à partir de l'événement, les encode en JSON (pour assurer la compatibilité avec WebSocket), puis les envoie à tous les clients connectés au groupe 'charge'.
        new_data = event['text']
        await self.send(json.dumps(new_data))
        

class ListeOrdoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        #Cette méthode est appelée lorsque le client WebSocket se connecte au serveur.
        #Elle ajoute le canal (channel) de la connexion à un groupe spécifique nommé 'charge'. Cela permet de regrouper plusieurs connexions WebSocket pour un traitement groupé. Le nom du groupe est arbitraire et peut être défini selon les besoins de votre application.
        #Enfin, elle accepte la connexion WebSocket.
        poste = self.scope.get("url_route").get("kwargs").get("nom_poste")
        await self.channel_layer.group_add(
            "ordo_"+poste, 
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, code):
        #Cette méthode est appelée lorsque le client se déconnecte du serveur WebSocket, soit volontairement soit suite à une erreur.
        #Elle retire le canal de la connexion du groupe 'charge'.
        poste = self.scope.get("url_route").get("kwargs").get("nom_poste")
        await self.channel_layer.group_discard(
            "ordo_"+poste, 
            self.channel_name
        )

    async def send_new_data(self, event):
        #Cette méthode est utilisée pour envoyer de nouvelles données à tous les clients connectés au groupe 'charge'.
        #Elle est généralement appelée lorsque de nouvelles données sont disponibles et doivent être diffusées à tous les clients.
        #L'argument event contient les données envoyées par l'événement déclencheur. Dans ce cas, l'événement est un simple texte.
        #La méthode récupère les nouvelles données à partir de l'événement, les encode en JSON (pour assurer la compatibilité avec WebSocket), puis les envoie à tous les clients connectés au groupe 'charge'.
        new_data = event['text']
        await self.send(json.dumps(new_data))