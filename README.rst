sl29.games.2048
=================
Une implémentation du jeu 2048 à des fins éducatives.

.. _readme-vue-d-ensemble:

📦 Vue d’ensemble
-----------------

L'objectif de ce projet est d'offrir un exemple minimal et éducatif de comment :

- Implémenter un **jeu** basique en Python (`2048`)
- Empaqueter correctement avec les conventions **PEP 621** (`pyproject.toml`)
- Écrire et exécuter des **tests unitaires** avec `pytest`
- Générer automatiquement de la **documentation** en utilisant `Sphinx`

.. _readme-installation:

🧩 Installation
---------------

Il est recommandé de travailler dans un **environnement virtuel** pour éviter les conflits de dépendances.

🔧 Créer et activer un environnement virtuel
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Sur Linux/Mac :

.. code-block:: bash

   python3 -m venv games2048
   source games2048/bin/activate

Sur Windows :

.. code-block:: bash

   python -m venv games2048
   games2048\Scripts\activate

Installer en mode développement
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Pour le développement, les tests et la documentation :

.. code-block:: bash

   pip install -e .[dev,test,doc]

Cela installera :

- Le package lui-même
- Les outils de développement (par exemple Jupyter, linters)
- Les dépendances de test (pytest, pytest-cov)
- Les outils de documentation (Sphinx, sphinx-rtd-theme, etc.)

Installation en production
~~~~~~~~~~~~~~~~~~~~~~~~~~

Pour installer le package comme un package Python standard :

.. code-block:: bash

   pip install -e .

ou construire et installer depuis une wheel :

.. code-block:: bash

   python -m build
   pip install dist/sl29.games.2048-*.whl

.. _readme-exemple-d-utilisation:

Exemple d’utilisation
---------------------

Pour jouer au jeu 2048 en mode texte via l'interface en ligne de commande :

.. code-block:: bash

   python -m sl29.games.cli_2048

Ou avec l'option pour désactiver le nettoyage du terminal (utile pour le débogage) :

.. code-block:: bash

   python -m sl29.games.cli_2048 --no-clear

Les commandes disponibles sont :
- g : déplacer à gauche
- d : déplacer à droite
- h : déplacer en haut
- b : déplacer en bas
- q : quitter le jeu

Pour utiliser la logique du jeu dans votre propre code :

.. code-block:: python

   from sl29.games._2048 import nouvelle_partie, jouer_coup

   # Créer une nouvelle partie
   plateau, score = nouvelle_partie()

   # Jouer un coup (par exemple, à gauche)
   nouveau_plateau, points_gagnes, partie_terminee = jouer_coup(plateau, 'g')
   score += points_gagnes

.. _readme-executer-les-tests:

Exécuter les tests
------------------

Exécuter tous les tests :

.. code-block:: bash

   pytest

Exécuter les tests avec couverture :

.. code-block:: bash

   pytest --cov=sl29.games.2048

Générer un rapport de couverture HTML :

.. code-block:: bash

   pytest --cov=sl29.games.2048 --cov-report=html

Le rapport HTML sera généré dans le répertoire `htmlcov/`. Ouvrez `htmlcov/index.html` dans votre navigateur web pour voir les détails de couverture.

.. _readme-construire-la-documentation:

Construire la documentation
---------------------------

La documentation est construite avec Sphinx et suppose que vous avez installé les dépendances optionnelles de doc.

Sur Linux/Mac :

.. code-block:: bash

   cd doc
   make html

Sur Windows :

.. code-block:: bash

   cd doc
   make.bat html

Ou alternativement sur tous les systèmes :

.. code-block:: bash

   sphinx-build doc _build/html

Les fichiers HTML générés seront dans `doc/_build/html/index.html`. Ouvrez ce fichier dans votre navigateur web pour voir la documentation.
