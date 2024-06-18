import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.core.cache import cache
from .models import Setup, Setup_OF, Setup_Last10OF, Setup_PDCMachine


class PlanChargeConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        #Cette méthode est appelée lorsque le client WebSocket se connecte au serveur.
        #Elle ajoute le canal (channel) de la connexion à un groupe spécifique nommé 'charge'. Cela permet de regrouper plusieurs connexions WebSocket pour un traitement groupé. Le nom du groupe est arbitraire et peut être défini selon les besoins de votre application.
        #Enfin, elle accepte la connexion WebSocket.
        self.site = self.scope.get("url_route").get("kwargs").get("nom_site")
        self.atelier = self.scope.get("url_route").get("kwargs").get("nom_atelier")
        self.annee = self.scope.get("url_route").get("kwargs").get("num_annee")
        self.semaine = self.scope.get("url_route").get("kwargs").get("num_semaine")

        self.ch_site = self.site.strip()
        self.ch_atelier = self.atelier.strip()
        self.ch_annee = self.annee.strip()
        self.ch_semaine = self.semaine.strip()

        self.group_name = f"charge_{self.ch_site}_{self.ch_atelier}_{self.ch_annee}_{self.ch_semaine}"
        await self.channel_layer.group_add(
            self.group_name, 
            self.channel_name
        )
        # Increment the connection count
        cache_key = f"{self.group_name}_count"
        current_count = cache.get(cache_key, 0)
        cache.set(cache_key, current_count + 1)
        await self.accept()
        print(current_count)

    async def disconnect(self, code):
        #Cette méthode est appelée lorsque le client se déconnecte du serveur WebSocket, soit volontairement soit suite à une erreur.
        #Elle retire le canal de la connexion du groupe 'charge'.
        await self.channel_layer.group_discard(
            self.group_name, 
            self.channel_name
        )
        # Decrement the connection count
        cache_key = f"{self.group_name}_count"
        current_count = cache.get(cache_key, 0)
        new_count = current_count - 1
        if new_count <= 0:
            # If this was the last connection, delete the setup_pdc
            cache.delete(cache_key)
            await self.delete_setup_pdc()
        else:
            cache.set(cache_key, new_count)

    async def send_new_data(self, event):
        #Cette méthode est utilisée pour envoyer de nouvelles données à tous les clients connectés au groupe 'charge'.
        #Elle est généralement appelée lorsque de nouvelles données sont disponibles et doivent être diffusées à tous les clients.
        #L'argument event contient les données envoyées par l'événement déclencheur. Dans ce cas, l'événement est un simple texte.
        #La méthode récupère les nouvelles données à partir de l'événement, les encode en JSON (pour assurer la compatibilité avec WebSocket), puis les envoie à tous les clients connectés au groupe 'charge'.
        new_data = event['text']
        await self.send(json.dumps(new_data))
    
    @database_sync_to_async
    def delete_setup_pdc(self):
        try:
            setup_pdc = Setup.objects.get(
                title=f"Setup_{self.site}_{self.atelier}_{self.annee}_{self.semaine}"
            )
            setup_pdc.delete()
        except Setup.DoesNotExist:
            pass
        

class ListeOrdoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        #Cette méthode est appelée lorsque le client WebSocket se connecte au serveur.
        #Elle ajoute le canal (channel) de la connexion à un groupe spécifique nommé 'charge'. Cela permet de regrouper plusieurs connexions WebSocket pour un traitement groupé. Le nom du groupe est arbitraire et peut être défini selon les besoins de votre application.
        #Enfin, elle accepte la connexion WebSocket.
        self.nom_poste = self.scope.get("url_route").get("kwargs").get("nom_poste") 

        self.ch_nom_poste = self.nom_poste.strip()

        self.group_name = f"ordo_{self.ch_nom_poste}"
        await self.channel_layer.group_add(
            self.group_name, 
            self.channel_name
        )
        # Increment the connection count
        cache_key = f"{self.group_name}_count"
        current_count = cache.get(cache_key, 0)
        cache.set(cache_key, current_count + 1)
        await self.accept()
        print(current_count)

    async def disconnect(self, code):
        #Cette méthode est appelée lorsque le client se déconnecte du serveur WebSocket, soit volontairement soit suite à une erreur.
        #Elle retire le canal de la connexion du groupe 'charge'.
        await self.channel_layer.group_discard(
            self.group_name, 
            self.channel_name
        )
        # Decrement the connection count
        cache_key = f"{self.group_name}_count"
        current_count = cache.get(cache_key, 0)
        new_count = current_count - 1
        if new_count <= 0:
            # If this was the last connection, delete the setup_pdc
            cache.delete(cache_key)
            await self.delete_setup_OF()
        else:
            cache.set(cache_key, new_count)

    async def send_new_data(self, event):
        #Cette méthode est utilisée pour envoyer de nouvelles données à tous les clients connectés au groupe 'charge'.
        #Elle est généralement appelée lorsque de nouvelles données sont disponibles et doivent être diffusées à tous les clients.
        #L'argument event contient les données envoyées par l'événement déclencheur. Dans ce cas, l'événement est un simple texte.
        #La méthode récupère les nouvelles données à partir de l'événement, les encode en JSON (pour assurer la compatibilité avec WebSocket), puis les envoie à tous les clients connectés au groupe 'charge'.
        new_data = event['text']
        await self.send(json.dumps(new_data))
    
    @database_sync_to_async
    def delete_setup_OF(self):
        try:
            setup_OF = Setup_OF.objects.get(
                title=f"Setup_OF_{self.nom_poste}"
            )
            setup_OF.delete()
        except Setup_OF.DoesNotExist:
            pass


