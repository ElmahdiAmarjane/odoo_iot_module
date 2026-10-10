{
    'name': 'TP Warranty Manager',
    'version': '1.0.0',
    'category': 'Sales',
    'summary': 'Gestion des garanties et réclamations',
    'description': """
TP N°2 - Gestion des garanties et réclamations.

Ce module permet de gérer les politiques de garantie,
les réclamations clients et leur traitement.
""",
    'depends': [
        'sale',
        'sale_stock',
        'stock',
        'account',
        'mail',
    ],
    'data': [
        'data/warranty_sequence.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}