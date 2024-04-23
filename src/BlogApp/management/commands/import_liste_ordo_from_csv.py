'''
import csv
from django.core.management.base import BaseCommand
from BlogApp.forms import ListeAttenteOrdoForm


class Command(BaseCommand):
    help = ("imports liste ordonnancement from a local csv file. Expects columns num_affaire, date_debut_ordo, client, etat_affaire, rang_OF, temps_prevu, temps_ecoule, temps_restant")

    def add_arguments(self, parser):
        parser.add_argument("file_path", nargs=1, type=str)
    
    def handle(self, *args, **options):
        self.file_path = options["file_path"][0]
        self.prepare()
        self.main()
        self.finalise()

    def prepare(self):
        self.imported_counter = 0
        self.skipped_counter = 0

    def main(self):
        self.stdout.write("=== Importing Liste Ordo ===")

        with open(self.file_path, mode="r") as f:
            reader = csv.DictReader(f)
            for index, row_dict in enumerate(reader):
                form = ListeAttenteOrdoForm(data=row_dict)
                if form.is_valid():
                    form.save()
                    self.imported_counter += 1
                else:
                    self.stderr.write(f"Errors importing ordo"
                                      f"{row_dict['make']} - {row_dict['model']}:\n"
                                      )
                    self.stderr.write(f"{form.errors.as_json()}\n")

    def finalise(self):
        self.stdout.write(f"-------------\n")
        self.stdout.write(f"Liste ordo imported: {self.imported_counter}\n")
        self.stdout.write(f"Liste ordo skipped: {self.skipped_counter}\n\n")
'''
# Importation des modules nécessaires
from django.core.management.base import BaseCommand
from BlogApp.models import *  # Importation des modèles Django
import pandas as pd  # Importation de pandas pour la manipulation des données CSV
from datetime import *  # Importation des modules datetime pour le traitement des dates

# Définition d'une classe de commande personnalisée héritant de BaseCommand
class Command(BaseCommand):

    # Implémentation de la méthode handle, appelée lors de l'exécution de la commande
    def handle(self, *args, **options):
        
        # Lecture du fichier CSV à l'aide de pandas et stockage dans un DataFrame
        df_ordo = pd.read_csv('data/test_data_liste_ordo.csv', sep=',')
        
        # Initialisation d'une liste vide pour stocker les objets à créer
        liste_ordo = []
        
        # Parcours des lignes du DataFrame
        for _, row in df_ordo.iterrows():
            
            # Récupération d'un objet ModelCalcul à partir d'une colonne du CSV
            #GETmodelCalcul = ModelCalcul.objects.get(nom=row['Contrat'])
            
            # Création d'un objet Centrale avec les données de la ligne du CSV et l'objet ModelCalcul récupéré
            donnees_centrale_obj = Centrale(
                nomCentrale=row['Centrale'],
                project_code=row['project_code'],
                puissanceInstallee=row['Puissance centrale'],
                nombreOnduleurs=row['Nombre onduleurs'],
                #idModelCalcul=GETmodelCalcul
            )
            
            # Ajout de l'objet créé à la liste des objets à créer
            liste_ordo.append(donnees_centrale_obj)
        
        # Utilisation de la méthode bulk_create pour créer les objets Centrale en une seule requête, améliorant ainsi les performances
        Centrale.objects.bulk_create(liste_centrale)
