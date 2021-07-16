from odoo.http import Controller, route


class MyController(Controller):
    @route('/some_url', auth='public')
    def handler(self):
        return "{'response': 'OK'}"
