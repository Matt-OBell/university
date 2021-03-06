from odoo import api, fields, models
from odoo.exceptions import Warning


class ProductTemplate(models.Model):
    def _check_isbn(self):
        self.ensure_one()
        digits = [int(x) for x in self.isbn if x.isdigit()]
        if len(digits) == 13:
            ponderations = [1, 3] * 6
            terms = [a * b for a, b in zip(digits[:12], ponderations)]
            remain = sum(terms) % 10
            check = 10 - remain if remain != 0 else 0
            return digits[-1] == check
    _inherit = 'product.template'
    _description = 'Category'
    active = fields.Boolean('Active?', default=True)
    additional_authors = fields.Many2one('res.partner', string='Additional Authors')
    author_ids = fields.Many2many('res.partner', string='Authors')
    book_number = fields.Char(string='Book Number')
    edition = fields.Char(string='Edition')
    is_a_book = fields.Boolean(string="Is A Book")
    isbn = fields.Char(string='ISBN')
    is_available = fields.Boolean(string='Is Available?')
    published_date = fields.Date(string='Published Date')
    publisher_id = fields.Many2one('res.partner', string='Publisher', index=True)
    series = fields.Char(string='Series')
    subject_area = fields.Many2one(string='Subject Area')
    subject_number = fields.Char(string='Subject Number')

    def button_check_isbn(self):
        for book in self:
            if book._check_isbn():
                raise Warning('The ISBN is valid')
            if not book.isbn:
                raise Warning('Please provide an ISBN for %s' % book.name)
            if book.isbn and not book._check_isbn():
                raise Warning('%s is an invalid ISBN' % book.isbn)
        return True
