{
    'name': "VISITOR LOG MANAGEMENT",

    'summary': """
       Resolve the manual process for keeping, maintaining the employees and visitor’s information.""",

    'description': """
        Any organization need an efficient method in order to handle the visitor's and employee’s information. For build strong business profile and smooth their business process, management need to record each and every detail of visitors and also record their visits.
Logbook resolve automate their manual process for keeping, maintaining the employees and visitor’s information.
    """,

    'author': "Metamorphosis",
    'website': "https://metamorphosis.com.bd",
    'category': 'Human Resources',
    'version': '12.0',
    'depends': [
        'base',
        'mail',
        'hr',

    ],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/appointment.xml',
        'views/employee.xml',
        'views/visitor.xml',
        'views/check_in_out.xml',


    ],
    "images": ["static/description/cover.png"],
    'icon': "/visitor_log_book/static/description/icon.png", 

    'license': "",
    'installable': True,
    'application': True,
    'sequence': 1,
    "license": "OPL-1",
}
