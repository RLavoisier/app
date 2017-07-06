## marketplace
Application de test marketplace.
Permet l'affichage et la création de commande via appels REST sur une app python.
Permet également de charger les commandes issues d'un XML

## App pythons
J'ai découpé l'application en 2 apps différentes

l'app "order" qui peut être appellée en REST via l'url /api/orders

    - index             : GET /api/orders
    - Chargement XML    : PUT /api/orders (pour les besoin du tests)
    - POST              : POST /api/orders
    - Show              : GET /api/orders/*id*
    - Delete            : DELETE /api/orders/*id*

l'app "www" qui présente l'interface utilisateur et utilise l'app order via rest

    - index             : get / ou /orders
    - new               : get /orders/new
    - show              : get /orders/*id*

