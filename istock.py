import psycopg
from psycopg import sql
#import psycopg
import bcrypt

def get_connexion():
    return psycopg.connect(
        host="bd-pedago.univ-lyon1.fr",
        user="p2002623",
        password="Reuse46Simile",
        dbname="p2002623"
    )


"""def get_connexion(host, username, password, db):
    try : 
        connexion = psycopg.connect(host = host, user = username, password = password, dbname = db)
    except Exception as e:
        print("Erreur :", e)
        return None
    return connexion
"""

def execute_select_query(connexion, query, params=[]):
    """
    Méthode générique pour exécuter une requête SELECT (qui peut retourner plusieurs instances).
    Utilisée par des fonctions plus spécifiques.
    """
    with connexion.cursor() as cursor:
        try:
            cursor.execute(query, params)
            result = cursor.fetchall()
            return result 
        except psycopg.Error as e:
            print("Erreur lors de l'exécution de la requête :", e)
    return None



def creer_utilisateur(login, password, role, entreprise_id):
    conn = get_connexion()
    with conn.cursor() as cursor:
        # Vérifier si l'utilisateur existe déjà
        cursor.execute("""
            SELECT id FROM istock.utilisateur
            WHERE login = %s
        """, (login,))
        existing = cursor.fetchone()

        if existing:
            print(f"⚠️ L'utilisateur '{login}' existe déjà. Pas d'insertion.")
            return

        # Hachage du mot de passe
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

        cursor.execute("""
            INSERT INTO istock.utilisateur (login, password_hash, role, entreprise_id)
            VALUES (%s, %s, %s, %s)
        """, (login, hashed.decode(), role, entreprise_id))
        conn.commit()

        print("✅ Utilisateur créé avec succès !")


def verifier_login(login, password):
    conn = get_connexion()
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT password_hash, role, entreprise_id
            FROM istock.utilisateur
            WHERE login = %s
        """, (login,))
        row = cursor.fetchone()

    if row:
        password_hash, role, entreprise_id = row
        if bcrypt.checkpw(password.encode(), password_hash.encode()):
            print("✅ Connexion réussie")
            print(f"Rôle : {role}, Entreprise ID : {entreprise_id}")
            return True
        else:
            print("❌ Mot de passe incorrect")
            return False
    else:
        print("❌ Utilisateur inconnu")
        return False

# Test :
if __name__ == "__main__":
    verifier_login("adminLogin", "123456")

# Exemple de création :
"""if __name__ == "__main__":
    creer_utilisateur(
        login="user2",
        password="123456",
        role="employe",
        entreprise_id=1
    )
"""