class Last10OFConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        #Cette méthode est appelée lorsque le client WebSocket se connecte au serveur.
        #Elle ajoute le canal (channel) de la connexion à un groupe spécifique nommé 'charge'. Cela permet de regrouper plusieurs connexions WebSocket pour un traitement groupé. Le nom du groupe est arbitraire et peut être défini selon les besoins de votre application.
        #Enfin, elle accepte la connexion WebSocket.
        self.nom_poste = self.scope.get("url_route").get("kwargs").get("nom_poste") 

        self.ch_nom_poste = self.nom_poste.strip()

        self.group_name = f"last10of_{self.ch_nom_poste}"
        await self.channel_layer.group_add(
            self.group_name, 
            self.channel_name
        )
        # Increment the connection count
        cache_key = f"{self.group_name}_count"
        current_count = cache.get(cache_key, 0)
        cache.set(cache_key, current_count + 1)
        await self.accept()
        print(current_count)

    async def disconnect(self, code):
        #Cette méthode est appelée lorsque le client se déconnecte du serveur WebSocket, soit volontairement soit suite à une erreur.
        #Elle retire le canal de la connexion du groupe 'charge'.
        await self.channel_layer.group_discard(
            self.group_name, 
            self.channel_name
        )
        # Decrement the connection count
        cache_key = f"{self.group_name}_count"
        current_count = cache.get(cache_key, 0)
        new_count = current_count - 1
        if new_count <= 0:
            # If this was the last connection, delete the setup_pdc
            cache.delete(cache_key)
            await self.delete_setup_last10of()
        else:
            cache.set(cache_key, new_count)

    async def send_new_data(self, event):
        #Cette méthode est utilisée pour envoyer de nouvelles données à tous les clients connectés au groupe 'charge'.
        #Elle est généralement appelée lorsque de nouvelles données sont disponibles et doivent être diffusées à tous les clients.
        #L'argument event contient les données envoyées par l'événement déclencheur. Dans ce cas, l'événement est un simple texte.
        #La méthode récupère les nouvelles données à partir de l'événement, les encode en JSON (pour assurer la compatibilité avec WebSocket), puis les envoie à tous les clients connectés au groupe 'charge'.
        new_data = event['text']
        await self.send(json.dumps(new_data))
    
    @database_sync_to_async
    def delete_setup_last10of(self):
        try:
            setup_last10of = Setup_Last10OF.objects.get(
                title=f"Setup_Last10OF_{self.nom_poste}"
            )
            setup_last10of.delete()
        except Setup_Last10OF.DoesNotExist:
            pass


class PDCMachineConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        #Cette méthode est appelée lorsque le client WebSocket se connecte au serveur.
        #Elle ajoute le canal (channel) de la connexion à un groupe spécifique nommé 'charge'. Cela permet de regrouper plusieurs connexions WebSocket pour un traitement groupé. Le nom du groupe est arbitraire et peut être défini selon les besoins de votre application.
        #Enfin, elle accepte la connexion WebSocket.
        self.poste = self.scope.get("url_route").get("kwargs").get("nom_poste")
        self.annee = self.scope.get("url_route").get("kwargs").get("num_annee")
        self.semaine = self.scope.get("url_route").get("kwargs").get("num_semaine")

        self.ch_poste = self.poste.strip()
        self.ch_annee = self.annee.strip()
        self.ch_semaine = self.semaine.strip()

        self.group_name = f"charge_machine_{self.ch_poste}_{self.ch_annee}_{self.ch_semaine}"
        await self.channel_layer.group_add(
            self.group_name, 
            self.channel_name
        )
        # Increment the connection count
        cache_key = f"{self.group_name}_count"
        current_count = cache.get(cache_key, 0)
        cache.set(cache_key, current_count + 1)
        await self.accept()
        print(current_count)

    async def disconnect(self, code):
        #Cette méthode est appelée lorsque le client se déconnecte du serveur WebSocket, soit volontairement soit suite à une erreur.
        #Elle retire le canal de la connexion du groupe 'charge'.
        await self.channel_layer.group_discard(
            self.group_name, 
            self.channel_name
        )
        # Decrement the connection count
        cache_key = f"{self.group_name}_count"
        current_count = cache.get(cache_key, 0)
        new_count = current_count - 1
        if new_count <= 0:
            # If this was the last connection, delete the setup_pdc
            cache.delete(cache_key)
            await self.delete_setup_pdc_machine()
        else:
            cache.set(cache_key, new_count)

    async def send_new_data(self, event):
        #Cette méthode est utilisée pour envoyer de nouvelles données à tous les clients connectés au groupe 'charge'.
        #Elle est généralement appelée lorsque de nouvelles données sont disponibles et doivent être diffusées à tous les clients.
        #L'argument event contient les données envoyées par l'événement déclencheur. Dans ce cas, l'événement est un simple texte.
        #La méthode récupère les nouvelles données à partir de l'événement, les encode en JSON (pour assurer la compatibilité avec WebSocket), puis les envoie à tous les clients connectés au groupe 'charge'.
        new_data = event['text']
        await self.send(json.dumps(new_data))
    
    @database_sync_to_async
    def delete_setup_pdc_machine(self):
        try:
            setup_pdc_machine = Setup_PDCMachine.objects.get(
                title=f"Setup_PDCMachine_{self.poste}_{self.annee}_{self.semaine}"
            )
            setup_pdc_machine.delete()
        except Setup_PDCMachine.DoesNotExist:
            pass